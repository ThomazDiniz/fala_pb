# -*- coding: utf-8 -*-
"""
Adaptador para o MOSA-Net Cross-Domain (Zezario et al., 2024) — referência [33]
da dissertação:
  "Deep learning-based non-intrusive multi-objective speech assessment model
   with cross-domain features".

Repositório oficial: https://github.com/dhimasryan/MOSA-Net-Cross-Domain

Este wrapper expõe uma interface mínima e estável para o passo 02:

    mn = MosaNet(repo_dir=<pasta do repo clonado>, device="cuda")
    mos = mn.predict(wav_tensor, sr)   # -> float (1..5)

O MOSA-Net Cross-Domain combina features de domínios distintos:
  (a) espectro de potência (LPS / STFT),
  (b) embeddings de um modelo SSL pré-treinado (ex.: wav2vec/HuBERT),
e prevê de forma multi-objetivo (Quality/MOS, Intelligibility, etc.).

IMPORTANTE — o que VOCÊ precisa fornecer (uma vez):
  1. Clonar o repo dentro de  Experimento final/mosanet/MOSA-Net-Cross-Domain
  2. Baixar o checkpoint treinado disponibilizado pelos autores e apontar
     MOSANET_CHECKPOINT abaixo (ou via variável de ambiente MOSANET_CKPT).
  3. Garantir o modelo SSL exigido pelo checkpoint (o repo indica qual).

Como os nomes de arquivos/funções variam entre versões do repo, os pontos
que podem precisar de ajuste estão marcados com  # >>> AJUSTE .
Se algo não casar, o passo 02 apenas registra o erro e segue com os demais
preditores (NISQA/DNSMOS/SQUIM) — o pipeline não quebra.
"""
from __future__ import annotations

import os
from pathlib import Path


class MosaNet:
    def __init__(self, repo_dir: Path, device: str = "cpu"):
        self.repo_dir = Path(repo_dir)
        self.device = device
        if not self.repo_dir.exists():
            raise FileNotFoundError(
                f"Repo do MOSA-Net não encontrado em {self.repo_dir}. "
                "Veja Experimento final/mosanet/README.md.")
        self.model = self._load_model()

    # ------------------------------------------------------------------
    def _checkpoint_path(self) -> Path:
        env = os.environ.get("MOSANET_CKPT")
        if env:
            return Path(env)
        # >>> AJUSTE: nome do checkpoint conforme baixado dos autores
        for nome in ("MOSA_Net_Cross_Domain.h5", "MOSA-Net+.h5",
                     "saved_model", "model.h5"):
            p = self.repo_dir / nome
            if p.exists():
                return p
        raise FileNotFoundError(
            "Checkpoint do MOSA-Net não encontrado. Defina MOSANET_CKPT "
            "ou coloque o .h5/SavedModel na pasta do repo.")

    def _load_model(self):
        """Carrega o modelo Keras/TensorFlow do MOSA-Net Cross-Domain."""
        import tensorflow as tf  # noqa
        ckpt = self._checkpoint_path()
        # >>> AJUSTE: se o repo usar custom_objects, passe-os aqui.
        model = tf.keras.models.load_model(str(ckpt), compile=False)
        return model

    # ------------------------------------------------------------------
    def _features(self, wav, sr):
        """Extrai as features cross-domain (LPS + SSL) esperadas pelo modelo.

        Implementação de referência seguindo o pipeline do MOSA-Net+. Os SSL
        embeddings usam um modelo pré-treinado; em máquina sem acesso ao Hub,
        baixe-o previamente e aponte MOSANET_SSL_MODEL.
        """
        import numpy as np
        import librosa

        y = wav.squeeze().detach().cpu().numpy().astype("float32")
        if sr != 16000:
            y = librosa.resample(y, orig_sr=sr, target_sr=16000)
            sr = 16000

        # (a) Espectro de potência logarítmico (LPS)
        n_fft, hop, win = 512, 256, 512
        D = librosa.stft(y, n_fft=n_fft, hop_length=hop, win_length=win)
        lps = np.log1p(np.abs(D) ** 2).T.astype("float32")  # (T, 257)

        # (b) Embeddings SSL  # >>> AJUSTE conforme o checkpoint (wav2vec/HuBERT)
        ssl = self._ssl_embeddings(y, sr)                    # (T', H)

        return lps, ssl

    _ssl_model = None

    def _ssl_embeddings(self, y, sr):
        import numpy as np
        import torch
        if self._ssl_model is None:
            import torchaudio
            # >>> AJUSTE: bundle exigido pelo checkpoint dos autores
            bundle = torchaudio.pipelines.WAV2VEC2_ASR_BASE_960H
            self._ssl_model = bundle.get_model().to(self.device).eval()
        with torch.no_grad():
            wav = torch.tensor(y, device=self.device).unsqueeze(0)
            feats, _ = self._ssl_model.extract_features(wav)
            emb = feats[-1].squeeze(0).cpu().numpy().astype("float32")
        return emb

    # ------------------------------------------------------------------
    def predict(self, wav, sr) -> float:
        """Retorna o MOS previsto (escala 1..5)."""
        import numpy as np
        lps, ssl = self._features(wav, sr)
        # >>> AJUSTE: ordem/nomes das entradas conforme a assinatura do modelo.
        # No MOSA-Net+ a saída de qualidade costuma ser um score por frame +
        # um score global; usamos o score global de qualidade.
        inputs = [lps[np.newaxis, ...], ssl[np.newaxis, ...]]
        out = self.model.predict(inputs, verbose=0)
        score = out[0] if isinstance(out, (list, tuple)) else out
        score = float(np.asarray(score).reshape(-1)[0])
        # garante faixa plausível de MOS
        return max(1.0, min(5.0, score))

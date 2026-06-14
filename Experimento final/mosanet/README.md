# MOSA-Net Cross-Domain — instalação

Preditor de MOS principal citado na dissertação (Zezario et al., 2024, ref. [33]).

## Passos

1. Clone o repositório oficial **dentro desta pasta**:

   ```bash
   cd "Experimento final/mosanet"
   git clone https://github.com/dhimasryan/MOSA-Net-Cross-Domain
   ```

   Resultado esperado: `Experimento final/mosanet/MOSA-Net-Cross-Domain/`
   (é o caminho em `config.py -> MOSANET_REPO`).

2. Baixe o **checkpoint treinado** disponibilizado pelos autores (link no
   README do repo) e coloque-o dentro da pasta do repo, ou aponte com:

   ```bash
   export MOSANET_CKPT=/caminho/para/o/checkpoint.h5      # Linux/Mac
   set    MOSANET_CKPT=C:\caminho\para\checkpoint.h5      # Windows
   ```

3. Instale as dependências do MOSA-Net (TensorFlow + librosa) no ambiente:

   ```bash
   pip install "tensorflow>=2.10" librosa
   ```

4. O modelo SSL (wav2vec/HuBERT) usado nas features precisa estar disponível.
   Em máquina sem acesso ao HuggingFace Hub, baixe-o antes e ajuste o bundle
   em `mosanet_wrapper.py` (`# >>> AJUSTE`).

## Verificação

```bash
cd "Experimento final"
python -c "import sys; sys.path.insert(0,'mosanet'); import mosanet_wrapper as m; \
print(m.MosaNet(repo_dir='mosanet/MOSA-Net-Cross-Domain', device='cpu'))"
```

Se aparecer um objeto `MosaNet`, está pronto — rode `02_mos_predictors.py`.

## Se não conseguir configurar agora

Sem problema: o `02_mos_predictors.py` é resiliente. Ele deixa a coluna
`mosanet_mos` vazia, registra o motivo no log e calcula normalmente os demais
preditores (NISQA, DNSMOS, SQUIM). A seleção composta e os gráficos usam o
primeiro MOS disponível na ordem definida em
`config.py -> MOS_PRINCIPAL_PREFERENCIA`.

## Pontos de ajuste no wrapper

Os nomes de arquivos e a assinatura do modelo variam entre versões do repo.
Procure os comentários `# >>> AJUSTE` em `mosanet_wrapper.py`:
- nome do checkpoint;
- `custom_objects` no `load_model` (se houver);
- bundle SSL exigido pelo checkpoint;
- ordem das entradas no `model.predict`.

# Diretivas — Experimento Final (análise objetiva automática)

> **Atualização:** o pipeline foi consolidado em **um único script** `experimento_final.py` (baseado no seu `avaliador.py`). Onde abaixo se fala em scripts 01–05 separados, leia como as etapas internas desse único script. Métricas, fórmulas e critérios permanecem idênticos.


Documento para você **validar a metodologia antes de rodar**. Descreve o que
cada passo faz, as fórmulas, os critérios de decisão e onde rodar. Se algo aqui
não bater com sua intenção, ajuste `config.py` (não é preciso mexer no código).

---

## 1. Objetivo

Análise científica **comparativa e automática** entre falas sintetizadas por
**modelo original** (base, sem adaptação) e **modelo ajustado** (fine-tune com
sotaque paraibano), em três stacks de TTS: **fishspeech**, **unsloth (Orpheus)**
e **xtts**.

Duas métricas objetivas, ambas fundamentadas na sua dissertação (Cap. 2.6):

1. **Similaridade de Levenshtein** entre o texto original (ground truth) e o
   texto reconhecido por STT (Whisper) — indicador indireto de **inteligibilidade**.
2. **Preditores automáticos de MOS** — **MOSA-Net Cross-Domain** (Zezario et al.,
   2024, ref. [33]) como principal, com **NISQA**, **DNSMOS** e **TorchAudio-SQUIM**
   como complementares/robustez.

Pergunta de pesquisa: **o fine-tuning de sotaque degrada a qualidade/inteligibilidade
em relação ao modelo original?**

---

## 2. Dados de entrada

- **Ground truth:** `docs/Inferencias finais/Audios/sentenças.txt` — **100 sentenças**,
  uma por linha. A linha *N* corresponde ao índice *N* (arquivo `NNN.wav`).
- **Áudios (1800 no total):**

  ```
  docs/Inferencias finais/Audios/<modelo>/outputs_final_experiment/<condicao>/<vN>/NNN.wav
  ```

  - `<modelo>` ∈ {fishspeech, unsloth, xtts}
  - `<condicao>` ∈ {original, ajustado}
  - `<vN>` ∈ {v1, v2, v3} — **3 repetições estocásticas** (seeds 42, 123, 456)
  - `NNN` ∈ {001 … 100}

  Contagem: 3 modelos × 2 condições × 3 variações × 100 sentenças = **1800 áudios**.
  (Conferido: todas as 18 pastas têm 100 wavs.)

> **Por que 3 repetições?** Às vezes o modelo gera áudio “lixo” (ininteligível).
> Gerar 3 e depois escolher a melhor reduz o efeito dessas falhas pontuais na
> comparação — é o que o CSV2 faz (passo 04).

---

## 3. Pipeline (passos)

| # | Script | O que faz | Saída | Onde rodar |
|---|---|---|---|---|
| 01 | `01_stt_whisper.py` | STT (Whisper `small`, pt) + Levenshtein dos 1800 | `resultados/transcricoes.csv` | **GPU** |
| 02 | `02_mos_predictors.py` | MOS: MOSA-Net + NISQA + DNSMOS + SQUIM | `resultados/mos_metrics.csv` | **GPU** |
| 03 | `03_build_csv1.py` | Merge tudo (1800 linhas) | `resultados/csv1_todas_metricas.csv` | qualquer |
| 04 | `04_build_csv2.py` | Melhor das 3 repetições (600 linhas) | `resultados/csv2_melhor_de_3.csv` | qualquer |
| 05 | `05_plots.py` | Gráficos + conclusões | `resultados/plots/*.png`, `conclusoes_preliminares.md` | qualquer |

Orquestrador: `python run_all.py` (ou `run_all.bat` no Windows). Veja `--skip-stt`,
`--skip-mos`, `--only`, `--limit`, `--overwrite`.

---

## 4. Fórmulas e critérios

### 4.1 Similaridade de Levenshtein

Sobre os textos **normalizados** (minúsculas, sem pontuação, espaços colapsados,
acentos mantidos):

```
sim = 1 − dist_Levenshtein(ref, hyp) / max(len(ref), len(hyp))
```

Nível de caractere. Reproduz o exemplo da **Tabela 2.4** da dissertação:
“Frei Damião” × “Freio de Caminhão” → dist 6, max_len 17 → **sim ≈ 0.65**.
`sim = 1.0` ⇒ transcrição idêntica (alta inteligibilidade); valores baixos ⇒
áudio “lixo” / perda de conteúdo. (Negativos são truncados em 0.)

### 4.2 Preditores de MOS

- **MOSA-Net Cross-Domain** — principal (ver `mosanet/README.md` para instalar).
- **NISQA** (torchmetrics): `nisqa_overall` + dimensões (noisiness, discontinuity,
  coloration, loudness).
- **DNSMOS** (torchmetrics): `dns_sig`, `dns_bak`, `dns_ovrl`.
- **SQUIM** (torchaudio): `squim_mos` (subjetivo, com referência não-pareada) e
  objetivos `squim_pesq`, `squim_stoi`, `squim_sisdr`.

Coluna **`mos_principal`** = primeiro disponível na ordem
`config.py → MOS_PRINCIPAL_PREFERENCIA` (`mosanet_mos → squim_mos → nisqa_overall → dns_ovrl`),
e `mos_principal_fonte` registra de qual preditor veio. Assim, mesmo que o
MOSA-Net não esteja configurado, a análise continua com o melhor MOS disponível.

### 4.3 CSV2 — “melhor das 3 repetições” (decisão: composto Lev + MOS)

Para cada grupo (modelo, condição, índice), normaliza-se min-max **dentro do grupo**:

```
lev01 = minmax(lev_sim)            # entre as 3 repetições
mos01 = minmax(mos_principal)      # entre as 3 repetições
score_composto = 0.5·lev01 + 0.5·mos01      # pesos em config.py
```

Escolhe-se a repetição de **maior `score_composto`**. Regras:
- min-max é **relativo às 3** daquela sentença (compara as takes entre si);
- se as 3 forem iguais numa métrica, aquele termo vale 1.0 para todas;
- se faltar MOS no grupo inteiro → usa só Levenshtein; se faltar Levenshtein → só MOS;
- empate: maior `lev_sim`, depois maior `mos_principal`, depois `v1`.

Resultado: 3 × 2 × 100 = **600 linhas**, descartando as takes ruins e mantendo,
entre as boas, a de melhor qualidade. Ajuste `PESO_LEV`/`PESO_MOS` em `config.py`
se quiser priorizar inteligibilidade ou qualidade.

### 4.4 Conclusões (passo 05)

Para cada modelo e métrica: média original, média ajustado, **Δ = ajustado − original**
e **teste de Wilcoxon pareado** (pareado por índice de sentença). Leitura:
Δ < 0 com p < 0,05 ⇒ degradou; Δ ≈ 0 e p ≥ 0,05 ⇒ adaptação não degradou
significativamente. São conclusões **automáticas/preliminares**; a validação
final é a avaliação perceptiva humana (formulários do projeto).

---

## 5. Saídas

```
Experimento final/resultados/
  transcricoes.csv               # passo 01
  mos_metrics.csv                # passo 02
  csv1_todas_metricas.csv        # CSV 1 — todas as métricas, 1800 linhas
  csv2_melhor_de_3.csv           # CSV 2 — melhor de 3, 600 linhas
  conclusoes_preliminares.md     # tabela Δ + Wilcoxon por modelo
  plots/                         # gráficos a partir do CSV2
  01_stt_run.log / 02_mos_run.log
```

### Colunas do CSV1
`modelo, condicao, variacao, indice, arquivo, texto_original, texto_transcrito,
duracao_s, lev_dist, lev_sim, mosanet_mos, nisqa_overall, nisqa_noisiness,
nisqa_discontinuity, nisqa_coloration, nisqa_loudness, dns_sig, dns_bak, dns_ovrl,
squim_mos, squim_stoi, squim_pesq, squim_sisdr, mos_principal, mos_principal_fonte,
status, erro`

### Colunas do CSV2
As mesmas, com `variacao_escolhida`, `score_composto`, `lev_norm01`, `mos_norm01`
à frente (uma linha por modelo×condição×índice).

---

## 6. Como rodar (na sua máquina com GPU)

```bash
cd "Experimento final"
pip install -r requirements.txt          # + tensorflow/librosa se usar MOSA-Net
# (opcional) configurar MOSA-Net: ver mosanet/README.md

python run_all.py                        # 01..05
# ou por partes:
python 01_stt_whisper.py
python 02_mos_predictors.py
python 03_build_csv1.py
python 04_build_csv2.py
python 05_plots.py
```

Teste rápido antes do lote completo: `python run_all.py --limit 30`.
Os passos 01/02 são **resumíveis** (relançar continua de onde parou; `--overwrite`
refaz tudo).

> **Nota sobre o ambiente onde os scripts foram criados:** o ambiente de
> desenvolvimento não tinha GPU e bloqueava o download dos pesos (Whisper/HF),
> então os passos 01/02 **não foram executados aqui**. A lógica de 03/04/05
> (Levenshtein, agregação, seleção composta, gráficos, Wilcoxon) **foi validada
> com dados sintéticos** — ver `resultados_DEMO_sintetico/`. Na sua máquina,
> rode 01/02 e os mesmos scripts produzirão os números reais.

---

## 7. Pontos para você confirmar

1. **Pesos do score composto** (`PESO_LEV=0.5`, `PESO_MOS=0.5`) — ok ou priorizar um?
2. **Ordem de preferência do MOS principal** — manter MOSA-Net no topo?
3. **Whisper `small`** — confirmado (pode trocar em `config.py → WHISPER_MODEL`).
4. **Mapeamento de `unsloth`** como o modelo Orpheus — confere com sua nomenclatura?

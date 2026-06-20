# Resumo da avaliação manual — sotaque paraibano em TTS (briefing para outro chat)

Este arquivo resume **o que foi pedido**, **como os dados estão estruturados** e **os resultados**, para que outro assistente consiga reproduzir ou continuar a análise sem contexto adicional.

---

## 1. Contexto do experimento

Treinei (fine-tuning) três modelos de Text-to-Speech para **adicionar sotaque paraibano** à fala sintetizada. Os três modelos base são:

- **XTTS**
- **FishSpeech**
- **Unsloth/Orpheus** (referido como "Orpheus" nos gráficos)

Apliquei um formulário de avaliação perceptual (Google Forms) em que cada respondente ouve **pares de áudios** e responde, para cada par, duas perguntas:

1. **Sotaque:** "Qual áudio representa melhor o sotaque paraibano?"
2. **Clareza e Naturalidade** (inteligibilidade): "Considerando naturalidade e clareza, qual áudio é melhor?"

Opções de resposta:
- Sotaque: `Áudio A`, `Áudio B`, `Ambos aparentam ter sotaque paraibano`, `Não consigo distinguir`.
- Clareza/Naturalidade: `Áudio A`, `Áudio B`, `Ambos soam igualmente bem`, `Não consigo distinguir`.

A ordem A/B foi **aleatorizada por questão**, então "Áudio A" não é um modelo fixo — é preciso o gabarito (abaixo) para saber qual áudio era qual.

**Amostra:** 56 respondentes. Distribuição de familiaridade: 14 "Sou da Paraíba", 13 familiarizados com sotaque paraibano, 20 familiarizados com sotaques nordestinos, 9 com pouca/nenhuma familiaridade.

---

## 2. Estrutura do CSV e gabarito (MUITO IMPORTANTE)

Arquivo: `Avaliação de Sotaque Paraibano em Falas Sintetizadas xtts (respostas) - Respostas ao formulário 1.csv` (39 colunas, índice 0–38).

- Coluna 0: carimbo de data/hora · Coluna 1: consentimento · Coluna 2: familiaridade.
- Colunas 3–38: pares de respostas (sempre **sotaque na coluna ímpar/primeira, clareza na seguinte**).

### Bloco 1 — Original × Adaptado (cada modelo contra sua versão ajustada)
Cada modelo tem **3 amostras de áudio** = 3 pares de colunas (sotaque, clareza). A letra indicada é **qual áudio era o modelo ADAPTADO** (resposta "positiva" para mim):

| Modelo | Par 1 (cols sotaque,clareza) | Par 2 | Par 3 |
|---|---|---|---|
| **XTTS** | (3,4) → adaptado = **B** | (5,6) → **A** | (7,8) → **B** |
| **FishSpeech** | (9,10) → **A** | (11,12) → **B** | (13,14) → **B** |
| **Unsloth/Orpheus** | (15,16) → **B** | (17,18) → **A** | (19,20) → **B** |

### Bloco 2 — Ranqueamento head-to-head (entre os 3 modelos ajustados)
18 colunas (21–38), 3 confrontos × 3 amostras × 2 perguntas. Mapeamento A/B fixo por confronto:

| Confronto | Cols (sotaque,clareza) | Modelo A | Modelo B |
|---|---|---|---|
| XTTS × FishSpeech | (21,22),(23,24),(25,26) | XTTS | FishSpeech |
| FishSpeech × Unsloth | (27,28),(29,30),(31,32) | FishSpeech | Unsloth/Orpheus |
| XTTS × Unsloth | (33,34),(35,36),(37,38) | XTTS | Unsloth/Orpheus |

### Regra de positividade (decisão minha de análise)
Como o objetivo é verificar se **ambos** os áudios carregam sotaque paraibano (e não apenas vencer o original), trato como **favoráveis ao meu trabalho**:
- No sotaque: escolher o adaptado **OU** "Ambos aparentam ter sotaque paraibano".
- Na clareza/naturalidade: escolher o adaptado **OU** "Ambos soam igualmente bem" (= o ajuste não piorou).
- "Não consigo distinguir" é tratado como neutro/inconclusivo (excluído dos testes binomiais).

---

## 3. Perguntas de pesquisa (com reformulação científica)

1. **"É adicionado sotaque do original para o ajustado?"** (por modelo)
   → *Reformulação:* "O fine-tuning incrementa, de forma estatisticamente significativa, a percepção de sotaque paraibano no modelo ajustado vs. o base?"
2. **"Nosso ajuste piora ou melhora os modelos originais?"** (por modelo)
   → *Reformulação:* "A adaptação preserva ou aprimora a clareza/naturalidade percebida, sem degradação significativa?"
3. **"Qual modelo ajustado se desempenhou melhor em sotaque e em clareza/naturalidade?"** (ranqueamento)

---

## 4. Método de análise

Agreguei as 3 amostras por modelo (3 × 56 = 168 respostas por critério). Classifiquei cada resposta em adaptado / original / ambos / não-distingue. Para significância, **teste binomial exato** (adaptado vs. original, descartando empates e "não distingue", H0: proporção = 0,5). No Bloco 2, **taxa de vitória** = vitórias / (vitórias + derrotas), empates excluídos. Tudo recalculado em 3 recortes: todos (n=56), só paraibanos (n=14), e familiarizados excluindo "pouca/nenhuma" (n=47) — conclusões idênticas nos três.

---

## 5. Resultados principais (todos os respondentes, n=56)

### Q1 — Sotaque foi adicionado? **SIM nos três** (efeito forte, p ≪ 0,001)

| Modelo | Adaptado tem mais sotaque | Ambos têm sotaque | Original | Não distingue | **Favorável (adaptado+ambos)** | binomial |
|---|---|---|---|---|---|---|
| XTTS | 84,5% | 5,4% | 5,4% | 4,8% | **89,9%** | p≈3,3e-32 |
| FishSpeech | 80,4% | 7,1% | 5,4% | 7,1% | **87,5%** | p≈2,7e-30 |
| Orpheus | 85,7% | 3,6% | 4,8% | 6,0% | **89,3%** | p≈1,1e-33 |

### Q2 — O ajuste piora/melhora a clareza e naturalidade?

| Modelo | Adaptado melhor | Ambos iguais | Original melhor | Não distingue | **Não piora (adaptado+ambos)** | binomial | Veredito |
|---|---|---|---|---|---|---|---|
| XTTS | 35,1% | 28,0% | 35,7% | 1,2% | **63,1%** | p≈0,57 (n.s.) | Neutro — preserva qualidade |
| FishSpeech | 56,0% | 32,1% | 7,7% | 4,2% | **88,1%** | p≈1,3e-16 | **Melhora** |
| Orpheus | 45,2% | 20,8% | 25,0% | 8,9% | **66,1%** | p≈1,1e-3 | Melhora moderada |

→ O ajuste **não degrada nenhum** modelo: FishSpeech e Orpheus melhoram; XTTS fica neutro (adiciona sotaque sem perder qualidade).

### Q3 — Ranqueamento entre os ajustados (taxa de vitória, empates excluídos)

| Posição | Modelo | Sotaque | Clareza/Naturalidade |
|---|---|---|---|
| 🥇 | **XTTS** | **71,8%** | **75,7%** |
| 🥈 | FishSpeech | 63,7% | 58,1% |
| 🥉 | Orpheus | 16,6% | 19,1% |

Confrontos diretos: XTTS vence FishSpeech (sotaque 38% × 21%; clareza 40% × 21%); FishSpeech vence Orpheus (61% × 8%; 58% × 17%); XTTS vence Orpheus (50% × 14%; 66% × 12%). Mesmo ranking nos dois critérios; entre paraibanos a vantagem do XTTS é ainda maior (~83% / ~80%).

---

## 6. Conclusões em uma frase

1. O fine-tuning **insere sotaque paraibano** nos três modelos (~88–90% favorável, altamente significativo).
2. A adaptação **não piora** a qualidade — melhora FishSpeech e Orpheus, preserva o XTTS. Sem trade-off perceptível.
3. **Campeão: XTTS ajustado**, em sotaque e em clareza/naturalidade; FishSpeech 2º, Orpheus 3º.

**Ressalva:** n=56 é modesto, mas os efeitos de Q1 e do ranqueamento são grandes e robustos. O resultado neutro de Q2 no XTTS é real (proporções quase iguais), não falta de potência.

---

## 7. Arquivos da análise (pasta `docs/22/`)

- `analise_sotaque.py` — lê o CSV, computa contagens/percentuais/binomiais/subgrupos → gera `resultados.json`.
- `resultados.json` — saída completa (3 subgrupos: TODOS, PARAIBANOS, FAMILIARIZADOS).
- `graficos.py` — lê o `resultados.json` e gera 4 PNGs em `figs/`:
  `q1_sotaque.png`, `q2_inteligibilidade.png`, `q3_ranking.png`, `q3_confrontos.png`.
- `22.md` — relatório completo com as respostas às 3 perguntas e gráficos embutidos.

Para reproduzir: `python3 analise_sotaque.py && python3 graficos.py` dentro de `docs/22/`.

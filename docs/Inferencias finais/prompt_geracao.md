Preciso de um script/notebook completo para gerar áudios de um experimento final de avaliação perceptual (mestrado), no estilo Unsloth/HuggingFace — pronto para rodar no Colab ou local com GPU. Implemente tudo, valide, execute a geração completa e mostre resumo final.

## Objetivo
Comparar dois modelos de TTS em avaliação perceptual:
1. **Original** — modelo base, sem fine-tune / sem adaptação regional
2. **Ajustado** — fine-tune com sotaque/dataset regional (ex.: sotaque paraibano)

Para cada sentença, gerar **3 variações estocásticas** nos dois modelos, com **seeds diferentes** (ex.: 42, 123, 456). O objetivo é permitir comparação original vs ajustado com variedade de realizações por frase.

**IMPORTANTE — seleção do modelo ajustado:**
O checkpoint ajustado **NÃO** é necessariamente o mais recente nem o de menor loss. Use o experimento que demonstrou melhor incorporação do sotaque nos testes do projeto. Prioridade de seleção:
1. Config/artefato explícito do projeto (testes A/B, `experiment_config.json`, relatório)
2. Métricas, logs, CSV de comparação, nomes de diretórios, checkpoints salvos
3. Desempate: melhor checkpoint do experimento promissor → menor eval loss → mais recente

Registre qual experimento/checkpoint foi escolhido e o critério em log + JSON.

## Entrada
- Arquivo `sentenças.txt` na raiz do projeto: **exatamente 100 sentenças**, uma por linha, sem linhas vazias. Validar contagem; se ≠ 100, abortar com mensagem clara.
- Pasta `refs/` com referências de voz para clonagem (XTTS ou equivalente):
  - sentenças 001–010 → `refs/1.wav`
  - 011–020 → `refs/2.wav`
  - 021–030 → `refs/3.wav`
  - 031–040 → `refs/4.wav`
  - 041–050 → `refs/5.wav`
  - 051–060 → `refs/6.wav`
  - 061–070 → `refs/7.wav`
  - 071–080 → `refs/8.wav`
  - 081–090 → `refs/9.wav`
  - 091–100 → `refs/10.wav`
- Se alguma ref não existir: usar a referência válida mais próxima; logar aviso.

## Saída — estrutura obrigatória
Criar pasta `outputs_final_experiment/` na raiz:

```
outputs_final_experiment/
  original/
    v1/001.wav … 100.wav
    v2/001.wav … 100.wav
    v3/001.wav … 100.wav
  ajustado/
    v1/001.wav … 100.wav
    v2/001.wav … 100.wav
    v3/001.wav … 100.wav
  generation_log.csv
  generation_run.log
  model_selection.json
```

## Regras de geração
- **600 áudios** no total: 100 sentenças × 3 variações × 2 modelos
- Mesmo texto em `original/vN/NNN.wav` e `ajustado/vN/NNN.wav` (pareamento por índice N e variação vN)
- Nomes com **3 dígitos**: `001.wav`, `002.wav`, … `100.wav`
- Mesmas referências de voz para original e ajustado na mesma sentença
- **Não sobrescrever** arquivos existentes por padrão; opção `--overwrite` para regenerar tudo
- Continuar execução se uma sentença falhar; não parar o lote inteiro
- Criar pastas automaticamente
- Log na **tela** e em **arquivo** (`generation_run.log`)

## Inferência (Unsloth / HuggingFace / stack TTS)
- Carregar modelo base (original) e checkpoint/adaptador fine-tuned (ajustado)
- Idioma: `pt` (PT-BR vem dos áudios/referências e fine-tune)
- Antes de cada variação, fixar seed reproducível:
  - `random.seed(seed)`, `numpy.random.seed(seed)`, `torch.manual_seed(seed)`, `torch.cuda.manual_seed_all(seed)` se CUDA
- Seeds padrão por variação: `[42, 123, 456]` para v1, v2, v3
- **Não** passar `generator` ao HF se o modelo rejeitar; usar só seed global (evitar `ValueError: model_kwargs ... generator`)
- Cache de conditioning/latents por arquivo de referência dentro de cada fase (original e ajustado) para não recomputar a mesma ref
- Processar em 2 fases: (1) todas as sentenças/variações do original, (2) todas do ajustado
- Liberar GPU entre fases: `del model`, `torch.cuda.empty_cache()` se aplicável
- Progresso no terminal: índice, variação, seed, modelo, referência, tempo por áudio

## CSV `generation_log.csv` — colunas obrigatórias
`indice`, `variacao`, `seed`, `texto`, `modelo`, `experimento`, `checkpoint`, `criterio_selecao`, `referencia`, `arquivo_gerado`, `status`, `tempo_s`, `erro`

Status: `ok`, `skipped`, `error`

## JSON `model_selection.json`
Incluir: `variations`, `seeds`, blocos `original` e `ajustado` com `experiment_id`, `checkpoint`, `criterion`, `notes`.

## Script e CLI
Criar `generate_final_experiment.py` na raiz (ou notebook equivalente) com funções separadas para:
- localizar modelo original
- localizar experimento/checkpoint ajustado (com critério documentado)
- carregar modelos
- escolher referência por índice
- gerar inferência
- salvar WAV (24 kHz se XTTS)
- registrar logs

Argumentos:
- `--overwrite` — regenerar mesmo se existir
- `--variations 3` — default 3
- `--seeds 42,123,456` — seeds explícitas (quantidade = variations)
- `--base-seed 1000` — alternativa: base, base+1000, base+2000…
- `--dry-run` — validar paths, sentenças, refs e seleção de modelos sem sintetizar
- `--device cuda` — default auto
- `--language pt`

Criar também `run-final-experiment.bat` (Windows) que:
- usa env conda correto (ex.: `coqui-xtts`), **não** o `python` do sistema
- chama: `conda run -n coqui-xtts --no-capture-output python generate_final_experiment.py %*`
- valida existência de `sentenças.txt`, `refs/`, script
- pausa em erro com código de saída

## Resumo final (obrigatório ao terminar)
Exibir:
- áudios gerados original / ajustado (esperado 300 cada)
- falhas
- tempo total
- experimento e checkpoint do ajustado
- critério de seleção
- caminho de `outputs_final_experiment/`

## Fluxo de execução esperado
1. Analisar estrutura do projeto/repo
2. Identificar modelo base e checkpoint ajustado bem-sucedido
3. Implementar script + launcher `.bat`
4. Validar 100 sentenças e refs
5. Executar geração completa (600 inferências)
6. Não parar após escrever código — rodar de fato até concluir ou reportar falhas parciais

## Robustez
- Rodar ~30–60 min sem intervenção
- Retomar execução pulando arquivos já existentes (sem `--overwrite`)
- Reutilizar código de inferência já existente no projeto quando houver (evitar duplicar lógica)

## Meu contexto (adaptar ao analisar o repo)
- Stack: Unsloth / HuggingFace / Coqui XTTS v2 (ou equivalente que encontrar)
- Fine-tune regional: dataset filtrado PT-BR / sotaque paraibano
- Checkpoint ajustado preferido se existir evidência: experimento validado em testes perceptivos (ex.: checkpoint step específico escolhido sobre `best_model.pth`)
- Referências: `refs/1.wav` … `refs/10.wav`
- Sentenças: `sentenças.txt` (100 linhas, sem ponto final se já sanitizado)

Implemente, execute e entregue os 600 WAVs em `outputs_final_experiment/` com logs completos.

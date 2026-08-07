# Amostras de audio — pagina de escuta

Esta pasta contem a **maquinaria** que gera a pagina publica de escuta
(`/fala_pb/amostras/`), citada por nota de rodape na dissertacao. Ela **nao**
guarda os arquivos de audio: os audios permanecem nas pastas de reuniao onde
foram produzidos, e o manifesto aponta para eles.

## Arquivos

| Arquivo | O que e |
|---|---|
| `montar_manifesto.py` | Percorre a arvore de `docs/`, le os CSVs/TXTs de acompanhamento e escreve o `manifest.json`. Valida que todo audio declarado existe. |
| `manifest.json` | Descricao declarativa da pagina: 8 blocos, suas afirmacoes, colunas, textos das frases e caminhos dos audios. Unica fonte de verdade. |
| `gerar_pagina.py` | Le o `manifest.json` e escreve `docs/amostras.md`. |

## Como regerar a pagina

```bash
python docs/amostras/montar_manifesto.py   # reconstroi o manifesto e valida caminhos
python docs/amostras/gerar_pagina.py       # renderiza docs/amostras.md
```

`docs/amostras.md` e **gerado** — nao edite a mao; edite `montar_manifesto.py`
e regere.

## Onde estao os audios

| Bloco | Conteudo | Pasta de origem |
|---|---|---|
| 1 | Clonagem de fala (referencias de 10 s, 30 s e 60 s) | `docs/audios/experimento_timbre/` (`refs/`, `output/`, `output texto original/`) |
| 2 | XTTS — ajuste fino, original x ajustado | `docs/15/xtts/` |
| 3 | F5-TTS — ajuste fino, original x ajustado | `docs/16/f5tts novo treino/` |
| 4 | Orpheus TTS — ajuste fino | `docs/15/artoodtoo_ft_e3/audios experimento/` + `docs/Inferencias finais/Audios/unsloth/` |
| 5 | Fish Speech — ajuste fino (LoRA, 1 epoca) | `docs/17/fishspeech/` |
| 6 | Qwen3-TTS — ajuste fino (3 checkpoints) | `docs/18/QWEEN - TTS/outputs/` |
| 7 | F5-TTS a partir de pesos aleatorios | `docs/19/f5tts_do_zero/` |
| 8 | Avaliacao automatica — amostra de 600 audios | `docs/Inferencias finais/Audios/<modelo>/outputs_final_experiment/<condicao>/<v1\|v2\|v3>/<NNN>.wav` |

## Convencao de caminhos

Todo caminho no `manifest.json` e relativo a `docs/` (a raiz publicada pelo
GitHub Pages), com barras normais e **sem** percent-encoding — o gerador
codifica espacos e acentos ao montar a URL.

A convencao alvo para material novo, ja seguida pelo bloco 8, e:

```
<contexto>/<modelo>/<condicao>/<indice>.wav
```

por exemplo `Inferencias finais/Audios/xtts/outputs_final_experiment/ajustado/v2/017.wav`,
onde `condicao` e `original` ou `ajustado`. Audios novos que sigam esse padrao
podem ser adicionados a pagina apenas declarando o bloco em
`montar_manifesto.py`, sem escrever HTML.

## Como acrescentar audios

1. Coloque os arquivos em algum lugar sob `docs/` (idealmente na convencao acima).
2. Em `montar_manifesto.py`, edite a funcao do bloco correspondente — ou crie
   uma nova e registre-a em `montar()`.
3. Rode os dois scripts. Se algum caminho estiver errado, `montar_manifesto.py`
   imprime `AUSENTE: <caminho>` e o numero de pendencias.

## Estrutura de um bloco no manifesto

```jsonc
{
  "id": "xtts-ajuste-fino",        // ancora na pagina (#xtts-ajuste-fino)
  "numero": 2,
  "titulo": "XTTS -- ajuste fino",
  "estrategia": "Ajuste fino",
  "resultado": "parcial",           // positivo | parcial | negativo | referencia
  "afirmacao": "...",               // o que o examinador deve poder confirmar
  "descricao": "...",               // o que se espera ouvir; aceita [link](url), **negrito**, *italico*
  "tabelas": [{
    "titulo": null,
    "nota": null,
    "colunas": ["Original (checkpoint base)", "Ajustado (FALA_PB)"],
    "linhas": [{
      "rotulo": null,               // rotulo curto opcional acima do texto
      "texto": "frase sintetizada",  // aparece escrito ao lado dos players
      "arquivos": ["15/xtts/a.wav", "15/xtts/b.wav"]  // null = "nao disponivel"
    }]
  }],
  "links": [{"rotulo": "...", "url": "/fala_pb/100/"}]  // opcional
}
```

O numero de itens em `arquivos` deve casar com o numero de `colunas`; use
`null` para uma celula vazia (a pagina mostra "nao disponivel" em vez de
esconder a comparacao).

## Requisitos da pagina gerada

- Reproducao com `<audio controls>` puro — funciona **sem JavaScript**.
- `preload="none"`: a pagina abre rapido mesmo com 175 players.
- Comparacoes `original x ajustado` ficam **na mesma linha**, com a mesma frase
  nas duas colunas e rotulos explicitos (a verificacao nao e cega).
- Layout em flexbox: as colunas empilham automaticamente em telas estreitas.
- Cada bloco tem uma ancora estavel, para citar um bloco especifico em nota de
  rodape (ex.: `.../amostras/#f5tts-do-zero`).

## Licenca e uso

Os audios sao **material de pesquisa academica**, gerados no ambito de uma
dissertacao de mestrado sobre a incorporacao do sotaque paraibano em modelos
abertos de sintese de fala. Estao disponiveis para fins de **verificacao
cientifica, ensino e pesquisa**.

As gravacoes de referencia usadas na clonagem foram cedidas pelo proprio autor.
As sinteses sao saidas de modelos de terceiros (XTTS, F5-TTS, Orpheus TTS, Fish
Speech, Qwen3-TTS) ajustados sobre o corpus FALA_PB, e permanecem sujeitas as
licencas originais desses modelos. Ao reutilizar qualquer material desta pasta,
cite a dissertacao.

O codigo desta pasta segue a licenca do repositorio (ver `LICENSE` na raiz).

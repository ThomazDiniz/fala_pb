#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Monta o manifesto (manifest.json) da pagina de escuta a partir da arvore de
arquivos de audio ja existente em docs/ e dos CSVs/TXTs de acompanhamento.

Uso:
    python docs/amostras/montar_manifesto.py

Saida:
    docs/amostras/manifest.json

O manifesto e' o unico lugar onde se declara o que a pagina mostra. Para
acrescentar audios novos, edite este script (ou o proprio manifest.json) e
rode em seguida `gerar_pagina.py`.

Convencao de caminhos: todo caminho no manifesto e' relativo a docs/ (a raiz
publicada pelo GitHub Pages), com barras normais e sem escapes de URL --
o gerador cuida do percent-encoding.
"""

import csv
import json
from pathlib import Path

DOCS = Path(__file__).resolve().parent.parent
SAIDA = DOCS / "amostras" / "manifest.json"

# --------------------------------------------------------------------------
# Fontes de texto
# --------------------------------------------------------------------------

# As cinco frases fixas de acompanhamento, usadas nos blocos 2 a 7.
FRASES_FIXAS = [
    "Hoje acordei cedo, preparei um cafe forte e organizei a mesa para estudar com calma.",
    "Enquanto o trem passava devagar, uma crianca sorria e apontava para as nuvens alaranjadas.",
    "O pesquisador analisou os dados, escreveu um relatorio objetivo e compartilhou as conclusoes com a equipe.",
    "Estamos construindo uma rotina mais saudavel, caminhando no bairro e cozinhando alimentos frescos todos os dias.",
    "A bibliotecaria catalogou romances, dicionarios e biografias, mantendo cada prateleira limpa e bem sinalizada.",
]


def frases_fixas():
    """Le as frases fixas do manifest.csv do Qwen3-TTS, com fallback embutido."""
    origem = DOCS / "18" / "QWEEN - TTS" / "outputs" / "prompts.txt"
    if origem.exists():
        linhas = [l.strip() for l in origem.read_text(encoding="utf-8").splitlines()]
        linhas = [l for l in linhas if l]
        if len(linhas) >= 5:
            return linhas[:5]
    return FRASES_FIXAS


# Os dez textos-chave sintetizados no experimento de clonagem (bloco 1).
TEXTOS_CLONAGEM = [
    "A tecnologia mudou a forma como nos comunicamos e aprendemos.",
    "A vida e feita de escolhas.",
    "Aprender nunca e demais.",
    "As bibliotecas publicas tem papel essencial na democratizacao do conhecimento, "
    "oferecendo nao so livros, mas tambem acesso a internet, cursos e espacos de "
    "convivencia para a comunidade local.",
    "Em um mundo cada vez mais conectado, e fundamental equilibrar o uso de "
    "dispositivos moveis com momentos de descanso e socializacao presencial, "
    "preservando nossa saude mental e bem-estar.",
    "Hoje o ceu amanheceu com nuvens carregadas e uma leve brisa.",
    "No interior da cidade, pracas antigas guardam historias de geracoes.",
    "O cafe fresco pela manha anima qualquer rotina.",
    "Ola, tudo bem?",
    "Projetos de ciencia cidada estimulam a participacao de voluntarios em coletas "
    "de dados ambientais e podem contribuir para pesquisas sobre mudancas "
    "climaticas, flora, fauna e qualidade da agua em diversas regioes.",
]


# --------------------------------------------------------------------------
# Blocos
# --------------------------------------------------------------------------

def bloco_1_clonagem():
    ref = "audios/experimento_timbre/refs"
    mesmo_texto = "audios/experimento_timbre/output texto original"
    chave = "audios/experimento_timbre/output"

    tabelas = []
    for letra, dur in (("a", "10 s"), ("b", "30 s"), ("c", "60 s")):
        tabelas.append({
            "titulo": f"Referencia de {dur}",
            "nota": (f"Cinco gravacoes de referencia de aproximadamente {dur} cada, "
                     "ao lado da sintese produzida com o mesmo texto da referencia. "
                     "Compare timbre (proximo) e sotaque (distante)."),
            "colunas": ["Referencia (locutor real)", "Sintese clonada (mesmo texto)"],
            "linhas": [
                {
                    "rotulo": f"Amostra {i}",
                    "texto": None,
                    "arquivos": [
                        f"{ref}/thomaz_{letra}{i}.wav",
                        f"{mesmo_texto}/xtts_{letra.upper()}{i}.wav",
                    ],
                }
                for i in range(1, 6)
            ],
        })

    tabelas.append({
        "titulo": "Dez frases-chave, nas tres duracoes de referencia",
        "nota": ("As mesmas dez frases sintetizadas a partir das referencias de 10 s, "
                 "30 s e 60 s. Aumentar a duracao da referencia nao aproxima a saida "
                 "do sotaque paraibano."),
        "colunas": ["Referencia de 10 s", "Referencia de 30 s", "Referencia de 60 s"],
        "linhas": [
            {
                "rotulo": None,
                "texto": TEXTOS_CLONAGEM[i - 1],
                "arquivos": [
                    f"{chave}/xtts_A{i}.wav",
                    f"{chave}/xtts_B{i}.wav",
                    f"{chave}/xtts_C{i}.wav",
                ],
            }
            for i in range(1, 11)
        ],
    })

    return {
        "id": "clonagem",
        "numero": 1,
        "titulo": "Clonagem de fala (XTTS)",
        "estrategia": "Clonagem de fala",
        "resultado": "negativo",
        "afirmacao": ("O timbre do locutor e reproduzido de forma reconhecivel, mas o "
                      "sotaque paraibano nao e capturado em nenhuma das tres condicoes "
                      "de referencia (10 s, 30 s e 60 s)."),
        "descricao": ("O que se espera ouvir: uma voz que soa como a do locutor de "
                      "referencia, porem com prosodia e realizacao fonetica de padrao "
                      "sudeste/neutro. Alongar a referencia de 10 s para 60 s melhora "
                      "pouco ou nada a transferencia de sotaque -- e este e o ponto do "
                      "bloco. Pagina completa do experimento: "
                      "[reuniao 2](/fala_pb/2/)."),
        "tabelas": tabelas,
    }


def bloco_2_xtts():
    base = "15/xtts"
    frases = frases_fixas()
    return {
        "id": "xtts-ajuste-fino",
        "numero": 2,
        "titulo": "XTTS -- ajuste fino",
        "estrategia": "Ajuste fino",
        "resultado": "positivo",
        "afirmacao": ("O ajuste fino incorporou o sotaque paraibano: tracos regionais "
                      "passam a ser audiveis na saida do modelo, num sotaque misto em que "
                      "convivem com o padrao do checkpoint base."),
        "descricao": ("Mesma frase nas duas colunas, mesmo prompt de voz. A coluna "
                      "*original* e o checkpoint publico do XTTS; a coluna *ajustado* e o "
                      "melhor checkpoint do ajuste fino sobre o FALA_PB. Ouca sobretudo a "
                      "realizacao das vogais atonas finais e o ritmo. Pagina completa: "
                      "[reuniao 15](/fala_pb/15/)."),
        "tabelas": [{
            "titulo": None,
            "nota": None,
            "colunas": ["Referencia de voz", "Original (checkpoint base)", "Ajustado (FALA_PB)"],
            "linhas": [
                {
                    "rotulo": None,
                    "texto": frases[i - 1],
                    "arquivos": [
                        f"{base}/xtts_ref_frase0{i}.wav",
                        f"{base}/xtts_model_original_frase0{i}.wav",
                        f"{base}/xtts_model_best_frase0{i}.wav",
                    ],
                }
                for i in range(1, 6)
            ],
        }],
    }


def bloco_3_f5tts():
    base = "16/f5tts novo treino"
    frases = frases_fixas()
    return {
        "id": "f5tts-ajuste-fino",
        "numero": 3,
        "titulo": "F5-TTS -- ajuste fino",
        "estrategia": "Ajuste fino",
        "resultado": "negativo",
        "afirmacao": ("As saidas do modelo ajustado ficaram praticamente identicas as do "
                      "checkpoint original, apesar de os pesos terem mudado ao longo do "
                      "treino."),
        "descricao": ("As duas colunas foram sintetizadas com a mesma semente e o mesmo "
                      "prompt, variando apenas o checkpoint. A quase indistinguibilidade "
                      "entre elas e o resultado -- e uma evidencia negativa, nao um erro "
                      "de montagem da pagina. Pagina completa: "
                      "[reuniao 16](/fala_pb/16/)."),
        "tabelas": [{
            "titulo": None,
            "nota": None,
            "colunas": ["Original (checkpoint base)", "Ajustado (FALA_PB, ultimo checkpoint)"],
            "linhas": [
                {
                    "rotulo": None,
                    "texto": frases[i - 1],
                    "arquivos": [
                        f"{base}/filtered_checkpoint_original_line0{i}.wav",
                        f"{base}/filtered_model_last_line0{i}.wav",
                    ],
                }
                for i in range(1, 6)
            ],
        }],
    }


def bloco_4_orpheus():
    ajustado = "15/artoodtoo_ft_e3/audios experimento"
    frases = frases_fixas()

    tabelas = [{
        "titulo": "Cinco frases fixas de acompanhamento",
        "nota": ("Para o Orpheus nao foi preservada a sintese do checkpoint base sobre "
                 "estas cinco frases; a comparacao original x ajustado aparece na tabela "
                 "seguinte, sobre as sentencas da avaliacao final."),
        "colunas": ["Ajustado (FALA_PB, 1 epoca)"],
        "linhas": [
            {
                "rotulo": None,
                "texto": frases[i - 1],
                "arquivos": [f"{ajustado}/unsloth_artoodtoo_model_1_frase0{i:d}.wav"],
            }
            for i in range(1, 6)
        ],
    }]

    tabelas.append(tabela_inferencias_finais(
        modelo="unsloth",
        titulo="Original x ajustado (sentencas da avaliacao final)",
        nota=("Cinco sentencas do conjunto de 100, na versao eleita pelo criterio "
              "melhor-de-3. Mesma sentenca nas duas colunas."),
    ))

    return {
        "id": "orpheus-ajuste-fino",
        "numero": 4,
        "titulo": "Orpheus TTS -- ajuste fino",
        "estrategia": "Ajuste fino",
        "resultado": "positivo",
        "afirmacao": "A incorporacao do sotaque paraibano foi satisfatoria.",
        "descricao": ("Este e o bloco em que a adaptacao mais se ouve. Compare a coluna "
                      "*ajustado* com a *original*: a diferenca esperada esta na abertura "
                      "das vogais pretonicas e no contorno entoacional. Paginas completas: "
                      "[reuniao 15](/fala_pb/15/) e [reuniao 16](/fala_pb/16/)."),
        "tabelas": tabelas,
    }


def bloco_5_fishspeech():
    base = "17/fishspeech"
    frases = frases_fixas()
    return {
        "id": "fishspeech-ajuste-fino",
        "numero": 5,
        "titulo": "Fish Speech -- ajuste fino",
        "estrategia": "Ajuste fino",
        "resultado": "positivo",
        "afirmacao": ("Uma unica epoca de ajuste fino (LoRA) ja bastou para tornar o "
                      "sotaque paraibano perceptivel nas sinteses."),
        "descricao": ("Mesmo prompt de voz de referencia nas duas colunas. Compare a "
                      "coluna *ajustado* com a *original*: a adaptacao se ouve com mais "
                      "forca em algumas frases do que em outras, o que era de esperar de "
                      "um treino de uma unica epoca. Ouca as cinco. Pagina completa: "
                      "[reuniao 17](/fala_pb/17/)."),
        "tabelas": [{
            "titulo": None,
            "nota": None,
            "colunas": ["Prompt de referencia", "Original (Fish Speech 1.5)", "Ajustado (LoRA, 1 epoca)"],
            "linhas": [
                {
                    "rotulo": None,
                    "texto": frases[i - 1],
                    "arquivos": [
                        f"{base}/reference_prompt.wav",
                        f"{base}/baseline_phrase_0{i}.wav",
                        f"{base}/step_000010488_phrase_0{i}.wav",
                    ],
                }
                for i in range(1, 6)
            ],
        }],
    }


def bloco_6_qwen():
    base = "18/QWEEN - TTS/outputs"
    frases = frases_fixas()
    return {
        "id": "qwen3-ajuste-fino",
        "numero": 6,
        "titulo": "Qwen3-TTS -- ajuste fino",
        "estrategia": "Ajuste fino",
        "resultado": "negativo",
        "afirmacao": ("A perda de treino caiu ao longo dos checkpoints, mas nao houve "
                      "aproximacao audivel ao sotaque paraibano."),
        "descricao": ("Tres checkpoints intermediarios (5 mil, 10 mil e 15 mil passos) "
                      "comparados ao baseline anterior ao ajuste. O que se espera ouvir e "
                      "ausencia de progressao: as quatro colunas soam equivalentes quanto "
                      "ao sotaque. Pagina completa: [reuniao 18](/fala_pb/18/)."),
        "tabelas": [{
            "titulo": None,
            "nota": None,
            "colunas": ["Original (baseline)", "Ajustado - 5.000 passos",
                        "Ajustado - 10.000 passos", "Ajustado - 15.000 passos"],
            "linhas": [
                {
                    "rotulo": None,
                    "texto": frases[i - 1],
                    "arquivos": [
                        f"{base}/pre_finetune_baseline_case_0{i}.wav",
                        f"{base}/step_5000_frase{i}.wav",
                        f"{base}/step_10000_frase{i}.wav",
                        f"{base}/step_15000_frase{i}.wav",
                    ],
                }
                for i in range(1, 6)
            ],
        }],
    }


def bloco_7_zero():
    base = "19/f5tts_do_zero"
    frases = frases_fixas()
    return {
        "id": "f5tts-do-zero",
        "numero": 7,
        "titulo": "F5-TTS treinado a partir de pesos aleatorios",
        "estrategia": "Treinamento a partir de pesos aleatorios",
        "resultado": "negativo",
        "afirmacao": ("O checkpoint final (epoca 150) produz saidas ininteligiveis: as "
                      "111 h do FALA_PB nao bastam para treinar o modelo do zero."),
        "descricao": ("Evidencia negativa. Nao ha coluna *original* aqui porque nao existe "
                      "checkpoint base -- o treino partiu de pesos aleatorios. A referencia "
                      "de voz esta na primeira coluna para dar a medida do que se esperava "
                      "obter. Pagina completa: [reuniao 19](/fala_pb/19/)."),
        "tabelas": [{
            "titulo": None,
            "nota": None,
            "colunas": ["Referencia de voz", "Do zero (epoca 150, checkpoint final)"],
            "linhas": [
                {
                    "rotulo": None,
                    "texto": frases[i - 1],
                    "arquivos": [
                        f"{base}/PB_0991_ref.wav",
                        f"{base}/zero_model_last_line0{i}.wav",
                    ],
                }
                for i in range(1, 6)
            ],
        }],
    }


# --------------------------------------------------------------------------
# Bloco 8 e a amostra melhor-de-3
# --------------------------------------------------------------------------

CSV_MELHOR_DE_3 = DOCS.parent / "Experimento final" / "resultados" / "csv2_melhor_de_3.csv"
INFER_BASE = "Inferencias finais/Audios"
INDICES_AMOSTRA = [1, 3, 12, 36, 71]  # sentencas curtas, medias e longas
NOME_MODELO = {"xtts": "XTTS", "unsloth": "Orpheus TTS", "fishspeech": "Fish Speech"}


def ler_melhor_de_3():
    """Devolve {(modelo, condicao, indice): (caminho_relativo, texto)}."""
    if not CSV_MELHOR_DE_3.exists():
        return {}
    escolhas = {}
    with CSV_MELHOR_DE_3.open(encoding="utf-8-sig", newline="") as fh:
        for r in csv.DictReader(fh):
            if r.get("status") != "ok":
                continue
            idx = int(r["indice"])
            var = r["variacao_escolhida"]
            caminho = (f"{INFER_BASE}/{r['modelo']}/outputs_final_experiment/"
                       f"{r['condicao']}/{var}/{idx:03d}.wav")
            escolhas[(r["modelo"], r["condicao"], idx)] = (caminho, r["texto_original"])
    return escolhas


def tabela_inferencias_finais(modelo, titulo, nota):
    escolhas = ler_melhor_de_3()
    linhas = []
    for idx in INDICES_AMOSTRA:
        orig = escolhas.get((modelo, "original", idx))
        ajus = escolhas.get((modelo, "ajustado", idx))
        if not orig or not ajus:
            continue
        linhas.append({
            "rotulo": f"Sentenca {idx:03d}",
            "texto": orig[1],
            "arquivos": [orig[0], ajus[0]],
        })
    return {
        "titulo": titulo,
        "nota": nota,
        "colunas": ["Original (checkpoint base)", "Ajustado (FALA_PB)"],
        "linhas": linhas,
    }


def bloco_8_avaliacao():
    escolhas = ler_melhor_de_3()
    tabelas = []
    for modelo in ("xtts", "unsloth", "fishspeech"):
        linhas = []
        for idx in INDICES_AMOSTRA:
            orig = escolhas.get((modelo, "original", idx))
            ajus = escolhas.get((modelo, "ajustado", idx))
            if not orig or not ajus:
                continue
            linhas.append({
                "rotulo": f"Sentenca {idx:03d}",
                "texto": orig[1],
                "arquivos": [orig[0], ajus[0]],
            })
        if linhas:
            tabelas.append({
                "titulo": NOME_MODELO[modelo],
                "nota": None,
                "colunas": ["Original (checkpoint base)", "Ajustado (FALA_PB)"],
                "linhas": linhas,
            })

    return {
        "id": "avaliacao-automatica",
        "numero": 8,
        "titulo": "Avaliacao automatica -- conjunto completo",
        "estrategia": "Ajuste fino (tres modelos)",
        "resultado": "referencia",
        "afirmacao": ("As metricas objetivas reportadas na dissertacao foram calculadas "
                      "sobre 600 audios: 3 modelos x 2 condicoes x 100 sentencas, cada um "
                      "eleito por melhor-de-3 entre tres sinteses independentes "
                      "(1.800 sinteses no total)."),
        "descricao": ("Este conjunto nao e listado item a item aqui. Abaixo estao cinco "
                      "sentencas por modelo, na versao efetivamente usada nas metricas, "
                      "como amostra. O catalogo completo dos 1.800 audios, com filtros por "
                      "modelo e condicao, esta na "
                      "**[pagina de inferencias finais](/fala_pb/100/)**."),
        "tabelas": tabelas,
        "links": [
            {"rotulo": "Catalogo completo dos 1.800 audios", "url": "/fala_pb/100/"},
            {"rotulo": "Metodologia e resultados da avaliacao automatica", "url": "/fala_pb/20/"},
            {"rotulo": "Validacao perceptual com ouvintes", "url": "/fala_pb/21/"},
        ],
    }


# --------------------------------------------------------------------------

def montar():
    return {
        "titulo": "Amostras de audio da dissertacao",
        "subtitulo": ("Material de escuta para verificacao das afirmacoes feitas nos "
                      "capitulos de resultados"),
        "corpus": "FALA_PB -- aproximadamente 111 h de fala com sotaque paraibano",
        "modelos": ["XTTS", "F5-TTS", "Orpheus TTS", "Fish Speech", "Qwen3-TTS"],
        "estrategias": ["Clonagem de fala", "Ajuste fino",
                        "Treinamento a partir de pesos aleatorios"],
        "blocos": [
            bloco_1_clonagem(),
            bloco_2_xtts(),
            bloco_3_f5tts(),
            bloco_4_orpheus(),
            bloco_5_fishspeech(),
            bloco_6_qwen(),
            bloco_7_zero(),
            bloco_8_avaliacao(),
        ],
    }


def main():
    manifesto = montar()

    ausentes = []
    total = 0
    for bloco in manifesto["blocos"]:
        for tabela in bloco["tabelas"]:
            for linha in tabela["linhas"]:
                for arq in linha["arquivos"]:
                    if not arq:
                        continue
                    total += 1
                    if not (DOCS / arq).exists():
                        ausentes.append(arq)

    SAIDA.parent.mkdir(parents=True, exist_ok=True)
    SAIDA.write_text(json.dumps(manifesto, ensure_ascii=False, indent=2) + "\n",
                     encoding="utf-8")

    print(f"manifesto escrito em {SAIDA}")
    print(f"{total} referencias de audio; {len(ausentes)} ausentes")
    for a in ausentes:
        print("  AUSENTE:", a)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Monta o manifesto (manifest.json) da página de escuta a partir da árvore de
arquivos de áudio já existente em docs/ e dos CSVs/TXTs de acompanhamento.

Uso:
    python docs/amostras/montar_manifesto.py

Saída:
    docs/amostras/manifest.json

O manifesto é o único lugar onde se declara o que a página mostra. Para
acrescentar áudios novos, edite este script (ou o próprio manifest.json) e
rode em seguida `gerar_pagina.py`.

Convenção de caminhos: todo caminho no manifesto é relativo a docs/ (a raiz
publicada pelo GitHub Pages), com barras normais e sem escapes de URL —
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
    "Hoje acordei cedo, preparei um café forte e organizei a mesa para estudar com calma.",
    "Enquanto o trem passava devagar, uma criança sorria e apontava para as nuvens alaranjadas.",
    "O pesquisador analisou os dados, escreveu um relatório objetivo e compartilhou as conclusões com a equipe.",
    "Estamos construindo uma rotina mais saudável, caminhando no bairro e cozinhando alimentos frescos todos os dias.",
    "A bibliotecária catalogou romances, dicionários e biografias, mantendo cada prateleira limpa e bem sinalizada.",
]


def frases_fixas():
    """Lê as frases fixas do prompts.txt do Qwen3-TTS, com fallback embutido."""
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
    "A vida é feita de escolhas.",
    "Aprender nunca é demais.",
    "As bibliotecas públicas têm papel essencial na democratização do conhecimento, "
    "oferecendo não só livros, mas também acesso à internet, cursos e espaços de "
    "convivência para a comunidade local.",
    "Em um mundo cada vez mais conectado, é fundamental equilibrar o uso de "
    "dispositivos móveis com momentos de descanso e socialização presencial, "
    "preservando nossa saúde mental e bem-estar.",
    "Hoje o céu amanheceu com nuvens carregadas e uma leve brisa.",
    "No interior da cidade, praças antigas guardam histórias de gerações.",
    "O café fresco pela manhã anima qualquer rotina.",
    "Olá, tudo bem?",
    "Projetos de ciência cidadã estimulam a participação de voluntários em coletas "
    "de dados ambientais e podem contribuir para pesquisas sobre mudanças "
    "climáticas, flora, fauna e qualidade da água em diversas regiões.",
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
            "titulo": f"Referência de {dur}",
            "nota": (f"Cinco gravações de referência de aproximadamente {dur} cada, "
                     "ao lado da síntese produzida com o mesmo texto da referência. "
                     "Compare o timbre (próximo) e o sotaque (distante)."),
            "colunas": ["Referência (locutor real)", "Síntese clonada (mesmo texto)"],
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
        "titulo": "Dez frases-chave, nas três durações de referência",
        "nota": ("As mesmas dez frases sintetizadas a partir das referências de 10 s, "
                 "30 s e 60 s. Aumentar a duração da referência não aproxima a saída "
                 "do sotaque paraibano."),
        "colunas": ["Referência de 10 s", "Referência de 30 s", "Referência de 60 s"],
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
        "afirmacao": ("O timbre do locutor é reproduzido de forma reconhecível, mas o "
                      "sotaque paraibano não é capturado em nenhuma das três condições "
                      "de referência (10 s, 30 s e 60 s)."),
        "descricao": ("O que se espera ouvir: uma voz que soa como a do locutor de "
                      "referência, porém com prosódia e realização fonética de padrão "
                      "sudeste/neutro. Alongar a referência de 10 s para 60 s melhora "
                      "pouco ou nada a transferência de sotaque — e este é o ponto do "
                      "bloco. Página completa do experimento: "
                      "[reunião 2](/fala_pb/2/)."),
        "tabelas": tabelas,
    }


def bloco_2_xtts():
    base = "15/xtts"
    frases = frases_fixas()
    return {
        "id": "xtts-ajuste-fino",
        "numero": 2,
        "titulo": "XTTS — ajuste fino",
        "estrategia": "Ajuste fino",
        "resultado": "positivo",
        "afirmacao": ("O ajuste fino incorporou o sotaque paraibano: traços regionais "
                      "passam a ser audíveis na saída do modelo, num sotaque misto em que "
                      "convivem com o padrão do checkpoint base."),
        "descricao": ("Mesma frase nas duas colunas, mesmo prompt de voz. A coluna "
                      "*original* é o checkpoint público do XTTS; a coluna *ajustado* é o "
                      "melhor checkpoint do ajuste fino sobre o FALA_PB. Ouça sobretudo a "
                      "realização das vogais átonas finais e o ritmo. Página completa: "
                      "[reunião 15](/fala_pb/15/)."),
        "tabelas": [{
            "titulo": None,
            "nota": None,
            "colunas": ["Referência de voz", "Original (checkpoint base)", "Ajustado (FALA_PB)"],
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
        "titulo": "F5-TTS — ajuste fino",
        "estrategia": "Ajuste fino",
        "resultado": "negativo",
        "afirmacao": ("As saídas do modelo ajustado ficaram praticamente idênticas às do "
                      "checkpoint original, apesar de os pesos terem mudado ao longo do "
                      "treino."),
        "descricao": ("As duas colunas foram sintetizadas com a mesma semente e o mesmo "
                      "prompt, variando apenas o checkpoint. A quase indistinguibilidade "
                      "entre elas é o resultado — é uma evidência negativa, não um erro "
                      "de montagem da página. Página completa: "
                      "[reunião 16](/fala_pb/16/)."),
        "tabelas": [{
            "titulo": None,
            "nota": None,
            "colunas": ["Original (checkpoint base)", "Ajustado (FALA_PB, último checkpoint)"],
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
        "nota": ("Para o Orpheus não foi preservada a síntese do checkpoint base sobre "
                 "estas cinco frases; a comparação original × ajustado aparece na tabela "
                 "seguinte, sobre as sentenças da avaliação final."),
        "colunas": ["Ajustado (FALA_PB, 1 época)"],
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
        titulo="Original × ajustado (sentenças da avaliação final)",
        nota=("Cinco sentenças do conjunto de 100, na versão eleita pelo critério "
              "melhor-de-3. Mesma sentença nas duas colunas."),
    ))

    return {
        "id": "orpheus-ajuste-fino",
        "numero": 4,
        "titulo": "Orpheus TTS — ajuste fino",
        "estrategia": "Ajuste fino",
        "resultado": "positivo",
        "afirmacao": "A incorporação do sotaque paraibano foi satisfatória.",
        "descricao": ("Este é o bloco em que a adaptação mais se ouve. Compare a coluna "
                      "*ajustado* com a *original*: a diferença esperada está na abertura "
                      "das vogais pretônicas e no contorno entoacional. Páginas completas: "
                      "[reunião 15](/fala_pb/15/) e [reunião 16](/fala_pb/16/)."),
        "tabelas": tabelas,
    }


def bloco_5_fishspeech():
    base = "17/fishspeech"
    frases = frases_fixas()
    return {
        "id": "fishspeech-ajuste-fino",
        "numero": 5,
        "titulo": "Fish Speech — ajuste fino",
        "estrategia": "Ajuste fino",
        "resultado": "positivo",
        "afirmacao": ("Uma única época de ajuste fino (LoRA) já bastou para tornar o "
                      "sotaque paraibano perceptível nas sínteses."),
        "descricao": ("Mesmo prompt de voz de referência nas duas colunas. Compare a "
                      "coluna *ajustado* com a *original*: a adaptação se ouve com mais "
                      "força em algumas frases do que em outras, o que era de esperar de "
                      "um treino de uma única época. Ouça as cinco. Página completa: "
                      "[reunião 17](/fala_pb/17/)."),
        "tabelas": [{
            "titulo": None,
            "nota": None,
            "colunas": ["Prompt de referência", "Original (Fish Speech 1.5)",
                        "Ajustado (LoRA, 1 época)"],
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
        "titulo": "Qwen3-TTS — ajuste fino",
        "estrategia": "Ajuste fino",
        "resultado": "negativo",
        "afirmacao": ("A perda de treino caiu ao longo dos checkpoints, mas não houve "
                      "aproximação audível ao sotaque paraibano."),
        "descricao": ("Três checkpoints intermediários (5 mil, 10 mil e 15 mil passos) "
                      "comparados ao baseline anterior ao ajuste. O que se espera ouvir é "
                      "ausência de progressão: as quatro colunas soam equivalentes quanto "
                      "ao sotaque. Página completa: [reunião 18](/fala_pb/18/)."),
        "tabelas": [{
            "titulo": None,
            "nota": None,
            "colunas": ["Original (baseline)", "Ajustado — 5.000 passos",
                        "Ajustado — 10.000 passos", "Ajustado — 15.000 passos"],
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
        "titulo": "F5-TTS treinado a partir de pesos aleatórios",
        "estrategia": "Treinamento a partir de pesos aleatórios",
        "resultado": "negativo",
        "afirmacao": ("O checkpoint final (época 150) produz saídas ininteligíveis: as "
                      "111 h do FALA_PB não bastam para treinar o modelo do zero."),
        "descricao": ("Evidência negativa. Não há coluna *original* aqui porque não existe "
                      "checkpoint base — o treino partiu de pesos aleatórios. A referência "
                      "de voz está na primeira coluna para dar a medida do que se esperava "
                      "obter. Página completa: [reunião 19](/fala_pb/19/)."),
        "tabelas": [{
            "titulo": None,
            "nota": None,
            "colunas": ["Referência de voz", "Do zero (época 150, checkpoint final)"],
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
INDICES_AMOSTRA = [1, 3, 12, 36, 71]  # sentenças curtas, médias e longas
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
            "rotulo": f"Sentença {idx:03d}",
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
                "rotulo": f"Sentença {idx:03d}",
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
        "titulo": "Avaliação automática — conjunto completo",
        "estrategia": "Ajuste fino (três modelos)",
        "resultado": "referencia",
        "afirmacao": ("As métricas objetivas reportadas na dissertação foram calculadas "
                      "sobre 600 áudios: 3 modelos × 2 condições × 100 sentenças, cada um "
                      "eleito por melhor-de-3 entre três sínteses independentes "
                      "(1.800 sínteses no total)."),
        "descricao": ("Este conjunto não é listado item a item aqui. Abaixo estão cinco "
                      "sentenças por modelo, na versão efetivamente usada nas métricas, "
                      "como amostra. O catálogo completo dos 1.800 áudios, com filtros por "
                      "modelo e condição, está na "
                      "**[página de inferências finais](/fala_pb/100/)**."),
        "tabelas": tabelas,
        "links": [
            {"rotulo": "Catálogo completo dos 1.800 áudios", "url": "/fala_pb/100/"},
            {"rotulo": "Metodologia e resultados da avaliação automática", "url": "/fala_pb/20/"},
            {"rotulo": "Validação perceptual com ouvintes", "url": "/fala_pb/21/"},
        ],
    }


# --------------------------------------------------------------------------

def montar():
    return {
        "titulo": "Amostras de áudio da dissertação",
        "subtitulo": ("Material de escuta para verificação das afirmações feitas nos "
                      "capítulos de resultados"),
        "corpus": "FALA_PB — aproximadamente 111 h de fala com sotaque paraibano",
        "modelos": ["XTTS", "F5-TTS", "Orpheus TTS", "Fish Speech", "Qwen3-TTS"],
        "estrategias": ["Clonagem de fala", "Ajuste fino",
                        "Treinamento a partir de pesos aleatórios"],
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
    print(f"{total} referências de áudio; {len(ausentes)} ausentes")
    for a in ausentes:
        print("  AUSENTE:", a)


if __name__ == "__main__":
    main()

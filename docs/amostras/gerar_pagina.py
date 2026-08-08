#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gera docs/amostras.md a partir de docs/amostras/manifest.json.

Uso:
    python docs/amostras/montar_manifesto.py   # (re)constroi o manifesto
    python docs/amostras/gerar_pagina.py       # renderiza a pagina

A página resultante é HTML estático dentro de um arquivo Markdown com front
matter do Jekyll. A reprodução dos áudios usa apenas <audio controls>, sem
JavaScript, e o layout se adapta a telas estreitas por CSS.
"""

import html
import json
from pathlib import Path
from urllib.parse import quote

AQUI = Path(__file__).resolve().parent
DOCS = AQUI.parent
MANIFESTO = AQUI / "manifest.json"
SAIDA = DOCS / "amostras.md"

SELO = {
    "positivo": ("resultado positivo", "art-selo--pos"),
    "parcial": ("resultado parcial", "art-selo--parc"),
    "negativo": ("resultado negativo", "art-selo--neg"),
    "referencia": ("conjunto de referência", "art-selo--ref"),
}

CSS = """<style>
  .wrapper, .markdown-body, .inner, #main_content {
    max-width: 1100px !important;
    padding: 1rem 1.5rem !important;
  }
  .art-intro { font-size: 1rem; line-height: 1.6; }
  .art-meta {
    border: 1px solid #d6d6d6; border-radius: 6px;
    padding: 0.75rem 1rem; margin: 1.25rem 0;
    background: #fafafa; font-size: 0.9rem; line-height: 1.7;
  }
  .art-meta dt { font-weight: 600; }
  .art-sumario { margin: 1.5rem 0 2.5rem; padding: 0; list-style: none; }
  .art-sumario li {
    padding: 0.35rem 0; border-bottom: 1px solid #ececec; font-size: 0.95rem;
  }
  .art-sumario .art-num {
    display: inline-block; min-width: 1.8rem; font-weight: 600; color: #666;
  }
  .art-bloco { margin: 3rem 0; padding-top: 1rem; border-top: 2px solid #e0e0e0; }
  .art-bloco h2 { margin-bottom: 0.35rem; }
  .art-selo {
    display: inline-block; font-size: 0.72rem; text-transform: uppercase;
    letter-spacing: 0.04em; padding: 0.18rem 0.5rem; border-radius: 3px;
    border: 1px solid currentColor; vertical-align: middle; margin-left: 0.5rem;
  }
  .art-selo--pos  { color: #1d6f42; }
  .art-selo--parc { color: #8a6100; }
  .art-selo--neg  { color: #9a2b2b; }
  .art-selo--ref  { color: #40566d; }
  .art-afirmacao {
    border-left: 4px solid #999; padding: 0.5rem 0 0.5rem 0.9rem;
    margin: 0.9rem 0 1rem; font-size: 0.95rem; background: #f7f7f7;
  }
  .art-afirmacao strong { display: block; font-size: 0.75rem;
    text-transform: uppercase; letter-spacing: 0.04em; color: #666;
    margin-bottom: 0.25rem; }
  .art-desc { font-size: 0.95rem; line-height: 1.65; }
  .art-tabela { margin: 1.75rem 0; }
  .art-tabela > h3 { font-size: 1.02rem; margin-bottom: 0.3rem; }
  .art-nota { font-size: 0.87rem; color: #555; margin: 0 0 0.9rem; line-height: 1.55; }
  .art-linha {
    border: 1px solid #e2e2e2; border-radius: 6px;
    padding: 0.8rem 0.9rem; margin-bottom: 0.7rem; background: #fff;
  }
  .art-rotulo-linha {
    font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.04em;
    color: #777; margin: 0 0 0.3rem;
  }
  .art-texto {
    margin: 0 0 0.7rem; font-size: 0.93rem; line-height: 1.5; color: #222;
  }
  .art-texto::before { content: "\\201C"; }
  .art-texto::after  { content: "\\201D"; }
  .art-cols { display: flex; flex-wrap: wrap; gap: 0.75rem; }
  .art-col { flex: 1 1 220px; min-width: 200px; }
  .art-col-rot {
    display: block; font-size: 0.78rem; font-weight: 600; color: #444;
    margin-bottom: 0.25rem;
  }
  .art-col audio { width: 100%; max-width: 100%; height: 36px; }
  .art-vazio {
    display: block; font-size: 0.8rem; color: #999; font-style: italic;
    padding: 0.55rem 0;
  }
  .art-links { margin: 1.25rem 0 0; padding: 0; list-style: none; font-size: 0.93rem; }
  .art-links li { padding: 0.2rem 0; }
  .art-topo { font-size: 0.82rem; color: #777; }
  .art-rodape {
    margin-top: 3rem; padding-top: 1rem; border-top: 1px solid #e5e5e5;
    font-size: 0.88rem; color: #555; line-height: 1.65;
  }
  @media (max-width: 640px) {
    .wrapper, .markdown-body, .inner, #main_content { padding: 0.75rem !important; }
    .art-col { flex: 1 1 100%; min-width: 0; }
  }
</style>"""


def url(caminho: str) -> str:
    """Caminho relativo a docs/ -> URL absoluta no site, com percent-encoding."""
    return "/fala_pb/" + quote(caminho.lstrip("/"))


def e(texto: str) -> str:
    return html.escape(texto, quote=False)


def render_linha(linha, colunas):
    partes = ['<div class="art-linha">']
    if linha.get("rotulo"):
        partes.append(f'<p class="art-rotulo-linha">{e(linha["rotulo"])}</p>')
    if linha.get("texto"):
        partes.append(f'<p class="art-texto">{e(linha["texto"])}</p>')
    partes.append('<div class="art-cols">')
    for rotulo, arq in zip(colunas, linha["arquivos"]):
        partes.append('<div class="art-col">')
        partes.append(f'<span class="art-col-rot">{e(rotulo)}</span>')
        if arq:
            partes.append(
                f'<audio controls preload="none" src="{url(arq)}">'
                f'<a href="{url(arq)}">baixar áudio</a></audio>'
            )
        else:
            partes.append('<span class="art-vazio">não disponível</span>')
        partes.append("</div>")
    partes.append("</div></div>")
    return "\n".join(partes)


def render_tabela(tabela):
    partes = ['<div class="art-tabela">']
    if tabela.get("titulo"):
        partes.append(f'<h3>{e(tabela["titulo"])}</h3>')
    if tabela.get("nota"):
        partes.append(f'<p class="art-nota">{e(tabela["nota"])}</p>')
    for linha in tabela["linhas"]:
        partes.append(render_linha(linha, tabela["colunas"]))
    partes.append("</div>")
    return "\n".join(partes)


def render_bloco(bloco):
    rotulo_selo, classe_selo = SELO.get(bloco["resultado"], ("", "art-selo--ref"))
    partes = [f'<section class="art-bloco" id="{bloco["id"]}" markdown="0">']
    partes.append(
        f'<h2>{bloco["numero"]}. {e(bloco["titulo"])}'
        f'<span class="art-selo {classe_selo}">{rotulo_selo}</span></h2>'
    )
    partes.append(f'<p class="art-topo">Estratégia: {e(bloco["estrategia"])} &middot; '
                  f'<a href="#sumario">voltar ao sumário</a></p>')
    partes.append('<div class="art-afirmacao"><strong>Afirmação verificável</strong>'
                  f'{e(bloco["afirmacao"])}</div>')
    partes.append(f'<p class="art-desc">{link_md(e(bloco["descricao"]))}</p>')
    for tabela in bloco["tabelas"]:
        partes.append(render_tabela(tabela))
    if bloco.get("links"):
        partes.append('<ul class="art-links">')
        for link in bloco["links"]:
            partes.append(f'<li><a href="{link["url"]}">{e(link["rotulo"])}</a></li>')
        partes.append("</ul>")
    partes.append("</section>")
    return "\n".join(partes)


def link_md(texto: str) -> str:
    """Converte [rotulo](url) e **negrito**/*italico* simples para HTML."""
    import re
    texto = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', texto)
    texto = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", texto)
    texto = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", texto)
    return texto


def render_sumario(blocos):
    partes = ['<ul class="art-sumario" id="sumario">']
    for b in blocos:
        rotulo_selo, classe_selo = SELO.get(b["resultado"], ("", "art-selo--ref"))
        partes.append(
            f'<li><span class="art-num">{b["numero"]}.</span>'
            f'<a href="#{b["id"]}">{e(b["titulo"])}</a>'
            f'<span class="art-selo {classe_selo}">{rotulo_selo}</span></li>'
        )
    partes.append("</ul>")
    return "\n".join(partes)


def contar_audios(manifesto):
    return sum(
        1
        for b in manifesto["blocos"]
        for t in b["tabelas"]
        for l in t["linhas"]
        for a in l["arquivos"]
        if a
    )


def main():
    manifesto = json.loads(MANIFESTO.read_text(encoding="utf-8"))
    n = contar_audios(manifesto)

    partes = [
        "---",
        f'title: "{manifesto["titulo"]}"',
        "permalink: /amostras/",
        "layout: default",
        "---",
        "",
        "<!-- ARQUIVO GERADO AUTOMATICAMENTE - nao edite a mao.",
        "     Fonte: docs/amostras/manifest.json",
        "     Regerar: python docs/amostras/montar_manifesto.py",
        "              python docs/amostras/gerar_pagina.py -->",
        "",
        CSS,
        "",
        f'# {e(manifesto["titulo"])}',
        "",
        f'<p class="art-intro">{e(manifesto["subtitulo"])}. Todos os áudios tocam '
        "diretamente no navegador, sem instalação e sem login. Cada bloco abaixo "
        "corresponde a uma afirmação feita na dissertação e reúne o material "
        "necessário para confirmá-la — inclusive quando o resultado é negativo.</p>",
        "",
        '<dl class="art-meta">',
        f'<dt>Corpus de adaptação</dt><dd>{e(manifesto["corpus"])}</dd>',
        f'<dt>Modelos investigados</dt><dd>{e(", ".join(manifesto["modelos"]))}</dd>',
        f'<dt>Estratégias de adaptação</dt><dd>{e(", ".join(manifesto["estrategias"]))}</dd>',
        f'<dt>Áudios nesta página</dt><dd>{n}</dd>',
        "</dl>",
        "",
        "## Sumário",
        "",
        render_sumario(manifesto["blocos"]),
        "",
    ]

    for bloco in manifesto["blocos"]:
        partes.append(render_bloco(bloco))
        partes.append("")

    partes.append(
        '<div class="art-rodape">'
        "<p>Os blocos 2 a 7 usam, em boa parte, o mesmo conjunto de cinco frases "
        "fixas de acompanhamento, o que permite comparar modelos diretamente entre "
        "seções.</p>"
        "<p>Os áudios são material de pesquisa acadêmica, gerados no âmbito de uma "
        "dissertação de mestrado, e estão disponíveis para fins de verificação "
        "científica, ensino e pesquisa. As gravações de referência foram cedidas "
        "pelo próprio autor. Ao reutilizar, cite a dissertação.</p>"
        '<p><a href="/fala_pb/">Índice de experimentos</a> &middot; '
        '<a href="/fala_pb/100/">Catálogo completo das inferências finais</a></p>'
        "</div>"
    )

    SAIDA.write_text("\n".join(partes) + "\n", encoding="utf-8")
    print(f"pagina escrita em {SAIDA} ({n} audios, {len(manifesto['blocos'])} blocos)")


if __name__ == "__main__":
    main()

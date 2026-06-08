"""Regenera a secao de tabela unificada em docs/100.md."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "100.md"
SENTENCES_FILE = ROOT / "Inferencias finais" / "Audios" / "sentenças.txt"
AUDIO_BASE = "/fala_pb/Inferencias%20finais/Audios"

MODELS = [
    ("xtts", "XTTS v2", "xtts"),
    ("fishspeech", "Fish Speech 1.5", "fish-speech"),
    ("unsloth", "Orpheus 3B (Unsloth)", "unsloth"),
]
VARS = [
    ("original", "v1", "Orig v1"),
    ("original", "v2", "Orig v2"),
    ("original", "v3", "Orig v3"),
    ("ajustado", "v1", "Ajust v1"),
    ("ajustado", "v2", "Ajust v2"),
    ("ajustado", "v3", "Ajust v3"),
]

STYLES = """<style>
  .wrapper,
  .markdown-body, .inner, #main_content {
    max-width: none !important;
    padding: 1rem 2rem !important;
    overflow-x: auto;
  }
  .muted { color: #666; }
  .infer-player-bar {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    gap: 0.75rem 1.25rem;
    margin: 0 0 1rem;
    padding: 0.65rem 0.85rem;
    border: 1px solid #444;
    border-radius: 4px;
    background: rgba(255, 255, 255, 0.03);
  }
  .infer-player-bar audio {
    width: min(420px, 100%);
    height: 36px;
  }
  #infer-now-playing {
    font-size: 0.85rem;
    line-height: 1.35;
    max-width: 60ch;
  }
  .infer-table-wrap {
    width: 100%;
    margin: 0 0 1.5rem;
  }
  .infer-table {
    font-size: 0.8rem;
    width: max-content;
    table-layout: auto;
    border-collapse: collapse;
  }
  .infer-table th,
  .infer-table td {
    vertical-align: middle;
    padding: 0.35rem 0.5rem;
    border: 1px solid #444;
    white-space: nowrap;
  }
  .infer-table thead th {
    background: #2a2a2a;
    color: #eee;
    font-weight: 600;
    text-align: center;
  }
  .infer-table .col-idx { text-align: center; }
  .infer-table .col-ref { text-align: center; font-size: 0.75rem; }
  .infer-table .col-texto {
    white-space: normal;
    min-width: 200px;
    max-width: 280px;
  }
  .infer-table .col-audio { text-align: center; }
  .infer-play {
    display: inline-block;
    padding: 0.15rem 0.45rem;
    border: 1px solid #666;
    border-radius: 4px;
    text-decoration: none;
    color: #9cdcfe;
    font-size: 0.78rem;
    line-height: 1.2;
  }
  .infer-play:hover { background: rgba(255, 255, 255, 0.08); }
  details.prompt-box pre {
    white-space: pre-wrap;
    font-size: 0.78rem;
    max-height: 420px;
    overflow: auto;
  }
</style>"""

PLAYER_SCRIPT = """<script>
(function () {
  var audio = document.getElementById("infer-shared-audio");
  var label = document.getElementById("infer-now-playing");
  if (!audio) return;
  document.querySelectorAll(".infer-play").forEach(function (link) {
    link.addEventListener("click", function (event) {
      event.preventDefault();
      audio.src = link.getAttribute("href");
      audio.load();
      if (label) {
        label.textContent = link.getAttribute("data-label") || link.getAttribute("title") || "";
      }
      audio.play().catch(function () {});
    });
  });
})();
</script>"""


def audio_src(slug: str, cond: str, var: str, idx: int) -> str:
    return f"{AUDIO_BASE}/{slug}/outputs_final_experiment/{cond}/{var}/{idx:03d}.wav"


def play_link(slug: str, label: str, cond: str, var: str, idx: int) -> str:
    src = audio_src(slug, cond, var, idx)
    return (
        f'<a class="infer-play" href="{src}" title="{label}" '
        f'data-label="{label}">&#9654;</a>'
    )


def build_table(sentences: list[str]) -> str:
    lines = [
        "## Tabela unificada de inferencias",
        "",
        "Uma linha por sentenca; **mesmo texto e ref** para os tres modelos. "
        "Clique em **&#9654;** para tocar no player abaixo (um unico `<audio>` — evita travar o navegador). "
        "A planilha pode **extrapolar para a direita**; role a pagina horizontalmente se precisar.",
        "",
        '<div class="infer-player-bar">',
        '<audio id="infer-shared-audio" controls preload="none"></audio>',
        '<span id="infer-now-playing" class="muted">Clique em &#9654; numa celula para carregar o audio aqui.</span>',
        "</div>",
        "",
        '<div class="infer-table-wrap">',
        '<table class="infer-table" markdown="0">',
        "<thead>",
        '<tr class="infer-head-model">',
        '<th rowspan="2" class="col-idx">#</th>',
        '<th rowspan="2" class="col-ref">Ref</th>',
        '<th rowspan="2" class="col-texto">Texto</th>',
    ]
    for _slug, title, anchor in MODELS:
        lines.append(f'<th colspan="6" class="col-audio" id="{anchor}">{title}</th>')
    lines.append("</tr>")
    lines.append('<tr class="infer-head-vars">')
    for _ in MODELS:
        for _c, _v, lab in VARS:
            lines.append(f'<th class="col-audio">{lab}</th>')
    lines.append("</tr>")
    lines.append("</thead>")
    lines.append("<tbody>")

    for i, text in enumerate(sentences, start=1):
        ref = (i - 1) // 10 + 1
        row = [
            f'<td class="col-idx">{i}</td>',
            f'<td class="col-ref">refs/{ref}.wav</td>',
            f'<td class="col-texto">{text}</td>',
        ]
        for slug, title, _anchor in MODELS:
            for cond, var, lab in VARS:
                cell_label = f"{title} — frase {i} — {lab}"
                row.append(f'<td class="col-audio">{play_link(slug, cell_label, cond, var, i)}</td>')
        lines.append("<tr>" + "".join(row) + "</tr>")

    lines.extend(
        [
            "</tbody></table>",
            "</div>",
            "",
            PLAYER_SCRIPT,
            "",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    text = SRC.read_text(encoding="utf-8")
    marker = "## Tabelas de inferencias"
    if marker not in text:
        marker = "## Tabela unificada de inferencias"
    head, _rest = text.split(marker, 1)
    footer = '\n---\n\n<p class="muted">Contexto:'
    if footer not in _rest:
        raise SystemExit("footer marker not found")
    _mid, foot = _rest.split(footer, 1)

    style_start = head.find("<style>")
    style_end = head.find("</style>") + len("</style>")
    if style_start < 0:
        raise SystemExit("style block not found")
    head = head[:style_start] + STYLES + head[style_end:]

    # remove standalone test player (shared bar replaces it)
    head = head.replace(
        "**Teste de player** (XTTS, sentenca 1, original v1):\n\n"
        '<audio controls src="/fala_pb/Inferencias%20finais/Audios/xtts/'
        'outputs_final_experiment/original/v1/001.wav"></audio>\n\n',
        "",
    )

    sentences = [
        ln.strip()
        for ln in SENTENCES_FILE.read_text(encoding="utf-8").splitlines()
        if ln.strip()
    ]
    out = head + build_table(sentences) + footer + foot
    SRC.write_text(out, encoding="utf-8")
    print(f"Wrote {SRC} ({len(out.splitlines())} lines, {len(sentences)} rows)")


if __name__ == "__main__":
    main()

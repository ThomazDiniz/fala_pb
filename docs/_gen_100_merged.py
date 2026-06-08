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
    max-width: 98% !important;
    padding: 1rem 2rem !important;
  }
  .muted { color: #666; }
  #main_content audio {
    display: block !important;
    visibility: visible !important;
    opacity: 1 !important;
  }
  .infer-scroll {
    overflow: auto;
    max-height: 75vh;
    width: 100%;
    margin: 0 0 1.5rem;
    -webkit-overflow-scrolling: touch;
    border: 1px solid #444;
    border-radius: 4px;
  }
  .infer-table {
    font-size: 0.8rem;
    width: max-content !important;
    min-width: 4100px;
    table-layout: fixed;
    border-collapse: separate;
    border-spacing: 0;
  }
  .infer-table th,
  .infer-table td {
    vertical-align: middle;
    padding: 0.4rem 0.45rem;
    overflow: visible;
    border-bottom: 1px solid #444;
    border-right: 1px solid #333;
  }
  .infer-table thead th {
    background: #252525;
    color: #eee;
    font-weight: 600;
    text-align: center;
  }
  .infer-table thead tr.infer-head-model th {
    position: sticky;
    top: 0;
    z-index: 12;
    box-shadow: 0 1px 0 #555;
  }
  .infer-table thead tr.infer-head-vars th {
    position: sticky;
    top: 2.35rem;
    z-index: 11;
    font-size: 0.72rem;
    font-weight: 500;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.35);
  }
  .infer-table .col-idx { width: 2.75rem; min-width: 2.75rem; text-align: center; }
  .infer-table .col-ref { width: 5.25rem; min-width: 5.25rem; text-align: center; }
  .infer-table .col-texto { width: 220px; min-width: 200px; text-align: left; }
  .infer-table .col-audio { width: 200px; min-width: 200px; max-width: 200px; }
  .infer-table audio {
    width: 188px !important;
    min-width: 188px !important;
    max-width: 188px !important;
    height: 32px !important;
  }
  details.prompt-box pre {
    white-space: pre-wrap;
    font-size: 0.78rem;
    max-height: 420px;
    overflow: auto;
  }
</style>"""

def audio_src(slug: str, cond: str, var: str, idx: int) -> str:
    return f"{AUDIO_BASE}/{slug}/outputs_final_experiment/{cond}/{var}/{idx:03d}.wav"


def audio_tag(slug: str, label: str, cond: str, var: str, idx: int) -> str:
    src = audio_src(slug, cond, var, idx)
    return f'<audio controls src="{src}" title="{label}"></audio>'


def build_table(sentences: list[str]) -> str:
    lines = [
        "## Tabela unificada de inferencias",
        "",
        "Uma linha por sentenca; **mesmo texto e ref** para os tres modelos. "
        "Por modelo: **Orig v1–v3** e **Ajust v1–v3**. "
        "A tabela rola dentro da caixa (vertical e horizontal); o **cabecalho fica fixo** ao descer pelas linhas.",
        "",
        '<div class="infer-scroll">',
        "",
        '<table class="infer-table" markdown="0">',
        '<thead>',
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
            lines.append(f"<th class=\"col-audio\">{lab}</th>")
    lines.append("</tr>")
    lines.append("</thead>")
    lines.append("<tbody>")

    for i, text in enumerate(sentences, start=1):
        ref = (i - 1) // 10 + 1
        cells = [str(i), f"refs/{ref}.wav", text]
        row = [
            f'<td class="col-idx">{cells[0]}</td>',
            f'<td class="col-ref">{cells[1]}</td>',
            f'<td class="col-texto">{cells[2]}</td>',
        ]
        for slug, title, _anchor in MODELS:
            for cond, var, lab in VARS:
                label = f"{title} {i} {lab}"
                row.append(
                    f'<td class="col-audio">{audio_tag(slug, label, cond, var, i)}</td>'
                )
        lines.append("<tr>" + "".join(row) + "</tr>")

    lines.extend(["</tbody></table>", "", "</div>", ""])
    return "\n".join(lines)


def main() -> None:
    text = SRC.read_text(encoding="utf-8")
    marker = "## Tabelas de inferencias"
    if marker not in text:
        marker = "## Tabela unificada de inferencias"
    head, _rest = text.split(marker, 1)
    footer = "\n---\n\n<p class=\"muted\">Contexto:"
    if footer not in _rest:
        raise SystemExit("footer marker not found")
    _mid, foot = _rest.split(footer, 1)

    # replace style block in head
    style_start = head.find("<style>")
    style_end = head.find("</style>") + len("</style>")
    if style_start < 0:
        raise SystemExit("style block not found")
    head = head[:style_start] + STYLES + head[style_end:]

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

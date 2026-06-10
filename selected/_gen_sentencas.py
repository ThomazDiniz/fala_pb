from pathlib import Path

root = Path(__file__).resolve().parent
master = root / "sentenças.txt"
lines = master.read_text(encoding="utf-8").splitlines()


def sentence_for_wav_num(n: int) -> str:
    if n < 1 or n > len(lines):
        return f"[linha {n} fora do intervalo]"
    return lines[n - 1]


def wav_num_from_name(p: Path) -> int:
    return int(p.stem)


wav_folders = sorted({p.parent for p in root.rglob("*.wav")})

for folder in wav_folders:
    wavs = sorted(folder.glob("*.wav"), key=wav_num_from_name)
    texts = [sentence_for_wav_num(wav_num_from_name(w)) for w in wavs]
    out = folder / "sentenças.txt"
    out.write_text("\n".join(texts) + ("\n" if texts else ""), encoding="utf-8")
    print(f"Wrote {out.relative_to(root)} ({len(texts)} linhas)")


def build_wav_list():
    rows = []
    for prefix, model_dir, fmt in [
        ("UO", root / "unsloth (orpheus)", "UO{:02d}"),
        ("X", root / "xtts", "X{:02d}"),
        ("FP", root / "fishspeech", "FP{:02d}"),
    ]:
        for sub in ("original", "adaptado"):
            folder = model_dir / sub
            if not folder.exists():
                continue
            wavs = sorted(folder.glob("*.wav"), key=wav_num_from_name)
            for i, w in enumerate(wavs, 1):
                n = wav_num_from_name(w)
                rows.append(
                    {
                        "slot": fmt.format(i),
                        "model": prefix,
                        "cond": sub,
                        "wav": w.name,
                        "sent_id": n,
                        "text": sentence_for_wav_num(n),
                    }
                )
    return rows


def build_video_list():
    video_map = [
        ("UO", root / "Videos" / "UNSLOTH", "UO{:02d}.mp4"),
        ("X", root / "Videos" / "XTTS", "X{:02d}.mp4"),
        ("FP", root / "Videos" / "fish speech", "FP{:02d}.mp4"),
    ]
    model_wav_dirs = {
        "UO": root / "unsloth (orpheus)" / "original",
        "X": root / "xtts" / "original",
        "FP": root / "fishspeech" / "original",
    }
    rows = []
    for prefix, vdir, fmt in video_map:
        wavs = sorted(model_wav_dirs[prefix].glob("*.wav"), key=wav_num_from_name)
        for i in range(1, 11):
            vid = fmt.format(i)
            n = wav_num_from_name(wavs[i - 1])
            rows.append(
                {
                    "slot": vid.replace(".mp4", ""),
                    "model": prefix,
                    "video": vid,
                    "wav_ref": wavs[i - 1].name,
                    "sent_id": n,
                    "text": sentence_for_wav_num(n),
                }
            )
    return rows


def format_wav_list(rows):
    parts = [
        "Lista de sentencas — WAVs (por pasta e ordem do arquivo)",
        "=" * 56,
        "",
    ]
    current = None
    for r in rows:
        key = (r["model"], r["cond"])
        if key != current:
            current = key
            parts.append(f"--- {r['model']} / {r['cond']} ---")
        parts.append(
            f"{r['slot']:6}  {r['wav']:8}  sent_{r['sent_id']:03d}  {r['text']}"
        )
        parts.append("")
    return "\n".join(parts)


def format_video_list(rows):
    parts = [
        "Lista de sentencas — Videos (UO / X / FP por slot 01-10)",
        "=" * 52,
        "",
        "Cada video N usa a mesma sentenca do N-esimo WAV (original) do modelo.",
        "",
    ]
    current = None
    for r in rows:
        if r["model"] != current:
            current = r["model"]
            parts.append(f"--- {r['model']} ---")
        parts.append(
            f"{r['slot']:6}  {r['video']:10}  ref {r['wav_ref']:8}  sent_{r['sent_id']:03d}  {r['text']}"
        )
        parts.append("")
    return "\n".join(parts)


wav_rows = build_wav_list()
vid_rows = build_video_list()

(root / "lista_sentencas_wavs.txt").write_text(format_wav_list(wav_rows), encoding="utf-8")
(root / "lista_sentencas_videos.txt").write_text(format_video_list(vid_rows), encoding="utf-8")
print("Wrote lista_sentencas_wavs.txt and lista_sentencas_videos.txt")

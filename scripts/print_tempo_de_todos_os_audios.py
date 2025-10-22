import os
import wave

path = r"C:\\Users\\Tumais\\Desktop\\dataset\\sotaque-brasileiro-data\\Paraiba"
total_seconds = 0

for root, _, files in os.walk(path):
    for file in files:
        if file.endswith(".wav"):
            with wave.open(os.path.join(root, file), "r") as w:
                total_seconds += w.getnframes() / w.getframerate()

print(f"Duração total: {int(total_seconds)} segundos")
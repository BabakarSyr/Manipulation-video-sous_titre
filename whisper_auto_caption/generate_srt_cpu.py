import whisper
import os
import sys
import time
from tqdm import tqdm

def format_timestamp(seconds: float) -> str:
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    milliseconds = int((seconds - int(seconds)) * 1000)
    return f"{hours:02}:{minutes:02}:{seconds:02},{milliseconds:03}"

def main():
    print("🚀 Chargement du modèle Whisper (large)...")
    model = whisper.load_model("large")
    print("✅ Modèle chargé.")

    while True:
        audio_path = input("📝 Chemin du fichier audio à transcrire (ou 'q' pour quitter) : ").strip()
        if audio_path.lower() == 'q':
            break
        if not os.path.isfile(audio_path):
            print("❌ Fichier introuvable. Réessaie.")
            continue

        print(f"\n🎧 Transcription de : {audio_path}\n")
        start_time = time.time()

        # Transcription complète
        result = model.transcribe(audio_path, verbose=False)

        segments = result.get("segments", [])
        total = len(segments)

        if total == 0:
            print("❌ Aucun segment détecté.")
            continue

        srt_path = os.path.splitext(audio_path)[0] + ".srt"
        with open(srt_path, "w", encoding="utf-8") as srt_file:
            for i, segment in enumerate(tqdm(segments, desc="⏳ Progression", unit="seg", ncols=100)):
                start = format_timestamp(segment["start"])
                end = format_timestamp(segment["end"])
                text = segment["text"].strip()
                srt_file.write(f"{i+1}\n{start} --> {end}\n{text}\n\n")

        elapsed = time.time() - start_time
        print(f"\n✅ Transcription terminée en {elapsed:.2f} secondes")
        print(f"📄 Fichier SRT généré : {srt_path}\n")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Local Whisper transcription (faster-whisper, CTranslate2) — copy to target box.
Usage:
  python run_whisper.py <audio_path> [--lang vi] [--model large-v3] [--json]
Prints text (or JSON segments) to stdout. First run downloads the model into
~/.cache/huggingface unless already cached.
"""
import sys, argparse, json

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("audio")
    ap.add_argument("--model", default="large-v3", help="Systran/faster-whisper-<model>")
    ap.add_argument("--lang", default=None)
    ap.add_argument("--json", action="store_true", help="print segments as JSON")
    args = ap.parse_args()

    from faster_whisper import WhisperModel
    model_id = f"Systran/faster-whisper-{args.model}"
    # Apple Silicon / CPU: int8 is the best-supported ctranslate2 path.
    model = WhisperModel(model_id, device="cpu", compute_type="int8")

    segments, info = model.transcribe(args.audio, language=args.lang, beam_size=5)
    if args.json:
        out = [{"start": round(s.start,2), "end": round(s.end,2), "text": s.text.strip()} for s in segments]
        print(json.dumps(out, ensure_ascii=False))
    else:
        text = " ".join(s.text.strip() for s in segments)
        print(text)

if __name__ == "__main__":
    main()
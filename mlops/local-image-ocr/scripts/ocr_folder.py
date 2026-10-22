# Batch OCR all PNG/JPG pages in a folder -> ocr_output.txt
# Run with: unset PYTHONPATH && /c/Python314/python.exe ocr_folder.py <dir>
# (rapidocr-onnxruntime lives in Python 3.14 user site-packages)
import glob, os, sys
from rapidocr_onnxruntime import RapidOCR

folder = sys.argv[1] if len(sys.argv) > 1 else "."
out = open(os.path.join(folder, "ocr_output.txt"), "w", encoding="utf-8")
engine = RapidOCR()
files = sorted(glob.glob(os.path.join(folder, "*.png")) + glob.glob(os.path.join(folder, "*.jpg")))
for p in files:
    out.write("=" * 20 + " " + os.path.basename(p) + " " + "=" * 20 + "\n")
    result, _ = engine(p)
    if not result:
        out.write("[no text]\n")
        continue
    for box, txt, conf in result:
        out.write(txt + "\n")
out.close()
print("done", len(files), "files -> ", os.path.join(folder, "ocr_output.txt"))
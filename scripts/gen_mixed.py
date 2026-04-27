import os
import numpy as np
from PIL import Image

INPUT_DIR = "seed"
SPECTRAL_DIR = "spectral"
OUTPUT_DIR = "data"

LEVELS = [0.15, 0.30, 0.50, 0.70, 0.85, 1.0]

def blend(img, spec, alpha):
    img = img.astype(np.float32)
    spec = spec.astype(np.float32)
    out = (1 - alpha) * img + alpha * spec
    return np.clip(out, 0, 255).astype(np.uint8)

def process(label):
    in_path = os.path.join(INPUT_DIR, label)
    spec_path = os.path.join(SPECTRAL_DIR, label)
    out_path = os.path.join(OUTPUT_DIR, label)

    os.makedirs(out_path, exist_ok=True)

    for fname in os.listdir(in_path):
        if not fname.endswith(".png"):
            continue

        img = np.array(Image.open(os.path.join(in_path, fname)).convert("RGB"))

        # match spectral variants
        stem = fname.replace(".png", "")

        for spec_file in os.listdir(spec_path):
            if not spec_file.startswith(stem):
                continue

            spec = np.array(Image.open(os.path.join(spec_path, spec_file)).convert("RGB"))

            for alpha in LEVELS:
                mixed = blend(img, spec, alpha)

                name = spec_file.replace(
                    ".png",
                    f"_mix_{int(alpha*100):03d}.png"
                )

                Image.fromarray(mixed).save(os.path.join(out_path, name))

def main():
    for label in ["blorbo", "not_blorbo"]:
        process(label)

if __name__ == "__main__":
    main()
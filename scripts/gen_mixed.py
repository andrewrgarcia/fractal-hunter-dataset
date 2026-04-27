import os
import numpy as np
from PIL import Image
import pandas as pd

INPUT_DIR = "seed"
SPECTRAL_DIR = "spectral"
OUTPUT_DIR = "data"

LEVELS = [0.0, 0.15, 0.30, 0.50, 0.70, 0.85, 1.0]


def blend(img, spec, alpha):
    img = img.astype(np.float32)
    spec = spec.astype(np.float32)
    out = (1 - alpha) * img + alpha * spec
    return np.clip(out, 0, 255).astype(np.uint8)


def extract_mode(stem, spec_file):
    return spec_file.replace(stem + "_", "").replace(".png", "")


def process(label):
    in_path = os.path.join(INPUT_DIR, label)
    spec_path = os.path.join(SPECTRAL_DIR, label)
    out_path = os.path.join(OUTPUT_DIR, label)

    os.makedirs(out_path, exist_ok=True)

    rows = []

    for fname in sorted(os.listdir(in_path)):
        if not fname.endswith(".png"):
            continue

        img_path = os.path.join(in_path, fname)
        img = np.array(Image.open(img_path).convert("RGB"))

        stem = fname.replace(".png", "")

        for spec_file in sorted(os.listdir(spec_path)):
            if not spec_file.startswith(stem):
                continue

            spec_path_full = os.path.join(spec_path, spec_file)
            spec = np.array(Image.open(spec_path_full).convert("RGB"))

            mode = extract_mode(stem, spec_file)

            for alpha in LEVELS:
                mixed = blend(img, spec, alpha)

                name = spec_file.replace(
                    ".png",
                    f"_mix_{int(alpha * 100):03d}.png"
                )

                out_file = os.path.join(out_path, name)
                Image.fromarray(mixed).save(out_file)

                rows.append({
                    "filename": name,
                    "label": label,
                    "group": stem,
                    "alpha": alpha,
                    "mode": mode
                })

    return rows


def main():
    all_rows = []

    for label in ["blorbo", "not_blorbo"]:
        all_rows.extend(process(label))

    df = pd.DataFrame(all_rows)
    df.to_csv("metadata_raw.csv", index=False)


if __name__ == "__main__":
    main()
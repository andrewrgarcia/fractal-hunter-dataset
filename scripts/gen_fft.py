from pathlib import Path
import numpy as np
from PIL import Image

INPUT_DIR = Path("seed")
OUTPUT_DIR = Path("spectral")
SIZE = 256

MODES = [
    "mag_log",
    "phase",
    "mag_phase_rgb",
    "annular_low",
    "annular_mid",
    "annular_high",
]

def normalize(x: np.ndarray) -> np.ndarray:
    x = x.astype(np.float32)
    x -= x.min()
    denom = x.max() - x.min()
    if denom < 1e-8:
        return np.zeros_like(x, dtype=np.uint8)
    return (255 * x / denom).astype(np.uint8)

def fft_channels(img: np.ndarray):
    gray = img.mean(axis=2)

    f = np.fft.fft2(gray)
    f = np.fft.fftshift(f)

    mag = np.log1p(np.abs(f))
    phase = np.angle(f)

    return mag, phase

def annular_mask(shape, r0, r1):
    h, w = shape
    cy, cx = h // 2, w // 2
    y, x = np.ogrid[:h, :w]
    r = np.sqrt((x - cx) ** 2 + (y - cy) ** 2)
    r /= r.max()
    return (r >= r0) & (r <= r1)

def make_spectral(img: np.ndarray, mode: str) -> np.ndarray:
    mag, phase = fft_channels(img)

    if mode == "mag_log":
        out = normalize(mag)
        return np.stack([out, out, out], axis=2)

    if mode == "phase":
        out = normalize(phase)
        return np.stack([out, out, out], axis=2)

    if mode == "mag_phase_rgb":
        r = normalize(mag)
        g = normalize(phase)
        b = normalize(mag * np.cos(phase))
        return np.stack([r, g, b], axis=2)

    if mode == "annular_low":
        mask = annular_mask(mag.shape, 0.00, 0.20)

    elif mode == "annular_mid":
        mask = annular_mask(mag.shape, 0.20, 0.55)

    elif mode == "annular_high":
        mask = annular_mask(mag.shape, 0.55, 1.00)

    else:
        raise ValueError(mode)

    out = normalize(mag * mask)
    return np.stack([out, out, out], axis=2)

def process_label(label: str):
    in_dir = INPUT_DIR / label
    out_dir = OUTPUT_DIR / label
    out_dir.mkdir(parents=True, exist_ok=True)

    for path in sorted(in_dir.glob("*.png")):
        img = Image.open(path).convert("RGB").resize((SIZE, SIZE))
        arr = np.asarray(img)

        stem = path.stem

        for mode in MODES:
            out = make_spectral(arr, mode)
            Image.fromarray(out).save(out_dir / f"{stem}_{mode}.png")

def main():
    for label in ["blorbo", "not_blorbo"]:
        process_label(label)

if __name__ == "__main__":
    main()
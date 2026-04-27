# scripts/rename_challenge.py
from pathlib import Path

for split in ["blorbo", "not_blorbo"]:
    files = sorted((Path("challenge") / split).glob("*.png"))
    for i, f in enumerate(files):
        f.rename(f.parent / f"img_{i:05d}.png")
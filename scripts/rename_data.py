import pandas as pd
from pathlib import Path

df = pd.read_csv("metadata_raw.csv")

new_rows = []

for split in ["blorbo", "not_blorbo"]:
    files = sorted((Path("data") / split).glob("*.png"))

    for i, f in enumerate(files):
        new_name = f"img_{i:05d}.png"
        old_name = f.name

        f.rename(f.parent / new_name)

        row = df[df["filename"] == old_name].iloc[0].to_dict()
        row["filename"] = new_name
        new_rows.append(row)

pd.DataFrame(new_rows).to_csv("metadata.csv", index=False)
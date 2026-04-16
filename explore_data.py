# explore_data.py
import pandas as pd
import os

raw_path = "data/raw/5G-production-dataset"

found = False
for app in os.listdir(raw_path):
    app_path = os.path.join(raw_path, app)
    if not os.path.isdir(app_path):
        continue
    for mobility in os.listdir(app_path):
        mobility_path = os.path.join(app_path, mobility)
        if not os.path.isdir(mobility_path):
            continue
        for content in os.listdir(mobility_path):
            content_path = os.path.join(mobility_path, content)
            if not os.path.isdir(content_path):
                continue
            for fname in os.listdir(content_path):
                if not fname.endswith(".csv"):
                    continue
                fpath = os.path.join(content_path, fname)
                df = pd.read_csv(fpath)
                print(f"=== {app}/{mobility}/{content}/{fname} ===")
                print(f"Shape: {df.shape}")
                print(f"Columns:\n{list(df.columns)}\n")
                print(f"Sample row:\n{df.iloc[0]}\n")
                print(f"Basic stats:\n{df.describe()}\n")
                found = True
                break
            if found:
                break
        if found:
            break
    if found:
        break
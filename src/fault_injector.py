# src/fault_injector.py
import pandas as pd
import numpy as np
import os
import glob
import random

random.seed(42)
np.random.seed(42)

RAW_PATH = "data/raw/5G-production-dataset"
OUT_PATH = "data/processed/faulted_dataset.csv"

# ── fault definitions ──────────────────────────────────────────────────────────

def inject_rsrp_drop(df, start_idx, duration=40):
    """Signal coverage hole — RSRP plummets, RSRQ and SNR degrade too."""
    end_idx = min(start_idx + duration, len(df))
    df.loc[start_idx:end_idx, "RSRP"] = np.random.randint(-120, -110, end_idx - start_idx + 1)
    df.loc[start_idx:end_idx, "RSRQ"] = np.random.randint(-22, -16, end_idx - start_idx + 1)
    df.loc[start_idx:end_idx, "SNR"] = np.random.uniform(-3, 2, end_idx - start_idx + 1).round(1)
    df.loc[start_idx:end_idx, "DL_bitrate"] = np.random.randint(0, 50, end_idx - start_idx + 1)
    df.loc[start_idx:end_idx, "fault_type"] = "rsrp_drop"
    df.loc[start_idx:end_idx, "fault_label"] = 1
    return df

def inject_handover_failure(df, start_idx, duration=20):
    """Handover failure — brief total throughput loss, CellID flaps."""
    end_idx = min(start_idx + duration, len(df))
    original_cell = df.loc[start_idx, "CellID"]
    flap_cell = original_cell + random.randint(1000, 5000)
    df.loc[start_idx:end_idx, "DL_bitrate"] = 0
    df.loc[start_idx:end_idx, "UL_bitrate"] = 0
    df.loc[start_idx:end_idx, "RSRP"] = np.random.randint(-112, -105, end_idx - start_idx + 1)
    # CellID flaps mid-window simulating failed handover attempt
    mid = start_idx + duration // 2
    df.loc[mid:end_idx, "CellID"] = flap_cell
    df.loc[start_idx:end_idx, "fault_type"] = "handover_failure"
    df.loc[start_idx:end_idx, "fault_label"] = 1
    return df

def inject_throughput_collapse(df, start_idx, duration=60):
    """Congestion/scheduling issue — throughput collapses while signal stays ok."""
    end_idx = min(start_idx + duration, len(df))
    df.loc[start_idx:end_idx, "DL_bitrate"] = np.random.randint(0, 30, end_idx - start_idx + 1)
    df.loc[start_idx:end_idx, "UL_bitrate"] = np.random.randint(0, 10, end_idx - start_idx + 1)
    # RSRP stays normal — this is NOT a coverage problem
    df.loc[start_idx:end_idx, "RSRP"] = np.random.randint(-85, -70, end_idx - start_idx + 1)
    df.loc[start_idx:end_idx, "fault_type"] = "throughput_collapse"
    df.loc[start_idx:end_idx, "fault_label"] = 1
    return df

# ── load all CSVs ──────────────────────────────────────────────────────────────

def load_all_csvs(raw_path):
    pattern = os.path.join(raw_path, "**", "*.csv")
    files = glob.glob(pattern, recursive=True)
    dfs = []
    for fpath in files:
        parts = fpath.replace("\\", "/").split("/")
        try:
            app      = parts[-4]
            mobility = parts[-3]
            content  = parts[-2]
        except IndexError:
            app = mobility = content = "unknown"
        df = pd.read_csv(fpath, low_memory=False)
        df["source_app"]      = app
        df["source_mobility"] = mobility
        df["source_content"]  = content
        df["source_file"]     = os.path.basename(fpath)
        dfs.append(df)
    print(f"Loaded {len(files)} CSV files, {sum(len(d) for d in dfs):,} total rows")
    return pd.concat(dfs, ignore_index=True)

# ── clean ──────────────────────────────────────────────────────────────────────

def clean(df):
    # replace "-" placeholders with NaN, then forward-fill
    df.replace("-", np.nan, inplace=True)
    for col in ["RSRP", "RSRQ", "SNR", "CQI", "DL_bitrate", "UL_bitrate"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df.sort_values(["source_file", "Timestamp"], inplace=True)
    df.reset_index(drop=True, inplace=True)
    # add clean labels
    df["fault_type"]  = "normal"
    df["fault_label"] = 0
    return df

# ── inject faults ──────────────────────────────────────────────────────────────

FAULT_INJECTORS = [
    inject_rsrp_drop,
    inject_handover_failure,
    inject_throughput_collapse,
]

def inject_faults(df, faults_per_file=3):
    files = df["source_file"].unique()
    for fname in files:
        mask = df["source_file"] == fname
        idxs = df[mask].index.tolist()
        if len(idxs) < 200:
            continue
        # pick N random non-overlapping injection points
        safe_range = idxs[50:-100]  # avoid start/end edges
        injection_points = random.sample(safe_range, min(faults_per_file, len(safe_range) // 80))
        for i, start_idx in enumerate(injection_points):
            injector = FAULT_INJECTORS[i % len(FAULT_INJECTORS)]
            df = injector(df, start_idx)
    return df

# ── main ───────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    os.makedirs("data/processed", exist_ok=True)

    df = load_all_csvs(RAW_PATH)
    df = clean(df)
    df = inject_faults(df, faults_per_file=3)

    df.to_csv(OUT_PATH, index=False)

    # summary
    total = len(df)
    faulted = df[df["fault_label"] == 1]
    print(f"\nDataset summary:")
    print(f"  Total rows      : {total:,}")
    print(f"  Normal rows     : {total - len(faulted):,}")
    print(f"  Faulted rows    : {len(faulted):,} ({100*len(faulted)/total:.1f}%)")
    print(f"\nFault breakdown:")
    print(faulted["fault_type"].value_counts().to_string())
    print(f"\nSaved to {OUT_PATH}")
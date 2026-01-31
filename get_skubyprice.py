#!/usr/bin/env python3

import os
from datetime import datetime
import pandas as pd
import logging

# Paths and dates
HOME = "/home/username/ACMECO"
DATE = datetime.now().strftime("%m%d")
LONGDATE = datetime.now().strftime("%m%d%H%M")

DOWNLOADS = os.path.join(HOME, "downloads", DATE)
PRICES = os.path.join(DOWNLOADS, "019210_Prices.txt")
RUN_HOME = os.path.join(HOME, DATE)

SKU100 = os.path.join(RUN_HOME, f"SKU100.{DATE}.csv")
SKU200 = os.path.join(RUN_HOME, f"SKU200.{DATE}.csv")

LOG_DIR = os.path.join(RUN_HOME, "logs")
LOGFILE = os.path.join(
    LOG_DIR, f"{os.path.basename(__file__)}.{LONGDATE}.log"
)

# Ensure directories exist
os.makedirs(RUN_HOME, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)

# Logging setup
logging.basicConfig(
    filename=LOGFILE,
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)

logging.info("Job started (idempotent run)")

# --- Remove previous outputs for this DATE (idempotency) ---
for path in (SKU100, SKU200):
    if os.path.exists(path):
        os.remove(path)
        logging.info("Removed existing file: %s", path)

# --- Read input file with auto header detection ---
df = pd.read_csv(
    PRICES,
    sep="|",
    dtype=str
)

# Detect header vs no-header
if all(col.isdigit() for col in df.columns):
    df = df[[0, 3, 6, 7]]
    df.columns = ["SKU", "DESCRIPTION", "LIST_PRICE", "UNIT_PRICE"]
else:
    df = df.rename(columns=str.upper)
    df = df[["SKU", "DESCRIPTION", "LIST_PRICE", "UNIT_PRICE"]]

initial_rows = len(df)

# Convert prices
df["UNIT_PRICE"] = pd.to_numeric(df["UNIT_PRICE"], errors="coerce")
df = df.dropna(subset=["UNIT_PRICE"])

logging.info(
    "Dropped %d rows with invalid UNIT_PRICE",
    initial_rows - len(df)
)

# --- Deterministic filtering ---
df_100 = df[df["UNIT_PRICE"] <= 100].copy()
df_200 = df[(df["UNIT_PRICE"] >= 101) & (df["UNIT_PRICE"] <= 200)].copy()

# Optional: stable ordering for repeatability
df_100.sort_values(by=["SKU"], inplace=True)
df_200.sort_values(by=["SKU"], inplace=True)

# --- Write outputs (overwrite mode) ---
df_100.to_csv(SKU100, index=False)
df_200.to_csv(SKU200, index=False)

# --- Logging counts ---
logging.info("Total input rows: %d", initial_rows)
logging.info("SKU100 rows written: %d", len(df_100))
logging.info("SKU200 rows written: %d", len(df_200))
logging.info("Job completed successfully")

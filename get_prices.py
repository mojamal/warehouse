#!/usr/bin/env python3

from datetime import datetime
from pathlib import Path

HOME = Path("/home/username/ACMECO")

DATE = datetime.now().strftime("%m%d")
LONGDATE = datetime.now().strftime("%m%d%H%M")

DOWNLOADS = HOME / "downloads" / DATE
PRICES = DOWNLOADS / "Prices.txt"
ITEMS = HOME / "items.txt"

RUN_HOME = HOME / DATE
PRICES_TMP = RUN_HOME / f"Prices.tmp.{DATE}.csv"
UPDATED_PRICES = RUN_HOME / f"Prices.{DATE}.csv"

LOGFILE = RUN_HOME / "logs" / f"prices.{LONGDATE}.log"

# Ensure directories exist
(RUN_HOME / "logs").mkdir(parents=True, exist_ok=True)

def log(msg: str):
    print(msg)
    with open(LOGFILE, "a") as lf:
        lf.write(msg + "\n")

RANGES = [
    (0, 100, 3.0),
    (101, 500, 2.0),
    (501, 1000, 1.8),
    (1001, 2000, 1.5),
]
DEFAULT_MULTIPLIER = 1.35

log("Begin Retrieve New Price per Item ...")

# Initialize files
PRICES_TMP.write_text("")
UPDATED_PRICES.write_text("")

# Load files once
prices_lines = PRICES.read_text().splitlines()
items = [line.strip() for line in ITEMS.read_text().splitlines() if line.strip()]

# --------------------------------
# Build PRICES_TMP (item list)
# --------------------------------

with open(PRICES_TMP, "a") as tmp:
    for item in items:
        key = f"{item}|"
        for line in prices_lines:
            if line.startswith(key):
                fields = line.split("|")
                if len(fields) >= 8:
                    tmp.write(f"{fields[0]} {fields[6]} {fields[7]}\n")
                break

log("End Retrieve New Price per Item")
log("Begin Re-calculate Prices Based on Value")

# Load temp prices
tmp_lines = PRICES_TMP.read_text().splitlines()

with open(UPDATED_PRICES, "a") as out:
    for item in items:
        list_price = None
        unit_price = None

        for line in tmp_lines:
            if line.startswith(item + " "):
                parts = line.split()
                if len(parts) >= 3:
                    list_price = parts[1]
                    unit_price = float(parts[2])
                break

        if unit_price is None:
            out.write(f"PROBLEM WITH {item} NOT IN {PRICES_TMP.name}\n")
            continue

        # Determine multiplier
        multiplier = DEFAULT_MULTIPLIER
        for low, high, mult in RANGES:
            if low <= unit_price <= high:
                multiplier = mult
                break

        new_unit_price = round(unit_price * multiplier, 2)
        out.write(f"{item},{list_price},{new_unit_price:.2f}\n")

log("End Re-calculate Prices Based on Value")

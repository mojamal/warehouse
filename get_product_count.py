#!/usr/bin/env python3

import os
import subprocess
from datetime import datetime
from pathlib import Path

# --- Variables (equivalent to Bash vars) ---

HOME = Path("/home/username/ACMECO")
DATE = datetime.now().strftime("%m%d")
LONG_DATE = datetime.now().strftime("%m%d%H%M")

RUN_HOME = HOME / DATE
DOWNLOADS = HOME / "downloads"
MASTER_LIST = HOME / "Warehouse.csv"  # not used in original script
ITEMS_LIST = HOME / "items.txt"        # 1299 items in the list
INVENTORY = DOWNLOADS / DATE / "Inventory.txt"
LOGFILE = RUN_HOME / "logs" / f"get_product_count_{LONG_DATE}.log"
INVENTORY_COUNT = RUN_HOME / f"InventoryCount_{DATE}.txt"

INVENTORY_SUM = RUN_HOME / "InventorySum.txt"
INVENTORY_TOTAL = RUN_HOME / "InventoryTotal.txt"

# --- Create directories (mkdir -p) ---

(RUN_HOME / "logs").mkdir(parents=True, exist_ok=True)
(DOWNLOADS / DATE).mkdir(parents=True, exist_ok=True)

# --- Logging setup (tee-like behavior) ---

def log(message: str):
    timestamped = message.rstrip()
    print(timestamped)
    with open(LOGFILE, "a") as lf:
        lf.write(timestamped + "\n")

# --- Begin processing ---

log(f"Begin product count aggregation {datetime.now()}")

# Truncate InventoryCount file (cat /dev/null > file)
INVENTORY_COUNT.write_text("")

# Load inventory once (faster than grepping 1299 times)
with open(INVENTORY, "r") as f:
    inventory_lines = f.readlines()

# Process items
with open(ITEMS_LIST, "r") as f:
    items = [line.strip() for line in f if line.strip()]

with open(INVENTORY_COUNT, "a") as out:
    for item in items:
        # grep item\| Inventory | awk -F\| '{print $8}'
        counts = []
        for line in inventory_lines:
            if f"{item}|" in line:
                fields = line.rstrip().split("|")
                if len(fields) >= 8:
                    try:
                        counts.append(int(fields[7]))
                    except ValueError:
                        pass

        # Match original behavior: print item + all matching $8 values
        row = item + "    " + " ".join(map(str, counts))
        out.write(row + "\n")

# --- Equivalent of first awk (sum columns 2..NF) ---

with open(INVENTORY_COUNT, "r") as fin, open(INVENTORY_SUM, "w") as fout:
    for line in fin:
        parts = line.split()
        item = parts[0]
        numbers = []
        for p in parts[1:]:
            try:
                numbers.append(int(p))
            except ValueError:
                pass
        total = sum(numbers)
        fout.write(line.rstrip() + f" {total}\n")

# --- Equivalent of second awk (print $1, $NF) ---

with open(INVENTORY_SUM, "r") as fin, open(INVENTORY_TOTAL, "w") as fout:
    for line in fin:
        parts = line.split()
        if parts:
            fout.write(f"{parts[0]} {parts[-1]}\n")

log(f"End product count aggregation {datetime.now()}")

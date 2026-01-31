#!/usr/bin/env python3

import os
import subprocess
from datetime import datetime
from pathlib import Path

# Variables
HOME = Path("/home/username/ACMECO")
DATE = datetime.now().strftime("%m%d")
LONG_DATE = datetime.now().strftime("%m%d%H%M")

RUN_HOME = HOME / DATE
DOWNLOADS = HOME / "downloads"
ITEMS_LIST = HOME / "items.txt"        # 1299 items in the list
INVENTORY = DOWNLOADS / DATE / "Inventory.txt"
LOGFILE = RUN_HOME / "logs" / f"get_product_count_{LONG_DATE}.log"
INVENTORY_COUNT = RUN_HOME / f"InventoryCount_{DATE}.txt"

INVENTORY_SUM = RUN_HOME / "InventorySum.txt"
INVENTORY_TOTAL = RUN_HOME / "InventoryTotal.txt"

# Create Directories
(RUN_HOME / "logs").mkdir(parents=True, exist_ok=True)
(DOWNLOADS / DATE).mkdir(parents=True, exist_ok=True)

# Setup Logging
def log(message: str):
    timestamped = message.rstrip()
    print(timestamped)
    with open(LOGFILE, "a") as lf:
        lf.write(timestamped + "\n")

# Begin processing
log(f"Begin product count aggregation {datetime.now()}")

# Truncate InventoryCount file
INVENTORY_COUNT.write_text("")

# Load inventory once
with open(INVENTORY, "r",encoding='latin-1') as f:
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

        # print item and matching values
        row = item + "    " + " ".join(map(str, counts))
        out.write(row + "\n")

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

with open(INVENTORY_SUM, "r") as fin, open(INVENTORY_TOTAL, "w") as fout:
    for line in fin:
        parts = line.split()
        if parts:
            fout.write(f"{parts[0]} {parts[-1]}\n")

log(f"End product count aggregation {datetime.now()}")

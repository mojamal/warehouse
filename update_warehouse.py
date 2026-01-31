#!/usr/bin/env python3

import shutil
from datetime import datetime
from pathlib import Path

# --- Variables (bash → python) ---

DATE = datetime.now().strftime("%m%d")
LONG_DATE = datetime.now().strftime("%m%d%H%M")

HOME = Path("/home/username/ACMECO")
OLD_CSV = HOME / "oldcsv"
RUN_HOME = HOME / DATE

MASTER_LIST = HOME / "Warehouse.csv"
MASTER_NEW = RUN_HOME / f"Warehouse.{DATE}.csv"

LOG_DIR = RUN_HOME / "logs"
LOGFILE = LOG_DIR / f"update_warehouse_{DATE}.log"

TOTALS_LIST = RUN_HOME / "InventoryTotal.txt"
TOTALS_SHORT = RUN_HOME / "InventoryTotalShort.txt"   # not used (same as bash)
INVENTORY_REPORT = RUN_HOME / f"updatewhse-report.{DATE}.txt"

TEMPFILE = RUN_HOME / "tempfile"
TEMPFILE_ALL = RUN_HOME / "tempfile.all"

# --- Setup directories ---

LOG_DIR.mkdir(parents=True, exist_ok=True)

# --- Logging (tee-like) ---

def log(msg: str):
    print(msg)
    with open(LOGFILE, "a") as lf:
        lf.write(msg + "\n")

# --- Begin processing ---

log(f"Begin updating inventory count for all items {datetime.now()}")

# Write first two header rows of MASTER_LIST to MASTER_NEW
with open(MASTER_LIST, "r") as src, open(MASTER_NEW, "w") as dst:
    for _ in range(2):
        line = src.readline()
        if not line:
            break
        dst.write(line.replace("\r", ""))

# Initialize files (cat /dev/null > file)
INVENTORY_REPORT.write_text("")
TEMPFILE.write_text("")
TEMPFILE_ALL.write_text("")

# Load files once (much faster than repeated awk/grep)
master_lines = [line.replace("\r", "") for line in MASTER_LIST.read_text().splitlines()]
totals_lines = TOTALS_LIST.read_text().splitlines()

# Extract item list from TOTALS_LIST (awk '{print $1}')
items = [line.split()[0] for line in totals_lines if line.strip()]

# --- Main loop ---

for item in items:
    # OLD_VALUE: last field from matching CSV row
    old_value = None
    for line in master_lines:
        if f"{item}," in line:
            old_value = line.split(",")[-1]
            break

    if old_value is None:
        old_value = "0"

    if old_value == "#N/A":
        old_value = "0"

    # NEW_VALUE: last field from TOTALS_LIST row
    new_value = None
    for line in totals_lines:
        if line.startswith(f"{item} "):
            new_value = line.split()[-1]
            break

    if new_value is None:
        new_value = "0"

    if old_value == new_value:
        # unchanged → append original row
        for line in master_lines:
            if f"{item}," in line:
                MASTER_NEW.open("a").write(line + "\n")
                break
    else:
        # changed → report + replace
        with INVENTORY_REPORT.open("a") as rpt:
            rpt.write(f"ITEM={item}\n")
            rpt.write(f"Old={old_value}, New={new_value}\n")

        for line in master_lines:
            if f"{item}," in line:
                updated = line.rstrip().rsplit(",", 1)[0] + f",{new_value}"
                MASTER_NEW.open("a").write(updated + "\n")
                break

# --- Validation section ---

log("Validate csv file")
log("ensure all items in InventoryTotal exist in the csv file")

BAD_CSV_FLAG = False
new_csv_text = MASTER_NEW.read_text()

for item in items:
    if item not in new_csv_text:
        log(f"ENTRY {item} is MISSING!! DO NOT USE THIS CSV.")
        BAD_CSV_FLAG = True

# --- Backup & update ---

if not BAD_CSV_FLAG:
    log("Updating the MASTER_LIST with MASTER_NEW since the CSV is good")
    log("Backup then Update the MASTER LIST")
    shutil.copy2(MASTER_LIST, OLD_CSV / f"Warehouse.{LONG_DATE}.csv")
    shutil.copy2(MASTER_NEW, MASTER_LIST)

# --- Cleanup ---

if TEMPFILE.exists():
    TEMPFILE.unlink()

log(f"End updating inventory count for all items {datetime.now()}")

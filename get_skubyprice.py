#!/usr/bin/env python3

import os
from datetime import datetime

# Paths and dates
HOME = "/home/mo/ExpressDiesel"
DATE = datetime.now().strftime("%m%d")
LONGDATE = datetime.now().strftime("%m%d%H%M")

DOWNLOADS = os.path.join(HOME, "downloads", DATE)
PRICES = os.path.join(DOWNLOADS, "019210_Prices.txt")
RUN_HOME = os.path.join(HOME, DATE)

SKU100 = os.path.join(RUN_HOME, f"SKU100.{DATE}.csv")
SKU200 = os.path.join(RUN_HOME, f"SKU200.{DATE}.csv")

LOGFILE = os.path.join(
    RUN_HOME, "logs", f"{os.path.basename(__file__)}.{LONGDATE}.log"
)

# Ensure output directories exist
os.makedirs(os.path.dirname(SKU100), exist_ok=True)
os.makedirs(os.path.dirname(LOGFILE), exist_ok=True)

# Write CSV headers
header = "SKU,DESCRIPTION,LIST_PRICE,UNIT_PRICE\n"
with open(SKU100, "w") as f:
    f.write(header)

with open(SKU200, "w") as f:
    f.write(header)

# Process price file
with open(PRICES, "r",encoding='latin-1') as infile:
    for line in infile:
        line = line.rstrip("\n")
        fields = line.split("|")

        if len(fields) < 8:
            continue  # skip malformed lines

        SKU = fields[0]
        DESCRIPTION = fields[3]
        LIST_PRICE = fields[6]
        UNIT_PRICE = fields[7]

        if UNIT_PRICE == "UNIT PRICE":
            continue

        try:
            unit_price = float(UNIT_PRICE)
        except ValueError:
            continue

        row = f"{SKU},{DESCRIPTION},{LIST_PRICE},{UNIT_PRICE}\n"

        if unit_price <= 100:
            with open(SKU100, "a") as f:
                f.write(row)
        elif 101 <= unit_price <= 200:
            with open(SKU200, "a") as f:
                f.write(row)

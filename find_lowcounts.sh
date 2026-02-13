#! /usr/bin/bash

DATE=$(date +%m%d)
HOME=/home/username/ACMECO
RUN_HOME=$HOME/$DATE
LOGFILE=$RUN_HOME/logs/find_lowcounts_$DATE.log
TOTALS_LIST=$RUN_HOME/InventoryTotal.txt
INVENTORY_REPORT=$RUN_HOME/updatewhse-report.$DATE.txt

for case in {1,2,3,4,5,6,7,8,9,12,20,32,37}; do
  for sku in $(cat $HOME/critical_$case); do
    CURRENT_INVENTORY=$(grep "$sku " $TOTALS_LIST | awk '{print $2}')
    if [[ $CURRENT_INVENTORY -lt $case ]]; then
      echo ALERT: The MIN THRESHOLD for $sku is $case but the inventory count is $CURRENT_INVENTORY!
      echo Please look into re-filling the stock for $sku.
      echo
    fi
  done
done

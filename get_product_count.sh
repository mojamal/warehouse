#! /usr/bin/bash

HOME=/home/username/ACMECO
DATE=$(date +%m%d)
LONG_DATE=$(date +%m%d%H%M)
RUN_HOME=$HOME/$DATE
LOGFILE=$RUN_HOME/logs/$(basename "$0").$LONG_DATE.log
MASTER_LIST=$HOME/Warehouse.csv
ITEMS_LIST=$HOME/items.txt	 
INVENTORY=$HOME/downloads/$DATE/Inventory.txt
INVENTORY_COUNT=$RUN_HOME/InventoryCount.$DATE.txt
INVENTORY_SUM=$RUN_HOME/InventorySum.$DATE.txt
INVENTORY_TOTAL=$RUN_HOME/InventoryTotal.$DATE.txt

{
echo Begin product count aggregation; date
cat /dev/null > $INVENTORY_COUNT

for item in $(cat $ITEMS_LIST)
do
  ROW_COUNT=$(grep $item\| $INVENTORY | awk -F\| '{print $8}')
  echo $item"    "$ROW_COUNT >> $INVENTORY_COUNT
done

awk '{
  sum=0;
  for (i=2; i<=NF; i++) {
    sum+=$i
  };
  print $0, sum
}' $INVENTORY_COUNT > $INVENTORY_SUM

awk '{print $1, $NF}' $INVENTORY_SUM > $INVENTORY_TOTAL

echo End product count aggregation ;date

} |& tee $LOGFILE

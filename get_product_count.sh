#! /usr/bin/bash

HOME=/home/username/ACMECO
DATE=$(date +%m%d)
RUN_HOME=$HOME/$DATE
DOWNLOADS=$HOME/downloads
MASTER_LIST=$HOME/Warehouse.csv
LONG_DATE=$(date +%m%d%H%M)
ITEMS_LIST=$HOME/items.txt	 # 1299 items in the list
INVENTORY=$HOME/downloads/$DATE/Inventory.txt
LOGFILE=$RUN_HOME/logs/get_product_count_$LONG_DATE.log
INVENTORY_COUNT=$RUN_HOME/InventoryCount_$DATE.txt

mkdir -p $HOME/$DATE/logs $HOME/downloads/$DATE
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
}' $INVENTORY_COUNT > $HOME/$DATE/InventorySum.txt

awk '{print $1, $NF}' $HOME/$DATE/InventorySum.txt > $HOME/$DATE/InventoryTotal.txt

echo End product count aggregation ;date

} |& tee $LOGFILE

#!/bin/bash

HOME=/home/username/ACME
DATE=$(date +%m%d)
LONGDATE=$(date +%m%d%H%M)
DOWNLOADS=$HOME/downloads/$DATE
PRICES=$DOWNLOADS/Prices.txt
ITEMS=$HOME/ebayitems.txt
RUN_HOME=$HOME/$DATE
PRICES_TMP=$RUN_HOME/ListPrices.ebay.tmp.$DATE.csv
UPDATED_PRICES=$RUN_HOME/ListPrices.ebay.$DATE.csv
LOGFILE=$RUN_HOME/logs/$(basename "$0").ebay.$LONGDATE.log

{
echo Begin Retrieve New Price per Item ...
cat /dev/null > $PRICES_TMP
cat /dev/null > $UPDATED_PRICES

for item in $(cat $ITEMS);do
  item+="|"
  grep $item $PRICES | awk -F'|' '{print $1","$7","$8}' >> $PRICES_TMP
done 

echo "SKU, LIST_PRICE,UNIT_PRICE" > $UPDATED_PRICES
cat $PRICES_TMP >> $UPDATED_PRICES

echo End Retrieve New Price per Item

echo End Re-calculate Prices Based on Value 

} |& tee $LOGFILE

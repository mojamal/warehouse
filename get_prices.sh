#!/bin/bash

# Setting prices based on the Unit Price
# RANGE		PERCENTAGE
# 0-100		3
# 101-500	2
# 501-1000	1.8
# 1001-2000	1.5
# 2000+		1.35

HOME=/home/username/ACMECO
DATE=$(date +%m%d)
LONGDATE=$(date +%m%d%H%M)
DOWNLOADS=$HOME/downloads/$DATE
PRICES=$DOWNLOADS/019210_Prices.txt
ITEMS=$HOME/items.txt
RUN_HOME=$HOME/$DATE
PRICES_TMP=$RUN_HOME/Prices.tmp.$DATE.csv
UPDATED_PRICES=$RUN_HOME/Prices.$DATE.csv
LOGFILE=$RUN_HOME/logs/$(basename "$0").$LONGDATE.log

{
echo Begin Retrieve New Price per Item ...
cat /dev/null > $PRICES_TMP
cat /dev/null > $UPDATED_PRICES

for item in $(cat $ITEMS);do
  item+="|"
  grep $item $PRICES | awk -F'|' '{print $1" "$7" "$8}' >> $PRICES_TMP
done 

echo End Retrieve New Price per Item

echo Begin Re-calculate Prices Based on Value 
RANGE1_MIN=0
RANGE1_MAX=100
RANGE1_MULTIPLIER=3
RANGE2_MIN=101
RANGE2_MAX=500
RANGE2_MULTIPLIER=2
RANGE3_MIN=501
RANGE3_MAX=1000
RANGE3_MULTIPLIER=1.8
RANGE4_MIN=1001
RANGE4_MAX=2000
RANGE4_MULTIPLIER=1.5
RANGE5_MULTIPLIER=1.35

for item in $(cat $ITEMS);do
  LIST_PRICE=$(awk '/'$item'/ {print $2;exit}' $PRICES_TMP)
  UNIT_PRICE=$(awk '/'$item'/ {print $3;exit}' $PRICES_TMP)

  # check for the existence of item in PRICES_TMP
  grep $item $PRICES_TMP > /dev/null
  EXIST_RESULT=$?

  # bc returns 1 of true, 0 if false
  if [ $EXIST_RESULT == 1 ]; then
    echo PROBLEM WITH $item NOT IN $PRICES_TMP >> $UPDATED_PRICES
  elif [ $(echo "$UNIT_PRICE >= $RANGE1_MIN && $UNIT_PRICE <= $RANGE1_MAX" | bc ) -eq 1 ]; then
    TMP_UNIT_PRICE=$(echo "$UNIT_PRICE *  $RANGE1_MULTIPLIER" | bc )
    NEW_UNIT_PRICE=$(printf "%.2f" $TMP_UNIT_PRICE)
    echo $item,$LIST_PRICE,$NEW_UNIT_PRICE >> $UPDATED_PRICES
  elif [ $(echo "$UNIT_PRICE >= $RANGE2_MIN && $UNIT_PRICE <= $RANGE2_MAX" | bc ) -eq 1 ]; then
    TMP_UNIT_PRICE=$(echo "$UNIT_PRICE *  $RANGE2_MULTIPLIER" | bc )
    NEW_UNIT_PRICE=$(printf "%.2f" $TMP_UNIT_PRICE)
    echo $item,$LIST_PRICE,$NEW_UNIT_PRICE >> $UPDATED_PRICES
  elif [ $(echo "$UNIT_PRICE >= $RANGE3_MIN && $UNIT_PRICE <= $RANGE3_MAX" | bc ) -eq 1 ]; then
    TMP_UNIT_PRICE=$(echo "$UNIT_PRICE *  $RANGE3_MULTIPLIER" | bc )
    NEW_UNIT_PRICE=$(printf "%.2f" $TMP_UNIT_PRICE)
    echo $item,$LIST_PRICE,$NEW_UNIT_PRICE >> $UPDATED_PRICES
  elif [ $(echo "$UNIT_PRICE >= $RANGE4_MIN && $UNIT_PRICE <= $RANGE4_MAX" | bc ) -eq 1 ]; then
    TMP_UNIT_PRICE=$(echo "$UNIT_PRICE *  $RANGE4_MULTIPLIER" | bc )
    NEW_UNIT_PRICE=$(printf "%.2f" $TMP_UNIT_PRICE)
    echo $item,$LIST_PRICE,$NEW_UNIT_PRICE >> $UPDATED_PRICES
  else
    TMP_UNIT_PRICE=$(echo "$UNIT_PRICE *  $RANGE5_MULTIPLIER" | bc )
    NEW_UNIT_PRICE=$(printf "%.2f" $TMP_UNIT_PRICE)
    echo $item,$LIST_PRICE,$NEW_UNIT_PRICE >> $UPDATED_PRICES
  fi
done

echo End Re-calculate Prices Based on Value 

} |& tee $LOGFILE

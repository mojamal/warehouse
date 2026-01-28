#! /usr/bin/bash

DATE=$(date +%m%d)
LONG_DATE=$(date +%m%d%H%M)
HOME=/home/username/ACMECO
OLD_CSV=$HOME/oldcsv
RUN_HOME=$HOME/$DATE
MASTER_LIST=$HOME/EXP_Warehouse.csv
MASTER_NEW=$RUN_HOME/EXP_Warehouse.$DATE.csv
mkdir $RUN_HOME/logs
LOGFILE=$RUN_HOME/logs/update_warehouse_$DATE.log
TOTALS_LIST=$RUN_HOME/InventoryTotal.txt
TOTALS_SHORT=$RUN_HOME/InventoryTotalShort.txt
INVENTORY_REPORT=$RUN_HOME/updatewhse-report.$DATE.txt

{
echo Begin updating inventory count for all items; date
head -2 $MASTER_LIST  | tr -d '\r' > $MASTER_NEW

# initialize 
cat /dev/null > $INVENTORY_REPORT
cat /dev/null > $RUN_HOME/tempfile.all
cat /dev/null > $RUN_HOME/tempfile

for item in $(awk '{print $1}' $TOTALS_LIST )
do
  OLD_VALUE=$(awk -F\, '/'$item,'/ {print $NF;exit}' $MASTER_LIST | tr -d '\r' )
  NEW_VALUE=$(awk '/'$item" "'/ {print $NF;exit}' $TOTALS_LIST )
  if [[ "$OLD_VALUE" == "#N/A" ]]; then
      OLD_VALUE="0"
  fi
  if  [[ "$OLD_VALUE" == "$NEW_VALUE" ]]; then
    grep "$item," $MASTER_LIST | tr -d '\r' >> $MASTER_NEW 
  else
    echo ITEM=$item >> $INVENTORY_REPORT
    echo Old=$OLD_VALUE, New=$NEW_VALUE >> $INVENTORY_REPORT
    grep "$item," $MASTER_LIST | tr -d '\r' > $RUN_HOME/tempfile 
    sed -i "s/$OLD_VALUE$/$NEW_VALUE/" $RUN_HOME/tempfile
    cat $RUN_HOME/tempfile >> $MASTER_NEW
  fi
done

echo Validate csv file
echo ensure all items in InventoryTotal exist in the csv file
MASTER_ROWS=$(wc -l $MASTER_NEW)
# Include a known total number to check against once we're happy with the csv

echo ensure all items exist in the new list
BAD_CSV_FLAG="false"
for i in $(awk '{print $1}' $TOTALS_LIST)
do 
  grep "$i" $MASTER_NEW > /dev/null
  RESULT=$(echo $?)
  if [[ "$RESULT" -eq "0" ]]; then
    continue
  else
    echo ENTRY $i is MISSING!! DO NOT USE THIS CSV.
    BAD_CSV_FLAG="true"
  fi
done

if [ $BAD_CSV_FLAG == "false" ]; then
  echo Updating the MASTER_LIST with MASTER_NEW since the CSV is good
  echo Backup then Update the MASTER LIST 
  cp -p $MASTER_LIST $OLD_CSV/EXP_Warehouse.$LONG_DATE.csv
  cp -p $MASTER_NEW $MASTER_LIST
fi

# clean working directory clean
rm tempfile

echo End updating inventory count for all items; date

} |& tee $LOGFILE

#! /bin/bash

export HOME=/Users/username/Documents/ACMECO
export DATE=$(date +%m%d)
export DOWNLOADS=$HOME/downloads/$DATE
export LOGFILE=$HOME/$DATE/logs/scpfiles_$DATE.log
export SSHPASS=<REDACTED>

echo SCP process start;date #  > $LOGFILE
mkdir -p $HOME/$DATE/logs $DOWNLOADS
cd $DOWNLOADS

/usr/local/bin/sshpass -e scp account@@<SFTPSITE>.com:/Inventory.txt $DOWNLOADS/
/usr/local/bin/sshpass -e scp account@@<SFTPSITE>.com:/Prices.txt $DOWNLOADS/
echo SCP process end;date # >> $LOGFILE

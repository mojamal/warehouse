# 💫 Warehouse:
🔭 Daily and Monthly Inventory and Pricing updates for Shopify and E-Bay storefronts.
Scheduled to run daily for Inventory and Monthly for Pricing updates.
The inventory total sum from six warehouses is updated and new spreadsheets created.


# 💻 Schedules:
07 7 * * * /home/ACMECO/do_diesel.sh

37 7 1 * * /home/ACMECO/do_monthly.sh

# File Structure
- /home/ACMECO
- ebayitems.txt       # list of ebay SKUs
- items.txt           # list of SKUs
- downloads/$DATE     # the latest Price and Inventory lists
- $DATE/logs          # Execution output and logs
- oldcsv              # Old *.csv file backups

# Do Diesel (Daily)
HOME=/home/ACMECO

DATE=$(date +%m%d)

$HOME/scp_files.sh

$HOME/get_product_count.py

$HOME/get_ebay_count.py

$HOME/update_warehouse.py

$HOME/update_ebay.py

$HOME/find_lowcounts.sh > $HOME/$DATE/lowcounts.$DATE.txt

# Do Prices (Monthly)
$HOME/get_skubyprice.py

$HOME/get_listandunitprice.sh

$HOME/get_listandunitprice_ebay.sh

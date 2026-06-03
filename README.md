# 💫 Warehouse:
🔭 Daily and Monthly Inventory and Pricing updates for Shopify and E-Bay storefronts.
Scheduled to run daily for Inventory and Monthly for Pricing updates.
The inventory total sum from six warehouses is updated and new spreadsheets created.


# 💻 Schedules:
07 7 * * * /ACME/do_diesel.sh

37 7 1 * * /ACME/do_monthly.sh

# Do Diesel (Daily)
HOME=/home/mo/ExpressDiesel

DATE=$(date +%m%d)

$HOME/scp_files.sh

python3 $HOME/get_product_count.py

python3 $HOME/get_ebay_count.py

python3 $HOME/update_warehouse.py

python3 $HOME/update_ebay.py

$HOME/find_lowcounts.sh > $HOME/$DATE/lowcounts.$DATE.txt

# Do Prices (Monthly)
/ACME/get_listandunitprice.sh

/ACME/get_listandunitprice_ebay.sh

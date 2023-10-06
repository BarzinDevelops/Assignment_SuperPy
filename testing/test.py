



import pandas as pd
from datetime import datetime as dt, timedelta, date

# ... Other functions ...

def check_expired_products():
    try:
        inventory_col_names = ['id', 'buy_date', 'buy_name', 'buy_amount', 'buy_price', 'expire_date']
        inventory_data = read_or_create_csv_file('inventory.csv', inventory_col_names, [])
        
        # Convert 'expire_date' column to datetime64[ns] type
        inventory_data['expire_date'] = pd.to_datetime(inventory_data['expire_date'])
        
        current_date = pd.to_datetime(get_current_date())  # Convert to datetime64[ns]
        expired_product_inventory = inventory_data[inventory_data['expire_date'] < current_date]

        if len(expired_product_inventory) > 0:
            print("Expired Products:")
            print(line)
            print(expired_product_inventory.to_string(index=False))
        else:
            print("No expired products found.")
    except Exception as e:
        # Handle the error
        print("An error occurred while checking for expired products ---->", e)


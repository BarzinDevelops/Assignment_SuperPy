# All the IMPORTS:
# ------------------------------------------#
from datetime import datetime as dt, timedelta, date
import pandas as pd # using pandas to read from and write to files:
import os
import reporting_logic
from config import SuperConfig

super_config = SuperConfig()
# ---------------------------------------------------------------------#
line = '-' * 20  # for underlining some columns
# ---------------------------------------------------------------------#
def read_or_create_csv_file(filename, col_names):
    # print(f"\n\n======== START OF  read_or_create_csv_file() function ========\n")
    # print(f"new_data ===>>>>>: {new_data}")
    try:
        if os.path.exists(filename):
            # data = pd.read_csv(filename, on_bad_lines='skip')
            read_file_df = pd.read_csv(filename, on_bad_lines='skip')
            # print(f"filename --> {filename}\nread_file_df =>>>>>>: {read_file_df}\nThis is of type: {type(read_file_df)}")
            # print(f"\n======== END OF  read_or_create_csv_file() function ========\n")
            return read_file_df
        else:
            print(f"This file: '{filename}' doesn't exist yet!")
            print("You will be redirected to file creator...")
            # print(f"\n======== END OF  read_or_create_csv_file() function ========\n")
            return create_custom_csv_file(filename, col_names)
    except FileNotFoundError:
        print(f"An error occurred while reading or creating the file: {filename}")
        # print(f"\n======== END OF  read_or_create_csv_file() function ========\n")
        return pd.DataFrame(columns=col_names)

# ---------------------------------------------------------------------#
def create_custom_csv_file(filename, col_names):
    # print(f"\n======== START OF  create_custom_csv_file() function ========\n")
    try:
        print(f"\nCreating your new csv file...filename in create_custom_csv_file ==> {filename}")
        df = pd.DataFrame(columns=col_names)
        df.to_csv(filename, index=False)
        print(f"\nThe file: {filename} is created.")
        # print(f"\n======== END OF  create_custom_csv_file() function ========\n")
        return df
    except FileExistsError:
        print(f"\nThis file: {filename}, already exists!")
        # print(f"\n======== END OF  create_custom_csv_file() function ========\n")

# ---------------------------------------------------------------------#

def update_inventory_expire_status():
    try:
        inventory_col_names = ['inventory_id', 'buy_id', 'buy_date', 'buy_name', 'buy_amount', 'buy_price', 'expire_date', 'is_expired']
        inventory_data = read_or_create_csv_file(super_config.inventory_file, inventory_col_names)

        if isinstance(inventory_data, str):
            print(inventory_data)  
            return

        if inventory_data.empty:
            print("The 'inventory.csv' file is empty. No data to update.")
            return

        inventory_data['expire_date'] = pd.to_datetime(inventory_data['expire_date'])
        current_date = pd.to_datetime(get_current_date())  

        # Update is_expired status based on expiration date
        inventory_data['is_expired'] = inventory_data['expire_date'] < current_date

        inventory_data.to_csv(super_config.inventory_file, index=False)
        
        return inventory_data  # Return the updated inventory_data

    except Exception as e:
        print("An error occurred while updating inventory expiration status ---->", e)
        return None
# ---------------------------------------------------------------------#
def validate_expire_date_before_buying(expire_date):
    return False if pd.to_datetime(get_current_date()) > pd.to_datetime(expire_date) else True

        
# ---------------------------------------------------------------------#
def get_next_id(filename, id_field_name=None):
    print(f"\n======== START OF  get_next_id() function ========\n")

    # If id_field_name is not provided, determine it based on the filename
    if id_field_name is None:
        id_field_name = 'buy_id' if filename == super_config.bought_file else 'inventory_id'
    print(f"In get_next_id ====> id_field_name is: {id_field_name}")

    try:
        if os.path.exists(filename):
            # Read the existing data and get the last id
            data = pd.read_csv(filename)
            if data.empty or id_field_name not in data.columns:
                new_id = 1
            else:
                last_id = data[id_field_name].max()
                new_id = int(last_id) + 1
        else:
            print("The file does not exist. Creating a new one.")
            new_id = 1

        print(f"\n======== END OF  get_next_id() function ========\n")
        return new_id

    except FileNotFoundError:
        print("In get_next_id() ==> An error occurred while getting the next ID.")
        print(f"\n======== END OF  get_next_id() function ========\n")
        return 1

# ---------------------------------------------------------------------#
def update_inventory(bought_file_data):
    print(f"\n======== START OF  update_inventory() function ========\n")
    try:
        inventory_col_names = ['inventory_id', 'buy_id', 'buy_date', 'buy_name', 'buy_amount', 'buy_price', 'expire_date', 'is_expired']
        inventory_df = read_or_create_csv_file(super_config.inventory_file, inventory_col_names)

    except Exception as e:
            print(f"In update_inventory ==> Exception when trying to get inventory_df from 'read_or_create_csv_file': {e}")

    try:
        bought_df = pd.read_csv(bought_file_data)
    except Exception as e:
        print(f"In update_inventory ==> Exception when trying to get bought_df: {e}")
    
    # get the sell_name and sell_amount
    try:
        sold_df = pd.read_csv(super_config.sold_file)
    except Exception as e:
        print(f"In update_inventory ==> Exception when trying to get sold_df: {e}")

    try:        

        # Add 'inventory_id' to the 'bought_df'
        bought_df['inventory_id'] =  bought_df['buy_id']
        
        print(f"im right before loop of sold_df in update_inventory()")
        for i, row in sold_df.iterrows():
            print(f"{row['sell_name']}", end=', ')
            print(f"amout: {row['sell_amount']}")
        
        
        # Concatenate 'inventory_df' and 'bought_df'
        updated_data = pd.concat([inventory_df, bought_df], ignore_index=True)
        
        # Convert 'expire_date' to datetime
        updated_data['expire_date'] = pd.to_datetime(updated_data['expire_date'])

        # Update 'is_expired' status based on expiration date
        current_date = pd.to_datetime(get_current_date())
        updated_data['is_expired'] = updated_data['expire_date'] < current_date

        # Drop duplicates based on 'buy_name' and 'expire_date' keeping the last occurrence
        updated_data.drop_duplicates(subset=['buy_name', 'expire_date'], keep='last', inplace=True)

        # Filter out rows with 'buy_amount' less than or equal to 0
        updated_data = updated_data[updated_data['buy_amount'] > 0]

        # Save the updated data to 'inventory.csv'
        updated_data.to_csv(super_config.inventory_file, index=False, mode='w', header=True)
        
        # updated_data['inventory_id'] = get_next_id(super_config.inventory_file, 'inventory_id')
        # print(f"updated_data['inventory_id'] ==============>>>>\n{updated_data}")

        
        print(f"\n======== END OF  update_inventory() function ========\n")
        return updated_data  # Return the updated inventory_data

    except Exception as e:
        print("An error occurred while updating inventory ---->", e)
        print(f"\n======== END OF  update_inventory() function ========\n")
        return None

# ---------------------------------------------------------------------#
def buy_product(product_name, amount, price, expire_date):
    print(f"\n======== START OF buy_product() function ========")

    try:
        bought_col_names = ['buy_id', 'buy_date', 'buy_name', 'buy_amount', 'buy_price', 'expire_date']

        # Read 'bought.csv' file
        bought_df = read_or_create_csv_file(super_config.bought_file, bought_col_names)

        # Check if the product already exists in 'bought.csv' with the same expire date
        existing_product = bought_df[(bought_df['buy_name'] == product_name) & (bought_df['expire_date'] == expire_date)]

        if not existing_product.empty:
            # Update 'buy_amount' for the existing product
            bought_df.loc[(bought_df['buy_name'] == product_name) & (bought_df['expire_date'] == expire_date), 'buy_amount'] += amount
            # print(f"bought_df ==============>>>>>\n{bought_df} ")
        else:
            if int(amount) > 0:
                # If 'bought.csv' is empty, initialize bought_df
                if bought_df.empty:
                    bought_df = pd.DataFrame(columns=bought_col_names)

                # Get the next available buy ID
                next_buy_id = get_next_id(super_config.bought_file, 'buy_id')

                # Create the data for the new entry
                new_entry = {
                    'buy_id': next_buy_id,
                    'buy_date': get_current_date(),
                    'buy_name': product_name,
                    'buy_amount': amount,
                    'buy_price': price,
                    'expire_date': expire_date,
                }

                # Convert the dictionary to a DataFrame with a single row
                new_entry_df = pd.DataFrame.from_records([new_entry], columns=bought_col_names)
                
                # Concatenate the new entry to 'bought.csv'
                bought_df = pd.concat([bought_df, new_entry_df], ignore_index=True)
                # print(f"bought_df ==============>>>>>\n{bought_df} ")
            
        # Save the updated 'bought.csv' file
        bought_df.to_csv(super_config.bought_file, index=False)
        
        update_inventory(super_config.bought_file)
        
        print(f"\n======== END OF  buy_product() function ========\n")
    except Exception as e:
        print("An error occurred while buying the product ---->", e)
        print(f"\n======== END OF  buy_product() function ========\n")
        
# ---------------------------------------------------------------------#
def get_next_id(filename, id_field_name=None):
    print(f"\n======== START OF  get_next_id() function ========\n")
    
    # If id_field_name is not provided, determine it based on the filename
    if id_field_name is None:
        id_field_name = 'buy_id' if filename == super_config.bought_file else 'inventory_id'
    print(f"In get_next_id ====> id_field_name is: {id_field_name}")
    
    try:
        if os.path.exists(filename):
            # Read the existing data and get the last buy_id or inventory_id
            data = pd.read_csv(filename)
            if data.empty:
                new_id = 1
            else:
                last_id = data[id_field_name].max()
                new_id = int(last_id) + 1
        else:
            print("The file does not exist. Creating a new one.")
            new_id = 1
        
        print(f"\n======== END OF  get_next_id() function ========\n")
        return new_id
    
    except FileNotFoundError:
        print("In get_next_id() ==> An error occurred while getting the next ID.")
        print(f"\n======== END OF  get_next_id() function ========\n")
        return 1

# ---------------------------------------------------------------------#
def update_csv_data(filename, columns, data):
    # Check if the file exists and create it if not
    if not os.path.exists(filename):
        df = pd.DataFrame(columns=columns)
        df.to_csv(filename, index=False)
    
    # Append the new data to the existing data
    new_line = ','.join([str(data[col]) for col in columns]) + '\n'

    # Read existing lines and remove unnecessary empty lines
    with open(filename, 'r') as file:
        lines = file.readlines()
    
    # Remove empty or whitespace-only lines
    lines = [line for line in lines if line.strip()]

    # Check if the last line is empty or contains only spaces
    with open(filename, 'w') as file:
        for line in lines:
            file.write(line)

        cursor_position = file.tell()

        # If the file is empty or cursor is not at the end of a line, add a newline
        if cursor_position == 0 or cursor_position > 0 and lines[-1][-1] != '\n':
            file.write('\n')

        # Write the new line
        file.write(new_line)

    print(f"Updated {filename} with new data.")
# ---------------------------------------------------------------------#
def calculate_profit(amount_bought, price_bought, amount_sold, price_sold):
    """
    Calculate profit based on amount bought, price bought, amount sold, and price sold.

    Parameters:
    amount_bought (float): Amount of product bought.
    price_bought (float): Price at which the product was bought.
    amount_sold (float): Amount of product sold.
    price_sold (float): Price at which the product was sold.

    Returns:
    float: Calculated profit.
    """
    revenue = amount_sold * price_sold
    cost = amount_bought * price_bought
    profit = revenue - cost

    return profit
# ---------------------------------------------------------------------#
def calculate_revenue_profit(bought_filename, sold_filename, inventory_filename):

    # Read bought and sold data from CSV files
    bought_data = pd.read_csv(bought_filename)
    sold_data = pd.read_csv(sold_filename)

    print(f"\nfrom bought.csv:\n{line}\n{bought_data.to_string(index=False)}")
    print(f"\nfrom sold.csv:\n{line}\n{sold_data.to_string(index=False)}")
    
    # Calculate revenue by summing the sold price multiplied by the sold amount
    sold_data['revenue'] = sold_data['sell_price'] * sold_data['sell_amount']

    # Merge the bought and sold data on the product name
    merged_data = pd.merge(bought_data, sold_data, left_on='buy_name', right_on='sell_name', how='left')

    # Calculate profit by subtracting the bought price multiplied by the sold amount from the revenue
    merged_data['profit'] = merged_data['revenue'] - (merged_data['buy_price'] * merged_data['sell_amount'])

    # Save the inventory data (including revenue and profit) to the inventory CSV file
    inventory_data = merged_data[['buy_name', 'buy_amount', 'buy_price', 'revenue', 'profit']]
    inventory_data.to_csv(inventory_filename, index=False)
# ---------------------------------------------------------------------#
def get_current_date():
    # setting values of a row:
    with open('time.txt') as f:
        today = f.readline()
    return dt.strptime(today, '%Y-%m-%d').date()
# ---------------------------------------------------------------------#
def advance_time(number):
    """
    Advance the current date in the 'time.txt' file by a specified number of days.
    
    Args:
        number (int): Number of days to advance the date.
    """
    current_date = get_current_date()
    advance = timedelta(number)
    new_date = current_date + advance
    with open('time.txt', 'w') as f:
        f.write(str(new_date))
# ---------------------------------------------------------------------#
def reset_date_in_time_file(custom_date='2023-07-01'):
    """
    Set date in the 'time.txt' file to a specified date.
    This function is executed every time the application starts.
    
    Args:
        custom_date (str): Date to set in the 'time.txt' file (default: '2023-07-01').
    """
    with open('time.txt', 'w') as f:
        f.write(custom_date)      
# ---------------------------------------------------------------------#
def check_if_has_run_today():
    """
    Check if the application has run today by comparing with the date in 'last_run_day.txt'.
    
    Returns:
        date: Date from 'last_run_day.txt' file.
    """
    with open('last_run_day.txt') as f:
        last_run_day_was = f.readline()
        last_run_day_was = dt.strptime(last_run_day_was, '%Y-%m-%d').date()
    return last_run_day_was
# ---------------------------------------------------------------------#
def check_before_reset_date():
    """
    Check if the application has run today, and reset the date if needed.
    This function is executed every time the application starts.
    """
    last_run_date = check_if_has_run_today()
    todays_date = date.today()
    if last_run_date != todays_date:
        reset_date_in_time_file()
        with open('last_run_day.txt', 'w') as f:
            f.write(str(todays_date))
# ---------------------------------------------------------------------#
def check_expired_products():
    try:
        inventory_col_names = ['id', 'buy_date', 'buy_name', 'buy_amount', 'buy_price', 'expire_date']
        inventory_data = read_or_create_csv_file(super_config.inventory_file, inventory_col_names)
        
        # Convert 'expire_date' column to datetime64[ns] type
        inventory_data['expire_date'] = pd.to_datetime(inventory_data['expire_date'])
        # Convert current_date to datetime64[ns]
        current_date = pd.to_datetime(get_current_date())  # Convert to datetime64[ns]
        
        expired_product_inventory = inventory_data[inventory_data['expire_date'] < current_date]

        if len(expired_product_inventory) > 0:
            print(f"Expired Products:")
            print(line)
            print(expired_product_inventory.to_string(index=False))
        else:
            print("No expired products found.")
    except Exception as e:
        # Handle the error
        print("An error occurred while checking for expired products ---->", e)
# ---------------------------------------------------------------------#
def sell_action(name, amount, price):
    # Update inventory expiration status
    update_inventory_expire_status()
    
    inventory_col_names = ['id', 'buy_date', 'buy_name', 'buy_amount', 'buy_price', 'expire_date']
    inventory_data = read_or_create_csv_file(super_config.inventory_file, inventory_col_names)
    print(f"In sell_action()\ninventory_data ==============>>>>>\n{inventory_data} ")
    
    
    # set columns of sold.csv file
    sold_col_names = ['sell_id','sell_date','sell_name','sell_amount','sell_price']
    # get the sold.csv file 
    sold_df = read_or_create_csv_file(super_config.sold_file, sold_col_names)
    
   
    # Convert 'expire_date' column to datetime64[ns] type
    inventory_data['expire_date'] = pd.to_datetime(inventory_data['expire_date'])

    # Strip leading and trailing spaces from the product name for comparison
    name_stripped = name.strip()

    # Filter products that match the name and have non-zero amount
    product_inventory = inventory_data[(inventory_data['buy_name'].str.strip() == name_stripped) & (inventory_data['buy_amount'] > 0)]

    if len(product_inventory) == 0:
        print(f"Error: Product '{name}' is out of stock and cannot be sold.")
        return

    current_date = pd.to_datetime(get_current_date())
    expired_product_inventory = product_inventory[pd.to_datetime(product_inventory['expire_date']) < current_date]

    # Print the inventory data for the specified product
    product_inventory = inventory_data[(inventory_data['buy_name'].str.strip() == name_stripped)]
    # print("Inventory data for the product:")
    # print(product_inventory)

    if len(expired_product_inventory) > 0:
        print(f"Error: Product '{name}' is expired and cannot be sold.")
        return

    if amount > product_inventory['buy_amount'].sum():
        print(f"Error: Not enough quantity of '{name}' available to sell.")
        return

    if price < 0:
        print("Error: Price cannot be negative.")
        return
    
    
    if int(amount) > 0:
                # If 'bought.csv' is empty, initialize bought_df
                if sold_df.empty:
                    sold_df = pd.DataFrame(columns=sold_col_names)

                # Get the next available buy ID
                next_sold_id = get_next_id(super_config.sold_file, 'sell_id')

                # Create the data for the new entry
                new_entry = {
                    'sell_id': next_sold_id,
                    'sell_date': get_current_date(),
                    'sell_name': name,
                    'sell_amount': amount,
                    'sell_price': price,
                }

                # Convert the dictionary to a DataFrame with a single row
                new_entry_df = pd.DataFrame.from_records([new_entry], columns=sold_col_names)
                
                # Concatenate the new entry to 'bought.csv'
                sold_df = pd.concat([sold_df, new_entry_df], ignore_index=True)
                # print(f"bought_df ==============>>>>>\n{bought_df} ")
    
    sold_df.to_csv(super_config.sold_file, index=False)
    
    

    # Calculate revenue and profit
    revenue = amount * price
    profit = revenue - (amount * product_inventory['buy_price'].values[0])

    # Update the inventory after the sale
    update_inventory_after_sell(name, amount)


    """ 
    # Update the management report for the sale
    management_report_col_names = ['buy_name', 'buy_amount', 'buy_price', 'sell_amount', 'sell_price', 'is_expired', 'revenue', 'profit']
    management_report_data = read_or_create_csv_file(super_config.management_report_file, management_report_col_names)
    new_sale_entry = pd.DataFrame({'buy_name': [name], 'buy_amount': [product_inventory['buy_amount'].values[0]], 'buy_price': [product_inventory['buy_price'].values[0]], 
                                   'sell_amount': [amount], 'sell_price': [price], 'is_expired': [False if len(expired_product_inventory) == 0 else True], 
                                   'revenue': [revenue], 'profit': [profit]})
    management_report_data = pd.concat([management_report_data, new_sale_entry], ignore_index=True)
    management_report_data.to_csv(super_config.management_report_file, index=False)
     """
    
    
    

    print("Sale successful.")
# ---------------------------------------------------------------------#
def check_sell_eligibility(name, amount):
    # Read 'inventory.csv' into a DataFrame
    inventory_data = pd.read_csv(super_config.inventory_file)

    # Find the product in the inventory
    product_inventory = inventory_data[inventory_data['buy_name'] == name]

    if len(product_inventory) == 0:
        print(f"Error: Product '{name}' not found in inventory.")
        return False

    # Check if the amount to sell is available
    available_quantity = product_inventory['buy_amount'].sum()
    if amount > available_quantity:
        print(f"Warning: Not enough quantity of '{name}' available to sell. You can sell up to {available_quantity} units.")
        return False

    # Check if the product is expired
    current_date = pd.to_datetime(get_current_date())
    expired_product_inventory = product_inventory[pd.to_datetime(product_inventory['expire_date']) < current_date]

    if len(expired_product_inventory) > 0:
        print(f"Error: Product '{name}' is expired and cannot be sold.")
        return False

    return True

# ---------------------------------------------------------------------#
def update_inventory_after_sell(name, amount):
    try:
        # Read 'inventory.csv' into a DataFrame
        inventory_data = pd.read_csv(super_config.inventory_file)

        # Find the product in the inventory
        product_inventory = inventory_data[inventory_data['buy_name'] == name]

        if len(product_inventory) == 0:
            print(f"Error: Product '{name}' not found in inventory.")
            return

        if amount > product_inventory['buy_amount'].sum():
            print(f"Error: Not enough quantity of '{name}' available to sell.")
            return

        # Update the sold amount in the 'inventory.csv' file
        inventory_data.loc[inventory_data['buy_name'] == name, 'buy_amount'] -= amount

        # Check if the product is sold out (the available amount is less than 1) and remove it from inventory
        available_quantity = inventory_data[inventory_data['buy_name'] == name]['buy_amount'].sum()
        if available_quantity < 1:
            inventory_data = inventory_data[inventory_data['buy_name'] != name]

        # Write the updated DataFrame back to the 'inventory.csv' file
        inventory_data.to_csv(super_config.inventory_file, index=False)
    except Exception as e:
        # Handle the error
        print("An error occurred while updating inventory after sell. Check this function: def update_inventory_after_sell(name, amount) ---->", e)
# ---------------------------------------------------------------------#
def save_to_csv(filename, data):
    """
    Save data to a CSV file.
    """
    try:
        data.to_csv(filename, index=False)
        print(f"Data saved to {filename}")
    except Exception as e:
        print(f"An error occurred while saving to {filename} ---->", e)
# ---------------------------------------------------------------------#
def load_csv_to_dataframe(filename):
    """
    Load data from a CSV file into a pandas DataFrame.
    """
    return pd.read_csv(filename)
# ---------------------------------------------------------------------#
def merge_inventory_sell_data(inventory_file, sell_file):
    inventory_data = pd.read_csv(inventory_file)
    sell_data = pd.read_csv(sell_file)
    
    # Print columns of inventory_data and sell_data
    print("Columns in inventory_data:", inventory_data.columns)
    print("Columns in sell_data:", sell_data.columns)

    # Merge based on common column 'buy_name'
    merged_data = pd.merge(inventory_data, sell_data, on='buy_name', how='inner')
    # maybe try this? -> pd.merge(bought_data, sold_data, left_on='buy_name', right_on='sell_name', how='left')
    
    return merged_data
# ---------------------------------------------------------------------#
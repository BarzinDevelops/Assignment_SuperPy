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
    try:
        if os.path.exists(filename):
            read_file_df = pd.read_csv(filename, on_bad_lines='skip')
            return read_file_df
        else:
            print(f"This file: '{filename}' doesn't exist yet!")
            print("You will be redirected to file creator...")
            return create_custom_csv_file(filename, col_names)
    except FileNotFoundError:
        print(f"An error occurred while reading or creating the file: {filename}")
        return pd.DataFrame(columns=col_names)

# ---------------------------------------------------------------------#
def create_custom_csv_file(filename, col_names):
    try:
        print(f"\nCreating your new csv file...filename in create_custom_csv_file ==> {filename}")
        df = pd.DataFrame(columns=col_names)
        df.to_csv(filename, index=False)
        print(f"\nThe file: {filename} is created.")
        return df
    except FileExistsError:
        print(f"\nThis file: {filename}, already exists!")

# ---------------------------------------------------------------------#

def update_inventory_expire_status():
    try:
        inventory_col_names = ['inventory_id', 'buy_id', 'buy_date', 'buy_name', 'buy_amount', 'buy_price', 'expire_date', 'is_expired']
        # Read or create the 'inventory.csv' file
        inventory_data = read_or_create_csv_file(super_config.inventory_file, inventory_col_names)

        # Check if the returned value is a DataFrame
        if isinstance(inventory_data, pd.DataFrame):
            # Check if the DataFrame is empty
            if not inventory_data.empty:
                inventory_data['expire_date'] = pd.to_datetime(inventory_data['expire_date'])
                current_date = pd.to_datetime(get_current_date())

                # Update is_expired status based on expiration date
                inventory_data['is_expired'] = inventory_data['expire_date'] < current_date
                inventory_data.to_csv(super_config.inventory_file, index=False)
            return inventory_data  # Return the updated inventory_data
        else:
            print(inventory_data)
            return None
    except Exception as e:
        print("An error occurred while updating inventory expiration status ---->", e)
        return None

# ---------------------------------------------------------------------#
def validate_expire_date_before_buying(expire_date):
    return False if pd.to_datetime(get_current_date()) > pd.to_datetime(expire_date) else True
        
# ---------------------------------------------------------------------#
def get_next_id(filename, id_field_name=None): 
    # If id_field_name is not provided, determine it based on the filename
    if id_field_name is None:
        id_field_name = 'buy_id' if filename == super_config.bought_file else 'inventory_id'
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
        return new_id
    except FileNotFoundError:
        print("In get_next_id() ==> An error occurred while getting the next ID.")
        return 1

# ---------------------------------------------------------------------#
def update_inventory(bought_file_data, amount_bought=0):
    try:
        inventory_col_names = ['inventory_id', 'buy_id', 'buy_date', 'buy_name', 'buy_amount', 'buy_price', 'expire_date', 'is_expired']
        inventory_df = read_or_create_csv_file(super_config.inventory_file, inventory_col_names)
        
    except Exception as e:
            print(f"In update_inventory ==> Exception when trying to get inventory_df from 'read_or_create_csv_file': {e}")
    try:
        bought_df = pd.read_csv(bought_file_data)
    except Exception as e:
        print(f"In update_inventory ==> Exception when trying to get bought_df: {e}")
    try:
        sold_df = pd.read_csv(super_config.sold_file)
    except Exception as e:
        print(f"In update_inventory ==> Exception when trying to get sold_df: {e}")
    try:        
        bought_df['inventory_id'] =  bought_df['buy_id']      
        
        updated_data = pd.concat([inventory_df, bought_df], ignore_index=True)
        
        # Update 'is_expired' status based on expiration date
        current_date = pd.to_datetime(get_current_date())
        updated_data['expire_date'] = pd.to_datetime(updated_data['expire_date'])
        updated_data['is_expired'] = updated_data['expire_date'] < current_date


        # Drop duplicates based on 'buy_name' and 'expire_date' keeping the last occurrence
        updated_data.drop_duplicates(subset=['buy_name', 'expire_date'], keep='last', inplace=True)

        # Filter out rows with 'buy_amount' less than or equal to 0
        updated_data = updated_data[updated_data['buy_amount'] > 0]
        
        # updated_data.update(inventory_df)
        print(f"updated_data before saving to inventory.csv ---->\n{updated_data}\n\n")
        # Save the updated data to 'inventory.csv'
        updated_data.to_csv(super_config.inventory_file, index=False, mode='w', header=True)
        
        return updated_data  # Return the updated inventory_data
        # """
    except Exception as e:
        print("An error occurred while updating inventory ---->", e)
        return None
  
# ---------------------------------------------------------------------#
def buy_product(product_name, amount, price, expire_date):
    try:
        bought_col_names = ['buy_id', 'buy_date', 'buy_name', 'buy_amount', 'buy_price', 'expire_date']
        
        # Read 'bought.csv' file
        bought_df = read_or_create_csv_file(super_config.bought_file, bought_col_names)

        # Check if the product already exists in 'bought.csv' with the same expire date
        existing_product = bought_df[(bought_df['buy_name'] == product_name) & (bought_df['expire_date'] == expire_date)]

        if not existing_product.empty:
            # Update 'buy_amount' for the existing product
            bought_df.loc[(bought_df['buy_name'] == product_name) & (bought_df['expire_date'] == expire_date), 'buy_amount'] += amount
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
                 
        update_inventory(super_config.bought_file, amount)
    
    except Exception as e:
        print("An error occurred while buying the product ---->", e)
        
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
    merged_data = pd.merge(bought_data, sold_data, left_on='buy_name', right_on='buy_name', how='left')

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
    
    # set columns of sold.csv file
    sold_col_names = ['sell_id','sell_date','buy_name','sell_amount','sell_price']
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

    product_not_expired = inventory_data.loc[(inventory_data['buy_name'] == name) & (inventory_data['is_expired'] == False)]
    product_is_expired = inventory_data.loc[(inventory_data['buy_name'] == name) & (inventory_data['is_expired'] == True)]
    quantity_not_expired = product_not_expired['buy_amount'].sum()
    quantity_expired = product_is_expired['buy_amount'].sum()

    if (len(product_is_expired) > 0) and (len(product_not_expired) <= 0):
        print(f"Error: Product '{name}' is expired and cannot be sold.")
        print(f"Amount expired: {quantity_expired}")
        return
    elif amount > quantity_not_expired:
        print(f"Error: Not enough quantity '{name}' left for this sale.")
        print(f"Current available quantity: {quantity_not_expired} ")
        return
    else:        
        if sold_df[sold_df['buy_name'] == name].empty:
            # Get the next available buy ID
            next_sold_id = get_next_id(super_config.sold_file, 'sell_id')

            # Create the data for the new entry
            new_entry = {
                'sell_id': next_sold_id,
                'sell_date': get_current_date(),
                'buy_name': name,
                'sell_amount': amount,
                'sell_price': price,
            }

            # Convert the dictionary to a DataFrame with a single row
            new_entry_df = pd.DataFrame.from_records([new_entry], columns=sold_col_names)
            
            # Concatenate the new entry to 'bought.csv'
            sold_df = pd.concat([sold_df, new_entry_df], ignore_index=True)
        else:
            sold_df.loc[sold_df['buy_name'] == name, 'sell_amount'] += amount

            
        sold_df.to_csv(super_config.sold_file, index=False)

    # Update the inventory after the sale
    update_inventory_after_sell(name, amount)

    # Call the function to calculate revenue and profit
    # revenue, profit = calculate_revenue_profit(name, amount, price, product_inventory)

    print("Sale successful.")
# ---------------------------------------------------------------------#

def update_inventory_after_sell(name, amount):  # version 1
    try:
        # Read 'inventory.csv' into a DataFrame
        inventory_data = pd.read_csv(super_config.inventory_file)
        # Find the product in the inventory
        product_inventory = inventory_data[inventory_data['buy_name'] == name]
        if len(product_inventory) == 0:
            print(f"Error: Product '{name}' not found in inventory.")
            return

        # Update the sold amount in the 'inventory.csv' file
        matching_rows = inventory_data.loc[(inventory_data['buy_name'] == name) & (inventory_data['is_expired'] == False)]
        
        for i, row in matching_rows.iterrows():
                current_amount = inventory_data.at[i, 'buy_amount']

                if amount <= current_amount:
                    # There is enough amount to sell
                    inventory_data.at[i, 'buy_amount'] -= amount
                    break
                
        # Check if the amount of the sold item is <= 0 and remove it
        inventory_data = inventory_data[inventory_data['buy_amount'] >= 1]

        # Check if the product is sold out (the available amount is less than 1) and remove it from inventory
        available_quantity = inventory_data[inventory_data['buy_name'] == name]['buy_amount'].sum()
        if available_quantity < 1:
            inventory_data = inventory_data[inventory_data['buy_name'] != name]

        # Write the updated DataFrame back to the 'inventory.csv' file
        inventory_data.to_csv(super_config.inventory_file, index=False)

    except Exception as e:
        print("An error occurred while updating inventory after sell. Check this function: def update_inventory_after_sell(name, amount) ---->", e)

# ---------------------------------------------------------------------#
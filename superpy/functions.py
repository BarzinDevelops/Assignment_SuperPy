# All the IMPORTS:
# ------------------------------------------#
from datetime import datetime as dt, timedelta, date
import pandas as pd # using pandas to read from and write to files:
import os
import reporting_logic
from config import SuperConfig


# ---------------------------------------------------------------------#
line = '-' * 20  # for underlining some columns
# ---------------------------------------------------------------------#
def read_or_create_csv_file(filename, col_names, new_data):
    #REMOVE## file_path = os.path.join('outputs', filename)
    file_path = os.path.join('outputs', filename)
    """
    Read data from a CSV file if it exists, otherwise create it.
    
    Args:
        filename (str): Name of the CSV file.
        col_names (list): List of column names for the CSV file.
        new_data (list): New data to be added to the file if it's created.
        
    Returns:
        pd.DataFrame: DataFrame containing the data from the CSV file.
    """
    try:
        data = pd.read_csv(file_path, on_bad_lines='skip')  # hier is even geprobeerd met on_bad_lines='skip'
        if len(data) > 0:
            return data
        else:
            colnames = " | ".join(data.columns)
            return f"This file: '{filename}' -> has no data yet, only these predefined columns:\n{colnames} |"
    except FileNotFoundError:
        print(f"This file doesn't exist yet!")
        print("You will be redirected to file creator...")
        create_custom_csv_file(file_path, col_names, new_data)
# ---------------------------------------------------------------------#
def create_custom_csv_file(filename, col_names, new_data):
    file_path = os.path.join('outputs', filename)
    try:
        print(f"\nCreating your new csv file...")        
        # print(f"NEW DATA is NOW -----------------> \n{new_data}")
        df = pd.DataFrame(columns=col_names)
        df.to_csv(file_path, index=False)
        print(f"\nThe file: {filename} is created.")
        # read_or_create_csv_file(filename)
    except FileExistsError:
        print(f"\nThis file: {filename}, already exists!")
    except ValueError as e:
            print(e)
# ---------------------------------------------------------------------#
def update_inventory_expire_status():
    try:
        inventory_col_names = ['inventory_id', 'buy_id', 'buy_date', 'buy_name', 'buy_amount', 'buy_price', 'expire_date', 'is_expired']
        inventory_data = read_or_create_csv_file('inventory.csv', inventory_col_names, [])

        # Convert 'expire_date' column to datetime64[ns] type
        inventory_data['expire_date'] = pd.to_datetime(inventory_data['expire_date'])
        # Convert current_date to datetime64[ns]
        current_date = pd.to_datetime(get_current_date())  # Convert to datetime64[ns]

        # Update is_expired status based on expiration date
        inventory_data['is_expired'] = inventory_data['expire_date'] < current_date

        # Save the updated inventory data to CSV
        inventory_data.to_csv('inventory.csv', index=False)
    except Exception as e:
        # Handle the error
        print("An error occurred while updating inventory expiration status ---->", e)
# ---------------------------------------------------------------------#
def update_inventory(source_file):
    update_inventory_expire_status()
    try:
        inventory_col_names = ['id', 'buy_date', 'buy_name', 'buy_amount', 'buy_price', 'expire_date', 'is_expired']
        inventory_data = read_or_create_csv_file('inventory.csv', inventory_col_names, [])

        try:
            # Read 'bought.csv' into a DataFrame
            bought_data = pd.read_csv(source_file)

            # Read 'inventory.csv' into a DataFrame
            inventory_data = pd.read_csv('inventory.csv', index_col=False)

        except Exception as e:
            print("An error occurred while reading the file ---->", e)
            return

        # Generate an auto-incremented ID for each row in 'bought.csv'
        new_ids = range(len(inventory_data) + 1, len(inventory_data) + 1 + len(bought_data))

        # Add the new IDs to the 'id' column of 'bought_data'
        bought_data['id'] = new_ids

        # Concatenate 'bought_data' with 'inventory_data'
        updated_data = pd.concat([inventory_data, bought_data], ignore_index=True)

        # Convert 'expire_date' column to datetime64[ns] type
        updated_data['expire_date'] = pd.to_datetime(updated_data['expire_date'])

        # Convert current_date to datetime64[ns]
        current_date = pd.to_datetime(get_current_date())

        # Check for expired products and update 'is_expired' field
        updated_data['is_expired'] = updated_data['expire_date'] < current_date

        # Remove duplicates based on 'buy_name' and 'expire_date'
        updated_data.drop_duplicates(subset=['buy_name', 'expire_date'], keep='last', inplace=True)

        # Check if the product is sold out and remove it from inventory
        updated_data = updated_data[updated_data['buy_amount'] > 0]

        # Write the updated DataFrame back to 'inventory.csv'
        updated_data.to_csv('inventory.csv', index=False, mode='w', header=True)  # Overwrite mode, with header

        print("Inventory updated successfully.")
    except Exception as e:
        print("An error occurred while updating inventory ---->", e)
# ---------------------------------------------------------------------#
def buy_product(product_name, amount, price, expire_date, inventory_file):
    global inventory_df

    try:
        # Update the inventory DataFrame
        if product_name in inventory_df['Product Name'].values:
            inventory_df.loc[inventory_df['Product Name'] == product_name, 'Bought Amount'] += amount
        else:
            new_row = {'Product Name': product_name, 'Bought Amount': amount}
            inventory_df = inventory_df.append(new_row, ignore_index=True)

        # Get the current date
        current_date = get_current_date()

        # Get the next available buy ID
        next_buy_id = get_next_id('bought.csv')

        # Define column names for 'bought.csv'
        buy_col_names = ['buy_id', 'buy_date', 'buy_name', 'buy_amount', 'buy_price', 'expire_date']

        # Create the data for the 'bought.csv' file
        bought_data = {
            'buy_id': next_buy_id,
            'buy_date': str(current_date),
            'buy_name': product_name,
            'buy_amount': amount,
            'buy_price': price,
            'expire_date': expire_date,  # Include the expire_date
        }

        # Create the data for the 'inventory.csv' file
        inventory_col_names = ['inventory_id', 'buy_id', 'buy_date', 'buy_name', 'buy_amount', 'buy_price', 'expire_date', 'is_expired']
        inventory_data = {
            'inventory_id': next_buy_id,  # Use the same ID as buy_id
            'buy_id': next_buy_id,
            'buy_date': str(current_date),
            'buy_name': product_name,
            'buy_amount': amount,
            'buy_price': price,
            'expire_date': expire_date,  # Include the expire_date
            'is_expired': 'False',  # Initially not expired
        }

        # Update the CSV files
        update_csv_data('bought.csv', buy_col_names, bought_data)
        update_csv_data(inventory_file, inventory_col_names, inventory_data)  # Use the correct inventory_file

        print("Product successfully bought.")
        # Update the management report for the purchase
        
        reporting_logic.update_management_report(inventory_file, SuperConfig.sold_file, SuperConfig.report_file)
    except Exception as e:
        print("An error occurred while buying the product ---->", e)
# ---------------------------------------------------------------------#
def get_next_id(filename):
    try:
        if os.path.exists(filename):
            # Read the existing data and get the last sell_id
            data = pd.read_csv(filename)
            if data.empty or 'sell_id' not in data.columns:
                print(f"The file does not contain valid 'sell_id' data. Starting with ID 1.")
                new_id = 1
            else:
                last_id = data['sell_id'].max()
                new_id = int(last_id) + 1
        else:
            print("The file does not exist. Creating a new one.")
            new_id = 1

        return new_id
    except FileNotFoundError:
        print("An error occurred while getting the next ID.")
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
        inventory_data = read_or_create_csv_file('inventory.csv', inventory_col_names, [])
        
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
def sell_action(name, amount, price, inventory_df):
    # Update inventory expiration status
    update_inventory_expire_status()
    
    inventory_col_names = ['id', 'buy_date', 'buy_name', 'buy_amount', 'buy_price', 'expire_date']
    inventory_data = read_or_create_csv_file('inventory.csv', inventory_col_names, [])

    # Convert 'expire_date' column to datetime64[ns] type
    inventory_data['expire_date'] = pd.to_datetime(inventory_data['expire_date'])

    # Strip leading and trailing spaces from the product name for comparison
    name_stripped = name.strip()

    # Filter products that match the name and have non-zero amount
    product_inventory = inventory_df[(inventory_df['buy_name'].str.strip() == name_stripped) & (inventory_df['buy_amount'] > 0)]

    if len(product_inventory) == 0:
        print(f"Error: Product '{name}' is out of stock and cannot be sold.")
        return

    current_date = pd.to_datetime(get_current_date())
    expired_product_inventory = product_inventory[pd.to_datetime(product_inventory['expire_date']) < current_date]

    # Print the inventory data for the specified product
    product_inventory = inventory_df[(inventory_df['buy_name'].str.strip() == name_stripped)]
    print("Inventory data for the product:")
    print(product_inventory)

    if len(expired_product_inventory) > 0:
        print(f"Error: Product '{name}' is expired and cannot be sold.")
        return

    if amount > product_inventory['buy_amount'].sum():
        print(f"Error: Not enough quantity of '{name}' available to sell.")
        return

    if price < 0:
        print("Error: Price cannot be negative.")
        return

    # Calculate revenue and profit
    revenue = amount * price
    profit = revenue - (amount * product_inventory['buy_price'].values[0])

    # Update the inventory after the sale
    update_inventory_after_sell(name, amount)

    # Update the management report for the sale
    management_report_col_names = ['buy_name', 'buy_amount', 'buy_price', 'sell_amount', 'sell_price', 'is_expired', 'revenue', 'profit']
    management_report_data = read_or_create_csv_file('management_report.csv', management_report_col_names, [])
    new_sale_entry = pd.DataFrame({'buy_name': [name], 'buy_amount': [product_inventory['buy_amount'].values[0]], 'buy_price': [product_inventory['buy_price'].values[0]], 
                                   'sell_amount': [amount], 'sell_price': [price], 'is_expired': [False if len(expired_product_inventory) == 0 else True], 
                                   'revenue': [revenue], 'profit': [profit]})
    management_report_data = pd.concat([management_report_data, new_sale_entry], ignore_index=True)
    management_report_data.to_csv('management_report.csv', index=False)

    print("Sale successful.")
# ---------------------------------------------------------------------#
def update_inventory_after_sell(name, amount):
    try:
        # Read 'inventory.csv' into a DataFrame
        inventory_data = pd.read_csv('inventory.csv')

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
        inventory_data.to_csv('inventory.csv', index=False)
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
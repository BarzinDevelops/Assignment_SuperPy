# All the IMPORTS:
# ------------------------------------------#
from datetime import datetime as dt, timedelta, date
import pandas as pd # using pandas to read from and write to files:
import numpy as np
import os

# ------------------------------------------#
line = '-' * 20  # for underlining some columns

def read_or_create_csv_file(filename, col_names, new_data):
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
        data = pd.read_csv(filename)
        if len(data) > 0:
            return data
        else:
            colnames = " | ".join(data.columns)
            return f"This file: '{filename}' -> has no data yet, only these predefined columns:\n{colnames} |"
    except FileNotFoundError:
        print(f"This file doesn't exist yet!")
        print("You will be redirected to file creator...")
        create_custom_csv_file(filename, col_names, new_data)
# ---------------------------------------------------------------------#

def create_custom_csv_file(filename, col_names, new_data):
    try:
        print(f"\nCreating your new csv file...")        
        # print(f"NEW DATA is NOW -----------------> \n{new_data}")
        df = pd.DataFrame(columns=col_names)
        df.to_csv(filename, index=False)
        print(f"\nThe file: {filename} is created.")
        # read_or_create_csv_file(filename)
    except FileExistsError:
        print(f"\nThis file: {filename}, already exists!")
    except ValueError as e:
            print(e)
# ---------------------------------------------------------------------#


def update_inventory(source_file):
    try:
        inventory_col_names = ['id', 'buy_date', 'buy_name', 'buy_amount', 'buy_price', 'expire_date', 'is_expired']
        inventory_data = read_or_create_csv_file('inventory.csv', inventory_col_names, [])
    except Exception as e:
        print("An error occurred while reading the file ---->", e)
        return

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











# ---------------------------------------------------------------------#
def buy_product(product_name, amount, price, expire_date):
    try:
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
        update_csv_data('inventory.csv', inventory_col_names, inventory_data)

        # Print the data that is being saved
        print("Data being saved to bought.csv:", bought_data)
        print("Data being saved to inventory.csv:", inventory_data)

        print("Product successfully bought.")
    except Exception as e:
        print("An error occurred while buying the product ---->", e)
        
#------------------------------------------------------------------------------------------------------

def get_next_id(filename):
    print(f"\n=========START of => get_next_id(filename)===============\n")
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

        print(f"\n=========END of => get_next_id(filename)===============\n")
        return new_id
    except FileNotFoundError:
        print("An error occurred while getting the next ID.")
        print(f"\n=========END of => get_next_id(filename)===============\n")
        return 1



    
# ---------------------------------------------------------------------------------------------------#

def update_csv_data(filename, columns, data):
    print(f"\n=========START of => update_csv_data(filename, columns, data)===============\n")

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

    print(f"\n=========END of => update_csv_data(filename, columns, data)===============\n")






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
# --------------------------------------------------------------------#        
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
    print(f"\n======START of => def check_if_has_run_today()======\n")
    with open('last_run_day.txt') as f:
        last_run_day_was = f.readline()
        last_run_day_was = dt.strptime(last_run_day_was, '%Y-%m-%d').date()
    print(f"\n======END of => def check_if_has_run_today()======\n")
    return last_run_day_was

def check_before_reset_date():
    """
    Check if the application has run today, and reset the date if needed.
    This function is executed every time the application starts.
    """
    print(f"\n======START of => def check_before_reset_date()======\n")
    last_run_date = check_if_has_run_today()
    todays_date = date.today()
    if last_run_date != todays_date:
        reset_date_in_time_file()
        with open('last_run_day.txt', 'w') as f:
            f.write(str(todays_date))
    print(f"\n======END of => def check_before_reset_date()======\n")


#=======================================SELL Implementation =============================
def check_expired_products():
    print(f"\n=========START of => def check_expired_products()===============\n")
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
    print(f"\n=========START of => sell_action(name, amount, price)===============\n")

#----------------------------------------------------------------------------------------------------------

def sell_action(name, amount, price):
    print(f"\n=========START of => def sell_action(name, amount, price)===============\n")

    inventory_col_names = ['id', 'buy_date', 'buy_name', 'buy_amount', 'buy_price', 'expire_date']
    inventory_data = read_or_create_csv_file('inventory.csv', inventory_col_names, [])

    # Convert 'expire_date' column to datetime64[ns] type
    inventory_data['expire_date'] = pd.to_datetime(inventory_data['expire_date'])

    # Filter products that match the name and have non-zero amount
    product_inventory = inventory_data[(inventory_data['buy_name'] == name) & (inventory_data['buy_amount'] > 0)]

    if len(product_inventory) == 0:
        print(f"Error: Product '{name}' is out of stock and cannot be sold.")
        return

    current_date = pd.to_datetime(get_current_date())
    expired_product_inventory = product_inventory[product_inventory['expire_date'] < current_date]

    if len(expired_product_inventory) > 0:
        print(f"Error: Product '{name}' is expired and cannot be sold.")
        return

    if amount > product_inventory['buy_amount'].sum():
        print(f"Error: Not enough quantity of '{name}' available to sell.")
        return

    if price < 0:
        print("Error: Price cannot be negative.")
        return

    # Generate a unique sell_id for the sale
    sell_id = get_next_id('sold.csv')

    # Add the sale data to the 'sold.csv' file
    sold_col_names = ['sell_id', 'sell_date', 'sell_name', 'sell_amount', 'sell_price']
    new_sale = pd.DataFrame({'sell_id': [sell_id], 'sell_date': [str(get_current_date())], 'sell_name': [name], 'sell_amount': [amount], 'sell_price': [price]})

    # Read 'sold.csv' into a DataFrame
    try:
        sold_data = pd.read_csv('sold.csv')
    except FileNotFoundError:
        sold_data = pd.DataFrame(columns=sold_col_names)

    # Concatenate the new sale data with existing sold data
    sold_data = pd.concat([sold_data, new_sale], ignore_index=True)

    # Write the updated DataFrame back to the 'sold.csv' file
    sold_data.to_csv('sold.csv', index=False)

    # Update the inventory after the sale
    update_inventory_after_sell(name, amount)

    print("Sale successful.")
    print(f"\n=========END of => sell_action(name, amount, price)===============\n")



#----------------------------------------------------------------------------------------------------------

def update_inventory_after_sell(name, amount):
    print(f"\n======START of => def update_inventory_after_sell(name, amount)======\n")
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
        print(f"\n======END of => def update_inventory_after_sell(name, amount)======\n")
    except Exception as e:
        # Handle the error
        print("An error occurred while updating inventory after sell. Check this function: def update_inventory_after_sell(name, amount) ---->", e)

#-------------------------------------------------------------------------------------
#==========================generating reports ======================================
def generate_inventory_report():
    print(f"\n======START of => def generate_inventory_report()======\n")
    try:
        inventory_col_names = ['id', 'buy_date', 'buy_name', 'buy_amount', 'buy_price', 'expire_date']
        inventory_data = read_or_create_csv_file('inventory.csv', inventory_col_names, [])
        print("Inventory Report:")
        print(line)
        print(inventory_data.to_string(index=False))
    except Exception as e:
        # Handle the error
        print("An error occurred while generating inventory report ---->", e)
    print(f"\n======END of => def generate_inventory_report()======\n")

# ... (the rest of the functions are unchanged)

def generate_revenue_report():
    print(f"\n======START of => def generate_revenue_report()======\n")
    try:
        # Calculate revenue and profit data by reading the required files
        calculate_revenue_profit('bought.csv', 'sold.csv', 'inventory.csv')
        revenue_col_names = ['buy_name', 'revenue']
        revenue_data = read_or_create_csv_file('inventory.csv', revenue_col_names, [])
        print("Revenue Report:")
        print(line)
        print(revenue_data.to_string(index=False))
    except Exception as e:
        # Handle the error
        print("An error occurred while generating revenue report ---->", e)
    print(f"\n======END of => def generate_revenue_report()======\n")


def generate_profit_report():
    print(f"\n======START of => def generate_profit_report()======\n")
    try:
        # Calculate revenue and profit data by reading the required files
        calculate_revenue_profit('bought.csv', 'sold.csv', 'inventory.csv')
        profit_col_names = ['buy_name', 'profit']
        profit_data = read_or_create_csv_file('inventory.csv', profit_col_names, [])
        print("Profit Report:")
        print(line)
        print(profit_data.to_string(index=False))
    except Exception as e:
        # Handle the error
        print("An error occurred while generating profit report ---->", e)
    print(f"\n======END of => def generate_profit_report()======\n")
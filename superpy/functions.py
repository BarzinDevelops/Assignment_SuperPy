# All the IMPORTS:
# ------------------------------------------#
from datetime import datetime as dt, timedelta, date
import pandas as pd # using pandas to read from and write to files:
import numpy as np

# ------------------------------------------#


# reading from the file if exists, otherwise create it:
def read_or_create_csv_file(filename, col_names, new_data):
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
        inventory_col_names = ['id', 'buy_date', 'buy_name', 'buy_amount', 'buy_price', 'expire_date']
        read_or_create_csv_file('inventory.csv', inventory_col_names, [])
    
    except Exception as e:
        # Handle the error
        print("in update_invetory() -> An error occurred while reading the file ---->", e)
        return 
    
    try:
        # Read 'bought.csv' into a DataFrame
        bought_data = pd.read_csv(source_file)
        
        # Read 'inventory.csv' into a DataFrame
        inventory_data = pd.read_csv('inventory.csv')
        
    except Exception as e:
        # Handle the error
        print("An error occurred while reading the file ---->", e)
        return
    
    # Generate an auto-incremented ID for each row in 'bought.csv'
    new_ids = range(len(inventory_data) + 1, len(inventory_data) + 1 + len(bought_data))
    
    # Add the new IDs to the 'id' column of 'bought_data'
    bought_data['id'] = new_ids
    
    # Concatenate 'bought_data' with 'inventory_data'
    updated_data = pd.concat([inventory_data, bought_data], ignore_index=True)
    
    # Write the updated DataFrame back to 'inventory.csv'
    updated_data.to_csv('inventory.csv', index=False)

# Call the function with the 'bought.csv' file
# update_inventory('bought.csv')







# ---------------------------------------------------------------------#


def update_csv_data(filename, col_names, new_data):
    try:
        read_or_create_csv_file(filename, col_names, new_data)
    except Exception as e:
        # Handle the error
        print("An error in UPDATE_CSV_DATA() function ---->", e)
    
    
    # Read existing CSV file into a DataFrame
    data = pd.read_csv(filename)

    # Generate an auto-incremented ID
    new_id = len(data) + 1

    # Create a new DataFrame with ID and other data
    # check if file is 'inventory.csv'-> it shoul also 
    # contain a bought_id field that contains the id of the bought item.
    if filename == 'bought.csv' or filename == 'sold.csv':
        new_row = pd.DataFrame([[new_id] + 
                                list(new_data)], 
                                columns=['id'] + 
                                list(data.columns[1:]))
    
    # Concatenate the new row with the existing DataFrame
    updated_data = pd.concat([data, new_row], ignore_index=True)

    # Write the updated DataFrame back to the CSV file
    updated_data.to_csv(filename, index=False)
    
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
    current_date = get_current_date()
    advance = timedelta(number)
    new_date = current_date + advance
    print(f"""in advance_time(number)--> 'new_date = {new_date}'
          'current_date = {current_date}' and
          'advance = {advance}' """)
    with open('time.txt', 'w') as f:
        f.write(str(new_date))
# --------------------------------------------------------------------#        
def reset_date_in_time_file(custom_date='2023-07-01'):
    """
    Set date in the time.txt file to '2023-07-01' as symbolic date 
    that represents current date in the application.
    Execute every time the application starts.
    """
    with open('time.txt', 'w') as f:
        f.write(custom_date)
        
# ---------------------------------------------------------------------#
def check_if_has_run_today():
    with open('last_run_day.txt') as f:
        last_run_day_was = f.readline()
        last_run_day_was = dt.strptime(last_run_day_was, '%Y-%m-%d').date()
    return last_run_day_was

def check_before_reset_date():
    last_run_date = check_if_has_run_today()
    todays_date = date.today()
    print(f"""check_before_reset_date() values: -> 
          last_run_date value ==> {last_run_date}, last_run_date type ==> {type(last_run_date)}
          todays_date ==> {todays_date}, todays_date type==> {type(todays_date)}
          last_run_date != todays_date => {last_run_date != todays_date}""")
    print('---'*30)
    if last_run_date != todays_date:
        reset_date_in_time_file()
        with open('last_run_day.txt', 'w') as f:
            f.write(str(todays_date))
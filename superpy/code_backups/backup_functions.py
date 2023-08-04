# All the IMPORTS:
# ------------------------------------------#
from datetime import datetime as dt, timedelta
import pandas as pd # using pandas to read from and write to files:

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
    new_row = pd.DataFrame([[new_id] + list(new_data)], columns=['id'] + list(data.columns[1:]))

    # Concatenate the new row with the existing DataFrame
    updated_data = pd.concat([data, new_row], ignore_index=True)

    # Write the updated DataFrame back to the CSV file
    updated_data.to_csv(filename, index=False)

    # current_data = read_or_create_csv_file(filename)
    # print(current_data.to_string(index=False, justify='center'))

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


def get_current_date():
    # setting values of a row:
    with open('time.txt') as f:
        today = f.readline()
    return dt.strptime(today, '%Y-%m-%d').date()

def advance_time(number):
    current_date = get_current_date()
    advance = timedelta(number)
    new_date = current_date + advance
    with open('time.txt', 'w') as f:
        f.write(str(new_date))
        
def reset_date_in_time_file(custom_date='2023-07-01'):
    """
    Set date in the time.txt file to '2023-01-01' as symbolic date 
    that represents current date in the application.
    Execute every time the application starts.
    """
    with open('time.txt', 'w') as f:
        f.write(custom_date)
            
 
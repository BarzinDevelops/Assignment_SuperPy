# Imports
import os
import argparse
import csv
from datetime import date
# using pandas to read from and write to files:
import pandas as pd

# Do not change these lines.
# __winc_id__ = "a2bc36ea784242e4989deb157d527ba0"
# __human_name__ = "superpy"


# Your code below this line.
#------------------------------------------

# Set pandas display options
pd.set_option('display.width', None)  # Allow unlimited width
pd.set_option('display.max_columns', None)  # Show all columns

def main():
    parser = argparse.ArgumentParser(
        description="Supermarket Inventory Tool.",
        )
    
    # indicating: to buy or to sell
    parser.add_argument(
        '--action', 
        choices=['buy', 'sel'],
        metavar='buy or sel',          
        type=str, 
        help='Choose if you want to buy or sel the product.'
        )

    # getting arguments
    parser.add_argument(
        '-pn', '--prod_name', 
        metavar='', 
        type=str, 
        help='Name of the product to add.'
        )
    parser.add_argument(
        '-q', '--quantity', 
        metavar='', 
        type=str, 
        help='How many of this product to add.'
        )
    parser.add_argument(
        '-pp', '--prod_price',
        metavar='', 
        type=float, 
        help='Price of the product to add.'
        )
    parser.add_argument(
        '-exp', '--exp_date',
        metavar='', 
        type=str, 
        default="None",
        help='Date of expiration (e.g., 2023-06-18)'
        )
    
    args = parser.parse_args()
    
    # setting values of a row:
    current_date = date.today().strftime('%Y-%m-%d')
    received_args_series = pd.Series([current_date,args.prod_name,args.quantity, args.prod_price, args.exp_date])

    update_csv_data('buy.csv', received_args_series)
    # read_or_create_csv_file('buy.csv')
#--------------------------------------------


# reading from the file if exists, otherwise create it:
def read_or_create_csv_file(filename):
    try:
        data = pd.read_csv(filename)
        if len(data) > 0:
            return data
        else:
            colnames = " | ".join(data.columns)
            return f"This file: '{filename}' -> has no data yet, only these predefined columns:\n{colnames} |"
        
    except FileNotFoundError:
        print(f"This file doesn't exist yet!")
        create_custom_csv_file(filename)


def create_custom_csv_file(filename):
    user_answer = input("\nDo you want to create a new csv file with your own columns? (enter: 'y' or 'n'): ").lower()
    
    if user_answer == 'y':
        column_names = input("\nEnter column names you want (separated by commas): ").split(',')
        try:
            print(f"\nCreating your new csv file...")
            df = pd.DataFrame(columns=column_names)
            df.to_csv(filename, index=False)
            print(f"\nThe file: {filename} is created.")
        except FileExistsError:
            print(f"\nThis file: {filename}, already exists!")
    else:
        print("\nNo problem. Good luck.")
    
def update_csv_data(filename, new_data):
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


        
        

if __name__ == "__main__":
    main()
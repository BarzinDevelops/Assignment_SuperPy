# Imports
import os
import argparse
import csv
from datetime import date
# using pandas to read from and write to files:
import pandas as pd

# Do not change these lines.
__winc_id__ = "a2bc36ea784242e4989deb157d527ba0"
__human_name__ = "superpy"


# Your code below this line.


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
        '-pp', '--price',
        metavar='', 
        type=float, 
        help='Price of the product to add.'
        )
    parser.add_argument(
        '-exp', '--expires',
        metavar='', 
        type=str, 
        default="None",
        help='The date of expiration (e.g., 2023-06-18)'
        )
    
    args = parser.parse_args()
    
    read_or_create_csv_file('buy.csv')
#--------------------------------------------


# reading from the file if exists, otherwise create it:
def read_or_create_csv_file(filename):
    try:
        data = pd.read_csv(filename)
        # data['id'] = range(1, len(data) + 1)
        # data.set_index('id', inplace=True)
        # data.to_csv('buy.csv', index=True)
        if len(data) > 0:
            print(f"The content of {filename} is: \n{data}")
        else:
            colnames = ",\n".join(data.columns)
            print(f"This file has no data, only these columns:\n{colnames}")
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
    

if __name__ == "__main__":
    main()
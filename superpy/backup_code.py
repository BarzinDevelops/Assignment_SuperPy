# Imports
import os
import argparse
import csv
from datetime import date

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
    
    
    args = parser.parse_args()
    # print(f"args: {args}")
    print(f"args.action: {args.action}")
    print(f"args.prod_name: {args.prod_name}")
    print(f"args.price: {args.price}")

            
    if args.prod_name is not None and args.price is not None:
        update_inventory(args.prod_name, args.price, args.expires)
    else:
        inventory = read_inventory()
        for i, item in enumerate(inventory):
            print(f"inventory item{i+1}:\n{inventory[i]}")

#--------------------------------------------
# using pandas to read from and write to files:

import pandas as pd

# reading from the file if exists, otherwise create it:
try:
    data = pd.read_csv('inventory.csv')
    print(data)
except FileNotFoundError:
    print(f"This file doesn't exist yet!")



def read_inventory():
    """The read_inventory function reads the inventory data from a CSV file named 'inventory.csv' and returns it as a list of rows."""
    inventory = []
    filename = 'inventory.csv'
    
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            reader = csv.reader(file)
            try:
                next(reader)  # Skip the header row
                for row in reader:
                    inventory.append(row)
            except StopIteration:
                pass  # Empty file, no rows to read
    else:
        print(f"The file '{filename}' does not exist. Creating a new file.")
        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Date', 'product_name', 'product_price', 'expire_date'])  # Write the headers to the new file
    return inventory

def write_inventory(inventory):
    """The write_inventory function takes the inventory data as input and writes it back to the CSV file, 
    overwriting the existing contents."""
    with open('inventory.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['date', 'product_name', 'product_price', 'expire_date'])
        writer.writerows(inventory)

def update_inventory(product_name, product_price,expire_date):
    """The update_inventory function reads the existing inventory, appends a new row with the current date, 
    item name, and quantity, and then writes the updated inventory back to the CSV file using the write_inventory function. Finally, it prints a success message."""
    inventory = read_inventory()
    inventory.append([str(date.today()), product_name.title(), str(product_price), expire_date])
    write_inventory(inventory)
    

if __name__ == "__main__":
    main()
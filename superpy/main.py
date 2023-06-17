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
        usage="Supermarket Inventory Tool.",
        # description="Supermarket Inventory Tool.",
        )
    parser.add_argument('pos', type=str, help='some positional arg.')
    parser.add_argument('--item', type=str, help='Name of the item to add to Inventory.')
    parser.add_argument('--quantity', type=int, help='Quantity of this item to add to Inventory.')
    
    args = parser.parse_args()
    item = args.item
    quantity = args.quantity
    
    if item is not None and quantity is not None:
        update_inventory(item, quantity)
    else:
        inventory = read_inventory()
        for i, item in enumerate(inventory):
            print(f"inventory item{i+1}:\n{inventory[i]}")

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
            writer.writerow(['Date', 'Item', 'Quantity'])  # Write the headers to the new file
    return inventory

def write_inventory(inventory):
    """The write_inventory function takes the inventory data as input and writes it back to the CSV file, 
    overwriting the existing contents."""
    with open('inventory.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Date', 'Item', 'Quantity'])
        writer.writerows(inventory)

def update_inventory(item, quantity):
    """The update_inventory function reads the existing inventory, appends a new row with the current date, 
    item name, and quantity, and then writes the updated inventory back to the CSV file using the write_inventory function. Finally, it prints a success message."""
    inventory = read_inventory()
    inventory.append([str(date.today()), item.title(), str(quantity)])
    write_inventory(inventory)
    

if __name__ == "__main__":
    main()
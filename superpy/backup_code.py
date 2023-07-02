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
    
    
    
    
    
    
""" 
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
    
"""
    
    
    
    
""" 
    # getting arguments
    # parser.add_argument(
    #     '-pn', '--prod_name', 
    #     metavar='', 
    #     type=str, 
    #     help='Name of the product to add.'
    #     )
    # parser.add_argument(
    #     '-q', '--quantity', 
    #     metavar='', 
    #     type=str, 
    #     help='How many of this product to add.'
    #     )
    # parser.add_argument(
    #     '-pp', '--prod_price',
    #     metavar='', 
    #     type=float, 
    #     help='Price of the product to add.'
    #     )
    # parser.add_argument(
    #     '-exp', '--exp_date',
    #     metavar='', 
    #     type=str, 
    #     default="None",
    #     help='Date of expiration (e.g., 2023-06-18)'
    #     )
"""


""" # ---------------Other version----------------------
    
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

    # created 5 backspaces to pull a string back 5 places:
    reverse_tab = '\b\b\b\b\b'



    def main():
        # To include the help messages for the subparser arguments in the overall help message when running python main.py -h, this class overrides the argparse default help formatter and provides a custom formatter class.
        class CustomHelpFormatter(argparse.HelpFormatter):
            def _format_action(self, action):
                parts = super()._format_action(action)
                if action.nargs != argparse.PARSER:
                    # The modification ensures that the help messages for subparser arguments are properly indented.
                    parts = parts.replace('\n', '\n    ')
                return parts

        # Formatter class that inherits from both argparse.RawTextHelpFormatter and CustomHelpFormatter. 
        class CombinedHelpFormatter(argparse.RawTextHelpFormatter, CustomHelpFormatter):
            pass

        parser = argparse.ArgumentParser(
            description="Supermarket Inventory Tool.",
            formatter_class=CombinedHelpFormatter
            )

        subparsers = parser.add_subparsers(dest='action')
    
        buy_parser = subparsers.add_parser(
            'buy', 
            help='Buy action help message'
            )
        buy_parser.add_argument(
            'product_name',
            metavar='', 
            type=str, 
            help='Specify the name of the product.')
        buy_parser.add_argument(
            '-pa','--prod_amount', 
            metavar='',
            type=int, 
            help='Specify the amount of the product you want.')
        buy_parser.add_argument(
            '-pp','-prod_price', 
            metavar='',
            type=float, 
            help='Specify the price of the product.')
        buy_parser.add_argument(
            '-ed','-expire_date', 
            metavar='',
            type=str, 
            help='Specify the expiration date of the product')

 sell_parser = subparsers.add_parser('sell')
        sell_parser.add_argument(
            'sell_product_name', 
            type=str, 
            help='Specify the name of the product being sold')
        sell_parser.add_argument(
            'sell_product_quantity', 
            type=int, 
            help='Specify the quantity of the product being sold')
        sell_parser.add_argument(
            'sell_product_price', 
            type=float, 
            help='Specify the price of the product being sold') 

        report_parser = subparsers.add_parser('report')
        report_parser.add_argument(
            'report_type', 
            choices=['inventory', 'revenue', 'profit'], 
            metavar='', 
            type=str,
            help=f'''Choose what kind of report you want: [buy or sel]'''
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
"""





""" 
    sell_parser = subparsers.add_parser('sell')
    sell_parser.add_argument(
        'sell_product_name', 
        type=str, 
        help='Specify the name of the product being sold')
    sell_parser.add_argument(
        'sell_product_quantity', 
        type=int, 
        help='Specify the quantity of the product being sold')
    sell_parser.add_argument(
        'sell_product_price', 
        type=float, 
        help='Specify the price of the product being sold') 
"""


""" 
    
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

"""
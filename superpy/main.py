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

line = '-'*20 # for underlining some columns 

# Set pandas display options
pd.set_option('display.width', None)  # Allow unlimited width
pd.set_option('display.max_columns', None)  # Show all columns

# created 5 backspaces to pull a string back 5 places:
reverse_tab = '\b\b\b\b\b'
reverse_tab2 = '\b\b\b\b\b\b\b\b\b\b'
reverse_tab3 = '\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b'


def main():
    
    parser = argparse.ArgumentParser(
        description="Supermarket Inventory Tool.",
        formatter_class=argparse.RawTextHelpFormatter
        )

    subparsers = parser.add_subparsers(dest='action')
 
    buy_parser = subparsers.add_parser(
        'buy', 
        help='Buy action help message'
        )
    buy_parser.add_argument(
        'buy_name',
        # metavar='',
        type=str,
        help='Specify the name of the product.'
    )
    buy_parser.add_argument(
        'buy_amount', 
        # metavar='',
        type=int, 
        help='Specify the amount of the product you want.')
    buy_parser.add_argument(
        'buy_price', 
        # metavar='',
        type=float, 
        help='Specify the price of the product.')
    buy_parser.add_argument(
        '--expire_date', 
        metavar='',
        type=str, 
        help='Provide expire date (year-month-day)-> 2013-05-23 ')

    sell_parser = subparsers.add_parser('sell')
    sell_parser.add_argument(
        'sell_name', 
        type=str, 
        help='Specify the name of the product being sold')
    sell_parser.add_argument(
        'sell_amount', 
        type=int, 
        help='Specify the amount of the product being sold')
    sell_parser.add_argument(
        'sell_price', 
        type=float, 
        help='Specify the price of the product being sold')

    report_parser = subparsers.add_parser('report')
    report_parser.add_argument(
        'report_type', 
        choices=['inventory', 'revenue', 'profit'], 
        metavar='report_type', 
        type=str,
        help=f"""Choose what kind of report you want: [inventory, revenue, profit]"""
    )

    args = parser.parse_args()
    
    # setting values of a row:
    current_date = date.today().strftime('%Y-%m-%d')
    # determine if the input is for buy/sell and set the received_args_series accordingly:
    print(args)
    if args.action=='buy':
        print(f"""
              {reverse_tab3}bought product name:    {args.buy_name}
              {reverse_tab3}bought product amount:  {args.buy_amount}
              {reverse_tab3}bought product price:   {args.buy_price}
              {reverse_tab3}product expire date:    {args.expire_date}
              """)
        #if bought:
        received_args_series = pd.Series([current_date,args.buy_name,args.buy_amount, args.buy_price, args.expire_date])
        col_names = ['id', 'buy_date', 'buy_name', 'buy_amount', 'buy_price', 'expire_date']
        update_csv_data('bought.csv', col_names, received_args_series)
    elif args.action=='sell':
        print(f"""
              {reverse_tab3}sold product name:    {args.sell_name}
              {reverse_tab3}sold product amount:  {args.sell_amount}
              {reverse_tab3}sold product price:   {args.sell_price}
              """)
         #if sold:  
        received_args_series = pd.Series([current_date,args.sell_name,args.sell_amount, args.sell_price])
        col_names = ['id', 'sell_date', 'sell_name', 'sell_amount', 'sell_price']
        update_csv_data('sold.csv', col_names, received_args_series, )

    # Example usage
    calculate_revenue_profit('bought.csv', 'sold.csv', 'inventory.csv')
    df =  pd.read_csv('inventory.csv')
    print(f"\nFrom inventory.csv :\n{line}\n{df.to_string(index=False)}")

#--------------------------------------------


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
        # new_data = pd.concat([pd.Series(['id']), new_data], ignore_index=True)
        
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



if __name__ == "__main__":
    main()
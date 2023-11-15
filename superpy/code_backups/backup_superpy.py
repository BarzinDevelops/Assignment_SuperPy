# Imports
import argparse
from functions import *
import pandas as pd
from rich import print as rprint

# Do not change these lines.
__winc_id__ = "a2bc36ea784242e4989deb157d527ba0"
__human_name__ = "superpy"

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

    subparsers = parser.add_subparsers(
        dest='action',
        help='Choose which action you want to take: buy/sell/report'
    )

    buy_parser = subparsers.add_parser('buy')
    buy_parser.add_argument('buy_name', type=str, help='Specify the name of the product.')
    buy_parser.add_argument('buy_amount', type=int, help='Specify the amount of the product you want.')
    buy_parser.add_argument('buy_price', type=float, help='Specify the price of the product.')
    buy_parser.add_argument('expire_date', metavar='', type=str, help='Provide expire date (year-month-day)')

    sell_parser = subparsers.add_parser('sell')
    sell_parser.add_argument('sell_name', type=str, help='Specify the name of the product being sold')
    sell_parser.add_argument('sell_amount', type=int, help='Specify the amount of the product being sold')
    sell_parser.add_argument('sell_price', type=float, help='Specify the price of the product being sold')

    time_parser = subparsers.add_parser('time')
    time_parser.add_argument('advance_time', type=int, help='Advance the current date by a specified number of days.')
    
    report_parser = subparsers.add_parser('report')
    report_parser.add_argument('report_type', choices=['inventory', 'revenue', 'profit', 'expired'], metavar='report_type', type=str, help="Choose what kind of report you want ['inventory', 'revenue', 'profit', or 'expired']")

    args = parser.parse_args()

    if args.action == 'time' and args.advance_time:  # Fixing the conditional check
        print(f"Current date in the application is --> {get_current_date()}")
        advance_time(int(args.advance_time))
        print(f"Now the date in time.txt file is --> {get_current_date()}")
        update_inventory_expire_status()
    
    elif args.action == 'buy':
        product_name = args.buy_name
        amount = args.buy_amount
        price = args.buy_price
        expire_date = args.expire_date
        update_inventory_expire_status()

        # Call the shared buy_product function with the correct arguments
        buy_product(product_name, amount, price, expire_date)  # Pass expire_date as an argument   
        
    elif args.action == 'sell':
        update_inventory_expire_status()
        sell_action(args.sell_name, args.sell_amount, args.sell_price)
    elif args.action == 'report':
        inventory_file = r'C:\Github\SuperPy\superpy\inventory.csv'
        update_inventory_expire_status()
        if args.report_type == 'expired':
            check_expired_products()
        elif args.report_type == 'inventory':
            generate_inventory_report()
        elif args.report_type == 'revenue':
            generate_revenue_report(inventory_file)
        elif args.report_type == 'profit':
            generate_profit_report()
        else:
            print("Invalid report type. Please choose 'inventory', 'revenue', 'profit', or 'expired'.")

if __name__ == "__main__":
    check_before_reset_date()
    main()

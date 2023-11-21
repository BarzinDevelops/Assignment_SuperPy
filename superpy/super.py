# Imports
import argparse, pandas as pd
import functions
from config import SuperConfig
import reporting_logic

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
    super_config = SuperConfig()
    
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
        print(f"Current date in the application is --> {reporting_logic.get_current_date()}")
        functions.advance_time(int(args.advance_time))
        print(f"Now the date in time.txt file is --> {functions.get_current_date()}")
        functions.update_inventory_expire_status()
    
    elif args.action == 'buy':
        product_name = args.buy_name
        amount = args.buy_amount
        price = args.buy_price
        expire_date = args.expire_date
        # functions.update_inventory_expire_status()

        if functions.validate_expire_date_before_buying(expire_date):
            # Call the shared buy_product function with the correct arguments
            functions.buy_product(product_name, amount, price, expire_date)  # Pass expire_date as an argument   
        else:
            print(f"Error: This Product: '{product_name}' is already expired and cannot be bought!")
            
    elif args.action == 'sell':
        # functions.sell_action(args.sell_name, args.sell_amount, args.sell_price, inventory_df)
        reporting_logic.update_management_report(super_config.inventory_file, super_config.sold_file, super_config.management_report_file)  # Correct arguments here
        # Add the call to update_expired_items_in_management_report here
        reporting_logic.update_expired_items_in_management_report()
        
    elif args.action == 'report':
        functions.update_inventory_expire_status()
        if args.report_type == 'expired':
            functions.check_expired_products() # Use the check_expired_products function
        elif args.report_type == 'inventory':
            reporting_logic.generate_inventory_report() # Use the generate_inventory_report function
        elif args.report_type == 'revenue':
            # inspection_code()
            reporting_logic.generate_revenue_report(super_config.inventory_file, super_config.bought_file, super_config.sold_file, super_config.management_report_file) # Use the generate_revenue_report function
        elif args.report_type == 'profit':
            reporting_logic.generate_profit_report(super_config.inventory_file, super_config.bought_file, super_config.sold_file, super_config.management_report_file) # Use the generate_profit_report function
        else:
            print("Invalid report type. Please choose 'inventory', 'revenue', 'profit', or 'expired'.")

if __name__ == "__main__":
    functions.check_before_reset_date()
    main()

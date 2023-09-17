# Imports
import argparse
from functions import * 
from rich.console import Console
from rich.table import Table

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

    # print(f"today is: {date.today()}")
    
    parser = argparse.ArgumentParser(
        description="Supermarket Inventory Tool.",
        formatter_class=argparse.RawTextHelpFormatter
        )

    subparsers = parser.add_subparsers(
        dest='action',
        help='Choose which action you want to take: buy/sell/report'
        )
    parser.add_argument(
        '--advance_time',
        metavar='',
        type=str,
        help='Specify how many days you want to go in future.'
    )
    buy_parser = subparsers.add_parser('buy')
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

    # report_parser = subparsers.add_parser('report')
    # report_parser.add_argument(
    #     'report_type', 
    #     choices=['inventory', 'revenue', 'profit'], 
    #     metavar='report_type', 
    #     type=str,
    #     help=f"""Choose what kind of report you want: [inventory, revenue, profit]"""
    # )
    
    report_parser = subparsers.add_parser('report')
    report_parser.add_argument(
        'report_type',
        choices=['inventory', 'revenue', 'profit', 'expired'],  # Add 'expired' as a choice
        metavar='report_type',
        type=str,
        help=f"Choose what kind of report you want: [inventory, revenue, profit, expired]"  # Add 'expired'
    )


    args = parser.parse_args()   
    
    # Check if --advance_time argument is present
    if args.advance_time:
        #first print the current date as saved in time.txt file:
        print(f"Current date in the application is --> {get_current_date()}")
        # Call the advance_time function with the specified number of days
        advance_time(int(args.advance_time)) 
        # print what your advanced time action did to the previous date in time.txt:
        print(f"Now the the date in time.txt file is --> {get_current_date()}")

    # determine if the input is for buy/sell and set the received_args_series accordingly:
    if args.action=='buy':
        #if bought:
        received_args_series = pd.Series([get_current_date(),args.buy_name,args.buy_amount, args.buy_price, args.expire_date])
        
        buy_col_names = ['id', 'buy_date', 'buy_name', 'buy_amount', 'buy_price', 'expire_date']
        
        update_csv_data('bought.csv', buy_col_names, received_args_series)
        update_inventory('bought.csv')
    
    
########################## SELL ACTIONS ##############################
    elif args.action == 'sell':
        # Sell action
        sell_action(args.sell_name, args.sell_amount, args.sell_price)
    elif args.action == 'report':
        if args.report_type == 'expired':
            check_expired_products()
        elif args.report_type == 'inventory':
            generate_inventory_report()
        elif args.report_type == 'revenue':
            generate_revenue_report()
        elif args.report_type == 'profit':
            generate_profit_report()
    else:
        print("Invalid action. Please choose 'buy', 'sell', or 'report'.")
#--------------------------------------------

if __name__ == "__main__":
    # check_if_has_run_today()
    check_before_reset_date()
    main()
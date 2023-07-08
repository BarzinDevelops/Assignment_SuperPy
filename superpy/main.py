# Imports
import argparse
from functions import * 

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
    reset_date_in_time_file()
    parser = argparse.ArgumentParser(
        description="Supermarket Inventory Tool.",
        formatter_class=argparse.RawTextHelpFormatter
        )

    subparsers = parser.add_subparsers(
        dest='action',
        help='Choose which action you want to take: buy/sell/report '
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

    report_parser = subparsers.add_parser('report')
    report_parser.add_argument(
        'report_type', 
        choices=['inventory', 'revenue', 'profit'], 
        metavar='report_type', 
        type=str,
        help=f"""Choose what kind of report you want: [inventory, revenue, profit]"""
    )

    args = parser.parse_args()    

    # determine if the input is for buy/sell and set the received_args_series accordingly:
    print(args)
    if args.action=='buy':
        #if bought:
        received_args_series = pd.Series([current_date,args.buy_name,args.buy_amount, args.buy_price, args.expire_date])
        col_names = ['id', 'buy_date', 'buy_name', 'buy_amount', 'buy_price', 'expire_date']
        update_csv_data('bought.csv', col_names, received_args_series)
    elif args.action=='sell':
         #if sold:  
        received_args_series = pd.Series([current_date,args.sell_name,args.sell_amount, args.sell_price])
        col_names = ['id', 'sell_date', 'sell_name', 'sell_amount', 'sell_price']
        update_csv_data('sold.csv', col_names, received_args_series, )

    # Example usage
    # df =  pd.read_csv('inventory.csv')
    # print(f"\nfrom inventory.csv :\n{line}\n{df.to_string(index=False)}")
    # calculate_revenue_profit('bought.csv', 'sold.csv', 'inventory.csv')
    print(get_current_date())
    advance_time(10)
    print(get_current_date())
#--------------------------------------------



if __name__ == "__main__":
    main()
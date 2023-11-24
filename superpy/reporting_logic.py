# Import third party modules
from rich.table import Table
from rich.console import Console
from rich.style import Style
from rich import box
import pandas as pd
# Import local modules:
import functions
from config import SuperConfig


# ===============================================================================
# ===============================================================================
# ===============================================================================
def calculate_revenue_profit(name, amount, price, product_inventory):
    # Calculate revenue and profit
    revenue = amount * price
    profit = revenue - (amount * product_inventory['buy_price'].values[0])

    # Update the management report for the sale
    management_report_col_names = ['buy_name', 'buy_amount', 'buy_price', 'sell_amount', 'sell_price', 'is_expired', 'revenue', 'profit']
    management_report_data = functions.read_or_create_csv_file(super_config.management_report_file, management_report_col_names)
    
    new_sale_entry = pd.DataFrame({
        'buy_name': [name],
        'buy_amount': [product_inventory['buy_amount'].values[0]],
        'buy_price': [product_inventory['buy_price'].values[0]],
        'sell_amount': [amount],
        'sell_price': [price],
        'is_expired': [False if pd.isna(product_inventory['expire_date'].values[0]) else True],
        'revenue': [revenue],
        'profit': [profit]
    })

    management_report_data = pd.concat([management_report_data, new_sale_entry], ignore_index=True)
    management_report_data.to_csv(super_config.management_report_file, index=False)

    return revenue, profit



#==========================generating reports ======================================
console = Console()
# This function is for investigating data in the .csv files to see if there are any data missing:
super_config = SuperConfig()

def inspection_code():
    # INSPECTION CODE -----------------------------
    print(f"-------------START INSPECTION CODE OUTPUT-----------------------")
    # Load and inspect data from CSV files
    bought_data = pd.read_csv(super_config.bought_file)
    sold_data = pd.read_csv(super_config.sold_file)
    inventory_data = pd.read_csv(super_config.inventory_file)

    # Inspect the data for missing values
    print("Bought Data:")
    print(bought_data.isna().sum())

    print("\nSold Data:")
    print(sold_data.isna().sum())

    print("\nInventory Data:")
    print(inventory_data.isna().sum())

    print(f"-------------END INSPECTION CODE OUTPUT-----------------------")
    #  END OF INSPECTION-----------------------------


# ----------------------------------------------------------------------------
def generate_inventory_report():
    """
    Generate an inventory report.
    
    This function reads the inventory data from 'inventory.csv'
    and prints a formatted report of the inventory.
    
    The report includes details such as product name, amount, price, and expiration date.
    """
    
    try:
        inventory_col_names = ['buy_name', 'buy_amount', 'buy_price', 'expire_date', 'is_expired']
        inventory_data = functions.read_or_create_csv_file(super_config.inventory_file, inventory_col_names)      
        table = Table(title="Inventory Report", style='white', box=box.ROUNDED)
        table.add_column("[bold purple]Product Name[/bold purple]")
        table.add_column("[bold dodger_blue3]Amount[/bold dodger_blue3]")
        table.add_column("[bold dark_green]Price[/bold dark_green]")
        table.add_column("[bold dark_orange]Expiration Date[/bold dark_orange]")
        table.add_column("[bold rgb(155,0,0)]Is the product expired?[/bold rgb(155,0,0)]")

        # Add rows to the table
        for _, row in inventory_data.iterrows():
            product_name = f"[medium_purple1]{row['buy_name']}[/medium_purple1]"
            amount = f"[dodger_blue1]{row['buy_amount']}[/dodger_blue1]"
            price = f"[green]{row['buy_price']}[/green]"
            expire_date = f"[orange1]{row['expire_date']}[/orange1]"
            if row['is_expired'] == True:
                is_expired = f"[yellow1]{row['is_expired']}[/yellow1]"
            else:
                is_expired = f"[red1]{row['is_expired']}[/red1]"
                
            

            table.add_row(product_name, amount, price, expire_date, is_expired)

        console = Console()
        console.print(table)

    except Exception as e:
        print("An error occurred while generating the inventory report ---->", e)


# -------------------------------------------------------------------------------------





def generate_revenue_report(inventory_file, bought_file, sold_file, management_report_file):
    # Load data from CSV files
    sold_data = pd.read_csv(sold_file)
    inventory_data = pd.read_csv(inventory_file)
    bought_data = pd.read_csv(bought_file)

    # Calculate revenue for products that are not expired
    revenue_data = sold_data[~sold_data['buy_name'].isin(inventory_data[inventory_data['is_expired']]['buy_name'])]
    revenue_data['revenue'] = revenue_data['sell_amount'] * revenue_data['sell_price']

    # Merge with bought data
    merged_data = revenue_data.merge(bought_data, left_on='buy_name', right_on='buy_name', suffixes=('_sold', '_bought'))

    # Update inventory based on items sold
    for _, row in merged_data.iterrows():
        product_name = row['buy_name']
        sold_amount = row['sell_amount']
        inventory_data.loc[inventory_data['buy_name'] == product_name, 'buy_amount'] -= sold_amount

    # Ensure total bought is not less than total sold
    merged_data['buy_amount'] = merged_data[['buy_amount', 'sell_amount']].max(axis=1)

    # Select relevant columns for the report
    report_data = merged_data.groupby('buy_name').agg({
        'buy_amount': 'sum',
        'buy_price': 'mean',
        'sell_amount': 'sum',
        'sell_price': 'mean',
        'revenue': 'sum'
    }).reset_index()

    # Append the new report data to the management report file
    report_data.to_csv(management_report_file, mode='w', header=True, index=False)  # Use mode='w' to overwrite the file
    print("Management report updated successfully.")

    # Print the report using a Rich table
    console = Console()
    table = Table(title="Revenue Report", style='blue', box=box.ROUNDED)
    table.add_column("[bold purple]Product Name[/bold purple]", justify="center", style="bold", no_wrap=True)
    table.add_column("Total Buy Amount", justify="center", style="bold", no_wrap=True)
    table.add_column("Buy Price", justify="center", style="bold", no_wrap=True)
    table.add_column("Sold Amount", justify="center", style="bold", no_wrap=True)
    table.add_column("Sold Price", justify="center", style="bold", no_wrap=True)
    table.add_column("Revenue Per Item", justify="center", style="bold", no_wrap=True)
    table.add_column("Total Revenue", justify="center", style="bold", no_wrap=True)

    for _, row in report_data.iterrows():
        revenue_per_item =  row['sell_price'] -  row['buy_price'] if row['sell_amount'] > 0 else 0
        table.add_row(
            row['buy_name'],
            f"{int(row['buy_amount'])}",
            f"{row['buy_price']:.2f}",
            f"{int(row['sell_amount'])}",
            f"{row['sell_price']:.2f}",
            f"{revenue_per_item:.2f}",
            f"{row['revenue']:.2f}"
        )

    console.print(table)




#-------------------------------------------------------------------------------------
def generate_profit_report(bought_data_file, sold_data_file):
    # Load bought data
    bought_data = pd.read_csv(bought_data_file)

    # Load sold data
    sold_data = pd.read_csv(sold_data_file) 
    
    merged_data = pd.merge(sold_data, bought_data, on='buy_name', how='left', suffixes=('_sell', '_buy'))
    
    # Explicitly create the buy_amount columns
    merged_data['buy_amount_buy'] = merged_data['buy_amount'].where(merged_data['buy_date'] <= merged_data['sell_date'], 0)
    merged_data['buy_amount_sell'] = merged_data['buy_amount'].where(merged_data['buy_date'] > merged_data['sell_date'], 0)
    
    # Calculate profit for each row
    merged_data['profit'] = merged_data.apply(lambda row: calculate_profit(row), axis=1)

    # Print merged data for debugging
    # print("Merged Data:")
    # print(merged_data)

    # Further debugging: Print column names in merged data
    # print("Column Names in Merged Data:")
    # print(merged_data.columns)

    # Update the aggregation logic based on the merged data
    report_data = merged_data.groupby(['buy_name', 'buy_id', 'buy_price']).agg({
        'sell_amount': 'first',
        'sell_price': 'first',
        'buy_amount_sell': 'sum',
        'buy_amount_buy': 'sum',
        'profit': 'sum',
        'expire_date': 'max'
    })

    # Reset index, dropping the existing 'buy_price' column
    report_data = report_data.reset_index()
    
    
    # Print the report data for debugging
    print("Report Data:")
    print(report_data)
# -------------------------------------------------------------------------------------

def calculate_profit(row):
    sell_amount = row['sell_amount']
    sell_price = row['sell_price']
    buy_price = row['buy_price']
    
    buy_amount_sell = row.get('buy_amount_sell', 0)
    buy_amount_buy = row.get('buy_amount_buy', 0)
    
    buy_amount = max(buy_amount_sell, buy_amount_buy)
    
    return sell_price - buy_price * buy_amount if sell_amount > 0 else 0

# -------------------------------------------------------------------------------------

def update_management_report(inventory_file, sold_file, management_report_file):
    # Load data
    inventory_data = pd.read_csv(inventory_file)
    sold_data = pd.read_csv(sold_file)

    # Merge data
    merged_data = pd.merge(sold_data, inventory_data, how='left', left_on='buy_name', right_on='buy_name')

    # Fill NaN values with 0
    merged_data.fillna(0, inplace=True)

    # Calculate profit
    merged_data['profit'] = merged_data['sell_amount'] * (merged_data['sell_price'] - merged_data['buy_price'])

    # Group by product and calculate totals
    grouped_data = merged_data.groupby('buy_name').agg(
        total_revenue=('sell_price', 'sum'),
        total_sell_amount=('sell_amount', 'sum'),
        buy_price=('buy_price', 'mean'),
        sell_price=('sell_price', 'mean'),
        profit=('profit', 'sum'),
        total_buy_amount=('buy_amount', 'sum'),
        total_expired_amount=('expire_date', lambda x: (x != '0').sum())
    ).reset_index()

    # Update the management report file
    grouped_data.to_csv(management_report_file, index=False)

    print("Management report updated.")


# ----------------------------------------------------------------------------------

def update_expired_items_in_management_report():
    # Load the inventory and sold data
    inventory_data = pd.read_csv(super_config.inventory_file)
    sold_data = pd.read_csv(super_config.sold_file)

    # Identify expired products
    expired_products = inventory_data[inventory_data['is_expired']]

    # Initialize a dictionary to store data for the management report
    report_data = {'buy_name': [],
                   'buy_amount': [],
                   'buy_price': [],
                   'sell_amount': [],
                   'sell_price': [],
                   'is_expired': [],
                   'revenue': [],
                   'profit': []}

    # Iterate through the expired products
    for index, product in expired_products.iterrows():
        buy_name = product['buy_name']
        buy_amount = product['buy_amount']
        buy_price = product['buy_price']
        sell_amount = 0  # No units sold for expired items
        sell_price = 0  # No revenue generated for expired items
        is_expired = True
        revenue = -buy_amount * buy_price  # Negative revenue for expired items
        profit = revenue  # Negative profit for expired items

        # Append the data to the report
        report_data['buy_name'].append(buy_name)
        report_data['buy_amount'].append(buy_amount)
        report_data['buy_price'].append(buy_price)
        report_data['sell_amount'].append(sell_amount)
        report_data['sell_price'].append(sell_price)
        report_data['is_expired'].append(is_expired)
        report_data['revenue'].append(revenue)
        report_data['profit'].append(profit)

    # Create a DataFrame from the report data
    report_df = pd.DataFrame(report_data)

    # Append the data to the management_report.csv file
    report_df.to_csv(super_config.management_report_file, mode='a', header=False, index=False)

    print("Expired items updated in the management report file.")
# -------------------------------------------------------------------------------------


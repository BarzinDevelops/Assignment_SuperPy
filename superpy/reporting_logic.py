# Import third party modules
from rich.table import Table
from rich.console import Console
from rich.style import Style
from rich import box
import pandas as pd
import numpy as np
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
def generate_revenue_report(management_report_file):
    # Load data from CSV files
    mangement_data = pd.read_csv(management_report_file)
    
    table = Table(title="Revenue Report", style='blue', box=box.ROUNDED)
    table.add_column("[bold purple]Product Name[/bold purple]", justify="left", style="bold", no_wrap=True)
    table.add_column("Sold Amount", justify="center", style="bold", no_wrap=True)
    table.add_column("Sold Price", justify="center", style="bold", no_wrap=True)
    table.add_column("Revenue", justify="center", style="bold", no_wrap=True)
    
    for _, row in mangement_data.iterrows():
        
        revenue =  row['sell_price'] * row['sell_amount']
        total_purchase_costs = row['buy_amount_buy'] * row['buy_price_buy']
        profit = revenue - total_purchase_costs  if (row['sell_amount'] > 0) and (row['expired_amount'] ) else 0
                
        if row['expired_amount'] <= 0:
            revenue =  row['sell_price'] * row['sell_amount']
            total_purchase_costs = row['buy_amount_buy'] * row['buy_price_buy']
            profit = revenue - total_purchase_costs if (row['sell_amount'] > 0) else 0
        
        else:
            expired_loss =  row['expired_amount'] * row['buy_price_buy']
            profit = profit - expired_loss

        table.add_row(
            row['buy_name_buy'],
            f"{row['sell_amount']:.2f}",
            f"{row['sell_price']:.2f}",
            f"{revenue:.2f}",
        )
    console.print(table) 
#-------------------------------------------------------------------------------------
def generate_profit_report(management_report_file):
    # Load data from CSV files
    mangement_data = pd.read_csv(management_report_file)
    
    
    # testing how to create pdf files for reporting:
    from reportlab.pdfgen.canvas import Canvas
    from reportlab.lib.pagesizes import A4
    from reportlab.platypus import Table as RLTable, TableStyle
    from reportlab.lib import colors
    
    pdf_filename = 'my_profit_report'
    pdf_file_name_and_path = f"outputs/PDF_reports/{pdf_filename}.pdf"
    pdf_canvas = Canvas(pdf_file_name_and_path, pagesize=A4)
    
    table_data = ["Product Name", "Buy Amount", "Buy Price", "Sold Amount", "Sold Price", "Total Purchasing Costs", "Revenue", "Expired Amount", "Profit/Loss"]
    
     # Create a ReportLab table
    pdf_table = RLTable(table_data)

    # Apply styles to the table
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.blue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
    ])

    pdf_table.setStyle(style)

    # Draw the table on the ReportLab canvas
    pdf_table.wrapOn(pdf_canvas, 0, 0)
    pdf_table.drawOn(pdf_canvas, 10, 600)

    # Save the canvas to the PDF file
    pdf_canvas.save()

    print(f"PDF report saved to: {pdf_file_name_and_path}")
   
    
    table = Table(title="Revenue Report", style='blue', box=box.ROUNDED)
    table.add_column("[bold purple]Product Name[/bold purple]", justify="left", style="bold", no_wrap=True)
    table.add_column("Buy Amount", justify="center", style="bold", no_wrap=True)
    table.add_column("Buy Price", justify="center", style="bold", no_wrap=True)
    table.add_column("Sold Amount", justify="center", style="bold", no_wrap=True)
    table.add_column("Sold Price", justify="center", style="bold", no_wrap=True)
    table.add_column("Total Purchasing Costs", justify="center", style="bold", no_wrap=True)
    table.add_column("Revenue", justify="center", style="bold", no_wrap=True)
    table.add_column("Expired Amount", justify="center", style="bold", no_wrap=True)
    table.add_column("[bold]Profit/Loss[/bold]", justify="center", style="bold", no_wrap=True)

    for _, row in mangement_data.iterrows():
        
        revenue =  row['sell_price'] * row['sell_amount']
        total_purchase_costs = row['buy_amount_buy'] * row['buy_price_buy']
        profit = revenue - total_purchase_costs  if (row['sell_amount'] > 0) and (row['expired_amount'] ) else 0
                
        if row['expired_amount'] <= 0:
            revenue =  row['sell_price'] * row['sell_amount']
            total_purchase_costs = row['buy_amount_buy'] * row['buy_price_buy']
            profit = revenue - total_purchase_costs if (row['sell_amount'] > 0) else 0
            profit_cell_color = 'blue'         
        else:
            expired_loss =  row['expired_amount'] * row['buy_price_buy']
            profit = profit - expired_loss
            profit_cell_color = 'red' if profit < 0 else 'green'
               
        
        table.add_row(
            row['buy_name_buy'],
            f"{int(row['buy_amount_buy'])}",
            f"{row['buy_price_buy']:.2f}",
            f"{row['sell_amount']:.2f}",
            f"{row['sell_price']:.2f}",
            f"{total_purchase_costs:.2f}",
            f"{revenue:.2f}",
            f"{row['expired_amount']}",
            f"[{profit_cell_color}]{profit:.2f}"
        )
    console.print(table) 
    
   
    
    # functions.generate_pdf_report(pdf_file_name_and_path)
# -------------------------------------------------------------------------------------

def update_management_report():
    # Read data from the CSV files
    bought_df = pd.read_csv(super_config.bought_file)
    inventory_df = pd.read_csv(super_config.inventory_file)
    sold_df = pd.read_csv(super_config.sold_file)

    # Merge 'bought_df' with 'inventory_df'
    management_data = pd.merge(bought_df, inventory_df, on='buy_id', how='inner', suffixes=('_buy', '_inventory'))

    # Merge the result with 'sold_df'
    management_data = pd.merge(management_data, sold_df, left_on='buy_name_buy', right_on='buy_name', how='left', suffixes=('_buy', '_sold'))

    # Calculate 'expired_amount' based on 'is_expired'
    management_data['expired_amount'] = management_data.apply(
        lambda row: row['buy_amount_inventory'] if row['is_expired'] else 0, axis=1
    )

    # Fill NaN values in 'sell_amount' and 'sell_price' with 0
    management_data[['sell_amount', 'sell_price']] = management_data[['sell_amount', 'sell_price']].fillna(0)

    # Select the desired columns
    management_data = management_data[['buy_name_buy', 'buy_amount_buy', 'buy_price_buy', 'sell_amount', 'sell_price', 'expired_amount']]

    # Save the result to 'management_report.csv'
    management_data.to_csv(super_config.management_report_file, index=False)



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


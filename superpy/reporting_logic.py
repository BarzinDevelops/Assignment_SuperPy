# Import third party modules
from rich.table import Table as rTable
from rich.console import Console
from rich.style import Style
from rich import box
import pandas as pd
import numpy as np

# Needed modules and functions for creating pdf files for reporting
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Frame
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import letter, inch

# Import local modules:
import functions
from config import SuperConfig

# ===============================================================================
console = Console()
super_config = SuperConfig()
# ===============================================================================

#==========================generating reports ======================================
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
        table = rTable(title="Inventory Report", style='white', box=box.ROUNDED)
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
    
    table = rTable(title="Revenue Report", style='blue', box=box.ROUNDED)
    table.add_column("[bold purple]Product Name[/bold purple]", justify="left", style="bold", no_wrap=True)
    table.add_column("Sold Amount", justify="center", style="bold", no_wrap=True)
    table.add_column("Sold Price", justify="center", style="bold", no_wrap=True)
    table.add_column("Revenue", justify="center", style="bold", no_wrap=True)
    
    for _, row in mangement_data.iterrows():
        
        revenue =  row['sell_price'] * row['sell_amount']
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
    
    table = rTable(title="Profit Report", style='blue', box=box.ROUNDED)
    table.add_column("[bold purple]Product Name[/bold purple]", justify="left", style="bold", no_wrap=True)
    table.add_column("Buy Amount", justify="center", style="bold", no_wrap=True)
    table.add_column("Buy Price", justify="center", style="bold", no_wrap=True)
    table.add_column("Sold Amount", justify="center", style="bold", no_wrap=True)
    table.add_column("Sold Price", justify="center", style="bold", no_wrap=True)
    table.add_column("Total Purchasing Costs", justify="center", style="bold", no_wrap=True)
    table.add_column("Revenue", justify="center", style="bold", no_wrap=True)
    table.add_column("Expired Amount", justify="center", style="bold", no_wrap=True)
    table.add_column("Total Expired Costs", justify="center", style="bold", no_wrap=True)
    table.add_column("[bold]Profit/Loss[/bold]", justify="center", style="bold", no_wrap=True)

    for _, row in mangement_data.iterrows():   
        profit = 0
        revenue =  row['sell_price'] * row['sell_amount']
        total_purchase_costs = row['buy_amount_buy'] * row['buy_price_buy']
        total_expired_costs = row['expired_amount'] * row['buy_price_buy']
        profit = revenue - total_purchase_costs - total_expired_costs      
        
        if profit == 0:
                profit_cell_color = 'blue'
        else:
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
            f"{total_expired_costs:.2f}",
            f"[{profit_cell_color}]{profit:.2f}"
        )
    console.print(table)     
# ---------------------------------------------------------------------#
def get_profit_color(profit_val, row_nr):       
        if profit_val == 0:
            return ('TEXTCOLOR', (-1, row_nr), (-1, -1), colors.blue),
        elif profit_val < 0:
            return ('TEXTCOLOR', (-1, row_nr), (-1, -1), colors.red),
        else:
            return ('TEXTCOLOR', (-1, row_nr), (-1, -1), colors.green),
# ---------------------------------------------------------------------#
def generate_pdf_report():
    data = pd.read_csv(super_config.management_report_file)

    new_data = [["Product Name", "Buy Amount", "Buy Price", "Total Buy Costs", "Sell Amount", "Sell Price", "Revenue", "Expired Amount", "Profit"]]

    for _, row in data.iterrows():
        profit = 0
        revenue =  row['sell_price'] * row['sell_amount']
        total_purchase_costs = row['buy_amount_buy'] * row['buy_price_buy']
        total_expired_costs = row['expired_amount'] * row['buy_price_buy']
        profit = revenue - total_purchase_costs - total_expired_costs     

        new_data.append([
            row['buy_name_buy'],
            f"{int(row['buy_amount_buy'])}",
            f"{row['buy_price_buy']:.2f}",
            f"{total_purchase_costs:.2f}",
            f"{row['sell_amount']:.2f}",
            f"{row['sell_price']:.2f}",
            f"{revenue:.2f}",
            f"{row['expired_amount']}",
            f"{profit:.2f}"
        ])

    # Convert the list to a DataFrame
    new_data_df = pd.DataFrame(new_data[1:], columns=new_data[0])

    # Set up PDF document
    extension = '.pdf'
    file_path = f"outputs/PDF_reports/management_report{extension}"

    # Create the SimpleDocTemplate with the frame
    doc = SimpleDocTemplate(file_path, pagesize=landscape(A4))

    # Create a list to hold the content of the PDF
    content = []
    styles = getSampleStyleSheet()

    # Add additional text
    text_to_write = """This is my report of all the bought and sold products. Also, it shows how much revenue each product has made and if any of it was expired. Based on those info, it then calculates the total profit of that product."""

    text_to_write_style = styles['Normal']
    # Modify properties
    text_to_write_style.fontName = 'Helvetica'
    text_to_write_style.fontSize = 14
    text_to_write_style.leading = 14
    text_to_write_style.spaceBefore = 20
    text_to_write_style.spaceAfter = 15
    text_to_write_style.leftIndent = 20
    text_to_write_style.rightIndent = 20
    text_to_write_style.firstLineIndent = 0
    text_to_write_style.textColor = colors.navy
    text_to_write_style.alignment = 0  # 0 for left, 1 for center, 2 for right, 3 for justify

    # Add a title with a different color
    title_style = ParagraphStyle(
        'Title',
        parent=getSampleStyleSheet()['Title'],
        textColor=colors.blueviolet
    )
    title = Paragraph("Management Report", title_style)
    content.append(title)

    # Add the modified text to the content
    content.append(Paragraph(text_to_write, text_to_write_style))

    # Create a ReportLab table
    pdf_table = Table([list(new_data_df.columns)] + new_data_df.values.tolist())
                   
    # Apply styles to the table
    style = [
        ('BACKGROUND', (0, 0), (-1, 0), colors.navy),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),  # Text color for the header row
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 5),
        ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),  # Text color for data rows
        ('TEXTCOLOR', (-1, 1), (-1, -1), colors.purple),  # Text color for data rows
    ]
    
    # Define styles for each row based on the 'Profit' column
    extra_style = []
    for k, profit_val in new_data_df['Profit'].items():   
        extra_style.append(get_profit_color(float(profit_val), k+1))
    
    style.extend(list(i[0] for i in extra_style))

    # Apply the modified style to the table
    pdf_table.setStyle(style)  

    # Add the table to the content
    content.append(pdf_table)

    # Build the PDF document
    doc.build(content)
# -------------------------------------------------------------------------------------

def update_management_report():
    # Read data from the CSV files
    bought_df = pd.read_csv(super_config.bought_file)
    inventory_df = pd.read_csv(super_config.inventory_file)
    sold_df = pd.read_csv(super_config.sold_file)

    # Merge bought_df and inventory_df on 'buy_id'
    bought_and_inventory = pd.merge(
        bought_df, inventory_df,
        left_on=['buy_id'],
        right_on=['buy_id'],
        how='left', suffixes=('_buy', '_inventory')
    )

    # Create a DataFrame for 'expired_amount' based on 'is_expired' column
    expired_amount_df = bought_and_inventory[bought_and_inventory['is_expired'].fillna(False)].groupby(['buy_name_buy', 'buy_price_buy']).agg({'buy_amount_buy': 'sum'}).reset_index()
    expired_amount_df.rename(columns={'buy_amount_buy': 'expired_amount'}, inplace=True)

    # Create a DataFrame for 'buy_amount_buy'
    buy_amount_df = bought_and_inventory.groupby(['buy_name_buy', 'buy_price_buy']).agg({'buy_amount_buy': 'sum'}).reset_index()

    # Create a DataFrame for 'sell_amount' and 'sell_price'
    sell_df = sold_df.groupby(['buy_name']).agg({'sell_amount': 'sum', 'sell_price': 'sum'}).reset_index()

    # Merge the DataFrames
    profit_report = pd.merge(buy_amount_df, sell_df, left_on=['buy_name_buy'], right_on=['buy_name'], how='left')
    profit_report = pd.merge(profit_report, expired_amount_df, on=['buy_name_buy', 'buy_price_buy'], how='left')

    # Fill NaN values in 'sell_amount', 'sell_price', and 'expired_amount' columns with 0
    profit_report['sell_amount'].fillna(0, inplace=True)
    profit_report['sell_price'].fillna(0, inplace=True)
    profit_report['expired_amount'].fillna(0, inplace=True)

    # Group by relevant columns and sum 'sell_amount', 'sell_price'
    group_columns = ['buy_name_buy', 'buy_price_buy']
    profit_report = profit_report.groupby(group_columns).agg({
        'buy_amount_buy': 'sum',
        'sell_amount': 'sum',
        'sell_price': 'sum',
        'expired_amount': 'sum',
    }).reset_index()

    # Save the updated report to a new CSV file
    profit_report.to_csv(super_config.management_report_file, index=False,
                         columns=['buy_name_buy', 'buy_amount_buy', 'buy_price_buy', 'sell_amount', 'sell_price', 'expired_amount'])

# ----------------------------------------------------------------------------------

def update_expired_items_in_management_report():
    # Load the inventory and sold data
    inventory_data = pd.read_csv(super_config.inventory_file)

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


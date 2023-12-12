

<hr style='border-width: 4px; border-color: orange;'>
<p align='center' style='font-size: 34px; color: orange; text-decoration: none; border: none; padding: 0; margin-bottom: 0'>Supermarket Inventory Tool User Guide</p>
<hr style='border-width: 4px; border-color: orange; margin-bottom: 30px'>


<h1 style="color: darkred; text-decoration: none; border: none; padding: 0; '">Overview</h1>
The Supermarket Inventory Tool is a command-line application that helps you manage and analyze your supermarket inventory. This tool supports actions like buying products, selling products, advancing time, and generating various reports such as inventory, revenue, profit, and expired products.

<h1 style="color: purple; text-decoration: none; border: none; padding: 0;  margin-top: 30px">Usage</h1>


### Installation
Before running the Supermarket Inventory Tool, make sure you have Python installed on your system. Additionally, install the required dependencies by running:

```bash
pip install -r requirements.txt
```

### Running the Tool

To run the Supermarket Inventory Tool, use the following command:

Replace `<action>` with the desired action (`buy`, `sell`, `time`, `report`), and provide appropriate `<arguments>` based on the chosen action.

<hr style='border-width: 4px; border-color: green; margin-top: 30px'>
<h1 style="color: green; text-decoration: none; border: none; padding: 0; margin: 0'">Actions</h1>
<hr style='border-width: 4px; border-color: green; margin-bottom: 30px'>

### **1.Buy**

Use the <big>**`buy`**</big> action to purchase products and add them to the inventory. Provide the following arguments:

```bash
python super.py buy <buy_name> <buy_amount> <buy_price> <expire_date>
```

- **\<buy_name\>**: Specify the name of the product.
- **\<buy_amount\>**: Specify the amount of the product you want.
- **\<buy_price\>**: Specify the price of the product.
- **\<expire_date\>**: Provide the expiration date in the format 'year-month-day'.


Example:

```bash
super.py buy "Product Name" 10 5.99 2023-12-31 
```
### **2. Sell**
Use the <big>**`sell`**</big> action to sell products and update the inventory. Provide the following arguments:

```bash
super.py sell <buy_name> <sell_amount> <sell_price>
```


### **2. Time**
Use the <big>**`time`**</big> action to advance the current date in the application. Provide the following argument:


```bash
super.py time <advance_time>
```
**\<advance_time\>**: Advance the current date by a specified number of days.

Example:

```bash 
python super.py time 7 
```

### **4. Report**
Use the <big>**`report`**</big> action to generate various reports. Provide the following arguments:


```bash
python super.py report <report_type>
```
**\<report_type\>**: Choose the type of report ['inventory', 'revenue', 'profit', or 'expired'].

Example:

```bash 
python super.py report inventory
```

<hr style='border-width: 4px; border-color: blue; margin-top: 30px'>
<h1 style="color: blue; text-decoration: none; border: none; padding: 0; margin: 0'">Reports</h1>
<hr style='border-width: 4px; border-color: blue; margin-bottom: 30px'>

### **1. Inventory Report**
Generate an inventory report to view the current state of your inventory.

```bash 
python super.py report inventory
```
### **2. Revenue Report**
Generate a revenue report to analyze the revenue from product sales.

```bash 
python super.py report revenue
```
### **3. Profit Report**
Generate a profit report to analyze the profit from product sales.

```bash 
python super.py report profit
```
### **4. Expired Products Report**
Generate a report to identify and manage expired products in your inventory.

```bash 
python super.py report expired
```


<hr style='border-width: 4px; border-color: magenta; margin-top: 30px'>
<h1 style="color: magenta; text-decoration: none; border: none; padding: 0; margin: 0'">Notes</h1>
<hr style='border-width: 4px; border-color: magenta; margin-bottom: 30px'>

- Ensure that the date in the **'time.txt'** file is updated after using the **'time'** action.
- Reports are automatically updated in the **'outputs'** folder.



<hr style='border-width: 4px; border-color: saddlebrown; margin-top: 30px'>
<h1 style="color: saddlebrown; text-decoration: none; border: none; padding: 0; margin: 0'">Examples</h1>
<hr style='border-width: 4px; border-color: saddlebrown; margin-bottom: 30px'>

### **1. Buy Example**
```bash 
python super.py buy "Product Name" 10 5.99 2023-12-31
```
### **2. Sell Example**
```bash 
python super.py buy "Product Name" 10 5.99 2023-12-31
```
### **3. Time Example**
```bash 
python super.py time 7
```
### **4. Report Example**
```bash 
python super.py report inventory
```


<hr style='border-width: 4px; border-color: deeppink; margin-top: 30px'>
<h1 style="color: deeppink; text-decoration: none; border: none; padding: 0; margin: 0'">Troubleshooting</h1>
<hr style='border-width: 4px; border-color: deeppink; margin-bottom: 30px'>

- If you encounter any issues, ensure that you have the required dependencies installed and that your Python environment is properly set up.
- Double-check the command syntax and provided arguments.
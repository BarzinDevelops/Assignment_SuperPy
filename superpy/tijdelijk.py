# Process sales and update inventory_df
    for _, sold_row in sold_df.iterrows():
        product_name = sold_row['buy_name']
        sell_amount = sold_row['sell_amount']

        # Filter matching rows based on product name and not expired
        matching_rows = inventory_df[(inventory_df['buy_name'] == product_name) & 
                                     (inventory_df['is_expired'] == False)]

        # Iterate through matching rows
        for _, row in matching_rows.iterrows():
            available_amount = row['buy_amount']

            # If available amount is greater than or equal to sell amount, update and break
            if available_amount >= sell_amount:
                inventory_df.loc[row.name, 'buy_amount'] -= sell_amount
                break
            else:
                # If available amount is less than sell amount, update and continue to next row
                inventory_df.loc[row.name, 'buy_amount'] = 0
                sell_amount -= available_amount
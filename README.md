# Assignment_SuperPy
WINC Assignment


Todos:
done -  Add function 'get_current_date()' to each sell/buy item (when getting created)
done -  Add function 'advance_time(number)', which adds the number of days that users 
        passes as argument (number), to the date in time.txt file.
done -  Create function that resets the date in time.txt back to determined date:       
        2023-01-01 as symbolic date for current day in this application.
done -  Create function: 'update_inventory()'. It takes filename to read the data from 
        the given argument and use it to update it's records.
done -  Add expiredate (from buy.csv) to inventory (actually each bought item needs to 
        be saved to inventory.csv)
done - Add function(s) that checks the last date the code has run and compares with today.
        if they are equal than the application date won't reset to (2023-07-01)
        if they arn't equal, this means that the code has'nt run today, and the application date
        will be reset to (2023-07-01). This way the application date will always start at (2023-07-01) 
        when the application is run for the first time on each new day.
-       if an item is sold, then the inventory.csv needs to be checked first to see:
            * if the item is still available -> 
                - if yes, then check how many (use amount field) you can sell
                - if not, let the user know that this item is not available anymore
            * if the item expire date exeeded get a message? (use date from time.txt and expiredate of inventory.csv) or make a function that does this!
            if the item can be sold, then the inventory.csv needs to be updated (for example: if 2 of 4 apples sold-> then inventory needs to have 2 apples left)
-       Find out how to adjust id's in buy/sell records that can be obtained whe items get deleted (so 
            * if id 2 is deleted -> the next added wont get id 2 but id 3)



$ python main.py buy --product-name orange --price 0.8 --expiration-date 2020-01-01
OK

$ python main.py report inventory --now
+--------------+-------+-----------+-----------------+
| Product Name | Count | Buy Price | Expiration Date |
+==============+=======+===========+=================+
| Orange       | 1     | 0.8       | 2020-01-01      |
+--------------+-------+-----------+-----------------+

$ python main.py --advance-time 2
OK

$ python main.py report inventory --yesterday
+--------------+-------+-----------+-----------------+
| Product Name | Count | Buy Price | Expiration Date |
+==============+=======+===========+=================+
| Orange       | 1     | 0.8       | 2020-01-01      |
+--------------+-------+-----------+-----------------+

$ python main.py sell --product-name orange --price 2
OK

$ python main.py report inventory --now
+--------------+-------+-----------+-----------------+
| Product Name | Count | Buy Price | Expiration Date |
+==============+=======+===========+=================+


$ python main.py report revenue --yesterday
Yesterday's revenue: 0

$ python main.py report revenue --today
Today's revenue so far: 2

$ python main.py report revenue --date 2019-12
Revenue from December 2019: 0

$ python main.py report profit --today
1.2

$ python main.py sell --product-name orange --price 2
ERROR: Product not in stock.
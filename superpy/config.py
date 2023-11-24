# config.py
import os
class SuperConfig:
    def __init__(self, outputs_dir='outputs'):
        self.outputs_dir = outputs_dir
        self.bought_file = os.path.join(self.outputs_dir, 'bought.csv')
        self.sold_file = os.path.join(self.outputs_dir, 'sold.csv')
        self.inventory_file = os.path.join(self.outputs_dir, 'inventory.csv')
        self.management_report_file = os.path.join(self.outputs_dir, 'management_report.csv')

        

# Instantiate the config if the script is run directly
if __name__ == "__main__":
    super_config = SuperConfig()
    

import pandas as pd

# Load dataset
file_path = "analyzed_supply_chain_data.csv"
data = pd.read_csv(file_path)


# Inventory Management System with enhanced risk alerts
class InventoryManagementSystem:
    def __init__(self, regions, default_warehouse_size):
        self.regions = regions
        self.default_warehouse_size = default_warehouse_size
        self.inventory = {
            region: {
                'warehouse_size': default_warehouse_size,
                'available_space': default_warehouse_size,
                'materials': [],
                'total_cost': 0
            }
            for region in regions
        }

    def monthly_incoming(self):
        """
        Handle the stocking of materials (incoming supplies from suppliers).
        """
        region = input("Enter region name: ")
        if region not in self.inventory:
            print(f"Region '{region}' not found.")
            return

        material_name = input("Enter material name: ")
        size = float(input("Enter material size (in cubic meters): "))
        cost = float(input("Enter material cost: "))

        if size > self.inventory[region]['available_space']:
            print(f"Not enough space in the warehouse for region '{region}'. Risk: Stock Overflow.")
            return

        self.inventory[region]['materials'].append({'name': material_name, 'size': size, 'cost': cost})
        self.inventory[region]['available_space'] -= size
        self.inventory[region]['total_cost'] += cost
        print(f"Stocked up {material_name} in {region}. Available space: {self.inventory[region]['available_space']}.")

    def monthly_outgoing(self):
        """
        Handle the supply of materials (outgoing supplies to customers).
        """
        region = input("Enter region name: ")
        if region not in self.inventory:
            print(f"Region '{region}' not found.")
            return

        material_name = input("Enter material name to supply: ")
        material_found = False
        for material in self.inventory[region]['materials']:
            if material['name'] == material_name:
                self.inventory[region]['available_space'] += material['size']
                self.inventory[region]['total_cost'] -= material['cost']
                self.inventory[region]['materials'].remove(material)
                material_found = True
                print(
                    f"Supplied {material_name} from {region}. Available space: {self.inventory[region]['available_space']}."
                )
                break

        if not material_found:
            print(f"Material '{material_name}' not found in region '{region}'.")

    def display_inventory(self):
        """
        Display the current inventory status for a specific region.
        """
        region = input("Enter the region name to display inventory: ")
        if region not in self.inventory:
            print(f"Region '{region}' not found.")
            return

        print(f"Region: {region}")
        print(f"  Warehouse Size: {self.inventory[region]['warehouse_size']} cubic meters")
        print(f"  Available Space: {self.inventory[region]['available_space']} cubic meters")
        print(f"  Materials:")
        for material in self.inventory[region]['materials']:
            print(f"    - {material['name']}: Size={material['size']} cubic meters, Cost=${material['cost']}")
        print(f"  Total Cost of Materials: ${self.inventory[region]['total_cost']}")
        print("-" * 40)

    def generate_risk_alerts(self):
        """
        Generate alerts for supply chain risks based on sentiment scores and warehouse capacity.
        """
        print("Generating Risk Alerts:")
        for _, row in data.iterrows():
            region = row['Region']
            sentiment_score = row['Sentiment Score']
            comment = row['Comment']
            available_space = self.inventory[region]['available_space']
            warehouse_size = self.inventory[region]['warehouse_size']

            print(f"  Region: {region}")
            print(f"    Sentiment Score: {sentiment_score}")
            print(f"    Comment: {comment}")

            # Generate sentiment-based risk alerts
            if sentiment_score < 0.50:
                print("    🚨 Alert: High risk of supply chain disruption!")
            elif 0.50 <= sentiment_score <= 0.52:
                print("    ⚠️ Warning: Moderate risk. Closely monitor the situation.")
            else:
                print("    ✅ Status: Low risk.")

            # Generate warehouse capacity-based alerts
            if available_space <= 0.1 * warehouse_size and available_space > 0:
                print(f"    ⚠️ Alert: Stock Shortage! Critical space available in {region}.")
            elif available_space == 0:
                print(f"    🚨 Alert: High Risk! Warehouse in {region} is empty. Immediate restocking required.")
            elif available_space < 0:
                print(f"    ⚠️ Alert: Stock Overflow! Exceeded space capacity in {region}.")
            elif available_space == warehouse_size:
                print(f"    ⚠️ Risk: Empty warehouse in {region}. No stock available!")

            print("-" * 40)

    def save_inventory_to_csv(self):
        """
        Save the current inventory status to a CSV file.
        """
        inventory_data = []
        for region, details in self.inventory.items():
            for material in details['materials']:
                inventory_data.append({
                    'Region': region,
                    'Material Name': material['name'],
                    'Size (cubic meters)': material['size'],
                    'Cost ($)': material['cost'],
                    'Available Space (cubic meters)': details['available_space'],
                    'Total Cost ($)': details['total_cost']
                })

        df = pd.DataFrame(inventory_data)
        df.to_csv('inventory_status.csv', index=False)
        print("Inventory saved to 'inventory_status.csv'.")


# Example Usage
regions = data['Region'].unique()  # Extract regions from dataset
ims = InventoryManagementSystem(regions=regions, default_warehouse_size=1000)

while True:
    print("\n1. Monthly incoming")
    print("2. Monthly outgoing")
    print("3. Display inventory")
    print("4. Generate risk alerts")
    print("5. Save and Exit")

    choice = input("Enter your choice: ")

    if choice == '1':
        ims.monthly_incoming()
    elif choice == '2':
        ims.monthly_outgoing()
    elif choice == '3':
        ims.display_inventory()
    elif choice == '4':
        ims.generate_risk_alerts()
    elif choice == '5':
        ims.save_inventory_to_csv()
        print("Exiting the system.")
        break
    else:
        print("Invalid choice. Please try again.")

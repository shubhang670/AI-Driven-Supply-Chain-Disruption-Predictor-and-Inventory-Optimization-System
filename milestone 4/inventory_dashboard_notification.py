import pandas as pd
import requests
import streamlit as st

# Load dataset
file_path = "analyzed_supply_chain_data.csv"
data = pd.read_csv(file_path)


# Inventory Management System with enhanced risk alerts
class InventoryManagementSystem:
    def __init__(self, regions, default_warehouse_size, slack_webhook_url):
        self.regions = regions
        self.default_warehouse_size = default_warehouse_size
        self.slack_webhook_url = slack_webhook_url  # Slack webhook URL
        self.inventory = {
            region: {
                'warehouse_size': default_warehouse_size,
                'available_space': default_warehouse_size,
                'materials': [],
                'total_cost': 0
            }
            for region in regions
        }

    def send_slack_notification(self, message):
        """
        Sends a message to Slack using the webhook URL.
        """
        payload = {
            "text": message
        }
        response = requests.post(self.slack_webhook_url, json=payload)

        if response.status_code == 200:
            st.success("Slack notification sent successfully.")
        else:
            st.error(f"Failed to send Slack notification. Status code: {response.status_code}")

    def monthly_incoming(self, region, material_name, size, cost):
        """
        Handle the stocking of materials (incoming supplies from suppliers).
        """
        if region not in self.inventory:
            st.error(f"Region '{region}' not found.")
            return

        if size > self.inventory[region]['available_space']:
            st.warning(f"Not enough space in the warehouse for region '{region}'. Risk: Stock Overflow.")
            return

        self.inventory[region]['materials'].append({'name': material_name, 'size': size, 'cost': cost})
        self.inventory[region]['available_space'] -= size
        self.inventory[region]['total_cost'] += cost
        st.success(
            f"Stocked up {material_name} in {region}. Available space: {self.inventory[region]['available_space']}.")

    def monthly_outgoing(self, region, material_name):
        """
        Handle the supply of materials (outgoing supplies to customers).
        """
        if region not in self.inventory:
            st.error(f"Region '{region}' not found.")
            return

        material_found = False
        for material in self.inventory[region]['materials']:
            if material['name'] == material_name:
                self.inventory[region]['available_space'] += material['size']
                self.inventory[region]['total_cost'] -= material['cost']
                self.inventory[region]['materials'].remove(material)
                material_found = True
                st.success(
                    f"Supplied {material_name} from {region}. Available space: {self.inventory[region]['available_space']}.")
                break

        if not material_found:
            st.error(f"Material '{material_name}' not found in region '{region}'.")

    def display_inventory(self, region):
        """
        Display the current inventory status for a specific region.
        """
        if region not in self.inventory:
            st.error(f"Region '{region}' not found.")
            return

        st.write(f"### Region: {region}")
        st.write(f"  Warehouse Size: {self.inventory[region]['warehouse_size']} cubic meters")
        st.write(f"  Available Space: {self.inventory[region]['available_space']} cubic meters")
        st.write(f"  Materials:")
        for material in self.inventory[region]['materials']:
            st.write(f"    - {material['name']}: Size={material['size']} cubic meters, Cost=${material['cost']}")
        st.write(f"  Total Cost of Materials: ${self.inventory[region]['total_cost']}")
        st.write("-" * 40)

    def generate_risk_alerts(self, region_filter=None, month_filter=None):
        """
        Generate alerts for supply chain risks based on sentiment scores and warehouse capacity.
        Filters can be applied for specific regions and months.
        """
        st.write("### Generating Risk Alerts:")
        for _, row in data.iterrows():
            region = row['Region']
            month = row['Month']
            sentiment_score = row['Sentiment Score']
            comment = row['Comment']
            available_space = self.inventory[region]['available_space']
            warehouse_size = self.inventory[region]['warehouse_size']

            # Apply region and month filters if provided
            if (region_filter and region != region_filter) or (month_filter and month != month_filter):
                continue

            alert_message = f"Region: {region}\nMonth: {month}\nSentiment Score: {sentiment_score}\nComment: {comment}\n"

            # Generate sentiment-based risk alerts
            if sentiment_score < 0.50:
                alert_message += "🚨 Alert: High risk of supply chain disruption!"
            elif 0.50 <= sentiment_score <= 0.52:
                alert_message += "⚠️ Warning: Moderate risk. Closely monitor the situation."
            else:
                alert_message += "✅ Status: Low risk."

            # Generate warehouse capacity-based alerts
            if available_space <= 0.1 * warehouse_size and available_space > 0:
                alert_message += f"\n⚠️ Alert: Stock Shortage! Critical space available in {region}."
            elif available_space == 0:
                alert_message += f"\n🚨 Alert: High Risk! Warehouse in {region} is empty. Immediate restocking required."
            elif available_space < 0:
                alert_message += f"\n⚠️ Alert: Stock Overflow! Exceeded space capacity in {region}."
            elif available_space == warehouse_size:
                alert_message += f"\n⚠️ Risk: Empty warehouse in {region}. No stock available!"

            # Send the alert to Slack
            self.send_slack_notification(alert_message)

            st.write("-" * 40)

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
        st.success("Inventory saved to 'inventory_status.csv'.")


# Streamlit App

slack_webhook_url = "https://hooks.slack.com/services/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"  # Your Slack webhook URL
regions = data['Region'].unique()  # Extract regions from dataset
ims = InventoryManagementSystem(regions=regions, default_warehouse_size=1000, slack_webhook_url=slack_webhook_url)

st.title("Inventory Management System")

# Select Region
region = st.selectbox("Select Region", regions)

# Actions
action = st.selectbox("Select Action",
                      ["Monthly Incoming", "Monthly Outgoing", "Display Inventory", "Generate Risk Alerts",
                       "Save and Exit"])

if action == "Monthly Incoming":
    material_name = st.text_input("Material Name")
    size = st.number_input("Material Size (in cubic meters)", min_value=0.0)
    cost = st.number_input("Material Cost", min_value=0.0)

    if st.button("Submit Incoming Stock"):
        ims.monthly_incoming(region, material_name, size, cost)

elif action == "Monthly Outgoing":
    material_name = st.text_input("Material Name to Supply")

    if st.button("Submit Outgoing Stock"):
        ims.monthly_outgoing(region, material_name)

elif action == "Display Inventory":
    ims.display_inventory(region)

elif action == "Generate Risk Alerts":
    region_filter = st.text_input("Region Filter (optional)")
    month_filter = st.text_input("Month Filter (optional)")

    if st.button("Generate Alerts"):
        ims.generate_risk_alerts(region_filter=region_filter, month_filter=month_filter)

elif action == "Save and Exit":
    ims.save_inventory_to_csv()
    st.success("Exiting the system.")


import pandas as pd

def analyze_tea_supply_data(file_path):
    # Load the CSV data
    data = pd.read_csv(file_path)

    # Define thresholds and conditions
    high_risk_threshold = "High"  # Risk levels: Low, Medium, High
    negative_sentiment = "Negative"  # Sentiment: Positive, Neutral, Negative

    alerts = []

    for index, row in data.iterrows():
        # Calculate supply-demand ratio
        supply_demand_ratio = row['Tea Supply (tons)'] / row['Tea Demand (tons)']

        # Analyze conditions
        if supply_demand_ratio < 0.8:  # Supply is significantly lower than demand
            action = "Increase Supply"
            reason = f"Low supply ({supply_demand_ratio:.2f}), demand exceeds supply."
        elif supply_demand_ratio > 1.2:  # Supply significantly exceeds demand
            action = "Reduce Supply"
            reason = f"High supply ({supply_demand_ratio:.2f}), oversupply risk."
        else:
            action = "Monitor"
            reason = f"Balanced supply-demand ({supply_demand_ratio:.2f})."

        # Check risk and sentiment for additional alerts
        if row['Risk Analysis'] == high_risk_threshold or row['Sentiment'] == negative_sentiment:
            action = "Critical Attention"
            reason = f"{row['Risk Analysis']} risk with {row['Sentiment']} sentiment."

        # Append alert
        alerts.append({
            "Region": row['Region'],
            "Month": row['Month'],
            "Year": row['Year'],
            "Action": action,
            "Reason": reason
        })

    # Convert alerts to a DataFrame and save to CSV
    alerts_df = pd.DataFrame(alerts)
    alerts_df.to_csv("modified sample code.csv", index=False)

    return alerts_df

# Analyze the dataset
file_path = "moddddddd.csv"  # Path to your dataset
alerts_df = analyze_tea_supply_data(file_path)

# Print the first few rows of the saved data for confirmation
print(alerts_df.head())

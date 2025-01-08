import pandas as pd
from transformers import pipeline

# Load the dataset
file_path = "tea_supply_chain_with_full_comments.csv"  
data = pd.read_csv(file_path)

# Initialize DistilBERT for sentiment analysis
sentiment_pipeline = pipeline("sentiment-analysis", model="distilbert-base-uncased")

# Function for detailed risk analysis
def analyze_risk(comment):
    comment_lower = comment.lower()
    if "flood" in comment_lower or "flooding" in comment_lower:
        return "Road blockages due to flooding."
    elif "weather" in comment_lower or "adverse" in comment_lower:
        return "Adverse weather conditions affecting supply."
    elif "customs" in comment_lower or "clearance" in comment_lower:
        return "Delays due to customs clearance issues."
    elif "rush" in comment_lower or "port" in comment_lower:
        return "Port congestion causing delays."
    elif "blockage" in comment_lower or "road" in comment_lower:
        return "Supply disrupted due to road blockages."
    else:
        return "No significant risk detected."


# Perform risk and sentiment analysis
def perform_analysis(data):
    results = []
    for _, row in data.iterrows():
        comment = row['Comment']
        sentiment = sentiment_pipeline(comment)[0]
        risk = analyze_risk(comment)

        results.append({
            "Region": row['Region'],
            "Month": row['Month'],
            "Year": row['Year'],
            "Comment": comment,
            "Sentiment": sentiment['label'],
            "Sentiment Score": sentiment['score'],
            "Risk Analysis": risk
        })

    return pd.DataFrame(results)

# Main function
def main():
    analyzed_data = perform_analysis(data)
    output_file = "analyzed_supply_chain_data.csv"
    analyzed_data.to_csv(output_file, index=False)
    print(f"Analysis complete. Results saved to {output_file}")
    print("\nSample Output:\n", analyzed_data.head())

if __name__ == "__main__":
    main()

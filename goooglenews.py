import requests
import pandas as pd

# Your API key
api_key = '35d0deb2fab14c229b05b30711044644'

# Base URL for Google News API
base_url = 'https://newsapi.org/v2/everything'

# Query parameters
query = 'supply chain'
page_size = 100  # Max articles to fetch in one request (API limit)
params = {
    'q': query,
    'apiKey': api_key,
    'pageSize': page_size,  # Number of articles to fetch
    'language': 'en',  # Fetch articles in English
}

# Fetch data
response = requests.get(base_url, params=params)

# Check if the request was successful
if response.status_code == 200:
    data = response.json()
    if 'articles' in data:
        articles = data['articles']
        
        # Process articles into a DataFrame
        articles_data = [
            {
                'Title': article.get('title', 'N/A'),
                'Description': article.get('description', 'N/A'),
                'URL': article.get('url', 'N/A'),
                'Published At': article.get('publishedAt', 'N/A'),
                'Source': article.get('source', {}).get('name', 'N/A'),
            }
            for article in articles
        ]
        articles_df = pd.DataFrame(articles_data)
        
        # Save the DataFrame to a CSV file
        csv_file = 'data.csv'
        articles_df.to_csv(csv_file, index=False)
        print(f"Saved {len(articles)} articles to {csv_file}")
    else:
        print("No articles found in the response.")
else:
    print(f"Error: Unable to fetch articles. Status code: {response.status_code}")

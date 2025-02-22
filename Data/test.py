import json
import requests
import time

json_file_path = "/Users/aviralbansal/Library/CloudStorage/OneDrive-ThePennsylvaniaStateUniversity/hackalytics25/golden_apple/Data/iphone_links.json"  # Updated to use relative path
    
    # Load iPhone links from JSON file
try:
    with open(json_file_path, "r") as f:
        iphone_links = json.load(f)
except FileNotFoundError:
        print(f"Error: Could not find {json_file_path}")
    

except json.JSONDecodeError:
    print(f"Error: Invalid JSON in {json_file_path}")
    
all_models_data = {}
    
session = requests.Session()
session.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
    })
    
for model_name, product_url in iphone_links.items():
    print(f"\nProcessing: {model_name}")
        
        # Convert to price-history URL - fixed URL transformation
    price_history_url = product_url


try:
            # Add delay to avoid rate limiting
            time.sleep(2)
            
            response = session.get(price_history_url)
            response.raise_for_status()
            
            # Debug: Save HTML for inspection
            with open(f"debug_{model_name}.html", "w", encoding="utf-8") as f:
                f.write(response.text)
            
            # Extract price history data
            #price_data = extract_price_data(response.text)
            
            #if price_data:
                all_models_data[model_name] = price_data
                print(f"Successfully extracted data for {model_name}")
            #else:
                print(f"No price data found for {model_name}")
                
except requests.exceptions.RequestException as e:
            print(f"Error fetching {price_history_url}: {e}")
            
import requests
from bs4 import BeautifulSoup
import json
import re
from datetime import datetime
import time

def extract_price_data(html):
    """
    Extracts price history from the JavaScript 'datasets' variable in the page source.
    Returns a dictionary where keys are 'Month Year' and values are { new: price, used: price }.
    """
    soup = BeautifulSoup(html, 'html.parser')
    
    # Look for script tags containing price data
    scripts = soup.find_all("script")
    
    for script in scripts:
        if not script.string:
            continue
            
        # Try different regex patterns to match the data
        patterns = [
            r"var\s+datasets\s*=\s*(\[[\s\S]+?\]);",
            r"datasets\s*=\s*(\[[\s\S]+?\])",
            r"data:\s*(\[[\s\S]+?\])"
        ]
        
        for pattern in patterns:
            match = re.search(pattern, script.string, re.DOTALL)
            if match:
                try:
                    # Clean the JSON string before parsing
                    json_str = match.group(1)
                    # Remove any JavaScript comments
                    json_str = re.sub(r'//.*?\n|/\*.*?\*/', '', json_str)
                    # Handle trailing commas
                    json_str = re.sub(r',(\s*[\]}])', r'\1', json_str)
                    
                    datasets = json.loads(json_str)
                    
                    price_history = {}
                    
                    for dataset in datasets:
                        if not isinstance(dataset, dict):
                            continue
                            
                        label = dataset.get("label", "").lower()
                        data = dataset.get("data", [])
                        
                        if not data or not isinstance(data, list):
                            continue
                        
                        is_new = "new" in label
                        is_used = "used" in label
                        
                        for entry in data:
                            if not isinstance(entry, dict):
                                continue
                                
                            try:
                                timestamp = int(entry["x"]) // 1000
                                price = float(entry["y"])
                                
                                month_year = datetime.utcfromtimestamp(timestamp).strftime("%b %Y")
                                
                                if month_year not in price_history:
                                    price_history[month_year] = {"new": None, "used": None}
                                    
                                if is_new:
                                    price_history[month_year]["new"] = price
                                elif is_used:
                                    price_history[month_year]["used"] = price
                                    
                            except (KeyError, ValueError, TypeError):
                                continue
                    
                    if price_history:
                        return price_history
                        
                except json.JSONDecodeError:
                    continue
    
    return {}

def main():
    json_file_path = "/Users/aviralbansal/Library/CloudStorage/OneDrive-ThePennsylvaniaStateUniversity/hackalytics25/golden_apple/Data/iphone_links.json"  # Updated to use relative path
    
    # Load iPhone links from JSON file
    try:
        with open(json_file_path, "r") as f:
            iphone_links = json.load(f)
    except FileNotFoundError:
        print(f"Error: Could not find {json_file_path}")
        return
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in {json_file_path}")
        return
        
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
        price_history_url = product_url + "/price-history"
        print(f"Fetching: {price_history_url}")
        
        try:
            # Add delay to avoid rate limiting
            time.sleep(2)
            
            response = session.get(price_history_url)
            response.raise_for_status()
            
            # Debug: Save HTML for inspection
            with open(f"debug_{model_name}.html", "w", encoding="utf-8") as f:
                f.write(response.text)
            
            # Extract price history data
            price_data = extract_price_data(response.text)
            
            if price_data:
                all_models_data[model_name] = price_data
                print(f"Successfully extracted data for {model_name}")
            else:
                print(f"No price data found for {model_name}")
                
        except requests.exceptions.RequestException as e:
            print(f"Error fetching {price_history_url}: {e}")
            continue
    
    if all_models_data:
        # Save data to JSON file
        output_file = "iphone_price_history.json"
        with open(output_file, "w") as out:
            json.dump(all_models_data, out, indent=2)
        print(f"\nDone! Data saved to {output_file}")
    else:
        print("\nNo data was collected for any model")

if __name__ == "__main__":
    main()
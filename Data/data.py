import re
from datetime import datetime
import json
import os
from pathlib import Path

def parse_price_history(html_content):
    # Extract the datasets section
    datasets_match = re.search(r'var\s+datasets\s*=\s*(\[[\s\S]+?\]);', html_content)
    if not datasets_match:
        return {}

    # Extract all data points using regex
    data_points = re.findall(r'{\s*x:\s*(\d+),\s*y:\s*(\d+\.?\d*)\s*}', html_content)
    
    # Initialize price history dictionary
    price_history = {}
    
    # First pass: new prices
    for timestamp_str, price_str in data_points[:len(data_points)//2]:
        # Convert timestamp to datetime
        timestamp = int(timestamp_str)
        date = datetime.fromtimestamp(timestamp/1000)  # Convert milliseconds to seconds
        month_year = date.strftime("%b %Y")
        
        # Convert price to float
        price = float(price_str)
        
        # Add to price history
        if month_year not in price_history:
            price_history[month_year] = {"new": None, "used": None}
        price_history[month_year]["new"] = price

    # Second pass: used prices
    for timestamp_str, price_str in data_points[len(data_points)//2:]:
        timestamp = int(timestamp_str)
        date = datetime.fromtimestamp(timestamp/1000)
        month_year = date.strftime("%b %Y")
        
        price = float(price_str)
        
        if month_year not in price_history:
            price_history[month_year] = {"new": None, "used": None}
        price_history[month_year]["used"] = price

    return price_history

def extract_product_name(filename):
    # Remove 'debug_' prefix and '.html' suffix
    name = filename.replace('debug_', '').replace('.html', '')
    return name

def process_html_files(input_folder, output_folder):
    # Create output folder if it doesn't exist
    Path(output_folder).mkdir(parents=True, exist_ok=True)
    
    # Counter for processed files
    processed_count = 0
    error_count = 0
    
    # Process each HTML file in the input folder
    for filename in os.listdir(input_folder):
        if filename.endswith('.html') and filename.startswith('debug_'):
            try:
                # Read HTML file
                file_path = os.path.join(input_folder, filename)
                with open(file_path, 'r', encoding='utf-8') as file:
                    html_content = file.read()
                
                # Parse price history
                price_history = parse_price_history(html_content)
                
                if price_history:
                    # Sort the dictionary by date
                    sorted_history = dict(sorted(price_history.items(), 
                                               key=lambda x: datetime.strptime(x[0], "%b %Y")))
                    
                    # Create JSON filename based on product name
                    product_name = extract_product_name(filename)
                    json_filename = f"{product_name}.json"
                    json_path = os.path.join(output_folder, json_filename)
                    
                    # Save to JSON file
                    with open(json_path, 'w', encoding='utf-8') as f:
                        json.dump(sorted_history, f, indent=2)
                    
                    processed_count += 1
                    print(f"Processed: {product_name}")
                else:
                    error_count += 1
                    print(f"No price data found in: {filename}")
                    
            except Exception as e:
                error_count += 1
                print(f"Error processing {filename}: {str(e)}")
    
    return processed_count, error_count

def main():
    # Define input and output folders
    input_folder = "/Users/aviralbansal/Library/CloudStorage/OneDrive-ThePennsylvaniaStateUniversity/hackalytics25/golden_apple/Data/HTML"  # Change this to your input folder path
    output_folder = "price_history"  # Change this to your desired output folder path
    
    print(f"Processing HTML files from: {input_folder}")
    print(f"Saving JSON files to: {output_folder}")
    
    processed, errors = process_html_files(input_folder, output_folder)
    
    print("\nProcessing complete!")
    print(f"Files processed successfully: {processed}")
    print(f"Files with errors: {errors}")

if __name__ == "__main__":
    main()
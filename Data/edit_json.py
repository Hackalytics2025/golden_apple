import json
import os
from datetime import datetime
from pathlib import Path

def calculate_price_changes(prices_dict):
    """Calculate month-over-month price changes for both new and used prices."""
    # Convert dictionary to sorted list of tuples (date, prices)
    sorted_prices = sorted(prices_dict.items(), 
                         key=lambda x: datetime.strptime(x[0], "%b %Y"))
    
    # Initialize previous prices
    prev_new = None
    prev_used = None
    
    # Updated dictionary with price changes
    updated_prices = {}
    
    for date, prices in sorted_prices:
        current_new = prices.get('new')
        current_used = prices.get('used')
        
        # Calculate changes
        new_change = 0
        used_change = 0
        
        if prev_new is not None and current_new is not None:
            new_change = round(current_new - prev_new, 2)
        
        if prev_used is not None and current_used is not None:
            used_change = round(current_used - prev_used, 2)
        
        # Update dictionary with changes
        updated_prices[date] = {
            'new': current_new,
            'used': current_used,
            'new_change': new_change,
            'used_change': used_change
        }
        
        # Update previous prices
        prev_new = current_new
        prev_used = current_used
    
    return updated_prices

def process_json_files(input_folder):
    """Process all JSON files in the input folder and add price changes."""
    # Create a counter for processed files
    processed_count = 0
    error_count = 0
    
    # Process each JSON file
    for filename in os.listdir(input_folder):
        if filename.endswith('.json'):
            try:
                file_path = os.path.join(input_folder, filename)
                
                # Read existing JSON file
                with open(file_path, 'r', encoding='utf-8') as f:
                    price_data = json.load(f)
                
                # Calculate price changes
                updated_data = calculate_price_changes(price_data)
                
                # Write updated data back to file
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(updated_data, f, indent=2)
                
                processed_count += 1
                print(f"Processed: {filename}")
                
            except Exception as e:
                error_count += 1
                print(f"Error processing {filename}: {str(e)}")
    
    return processed_count, error_count

def main():
    # Define input folder containing JSON files
    input_folder = "/Users/aviralbansal/Library/CloudStorage/OneDrive-ThePennsylvaniaStateUniversity/hackalytics25/golden_apple/price_history"  # Change this to your JSON files folder path
    
    print(f"Processing JSON files from: {input_folder}")
    
    processed, errors = process_json_files(input_folder)
    
    print("\nProcessing complete!")
    print(f"Files processed successfully: {processed}")
    print(f"Files with errors: {errors}")
    
    # Print example of the format
    print("\nOutput format example:")
    example = {
        "Jan 2023": {
            "new": 1000.00,
            "used": 800.00,
            "new_change": 0,  # First month
            "used_change": 0   # First month
        },
        "Feb 2023": {
            "new": 950.00,
            "used": 780.00,
            "new_change": -50.00,  # Decreased by 50
            "used_change": -20.00   # Decreased by 20
        }
    }
    print(json.dumps(example, indent=2))

if __name__ == "__main__":
    main()
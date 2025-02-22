import os
import json
from datetime import datetime

# Folder containing JSON files
folder_path = "/Users/aviralbansal/Library/CloudStorage/OneDrive-ThePennsylvaniaStateUniversity/hackalytics25/golden_apple/price_history_new"  # Change this to your folder path

# Ensure the output folder exists
output_folder = os.path.join(folder_path, "updated")
os.makedirs(output_folder, exist_ok=True)

# Iterate over all JSON files in the folder
for filename in os.listdir(folder_path):
    if filename.endswith(".json"):
        file_path = os.path.join(folder_path, filename)

        # Load JSON file
        with open(file_path, "r") as file:
            data = json.load(file)

        # Convert date format
        converted_data = {datetime.strptime(date, "%b %Y").strftime("%Y-%m"): values for date, values in data.items()}

        # Save the updated JSON file
        output_path = os.path.join(output_folder, filename)
        with open(output_path, "w") as file:
            json.dump(converted_data, file, indent=4)

        print(f"Processed: {filename} -> Saved to: {output_path}")

print("All JSON files have been processed.")

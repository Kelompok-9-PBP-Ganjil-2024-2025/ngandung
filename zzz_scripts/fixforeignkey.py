import json

# Load the original JSON data
with open("makanan_data.json", "r") as file:
    data = json.load(file)

# Process each item to add 'rumah_makan' and remove 'fk'
for item in data:
    # Add 'rumah_makan' with the value from 'fk'
    item["fields"]["rumah_makan"] = item["fk"]
    # Remove 'fk' from the item
    del item["fk"]

# Save the modified data back to a new JSON file
with open("makanan_data_modified.json", "w") as file:
    json.dump(data, file, indent=2)

print("Modified JSON data saved to makanan_data_modified.json")

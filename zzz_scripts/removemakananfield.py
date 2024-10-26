import json

# Load JSON data from the file
with open("rumah_makan_data.json", "r") as file:
    data = json.load(file)

# Remove the 'makanan_dijual' field from each item in the list
for item in data:
    if "makanan_dijual" in item["fields"]:
        del item["fields"]["makanan_dijual"]

# Write the modified data back to the file
with open("rumah_makan_data.json", "w") as file:
    json.dump(data, file, indent=2)

print("The 'makanan_dijual' array has been removed successfully.")

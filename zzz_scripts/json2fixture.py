import json

# Load the original data
with open("csvjson.json", "r") as f:
    data = json.load(f)

# Transform data to fixture format
fixture_data = []
for entry in data:
    fixture_entry = {
        "model": "yourapp.rumahmakan",  # Replace 'yourapp' and 'rumahmakan' with your actual app and model name
        "pk": entry["id"],  # Assuming 'id' is the primary key
        "fields": {
            "kode_provinsi": entry["kode_provinsi"],
            "nama_provinsi": entry["nama_provinsi"],
            "bps_kode_kabupaten_kota": entry["bps_kode_kabupaten_kota"],
            "bps_nama_kabupaten_kota": entry["bps_nama_kabupaten_kota"],
            "nama_rumah_makan": entry["nama_rumah_makan"],
            "alamat": entry["alamat"],
            "latitude": entry["latitude"].replace(
                ",", "."
            ),  # Convert comma to dot for decimal format
            "longitude": entry["longitude"].replace(
                ",", "."
            ),  # Convert comma to dot for decimal format
            "tahun": entry["tahun"],
            "masakan_dari_mana": entry["masakan_dari_mana"],
            "makanan_berat_ringan": entry["makanan_berat_ringan"],
            "makanan_dijual": json.loads(
                entry["makanan_dijual"].replace("'", '"')
            ),  # Convert to JSON array
        },
    }
    fixture_data.append(fixture_entry)

# Save the transformed data to a new file
with open("rumah_makan_data.json", "w") as f:
    json.dump(fixture_data, f, indent=2)

print("Fixture data saved to rumah_makan_data.json")

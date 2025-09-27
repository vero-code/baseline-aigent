import requests
import json

# URL to a JSON file with web features data
url = "https://cdn.jsdelivr.net/npm/web-features/data.json"
file_path = "data/web_features.json"

try:
    print("Downloading web features data...")
    response = requests.get(url)
    response.raise_for_status()  # Checking for HTTP errors

    # Saving data to a file
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(response.json(), f, ensure_ascii=False, indent=2)

    print(f"Data successfully downloaded and saved to {file_path}")

except requests.exceptions.RequestException as e:
    print(f"Error downloading data: {e}")
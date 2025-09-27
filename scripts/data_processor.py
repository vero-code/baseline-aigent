# scripts/data_processor.py
import json

INPUT_FILE = "data/web_features.json"
OUTPUT_FILE = "data/processed_features.json"

def process_data():
    """
    Reads raw data, converts it into text documents, and saves it in a new file.
    """
    print(f"Reading data from {INPUT_FILE}...")
    try:
        with open(INPUT_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: Input file not found at {INPUT_FILE}")
        print("Please run 'scripts/download_data.py' first.")
        return

    processed_documents = []

    # Go through each feature in the JSON file
    for feature_id, feature_data in data['features'].items():
        name = feature_data.get("name", "N/A")
        description = feature_data.get("description", "No description available.")
        status_data = feature_data.get("status", {})
        baseline_status = status_data.get("baseline")

        # Converting the status into understandable text
        if baseline_status == "high":
            status_text = "Widely available"
        elif baseline_status == "low":
            status_text = "Newly available"
        else:
            status_text = "Limited availability"

        # Creating a single text document for AI
        document = (
            f"Feature Name: {name}\n"
            f"Feature ID: {feature_id}\n"
            f"Baseline Status: {status_text}\n"
            f"Description: {description}"
        )

        processed_documents.append(document)

    print(f"Processed {len(processed_documents)} features.")

    # Save processed documents in a new file
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(processed_documents, f, indent=2, ensure_ascii=False)

    print(f"Successfully processed data and saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    process_data()
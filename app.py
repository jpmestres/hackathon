from flask import Flask, jsonify, request
import json

app = Flask(__name__)

def load_data_from_json(file_path):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
        return []
    except json.JSONDecodeError:
        print(f"Error: The file {file_path} contains invalid JSON.")
        return []

# Load data when the application starts
MOCK_DATA = load_data_from_json("data.json")

@app.route('/')
def home():
    return "Mock Backend is Running!"

@app.route('/api/v1/items')
def get_items():
    # Get query parameters
    query_params = request.args.to_dict()
    
    # Initialize data to filter
    data_to_filter = list(MOCK_DATA)
    
    # Filter data based on query parameters
    if query_params:
        results = []
        for item in data_to_filter:
            # Check if item matches all query parameters
            matches = all(
                str(item.get(key, '')) == value
                for key, value in query_params.items()
            )
            if matches:
                results.append(item)
    else:
        results = data_to_filter
    
    return jsonify(results)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True) 
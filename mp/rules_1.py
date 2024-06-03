import json

def load_json_to_dict(file_name):
    try:
        with open(file_name, 'r') as file:
            data = json.load(file)
        print("Data loaded successfully.")
        return data
    except Exception as e:
        print("Error:", e)
        return None

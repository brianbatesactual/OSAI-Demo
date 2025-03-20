# src/utils/file_handler.py
import json
import csv

def read_json_file(file_path):
    data =[]
    with open(file_path, 'r') as file:
        for line in file:
            log_entry = json.loads(line.strip())
            data.append(log_entry)
        return data

def write_to_csv(file_path, data, fieldnames):
    with open(file_path, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

def write_to_json(file_path, data):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)
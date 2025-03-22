# src/utils/file_handler.py
import json
import csv
import os

def read_json_file(file_path):
    data =[]
    with open(file_path, 'r') as file:
        for line in file:
            log_entry = json.loads(line.strip())
            data.append(log_entry)
        return data

def write_to_csv(file_path, data, fieldnames):
    file_exists = os.path.isfile(file_path)
    
    with open(file_path, 'a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        if not file_exists:
            writer.writeheader()
        
        writer.writerows(data)

def write_to_json(file_path, data):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)
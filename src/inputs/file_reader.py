# 	Wraps read_json_lines, etc.

import os
import json
import logging
logger = logging.getLogger(__name__)

def read_from_default_data(file_name='input_logs.json'):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(script_dir, '../../data', file_name)
    data_path = os.path.abspath(data_path)
    return read_json_lines(data_path)

def read_json_lines(file_path):
    logs = []
    if not os.path.exists(file_path):
        logger.error(f"File not found: {file_path}")
        raise FileNotFoundError(f"File not found: {file_path}")
    with open(file_path, 'r') as f:
        for line in f:
            try:
                logs.append(json.loads(line.strip()))
            except json.JSONDecodeError:
                continue
    return logs
# Handles all argparse config + default paths

import argparse

def parse_args():
    parser = argparse.ArgumentParser(description='Process logs using templates.')
    parser.add_argument('--input-file', type=str, help='Path to input JSON file.')
    parser.add_argument('--input', type=str, default='data/input_logs.json', help='Path to input log file')
    parser.add_argument('--mode', choices=['file', 'stream'], default='file', help='Input mode: "file" or "stream"')
    parser.add_argument('--render-mode', choices=['random', 'all'], default='random', help='Template render mode: "random" or "all"')
    parser.add_argument('--output', type=str, default='data/processed_logs.csv', help='Path to output CSV file.')
    parser.add_argument('--unmatched', type=str, default='data/unmatched_json.csv', help='Path to unmatched JSON file.')
    parser.add_argument('--generate-sbert-data', action='store_true', help='Export sentence pairs for SBERT fine-tuning.')
    parser.add_argument('--log-level', default='INFO', choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'], help='Set logging level (default: INFO).')
    parser.add_argument('--log-file', default=None, help='Optional path to save logs to a file in addition to stdout.')

    return parser.parse_args()
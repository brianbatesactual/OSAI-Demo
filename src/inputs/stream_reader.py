import sys
import json

def read_from_stdin():
    print("Listening for JSON log events via stdin...")
    for line in sys.stdin:
        try:
            yield json.loads(line.strip())
        except json.JSONDecodeError:
            continue

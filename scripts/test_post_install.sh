#!/bin/bash

set -e

echo "Waiting for Vatrix service to come up on port 8000..."
until curl -s http://10.0.1.159:8000/docs > /dev/null; do
  sleep 1
done

echo "✅ FastAPI is up"

VECTOR=$(python3 -c 'import json; print(json.dumps([0.1, 0.2, 0.3, 0.4, 0.5] + [0.0]*379))')

echo "Sending test /add_log payload..."
curl -s -X POST http://10.0.1.159:8000/add_log/ \
  -H "Content-Type: application/json" \
  -d "{\"log_id\": 1, \"vector\": $VECTOR, \"payload\": {\"log_text\": \"Sample log from test script\"}}" | jq .

echo "Sending test /search_logs query..."
curl -s -X POST http://10.0.1.159:8000/search_logs/ \
  -H "Content-Type: application/json" \
  -d "{\"query_vector\": $VECTOR, \"top_k\": 1}" | jq .

echo "✅ Test complete"
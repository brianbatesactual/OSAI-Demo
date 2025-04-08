#!/bin/bash

set -euo pipefail

# Make sure to set you token
AUTH_HEADER="Authorization: Bearer changeme123"

# Extract first ansible_host from inventory
HOST=$(awk '/ansible_host=/{print $2}' inventory/hosts.ini | head -n 1 | cut -d= -f2)

# Try port 80 first
if curl -s "http://${HOST}:80/docs" | grep -q "Vatrix" ; then
  PORT=80
  echo "🌐 NGINX is serving Vatrix Gateway — using port 80"
elif curl -s "http://${HOST}:8000/docs" | grep -q "Vatrix" ; then
  PORT=8000
  echo "🚧 NGINX not found — falling back to port 8000"
else
  echo "❌ Vatrix Gateway not responding on expected ports"
  exit 1
fi

URL="http://${HOST}:${PORT}"

echo "📡 Target: ${URL}"

# Wait for Gateway to respond
echo "Waiting for Vatrix Gateway service to come up on ${URL}..."
until curl -s "${URL}/docs" > /dev/null; do
  sleep 1
done

echo "✅ Vatrix Gateway is up"

# Generate a valid 384-dim vector
VECTOR=$(python3 -c 'import json; print(json.dumps([0.1, 0.2, 0.3, 0.4, 0.5] + [0.0]*379))')
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
UUID=$(python3 -c 'import uuid; print(uuid.uuid4())')

TMPFILE=$(mktemp /tmp/vatrix-test.XXXXXX).json

python3 -c "
import json
with open('$TMPFILE', 'w') as f:
    json.dump({
        'project': 'osai-demo',
        'entries': [{
            'id': '$UUID',
            'vector': $VECTOR,
            'payload': {
                'log_text': 'This is a test log sent via post-install script',
                'test_flag': 'true'
            },
            'timestamp': '$TIMESTAMP'
        }]
    }, f)
"

dos2unix "$TMPFILE" 2>/dev/null || true

# Debug print payload, uncomment below two lines to enable
# echo "Payload:"
# cat "$TMPFILE" | jq .

# Testing ingest pipeline
echo "🚀 Sending test /api/v1/ingest payload..."

RESPONSE=$(curl -s -X POST "${URL}/api/v1/ingest" \
  -H "Authorization: Bearer changeme123" \
  -H "Content-Type: application/json" \
  --data @"$TMPFILE")

echo "$RESPONSE" | jq .

if ! echo "$RESPONSE" | jq -e '.status == "ok"' > /dev/null; then
  echo "❌ Ingest failed!"
  exit 1
fi

# Testing search API
echo "🔍 Sending test /api/v1/search query..."

SEARCH_OUTPUT=$(curl -s -X POST "${URL}/api/v1/search" \
  -H "Authorization: Bearer changeme123" \
  -H "Content-Type: application/json" \
  -d "{\"query_vector\": $VECTOR, \"top_k\": 1}")

echo "$SEARCH_OUTPUT" | jq .

echo "✅ Test complete"
exit 0
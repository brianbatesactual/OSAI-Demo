import sys
import json
import logging
logger = logging.getLogger(__name__)

def read_from_stdin():
    logger.info("Listening for NDJSON input (Ctrl+D to end)...")
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        
        logger.debug(f"📥 Received line: {line}")
        
        try:
            yield json.loads(line)
        except json.JSONDecodeError as e:
            logger.warning(f"❌ Invalid JSON input: {e}")
            continue
        
        # try:
        #     yield json.loads(line.strip())
        # except json.JSONDecodeError:
        #     continue

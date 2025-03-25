import json
import os
import logging
from templates.template_map import TEMPLATE_MAP

logger = logging.getLogger(__name__)

def load_template_map(override_path=None):
    if override_path:
        logger.info(f"📄 Attempting to load template map from: {override_path}")
        try:
            with open(override_path, 'r') as f:
                loaded = json.load(f)
                logger.info(f"📄 Loading custom template map from: {override_path}")
                return json.load(f)
        except Exception as e:
            logger.warning(f"⚠️ Failed to load custom template map: {e}. Using default.")
    else:
        logger.info("📄 Loading default template map.")
    return TEMPLATE_MAP

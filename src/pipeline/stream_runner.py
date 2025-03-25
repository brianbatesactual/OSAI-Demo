# Handles streaming logic

import logging
from templates.tmanager import TManager
from templates.loader import load_template_map
from inputs.stream_reader import read_from_stdin
from utils.file_handler import write_to_csv, write_to_json
# from pipeline.context_builder import build_context
# from outputs.file_writer import write_to_csv, write_to_json

logger = logging.getLogger(__name__)

def process_stream(output_csv='data/streamed_logs.csv', unmatched_json='data/unmatched_streamed.json', render_mode='random'):
    template_manager = TManager()
    template_map = load_template_map()

    output_csv = 'data/streamed_logs.csv'
    unmatched_logs = []
    fieldnames = ['log']
    rendered_count = 0

    for log_entry in read_from_stdin():
        # logger.debug(f"📥 Received line: {json.dumps(line)}")
        context = {
            'ALGDATE': log_entry.get('ALGDATE', ''),
            'ALGTIME': log_entry.get('ALGTIME', ''),
            'ALGUSER': log_entry.get('ALGUSER', ''),
            'ALGCLIENT': log_entry.get('ALGCLIENT', ''),
            'ALGTEXT': log_entry.get('ALGTEXT', ''),
            'PARAM1': log_entry.get('PARAM1', ''),
            'PARAM3': log_entry.get('PARAM3', ''),
            'ALGSYSTEM': log_entry.get('ALGSYSTEM', ''),
        }

        template_name = template_map.get(log_entry.get('TXSUBCLSID'), 'default_template.txt')
        if template_name == 'default_template.txt':
            logger.warning(f"TXSUBCLSID '{log_entry.get('TXSUBCLSID')}' not found. Using default template.")
            unmatched_logs.append(log_entry)
        else:
            rendered = template_manager.render_random_template(template_name, context)
            write_to_csv(output_csv, [{'log': rendered}], fieldnames)
            rendered_count += 1
            logger.info(f"✅ Rendered log with template: {template_name}")

    logger.info(f"📝 Stream ended. {rendered_count} logs written to {output_csv}")


    if unmatched_logs:
        write_to_json('data/unmatched_streamed.json', unmatched_logs)
        logger.warning(f"⚠️ {len(unmatched_logs)} unmatched logs saved to {unmatched_json}")
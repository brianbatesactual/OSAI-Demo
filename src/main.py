import argparse
from templates.tmanager import TManager
from utils.file_handler import write_to_csv, write_to_json
from inputs import file_reader
from inputs.stream_reader import read_from_stdin
from utils.exporter import export_sentence_pairs
from sentence_transformers import SentenceTransformer, util
from utils.similarity import get_similarity_score
from utils.logger import setup_logger
import logging

logger = setup_logger()

# model = SentenceTransformer('all-MiniLM-L6-v2')

# score = util.cos_sim(model.encode(sent1), model.encode(sent2))

def process_logs(logs, output_csv, unmatched_json, render_mode='random', generate_sbert=False):
    logger.info(f"🔧 Processing {len(logs)} log entries")
    template_manager = TManager()
    processed_logs = []
    unmatched_logs = []
    sbert_pairs = []

    template_map = {
        'Dialog Logon': 'dialog_logon',
        # 'Other Events': 'other_events_template.txt',
        # 'Report Start': 'report_start_template.txt',
        # 'RFC Call': 'rfc_call_template.txt',
        # 'RFC/CPIC Logon': 'rfc_cpic_logon_template.txt',
        # 'RFC Function Call': 'rfc_function_call_template.txt',
        # 'System Events': 'system_events_template.txt',
        # 'Transaction Start': 'transaction_start_template.txt',
        # 'User Master Changes': 'user_master_changes_template.txt',
        
        # Map other TXSUBCLSID values to their templates
    }

    for log_entry in logs:
        # context = {key: log_entry.get(key, 'N/A') for key in [
        #     'TXSUBCLSID', 'EVENT_TYPE', 'EVENT_SUBTYPE', 'CURRENT_TIMESTAMP', 'ALGSYSTEM',
        #     'ALGINST', 'ALGCLIENT', 'ALGUSER', 'ALGLTERM', 'ALGTCODE',
        #     'ALGREPNA', 'ALGAREA', 'ALGSUBID', 'TXSEVERITY', 'ALGTEXT',
        #     'PARAM1', 'PARAM2', 'PARAM3', 'PARAM4', 'MSG'
        # ]

            # Phase 1, without loop
        context = {
            'ALGDATE': log_entry["ALGDATE"],
            'ALGTIME': log_entry['ALGTIME'],
            'ALGUSER': log_entry['ALGUSER'],
            'ALGCLIENT': log_entry['ALGCLIENT'],
            'ALGTEXT': log_entry['ALGTEXT'],
            'PARAM1': log_entry.get('PARAM1', ''),
            'PARAM2': log_entry.get('PARAM2', ''),
            'PARAM3': log_entry.get('PARAM3', ''),
            'PARAM4': log_entry.get('PARAM4', ''),
            'ALGSYSTEM': log_entry['ALGSYSTEM'],

            # Add other necessary fields
        }

    
        template_name = template_map.get(log_entry['TXSUBCLSID'], 'default_template.txt')
        
        if template_name == 'default_template.txt':
            logger.warning(f"TXSUBCLSID '{log_entry.get('TXSUBCLSID')}' not found. Using default template.")
            unmatched_logs.append(log_entry)
            logger.warning(f"⚠️ {len(unmatched_logs)} unmatched logs written to {unmatched_json}")

        else:
            if render_mode == 'random':
                rendered_text = template_manager.render_random_template(template_name, context)
                processed_logs.append({'log': rendered_text})
                logger.info(f"✅ Rendered {len(processed_logs)} logs")
            
            elif render_mode == 'all':
                rendered_texts = template_manager.render_all_templates(template_name, context)
                processed_logs.extend([{'log': t} for t in rendered_texts])
                logger.info(f"✅ Rendered {len(processed_logs)} logs")

                if generate_sbert:
                    base = rendered_texts[0]
                    for variation in rendered_texts[1:]:
                        sim_score = get_similarity_score(base, variation)
                        sbert_pairs.append((base, variation, sim_score)) # all variations are highly similar
                logger.info(f"📊 Generated {len(sbert_pairs)} SBERT training pairs")

                # rendered_texts = template_manager.render_all_templates(template_name, context)
                # for text in rendered_texts:
                    # processed_logs.append({'log': text})
            else:
                raise ValueError('Invalid render mode. Use "random" or "all".')

    if generate_sbert:
        export_sentence_pairs(sbert_pairs)
        logger.info(f'📦 Exported {len(sbert_pairs)} SBERT training pairs to data/sbert_training_pairs.csv.')

    if processed_logs:
        # fieldnames = ['log'] v1 legacy, delete?
        write_to_csv(output_csv, processed_logs, fieldnames=['log'])

    if unmatched_logs:
        write_to_json(unmatched_json, unmatched_logs)

def process_stream(output_csv='data/streamed_logs.csv', unmatched_json='data/unmatched_streamed.json', render_mode='random'):
    template_manager = TManager()
    template_map = {
        'Dialog Logon': 'dialog_logon',
        # ... other mappings
    }

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

if __name__ == "__main__":
    from inputs.file_reader import read_from_default_data, read_json_lines

    # parse arguments
    parser = argparse.ArgumentParser(description='Process logs using templates.')
    parser.add_argument('--input-file', type=str, help='Path to input JSON file.')
    parser.add_argument('--input', type=str, default='data/input_logs.json', help='Path to input log file')
    parser.add_argument('--mode', choices=['file', 'stream'], default='file', help='Input mode: "file" or "stream"')
    parser.add_argument('--render-mode', choices=['random', 'all'], default='random', help='Template render mode: "random" or "all"')
    parser.add_argument('--output', type=str, default='data/processed_logs.csv', help='Path to output CSV file.')
    parser.add_argument('--unmatched', type=str, default='data/unmatched_json.csv', help='Path to unmatched JSON file.')
    parser.add_argument('--generate-sbert-data', action='store_true', help='Export sentence pairs for SBERT fine-tuning.')
    parser.add_argument('--log-level', default='INFO', choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'], help='Set logging level (default: INFO).')
    
    args = parser.parse_args()

    logger = setup_logger(level=getattr(logging, args.log_level.upper()))
    
    logger.info("Starting osai pipeline...")
    logger.info(f"Mode: {args.mode} | Render mode: {args.render_mode} | SBERT Data: {args.generate_sbert_data}")

    # file mode
    if args.mode == 'file':
        logger.info(f"📁 File mode selected. Reading logs from {args.input}")
        logs = read_json_lines(args.input)
        logger.info(f"Loaded {len(logs)} logs from input file.")
        process_logs(
            logs,
            args.output,
            args.unmatched,
            render_mode=args.render_mode,
            generate_sbert=args.generate_sbert_data
        )

    # stream mode
    elif args.mode == 'stream':
        logger.info(f"🌊 Stream mode selected. Waiting for NSJSON from standard input.")
        process_stream(
            output_csv=args.output,
            unmatched_json=args.unmatched,
            render_mode=args.render_mode
        )
        
    else:
        if args.input_file:
            logs = file_reader.read_json_lines(args.input_file)
        else:
            logs = file_reader.read_from_default_data()
        process_stream(logs, args.output, args.unmatched, render_mode=args.render_mode)
    
    # from inputs.file_reader import read_from_default_data
    # input_file = read_from_default_data()
    # output_csv = '../data/processed_logs.csv'
    # unmatched_json = '../data/unmatched_logs.json'
    # process_logs(
        # input_file,
        # output_csv='data/processed_logs.csv',
        # unmatched_json='data/unmatched_logs.json'
    # )
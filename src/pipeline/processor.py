# 	Main process_logs() logic

import logging
from templates.tmanager import TManager
from templates.loader import load_template_map
# from outputs.file_writer import write_to_csv, write_to_json
from utils.file_handler import write_to_csv, write_to_json
# from outputs.sbert_writer import write_sbert_pairs
# from pipeline.context_builder import build_context
from utils.exporter import export_sentence_pairs
from utils.similarity import get_similarity_score

logger = logging.getLogger(__name__)

def process_logs(logs, output_csv, unmatched_json, render_mode='random', generate_sbert=False):
    logger.info(f"🔧 Processing {len(logs)} log entries")
    template_manager = TManager()

    processed_logs = []
    unmatched_logs = []
    sbert_pairs = []

    template_map = load_template_map()
    logger.debug(f"🧭 Template map loaded: {list(template_map.keys())}")


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
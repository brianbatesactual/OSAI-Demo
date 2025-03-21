from templates.tmanager import TManager
from utils.file_handler import read_json_file, write_to_csv, write_to_json
from inputs import file_reader

def process_logs(logs, output_csv, unmatched_json, render_mode='random'):
    template_manager = TManager()
    processed_logs = []
    unmatched_logs = []

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
            unmatched_logs.append(log_entry)
        else:
            if render_mode == 'random':
                rendered_text = template_manager.render_random_template(template_name, context)
                processed_logs.append({'log': rendered_text})
            elif render_mode == 'all':
                rendered_texts = template_manager.render_all_templates(template_name, context)
                for text in rendered_texts:
                    processed_logs.append({'log': text})
            else:
                raise ValueError('Invalid render mode. Use "random" or "all".')

    if processed_logs:
        # fieldnames = ['log'] v1 legacy, delete?
        write_to_csv(output_csv, processed_logs, fieldnames=['log'])

    if unmatched_logs:
        write_to_json(unmatched_json, unmatched_logs)

if __name__ == "__main__":
    from inputs.file_reader import read_from_default_data
    input_file = read_from_default_data()
    # output_csv = '../data/processed_logs.csv'
    # unmatched_json = '../data/unmatched_logs.json'
    process_logs(
        input_file,
        output_csv='data/processed_logs.csv',
        unmatched_json='data/unmatched_logs.json'
    )
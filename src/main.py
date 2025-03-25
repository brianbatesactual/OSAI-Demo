# src/main.py
# CLI entrypoint, argument parsing, and orchestration only

import logging
# import argparse
from cli.args import parse_args
from utils.logger import setup_logger
from pipeline.processor import process_logs
from pipeline.stream_runner import process_stream
from inputs.file_reader import read_from_default_data, read_json_lines

from templates.tmanager import TManager
from utils.file_handler import write_to_csv, write_to_json
from inputs import file_reader
from inputs.stream_reader import read_from_stdin
from utils.exporter import export_sentence_pairs
from sentence_transformers import SentenceTransformer, util
from utils.similarity import get_similarity_score


def main():
    args = parse_args()

    # logging init
    log_path = setup_logger(
        level=getattr(logging, args.log_level.upper(), "INFO"),
        log_file=args.log_file,
        mode=args.mode
    )   

    args.log_file = log_path

    logger = logging.getLogger(__name__)
    
    logger.info("✅ Logging system initialized")
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

if __name__ == "__main__":
    main()
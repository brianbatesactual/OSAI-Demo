# Sets up logger and levels across all modules

import logging
import os
from datetime import datetime
from logging.handlers import TimedRotatingFileHandler
from colorlog import ColoredFormatter

def setup_logger(level='INFO', log_file=None, mode='file', rotate_daily=True, keep_logs=7):
    if not log_file:
        today = datetime.now().strftime('%Y-%m-%d')
        log_file = f'logs/{mode}_{today}_run.log'
    
        log_dir = os.path.dirname(log_file)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir, exist_ok=True)

    color_formatter = ColoredFormatter(
        "%(log_color)s[%(levelname)s] %(asctime)s - %(name)s - %(message)s",
        datefmt=None,
        reset=True,
        log_colors={
            'DEBUG':    'cyan',
            'INFO':     'green',
            'WARNING':  'yellow',
            'ERROR':    'red',
            'CRITICAL': 'red,bg_white',
        },
        secondary_log_colors={},
        style='%'
    )

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(color_formatter)
    
    handlers = [console_handler]
    
    if rotate_daily:
        file_handler = TimedRotatingFileHandler(
            log_file,
            when='midnight',
            interval=1,
            backupCount=7,
            encoding='utf-8'
        )
    else:
        from logging.handlers import RotatingFileHandler
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=5_000_000,
            backupCount=keep_logs,
            encoding='utf-8'
        )    
    file_formatter = logging.Formatter('[%(levelname)s] %(asctime)s - %(name)s - %(message)s')
    file_handler.setFormatter(file_formatter)
    handlers.append(file_handler)

    logging.basicConfig(
        level=level,
        handlers=handlers,
        force=True
    )

    return log_file 
    
    
    
    
    # logger = logging.getLogger(name)
    # if not logger.handlers:
       
    #     formatter = logging.Formatter('[%(levelname)s] %(asctime)s - %(message)s')
    #     handler.setFormatter(formatter)
    #     logger.addHandler(handler)
    # logger.setLevel(level)
    # return logger

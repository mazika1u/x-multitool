import logging
import os
from datetime import datetime
from logging.handlers import RotatingFileHandler

def setup_logger(name: str, log_level: int = logging.INFO) -> logging.Logger:
    logger = logging.getLogger(name)
    
    if logger.handlers:
        return logger
        
    logger.setLevel(log_level)
    os.makedirs('logs', exist_ok=True)
    
    # Formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # File handler with rotation
    log_file = f"logs/operation.log"
    file_handler = RotatingFileHandler(
        log_file, 
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5,
        encoding='utf-8'
    )
    file_handler.setLevel(log_level)
    file_handler.setFormatter(formatter)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)
    
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

"""
Logger - Sistema di logging
Configura e gestisce il logging dell'applicazione
"""

import logging
import sys
from pathlib import Path
from datetime import datetime


def setup_logger(name: str = "MemoryReader", level: int = logging.INFO) -> logging.Logger:
    """
    Configura il sistema di logging
    
    Args:
        name: Nome del logger
        level: Livello di logging (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        
    Returns:
        Logger configurato
    """
    
    # Crea il logger
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Evita duplicati se già configurato
    if logger.handlers:
        return logger
    
    # Formato del log
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Handler per console
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # Handler per file
    log_dir = Path(__file__).parent.parent.parent / "logs"
    log_dir.mkdir(exist_ok=True)
    
    log_file = log_dir / f"memory_reader_{datetime.now().strftime('%Y%m%d')}.log"
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)  # File più dettagliato
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    return logger


# Logger globale
default_logger = setup_logger()

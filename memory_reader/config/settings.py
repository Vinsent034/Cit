"""
Configurazione - Impostazioni dell'applicazione
"""

# Configurazioni logging
LOG_LEVEL = "INFO"  # DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_TO_FILE = True
LOG_TO_CONSOLE = True

# Configurazioni memoria
DEFAULT_READ_SIZE = 1024  # Dimensione default per lettura memoria
MAX_SCAN_SIZE = 10 * 1024 * 1024  # 10 MB max per scan

# Configurazioni pattern scanner
PATTERN_SCAN_TIMEOUT = 30  # secondi

# Configurazioni processo
AUTO_ATTACH = False  # Attacca automaticamente al primo processo trovato
REQUIRE_ADMIN = True  # Richiedi privilegi amministrativi

# Configurazioni visualizzazione
HEX_DUMP_WIDTH = 16  # Bytes per riga nel hex dump
SHOW_ASCII = True  # Mostra ASCII nel hex dump

# Configurazioni avanzate
CACHE_ADDRESSES = True  # Cache degli indirizzi trovati
MAX_CACHE_SIZE = 1000  # Numero massimo di indirizzi in cache

"""
Helpers - Funzioni di utilità
Funzioni helper varie per l'applicazione
"""

from typing import Any


def format_address(address: int) -> str:
    """
    Formatta un indirizzo in esadecimale
    
    Args:
        address: Indirizzo numerico
        
    Returns:
        Stringa formattata (es. "0x12345678")
    """
    return f"0x{address:X}"


def format_bytes(num_bytes: int) -> str:
    """
    Formatta una dimensione in bytes in modo leggibile
    
    Args:
        num_bytes: Numero di bytes
        
    Returns:
        Stringa formattata (es. "1.5 MB")
    """
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if num_bytes < 1024.0:
            return f"{num_bytes:.2f} {unit}"
        num_bytes /= 1024.0
    return f"{num_bytes:.2f} PB"


def hex_to_int(hex_string: str) -> int:
    """
    Converte una stringa esadecimale in intero
    
    Args:
        hex_string: Stringa esadecimale (con o senza "0x")
        
    Returns:
        Valore intero
    """
    if hex_string.startswith('0x') or hex_string.startswith('0X'):
        hex_string = hex_string[2:]
    return int(hex_string, 16)


def bytes_to_hex_string(data: bytes) -> str:
    """
    Converte bytes in stringa esadecimale
    
    Args:
        data: Dati in bytes
        
    Returns:
        Stringa esadecimale separata da spazi
    """
    return " ".join(f"{b:02X}" for b in data)


def hex_string_to_bytes(hex_string: str) -> bytes:
    """
    Converte stringa esadecimale in bytes
    
    Args:
        hex_string: Stringa esadecimale (es. "AB CD EF")
        
    Returns:
        Bytes
    """
    # Rimuovi spazi e converti
    hex_string = hex_string.replace(" ", "").replace("0x", "")
    return bytes.fromhex(hex_string)


def is_valid_address(address: int, max_address: int = 0x7FFFFFFFFFFFFFFF) -> bool:
    """
    Verifica se un indirizzo è valido
    
    Args:
        address: Indirizzo da verificare
        max_address: Indirizzo massimo valido
        
    Returns:
        True se valido, False altrimenti
    """
    return 0 < address < max_address


def calculate_offset(base_address: int, target_address: int) -> int:
    """
    Calcola l'offset tra due indirizzi
    
    Args:
        base_address: Indirizzo base
        target_address: Indirizzo target
        
    Returns:
        Offset
    """
    return target_address - base_address


def print_header(title: str, width: int = 60):
    """
    Stampa un header formattato
    
    Args:
        title: Titolo da mostrare
        width: Larghezza totale
    """
    print("\n" + "=" * width)
    print(f" {title.center(width-2)} ")
    print("=" * width)


def print_separator(char: str = "-", width: int = 60):
    """
    Stampa un separatore
    
    Args:
        char: Carattere da usare
        width: Larghezza
    """
    print(char * width)


def confirm_action(message: str) -> bool:
    """
    Chiede conferma all'utente
    
    Args:
        message: Messaggio da mostrare
        
    Returns:
        True se confermato, False altrimenti
    """
    response = input(f"{message} (s/n): ").lower().strip()
    return response in ['s', 'si', 'y', 'yes']


def safe_int_input(prompt: str, default: int = 0) -> int:
    """
    Input sicuro di un numero intero
    
    Args:
        prompt: Messaggio per l'input
        default: Valore di default
        
    Returns:
        Numero intero
    """
    try:
        value = input(prompt).strip()
        if not value:
            return default
        
        # Supporta formato esadecimale
        if value.startswith('0x') or value.startswith('0X'):
            return hex_to_int(value)
        else:
            return int(value)
    except ValueError:
        print(f"⚠️ Valore non valido, uso default: {default}")
        return default

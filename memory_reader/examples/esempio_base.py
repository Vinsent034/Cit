"""
Esempio Base - Utilizzo del Memory Reader
Dimostra le funzionalità base dell'applicazione
"""

import sys
from pathlib import Path

# Aggiungi src al path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from core.process_manager import ProcessManager
from core.memory_reader import MemoryReader
from scanners.pattern_scanner import PatternScanner
from utils.helpers import format_address, print_header, safe_int_input


def esempio_lettura_base():
    """Esempio: Attacca a un processo e leggi un valore"""
    
    print_header("Esempio 1: Lettura Base")
    
    # Crea il process manager
    pm = ProcessManager()
    
    # Nome del processo (modifica con il tuo processo)
    process_name = "notepad.exe"
    
    # Attacca al processo
    print(f"\n🔍 Tentativo di attacco a {process_name}...")
    process = pm.attach_to_process(process_name)
    
    if not process:
        print("❌ Processo non trovato o permessi insufficienti")
        return
    
    print(f"✓ Connesso a {process_name}")
    
    # Ottieni info processo
    info = pm.get_process_info()
    print(f"  PID: {info['pid']}")
    print(f"  Base Address: {format_address(info['base_address'])}")
    
    # Crea il memory reader
    reader = MemoryReader(process)
    
    # Esempio: Leggi un valore (sostituisci con un indirizzo reale)
    print("\n📖 Lettura memoria...")
    address = safe_int_input("Inserisci indirizzo (hex con 0x): ", 0)
    
    if address > 0:
        value = reader.read_int(address)
        if value is not None:
            print(f"✓ Valore a {format_address(address)}: {value}")
    
    # Chiudi
    pm.close()


def esempio_pattern_scan():
    """Esempio: Cerca pattern in memoria"""
    
    print_header("Esempio 2: Pattern Scanner")
    
    pm = ProcessManager()
    
    # Attacca a un processo
    process_name = input("\nNome processo: ")
    process = pm.attach_to_process(process_name)
    
    if not process:
        return
    
    print(f"✓ Connesso a {process_name}")
    
    # Crea lo scanner
    scanner = PatternScanner(process)
    
    # Lista i moduli
    print("\n📚 Moduli caricati:")
    modules = scanner.list_modules()
    
    for i, module in enumerate(modules[:10], 1):
        print(f"{i}. {module['name']}")
        print(f"   Base: {format_address(module['base_address'])}")
        print(f"   Size: {module['size']} bytes")
    
    # Cerca un valore
    print("\n🔎 Ricerca valore...")
    value = safe_int_input("Inserisci valore da cercare: ", 0)
    
    if value > 0:
        addresses = scanner.scan_for_value(value)
        
        if addresses:
            print(f"\n✓ Trovato in {len(addresses)} posizioni:")
            for addr in addresses[:5]:  # Mostra prime 5
                print(f"  {format_address(addr)}")
        else:
            print("❌ Valore non trovato")
    
    pm.close()


def esempio_hex_dump():
    """Esempio: Dump della memoria in formato hex"""
    
    print_header("Esempio 3: Hex Dump")
    
    pm = ProcessManager()
    
    # Attacca a un processo
    process_name = input("\nNome processo: ")
    process = pm.attach_to_process(process_name)
    
    if not process:
        return
    
    print(f"✓ Connesso a {process_name}")
    
    # Crea il reader
    reader = MemoryReader(process)
    
    # Richiedi indirizzo
    address = safe_int_input("\nIndirizzo da dumpare (hex con 0x): ", 0)
    size = safe_int_input("Numero di bytes (default 256): ", 256)
    
    if address > 0:
        dump = reader.dump_memory(address, size)
        if dump:
            print(dump)
    
    pm.close()


def main():
    """Menu principale degli esempi"""
    
    print("=" * 60)
    print(" MEMORY READER - Esempi di Utilizzo ".center(60))
    print("=" * 60)
    
    while True:
        print("\n📋 Seleziona un esempio:")
        print("1. Lettura base della memoria")
        print("2. Pattern scanner e ricerca valori")
        print("3. Hex dump della memoria")
        print("0. Esci")
        
        choice = input("\nScelta: ").strip()
        
        if choice == "1":
            esempio_lettura_base()
        elif choice == "2":
            esempio_pattern_scan()
        elif choice == "3":
            esempio_hex_dump()
        elif choice == "0":
            print("\n👋 Arrivederci!")
            break
        else:
            print("❌ Scelta non valida")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Interruzione da utente")
    except Exception as e:
        print(f"\n❌ Errore: {e}")

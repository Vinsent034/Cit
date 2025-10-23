"""
Memory Reader - Entry Point Principale
Applicazione per leggere e analizzare la memoria di processi
"""

import sys
from pathlib import Path

# Aggiungi il path src al PYTHONPATH
sys.path.insert(0, str(Path(__file__).parent / "src"))

from core.process_manager import ProcessManager
from core.memory_reader import MemoryReader
from utils.logger import setup_logger

def main():
    """Funzione principale dell'applicazione"""
    
    # Setup del logger
    logger = setup_logger()
    logger.info("Avvio Memory Reader Application")
    
    try:
        # Inizializza il gestore processi
        process_manager = ProcessManager()
        
        # Lista tutti i processi attivi
        logger.info("Processi disponibili:")
        processes = process_manager.list_processes()
        
        for i, proc in enumerate(processes[:10], 1):  # Mostra primi 10
            print(f"{i}. {proc['name']} (PID: {proc['pid']})")
        
        # Esempio: Richiedi nome processo
        print("\n" + "="*50)
        process_name = input("Inserisci il nome del processo da analizzare: ")
        
        # Attacca al processo
        process = process_manager.attach_to_process(process_name)
        
        if process:
            logger.info(f"Collegato al processo: {process_name}")
            
            # Crea il memory reader
            reader = MemoryReader(process)
            
            # Qui puoi aggiungere le tue operazioni
            print(f"\n✓ Processo {process_name} caricato con successo!")
            print(f"  PID: {process.process_id}")
            print(f"  Base Address: 0x{process.process_base.base_address:X}")
            
        else:
            logger.error(f"Impossibile connettersi al processo: {process_name}")
            
    except KeyboardInterrupt:
        logger.info("\nInterruzione da utente")
    except Exception as e:
        logger.error(f"Errore: {e}")
    finally:
        logger.info("Chiusura applicazione")

if __name__ == "__main__":
    main()

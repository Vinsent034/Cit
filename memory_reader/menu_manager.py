"""
Menu Manager - Sistema di menu interattivi
Gestisce i menu e le opzioni dell'applicazione
"""

import sys
from pathlib import Path

# Aggiungi src al path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from core.process_manager import ProcessManager
from core.memory_reader import MemoryReader
from scanners.pattern_scanner import PatternScanner
from utils.helpers import (
    format_address, print_header, print_separator, 
    safe_int_input, confirm_action
)
from utils.logger import setup_logger
import pymem.process


class MenuManager:
    """Gestisce i menu interattivi dell'applicazione"""
    
    def __init__(self):
        """Inizializza il Menu Manager"""
        self.logger = setup_logger()
        self.process_manager = ProcessManager()
        self.current_process = None
        self.reader = None
        self.scanner = None
        self.process_name = None
        
    def clear_screen(self):
        """Pulisce lo schermo (opzionale)"""
        import os
        os.system('cls' if os.name == 'nt' else 'clear')
        
    def show_main_menu(self):
        """Mostra il menu principale"""
        while True:
            print_header("MEMORY READER - Menu Principale", 70)
            
            if self.current_process:
                print(f"\n🟢 Processo connesso: {self.process_name} (PID: {self.current_process.process_id})")
            else:
                print("\n🔴 Nessun processo connesso")
            
            print("\n📋 MENU PRINCIPALE:")
            print_separator("─", 70)
            print("  1. 🔗 Connetti a un processo")
            print("  2. 📋 Lista tutti i processi attivi")
            print("  3. 📖 Leggi valore dalla memoria")
            print("  4. ✍️  Scrivi valore in memoria")
            print("  5. 🔍 Cerca valore in memoria")
            print("  6. 📊 Hex Dump memoria")
            print("  7. 🗂️  Mostra moduli caricati")
            print("  8. 🎯 Pattern Scanner")
            print("  9. ℹ️  Info processo corrente")
            print("  0. ❌ Esci")
            print_separator("─", 70)
            
            choice = input("\n👉 Seleziona un'opzione: ").strip()
            
            if choice == "1":
                self.connect_to_process()
            elif choice == "2":
                self.list_all_processes()
            elif choice == "3":
                self.read_memory_value()
            elif choice == "4":
                self.write_memory_value()
            elif choice == "5":
                self.search_value()
            elif choice == "6":
                self.hex_dump()
            elif choice == "7":
                self.show_modules()
            elif choice == "8":
                self.pattern_scanner_menu()
            elif choice == "9":
                self.show_process_info()
            elif choice == "0":
                if confirm_action("Sei sicuro di voler uscire?"):
                    print("\n👋 Arrivederci!")
                    break
            else:
                print("\n❌ Opzione non valida!")
                input("\nPremi INVIO per continuare...")
    
    def connect_to_process(self):
        """Menu per connettersi a un processo"""
        print_header("Connetti a un Processo")
        
        print("\n📋 Ultimi 15 processi:")
        processes = self.process_manager.list_processes()
        
        for i, proc in enumerate(processes[:15], 1):
            print(f"  {i:2}. {proc['name']:30} (PID: {proc['pid']})")
        
        print_separator()
        process_name = input("\n👉 Nome del processo (es: notepad.exe): ").strip()
        
        if not process_name:
            print("❌ Nome processo vuoto!")
            input("\nPremi INVIO per continuare...")
            return
        
        print(f"\n🔄 Connessione a {process_name}...")
        process = self.process_manager.attach_to_process(process_name)
        
        if process:
            self.current_process = process
            self.process_name = process_name
            self.reader = MemoryReader(process)
            self.scanner = PatternScanner(process)
            
            print(f"\n✅ Connesso con successo!")
            print(f"   PID: {process.process_id}")
            
            try:
                main_module = pymem.process.module_from_name(
                    process.process_handle, 
                    process_name
                )
                print(f"   Base Address: {format_address(main_module.lpBaseOfDll)}")
            except:
                pass
            
            self.logger.info(f"Connesso a {process_name}")
        else:
            print("\n❌ Impossibile connettersi al processo!")
        
        input("\nPremi INVIO per continuare...")
    
    def list_all_processes(self):
        """Lista tutti i processi"""
        print_header("Lista Processi Attivi")
        
        processes = self.process_manager.list_processes()
        
        print(f"\n📊 Trovati {len(processes)} processi\n")
        
        for i, proc in enumerate(processes[:50], 1):
            print(f"{i:3}. {proc['name']:35} (PID: {proc['pid']:6})")
        
        if len(processes) > 50:
            print(f"\n... e altri {len(processes) - 50} processi")
        
        input("\nPremi INVIO per continuare...")
    
    def read_memory_value(self):
        """Menu per leggere un valore dalla memoria"""
        if not self._check_connection():
            return
        
        print_header("Leggi Valore dalla Memoria")
        
        address = safe_int_input("\n👉 Indirizzo (hex con 0x): ", 0)
        
        if address == 0:
            print("❌ Indirizzo non valido!")
            input("\nPremi INVIO per continuare...")
            return
        
        print("\n📖 Tipo di dato:")
        print("  1. Intero (4 byte)")
        print("  2. Long (8 byte)")
        print("  3. Float (4 byte)")
        print("  4. Double (8 byte)")
        print("  5. Stringa")
        print("  6. Bytes (custom)")
        
        type_choice = input("\n👉 Seleziona tipo: ").strip()
        
        print(f"\n🔍 Lettura da {format_address(address)}...")
        
        if type_choice == "1":
            value = self.reader.read_int(address)
            if value is not None:
                print(f"✅ Valore (int): {value}")
        elif type_choice == "2":
            value = self.reader.read_long(address)
            if value is not None:
                print(f"✅ Valore (long): {value}")
        elif type_choice == "3":
            value = self.reader.read_float(address)
            if value is not None:
                print(f"✅ Valore (float): {value}")
        elif type_choice == "4":
            value = self.reader.read_double(address)
            if value is not None:
                print(f"✅ Valore (double): {value}")
        elif type_choice == "5":
            max_len = safe_int_input("Lunghezza massima (default 256): ", 256)
            value = self.reader.read_string(address, max_len)
            if value is not None:
                print(f"✅ Valore (string): {value}")
        elif type_choice == "6":
            length = safe_int_input("Numero di bytes: ", 16)
            value = self.reader.read_bytes(address, length)
            if value is not None:
                print(f"✅ Bytes: {value.hex()}")
        else:
            print("❌ Tipo non valido!")
        
        input("\nPremi INVIO per continuare...")
    
    def write_memory_value(self):
        """Menu per scrivere un valore in memoria"""
        if not self._check_connection():
            return
        
        print_header("Scrivi Valore in Memoria")
        print("\n⚠️  ATTENZIONE: Modificare la memoria può causare crash!")
        
        if not confirm_action("Vuoi continuare?"):
            return
        
        address = safe_int_input("\n👉 Indirizzo (hex con 0x): ", 0)
        
        if address == 0:
            print("❌ Indirizzo non valido!")
            input("\nPremi INVIO per continuare...")
            return
        
        print("\n📝 Tipo di dato:")
        print("  1. Intero (4 byte)")
        print("  2. Float (4 byte)")
        
        type_choice = input("\n👉 Seleziona tipo: ").strip()
        
        if type_choice == "1":
            value = safe_int_input("Valore intero da scrivere: ", 0)
            if self.reader.write_int(address, value):
                print(f"✅ Valore {value} scritto a {format_address(address)}")
            else:
                print("❌ Errore durante la scrittura!")
        elif type_choice == "2":
            try:
                value = float(input("Valore float da scrivere: ").strip())
                if self.reader.write_float(address, value):
                    print(f"✅ Valore {value} scritto a {format_address(address)}")
                else:
                    print("❌ Errore durante la scrittura!")
            except ValueError:
                print("❌ Valore float non valido!")
        else:
            print("❌ Tipo non valido!")
        
        input("\nPremi INVIO per continuare...")
    
    def search_value(self):
        """Menu per cercare un valore in memoria"""
        if not self._check_connection():
            return
        
        print_header("Cerca Valore in Memoria")
        
        print("\n🔍 Tipo di ricerca:")
        print("  1. Cerca intero")
        print("  2. Cerca stringa")
        
        search_type = input("\n👉 Seleziona tipo: ").strip()
        
        if search_type == "1":
            value = safe_int_input("Valore intero da cercare: ", 0)
            if value == 0:
                print("❌ Valore non valido!")
            else:
                print(f"\n🔄 Ricerca di {value} in corso...")
                addresses = self.scanner.scan_for_value(value)
                
                if addresses:
                    print(f"\n✅ Trovato in {len(addresses)} posizioni:")
                    for i, addr in enumerate(addresses[:10], 1):
                        print(f"  {i}. {format_address(addr)}")
                    
                    if len(addresses) > 10:
                        print(f"  ... e altre {len(addresses) - 10} posizioni")
                else:
                    print("❌ Valore non trovato!")
        
        elif search_type == "2":
            text = input("Stringa da cercare: ").strip()
            if not text:
                print("❌ Stringa vuota!")
            else:
                print(f"\n🔄 Ricerca di '{text}' in corso...")
                addresses = self.scanner.scan_string(text)
                
                if addresses:
                    print(f"\n✅ Trovato in {len(addresses)} posizioni:")
                    for i, addr in enumerate(addresses[:10], 1):
                        print(f"  {i}. {format_address(addr)}")
                else:
                    print("❌ Stringa non trovata!")
        else:
            print("❌ Tipo non valido!")
        
        input("\nPremi INVIO per continuare...")
    
    def hex_dump(self):
        """Menu per fare un hex dump"""
        if not self._check_connection():
            return
        
        print_header("Hex Dump Memoria")
        
        address = safe_int_input("\n👉 Indirizzo (hex con 0x): ", 0)
        
        if address == 0:
            print("❌ Indirizzo non valido!")
            input("\nPremi INVIO per continuare...")
            return
        
        size = safe_int_input("Numero di bytes (default 256): ", 256)
        
        print(f"\n🔄 Dump in corso...")
        dump = self.reader.dump_memory(address, size)
        
        if dump:
            print(dump)
        else:
            print("❌ Impossibile fare il dump!")
        
        input("\nPremi INVIO per continuare...")
    
    def show_modules(self):
        """Mostra i moduli caricati dal processo"""
        if not self._check_connection():
            return
        
        print_header("Moduli Caricati")
        
        print("\n🔄 Caricamento moduli...")
        modules = self.scanner.list_modules()
        
        if modules:
            print(f"\n📚 Trovati {len(modules)} moduli:\n")
            
            for i, module in enumerate(modules[:30], 1):
                print(f"{i:3}. {module['name']:40}")
                print(f"     Base: {format_address(module['base_address'])} | Size: {module['size']:,} bytes")
            
            if len(modules) > 30:
                print(f"\n... e altri {len(modules) - 30} moduli")
        else:
            print("❌ Nessun modulo trovato!")
        
        input("\nPremi INVIO per continuare...")
    
    def pattern_scanner_menu(self):
        """Menu per il pattern scanner"""
        if not self._check_connection():
            return
        
        print_header("Pattern Scanner")
        
        print("\n📝 Pattern in formato: AB CD ?? EF")
        print("   (?? = wildcard per qualsiasi byte)")
        
        pattern = input("\n👉 Inserisci pattern: ").strip()
        
        if not pattern:
            print("❌ Pattern vuoto!")
            input("\nPremi INVIO per continuare...")
            return
        
        print(f"\n🔄 Ricerca pattern in corso...")
        address = self.scanner.pattern_scan(pattern)
        
        if address:
            print(f"\n✅ Pattern trovato a: {format_address(address)}")
        else:
            print("❌ Pattern non trovato!")
        
        input("\nPremi INVIO per continuare...")
    
    def show_process_info(self):
        """Mostra informazioni sul processo corrente"""
        if not self._check_connection():
            return
        
        print_header("Informazioni Processo")
        
        info = self.process_manager.get_process_info()
        
        if info:
            print(f"\n📊 Dettagli processo:")
            print(f"  Nome: {info['name']}")
            print(f"  PID: {info['pid']}")
            print(f"  Base Address: {format_address(info['base_address'])}")
            print(f"  Handle: {info['handle']}")
            
            # Info aggiuntive
            try:
                main_module = pymem.process.module_from_name(
                    self.current_process.process_handle,
                    self.process_name
                )
                print(f"  Module Size: {main_module.SizeOfImage:,} bytes")
            except:
                pass
        else:
            print("❌ Impossibile ottenere informazioni!")
        
        input("\nPremi INVIO per continuare...")
    
    def _check_connection(self):
        """Verifica se c'è una connessione attiva"""
        if not self.current_process:
            print("\n❌ Nessun processo connesso!")
            print("   Usa l'opzione 1 per connetterti a un processo.")
            input("\nPremi INVIO per continuare...")
            return False
        return True


def main():
    """Funzione principale"""
    menu = MenuManager()
    
    try:
        menu.show_main_menu()
    except KeyboardInterrupt:
        print("\n\n👋 Interruzione da utente")
    except Exception as e:
        print(f"\n❌ Errore: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
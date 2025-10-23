"""
Memory Scanner Module
Fornisce funzionalità di scansione e ricerca in memoria
"""

import struct
from typing import List, Optional


class MemoryScanner:
    """Scanner per cercare valori specifici in memoria"""
    
    def __init__(self, process_handler):
        """
        Inizializza lo scanner
        
        Args:
            process_handler: Istanza di ProcessHandler collegata a un processo
        """
        self.process = process_handler
        self.pm = process_handler.pm
        
    def search_integer(self, value: int, start_address: int = None, end_address: int = None, max_results: int = 100) -> List[int]:
        """
        Cerca un valore intero (4 bytes) in memoria
        
        Args:
            value: Valore intero da cercare
            start_address: Indirizzo iniziale (opzionale)
            end_address: Indirizzo finale (opzionale)
            max_results: Numero massimo di risultati
            
        Returns:
            Lista di indirizzi dove è stato trovato il valore
        """
        results = []
        
        try:
            # Se non specificati, usa range predefinito
            if start_address is None:
                start_address = 0x10000
            if end_address is None:
                end_address = 0x7FFFFFFF
            
            # Converti il valore in bytes (little-endian, 4 bytes)
            value_bytes = struct.pack('<i', value)
            
            # Dimensione del chunk da leggere per volta (1 MB)
            chunk_size = 1024 * 1024
            current_address = start_address
            
            print(f"🔍 Ricerca di {value} in memoria...")
            print(f"📍 Range: 0x{start_address:X} - 0x{end_address:X}")
            
            scanned_mb = 0
            
            while current_address < end_address and len(results) < max_results:
                try:
                    # Leggi chunk di memoria
                    data = self.pm.read_bytes(current_address, chunk_size)
                    
                    # Cerca il valore nel chunk
                    offset = 0
                    while True:
                        offset = data.find(value_bytes, offset)
                        if offset == -1:
                            break
                        
                        # Indirizzo trovato
                        found_address = current_address + offset
                        results.append(found_address)
                        
                        if len(results) >= max_results:
                            break
                        
                        offset += 1
                    
                    # Aggiorna progress
                    scanned_mb += 1
                    if scanned_mb % 100 == 0:
                        print(f"📊 Scansionati {scanned_mb} MB... (trovati: {len(results)})")
                    
                except:
                    # Memoria non accessibile, salta al prossimo chunk
                    pass
                
                current_address += chunk_size
            
            print(f"✅ Ricerca completata! Trovati {len(results)} risultati")
            
        except Exception as e:
            print(f"❌ Errore durante la ricerca: {e}")
        
        return results
    
    def search_long(self, value: int, start_address: int = None, end_address: int = None, max_results: int = 100) -> List[int]:
        """
        Cerca un valore long (8 bytes) in memoria
        
        Args:
            value: Valore long da cercare
            start_address: Indirizzo iniziale (opzionale)
            end_address: Indirizzo finale (opzionale)
            max_results: Numero massimo di risultati
            
        Returns:
            Lista di indirizzi dove è stato trovato il valore
        """
        results = []
        
        try:
            if start_address is None:
                start_address = 0x10000
            if end_address is None:
                end_address = 0x7FFFFFFF
            
            # Converti il valore in bytes (little-endian, 8 bytes)
            value_bytes = struct.pack('<q', value)
            
            chunk_size = 1024 * 1024
            current_address = start_address
            
            print(f"🔍 Ricerca di {value} (long) in memoria...")
            
            while current_address < end_address and len(results) < max_results:
                try:
                    data = self.pm.read_bytes(current_address, chunk_size)
                    
                    offset = 0
                    while True:
                        offset = data.find(value_bytes, offset)
                        if offset == -1:
                            break
                        
                        found_address = current_address + offset
                        results.append(found_address)
                        
                        if len(results) >= max_results:
                            break
                        
                        offset += 1
                    
                except:
                    pass
                
                current_address += chunk_size
            
            print(f"✅ Trovati {len(results)} risultati")
            
        except Exception as e:
            print(f"❌ Errore durante la ricerca: {e}")
        
        return results
    
    def search_float(self, value: float, start_address: int = None, end_address: int = None, max_results: int = 100) -> List[int]:
        """
        Cerca un valore float (4 bytes) in memoria
        
        Args:
            value: Valore float da cercare
            start_address: Indirizzo iniziale (opzionale)
            end_address: Indirizzo finale (opzionale)
            max_results: Numero massimo di risultati
            
        Returns:
            Lista di indirizzi dove è stato trovato il valore
        """
        results = []
        
        try:
            if start_address is None:
                start_address = 0x10000
            if end_address is None:
                end_address = 0x7FFFFFFF
            
            # Converti il valore in bytes (little-endian, 4 bytes float)
            value_bytes = struct.pack('<f', value)
            
            chunk_size = 1024 * 1024
            current_address = start_address
            
            print(f"🔍 Ricerca di {value} (float) in memoria...")
            
            while current_address < end_address and len(results) < max_results:
                try:
                    data = self.pm.read_bytes(current_address, chunk_size)
                    
                    offset = 0
                    while True:
                        offset = data.find(value_bytes, offset)
                        if offset == -1:
                            break
                        
                        found_address = current_address + offset
                        results.append(found_address)
                        
                        if len(results) >= max_results:
                            break
                        
                        offset += 1
                    
                except:
                    pass
                
                current_address += chunk_size
            
            print(f"✅ Trovati {len(results)} risultati")
            
        except Exception as e:
            print(f"❌ Errore durante la ricerca: {e}")
        
        return results
    
    def search_string(self, text: str, start_address: int = None, end_address: int = None, max_results: int = 100) -> List[int]:
        """
        Cerca una stringa in memoria
        
        Args:
            text: Testo da cercare
            start_address: Indirizzo iniziale (opzionale)
            end_address: Indirizzo finale (opzionale)
            max_results: Numero massimo di risultati
            
        Returns:
            Lista di indirizzi dove è stata trovata la stringa
        """
        results = []
        
        try:
            if start_address is None:
                start_address = 0x10000
            if end_address is None:
                end_address = 0x7FFFFFFF
            
            # Converti la stringa in bytes (UTF-8)
            text_bytes = text.encode('utf-8')
            
            chunk_size = 1024 * 1024
            current_address = start_address
            
            print(f"🔍 Ricerca di '{text}' in memoria...")
            
            while current_address < end_address and len(results) < max_results:
                try:
                    data = self.pm.read_bytes(current_address, chunk_size)
                    
                    offset = 0
                    while True:
                        offset = data.find(text_bytes, offset)
                        if offset == -1:
                            break
                        
                        found_address = current_address + offset
                        results.append(found_address)
                        
                        if len(results) >= max_results:
                            break
                        
                        offset += 1
                    
                except:
                    pass
                
                current_address += chunk_size
            
            print(f"✅ Trovati {len(results)} risultati")
            
        except Exception as e:
            print(f"❌ Errore durante la ricerca: {e}")
        
        return results
    
    def search_pattern(self, pattern: str, start_address: int = None, end_address: int = None) -> Optional[int]:
        """
        Cerca un pattern di bytes in memoria (es: "AB CD ?? EF")
        
        Args:
            pattern: Pattern da cercare (formato hex con ?? per wildcard)
            start_address: Indirizzo iniziale (opzionale)
            end_address: Indirizzo finale (opzionale)
            
        Returns:
            Primo indirizzo trovato o None
        """
        try:
            if start_address is None:
                start_address = 0x10000
            if end_address is None:
                end_address = 0x7FFFFFFF
            
            # Converte il pattern in bytes
            pattern_parts = pattern.split()
            pattern_bytes = bytearray()
            mask = bytearray()
            
            for part in pattern_parts:
                if part == "??":
                    pattern_bytes.append(0)
                    mask.append(0)
                else:
                    pattern_bytes.append(int(part, 16))
                    mask.append(0xFF)
            
            chunk_size = 1024 * 1024
            current_address = start_address
            
            print(f"🔍 Ricerca pattern: {pattern}")
            
            while current_address < end_address:
                try:
                    data = self.pm.read_bytes(current_address, chunk_size)
                    
                    # Cerca il pattern
                    for i in range(len(data) - len(pattern_bytes) + 1):
                        match = True
                        for j in range(len(pattern_bytes)):
                            if mask[j] != 0 and data[i + j] != pattern_bytes[j]:
                                match = False
                                break
                        
                        if match:
                            found_address = current_address + i
                            print(f"✅ Pattern trovato a: 0x{found_address:X}")
                            return found_address
                    
                except:
                    pass
                
                current_address += chunk_size
            
            print(f"❌ Pattern non trovato")
            return None
            
        except Exception as e:
            print(f"❌ Errore durante il pattern scan: {e}")
            return None
    
    def search_value(self, value, value_type: str = "int", **kwargs) -> List[int]:
        """
        Funzione generica per cercare valori in memoria
        
        Args:
            value: Valore da cercare
            value_type: Tipo del valore ("int", "long", "float", "string")
            **kwargs: Parametri aggiuntivi (start_address, end_address, max_results)
            
        Returns:
            Lista di indirizzi trovati
        """
        if value_type == "int":
            return self.search_integer(int(value), **kwargs)
        elif value_type == "long":
            return self.search_long(int(value), **kwargs)
        elif value_type == "float":
            return self.search_float(float(value), **kwargs)
        elif value_type == "string":
            return self.search_string(str(value), **kwargs)
        else:
            print(f"❌ Tipo non supportato: {value_type}")
            return []
    
    def hex_dump(self, address: int, size: int = 256) -> str:
        """
        Crea un hex dump della memoria
        
        Args:
            address: Indirizzo iniziale
            size: Numero di bytes da leggere
            
        Returns:
            Stringa con hex dump formattato
        """
        try:
            data = self.pm.read_bytes(address, size)
            
            output = []
            output.append(f"\n{'='*60}")
            output.append(f"Hex Dump - Indirizzo: 0x{address:X} - Size: {size} bytes")
            output.append(f"{'='*60}\n")
            
            for i in range(0, len(data), 16):
                # Indirizzo
                line_addr = address + i
                hex_part = f"0x{line_addr:08X}  "
                
                # Hex bytes
                hex_bytes = []
                ascii_part = ""
                
                for j in range(16):
                    if i + j < len(data):
                        byte = data[i + j]
                        hex_bytes.append(f"{byte:02X}")
                        # ASCII (printable chars only)
                        if 32 <= byte <= 126:
                            ascii_part += chr(byte)
                        else:
                            ascii_part += "."
                    else:
                        hex_bytes.append("  ")
                        ascii_part += " "
                
                # Formatta con spazio ogni 8 bytes
                hex_part += " ".join(hex_bytes[:8]) + "  " + " ".join(hex_bytes[8:])
                hex_part += f"  |{ascii_part}|"
                
                output.append(hex_part)
            
            output.append(f"\n{'='*60}\n")
            
            return "\n".join(output)
            
        except Exception as e:
            return f"❌ Errore durante hex dump: {e}"
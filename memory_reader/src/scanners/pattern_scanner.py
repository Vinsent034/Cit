"""
Pattern Scanner - Ricerca pattern in memoria
Trova sequenze di bytes e pattern nella memoria del processo
"""

import pymem
from typing import List, Optional, Tuple
import re


class PatternScanner:
    """
    Scanner per trovare pattern di bytes in memoria
    """
    
    def __init__(self, process: pymem.Pymem):
        """
        Inizializza lo scanner
        
        Args:
            process: Oggetto Pymem connesso a un processo
        """
        self.process = process
        
    def pattern_scan(self, pattern: str, module_name: Optional[str] = None) -> Optional[int]:
        """
        Cerca un pattern di bytes nella memoria
        
        Args:
            pattern: Pattern in formato "AB CD ?? EF" (?? = wildcard)
            module_name: Nome del modulo dove cercare (None = processo principale)
            
        Returns:
            Indirizzo del primo match o None
        """
        try:
            if module_name:
                module = pymem.process.module_from_name(
                    self.process.process_handle, 
                    module_name
                )
                return pymem.pattern.pattern_scan_module(
                    self.process.process_handle,
                    module,
                    pattern
                )
            else:
                return pymem.pattern.pattern_scan_all(
                    self.process.process_handle,
                    pattern
                )
        except Exception as e:
            print(f"❌ Errore durante il pattern scan: {e}")
            return None
    
    def scan_for_value(self, value: int, value_type: str = 'int') -> List[int]:
        """
        Cerca un valore specifico in memoria
        
        Args:
            value: Valore da cercare
            value_type: Tipo di dato ('int', 'float', 'long')
            
        Returns:
            Lista di indirizzi dove è stato trovato il valore
        """
        addresses = []
        
        try:
            # Converti il valore in bytes secondo il tipo
            if value_type == 'int':
                byte_pattern = value.to_bytes(4, byteorder='little', signed=True)
            elif value_type == 'long':
                byte_pattern = value.to_bytes(8, byteorder='little', signed=True)
            elif value_type == 'float':
                import struct
                byte_pattern = struct.pack('f', value)
            else:
                print(f"❌ Tipo non supportato: {value_type}")
                return addresses
            
            # Converti in pattern string
            pattern = " ".join(f"{b:02X}" for b in byte_pattern)
            
            # Cerca nella memoria
            address = self.pattern_scan(pattern)
            if address:
                addresses.append(address)
                
        except Exception as e:
            print(f"❌ Errore durante la ricerca del valore: {e}")
            
        return addresses
    
    def scan_string(self, text: str, encoding: str = 'utf-8') -> List[int]:
        """
        Cerca una stringa in memoria
        
        Args:
            text: Testo da cercare
            encoding: Encoding della stringa
            
        Returns:
            Lista di indirizzi dove è stata trovata la stringa
        """
        addresses = []
        
        try:
            # Converti la stringa in bytes
            byte_pattern = text.encode(encoding)
            
            # Converti in pattern string
            pattern = " ".join(f"{b:02X}" for b in byte_pattern)
            
            # Cerca nella memoria
            address = self.pattern_scan(pattern)
            if address:
                addresses.append(address)
                
        except Exception as e:
            print(f"❌ Errore durante la ricerca della stringa: {e}")
            
        return addresses
    
    def get_module_info(self, module_name: str) -> Optional[dict]:
        """
        Ottiene informazioni su un modulo caricato
        
        Args:
            module_name: Nome del modulo (es. "kernel32.dll")
            
        Returns:
            Dizionario con informazioni sul modulo
        """
        try:
            module = pymem.process.module_from_name(
                self.process.process_handle,
                module_name
            )
            
            return {
                'name': module.name,
                'base_address': module.lpBaseOfDll,
                'size': module.SizeOfImage,
                'entry_point': module.EntryPoint
            }
        except Exception as e:
            print(f"❌ Errore nel recupero info modulo: {e}")
            return None
    
    def list_modules(self) -> List[dict]:
        """
        Lista tutti i moduli caricati dal processo
        
        Returns:
            Lista di dizionari con info sui moduli
        """
        modules = []
        
        try:
            module_list = list(pymem.process.enum_process_module(
                self.process.process_handle
            ))
            
            for module in module_list:
                modules.append({
                    'name': module.name,
                    'base_address': module.lpBaseOfDll,
                    'size': module.SizeOfImage
                })
                
        except Exception as e:
            print(f"❌ Errore nell'enumerazione moduli: {e}")
            
        return modules

"""
Memory Reader - Lettura della memoria
Fornisce metodi per leggere diversi tipi di dati dalla memoria
"""

import pymem
from typing import Optional, List
import struct


class MemoryReader:
    """
    Classe per leggere dati dalla memoria di un processo
    """
    
    def __init__(self, process: pymem.Pymem):
        """
        Inizializza il Memory Reader
        
        Args:
            process: Oggetto Pymem connesso a un processo
        """
        self.process = process
        
    def read_int(self, address: int) -> Optional[int]:
        """
        Legge un intero a 32 bit (4 bytes)
        
        Args:
            address: Indirizzo di memoria
            
        Returns:
            Valore intero o None se errore
        """
        try:
            return self.process.read_int(address)
        except Exception as e:
            print(f"❌ Errore lettura int a 0x{address:X}: {e}")
            return None
    
    def read_long(self, address: int) -> Optional[int]:
        """
        Legge un intero a 64 bit (8 bytes)
        
        Args:
            address: Indirizzo di memoria
            
        Returns:
            Valore long o None se errore
        """
        try:
            return self.process.read_longlong(address)
        except Exception as e:
            print(f"❌ Errore lettura long a 0x{address:X}: {e}")
            return None
    
    def read_float(self, address: int) -> Optional[float]:
        """
        Legge un float (4 bytes)
        
        Args:
            address: Indirizzo di memoria
            
        Returns:
            Valore float o None se errore
        """
        try:
            return self.process.read_float(address)
        except Exception as e:
            print(f"❌ Errore lettura float a 0x{address:X}: {e}")
            return None
    
    def read_double(self, address: int) -> Optional[float]:
        """
        Legge un double (8 bytes)
        
        Args:
            address: Indirizzo di memoria
            
        Returns:
            Valore double o None se errore
        """
        try:
            return self.process.read_double(address)
        except Exception as e:
            print(f"❌ Errore lettura double a 0x{address:X}: {e}")
            return None
    
    def read_bytes(self, address: int, length: int) -> Optional[bytes]:
        """
        Legge una sequenza di bytes
        
        Args:
            address: Indirizzo di memoria
            length: Numero di bytes da leggere
            
        Returns:
            Bytes letti o None se errore
        """
        try:
            return self.process.read_bytes(address, length)
        except Exception as e:
            print(f"❌ Errore lettura bytes a 0x{address:X}: {e}")
            return None
    
    def read_string(self, address: int, max_length: int = 256) -> Optional[str]:
        """
        Legge una stringa ASCII
        
        Args:
            address: Indirizzo di memoria
            max_length: Lunghezza massima da leggere
            
        Returns:
            Stringa letta o None se errore
        """
        try:
            return self.process.read_string(address, max_length)
        except Exception as e:
            print(f"❌ Errore lettura stringa a 0x{address:X}: {e}")
            return None
    
    def read_pointer(self, address: int, offsets: List[int] = None) -> Optional[int]:
        """
        Legge un pointer e segue gli offsets
        
        Args:
            address: Indirizzo base
            offsets: Lista di offsets da seguire
            
        Returns:
            Indirizzo finale o None se errore
        """
        try:
            current_address = address
            
            if offsets:
                for offset in offsets[:-1]:
                    current_address = self.process.read_longlong(current_address)
                    if current_address:
                        current_address += offset
                    else:
                        return None
                
                # Ultimo offset
                current_address = self.process.read_longlong(current_address)
                if current_address and offsets:
                    current_address += offsets[-1]
            else:
                current_address = self.process.read_longlong(current_address)
                
            return current_address
        except Exception as e:
            print(f"❌ Errore lettura pointer a 0x{address:X}: {e}")
            return None
    
    def write_int(self, address: int, value: int) -> bool:
        """
        Scrive un intero a 32 bit
        
        Args:
            address: Indirizzo di memoria
            value: Valore da scrivere
            
        Returns:
            True se successo, False altrimenti
        """
        try:
            self.process.write_int(address, value)
            return True
        except Exception as e:
            print(f"❌ Errore scrittura int a 0x{address:X}: {e}")
            return False
    
    def write_float(self, address: int, value: float) -> bool:
        """
        Scrive un float
        
        Args:
            address: Indirizzo di memoria
            value: Valore da scrivere
            
        Returns:
            True se successo, False altrimenti
        """
        try:
            self.process.write_float(address, value)
            return True
        except Exception as e:
            print(f"❌ Errore scrittura float a 0x{address:X}: {e}")
            return False
    
    def write_bytes(self, address: int, value: bytes) -> bool:
        """
        Scrive una sequenza di bytes
        
        Args:
            address: Indirizzo di memoria
            value: Bytes da scrivere
            
        Returns:
            True se successo, False altrimenti
        """
        try:
            self.process.write_bytes(address, value, len(value))
            return True
        except Exception as e:
            print(f"❌ Errore scrittura bytes a 0x{address:X}: {e}")
            return False
    
    def dump_memory(self, address: int, size: int) -> Optional[str]:
        """
        Dump della memoria in formato hex
        
        Args:
            address: Indirizzo di inizio
            size: Numero di bytes da dumpare
            
        Returns:
            Stringa formattata con hex dump
        """
        try:
            data = self.read_bytes(address, size)
            if not data:
                return None
                
            result = []
            result.append(f"\nMemory Dump @ 0x{address:X} ({size} bytes):")
            result.append("=" * 60)
            
            for i in range(0, len(data), 16):
                chunk = data[i:i+16]
                
                # Indirizzo
                hex_str = f"{address + i:08X}  "
                
                # Bytes in hex
                hex_bytes = " ".join(f"{b:02X}" for b in chunk)
                hex_str += f"{hex_bytes:<48}  "
                
                # ASCII rappresentation
                ascii_str = "".join(chr(b) if 32 <= b < 127 else "." for b in chunk)
                hex_str += ascii_str
                
                result.append(hex_str)
            
            return "\n".join(result)
        except Exception as e:
            print(f"❌ Errore dump memoria: {e}")
            return None

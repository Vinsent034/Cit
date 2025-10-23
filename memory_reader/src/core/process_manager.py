"""
Process Manager - Gestione dei processi
Gestisce l'attacco e la gestione dei processi in esecuzione
"""

import pymem
import pymem.process
from typing import Optional, List, Dict
import psutil


class ProcessManager:
    """
    Gestisce l'attacco ai processi e fornisce informazioni sui processi attivi
    """
    
    def __init__(self):
        """Inizializza il Process Manager"""
        self.current_process: Optional[pymem.Pymem] = None
        self.process_name: Optional[str] = None
        
    def list_processes(self) -> List[Dict[str, any]]:
        """
        Restituisce una lista di tutti i processi attivi
        
        Returns:
            Lista di dizionari con informazioni sui processi
        """
        processes = []
        
        for proc in psutil.process_iter(['pid', 'name', 'memory_info']):
            try:
                info = proc.info
                processes.append({
                    'pid': info['pid'],
                    'name': info['name'],
                    'memory': info['memory_info'].rss if info['memory_info'] else 0
                })
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
                
        return sorted(processes, key=lambda x: x['name'].lower())
    
    def attach_to_process(self, process_name: str) -> Optional[pymem.Pymem]:
        """
        Si attacca a un processo specifico per nome
        
        Args:
            process_name: Nome del processo (es. "notepad.exe")
            
        Returns:
            Oggetto Pymem se successo, None altrimenti
        """
        try:
            self.current_process = pymem.Pymem(process_name)
            self.process_name = process_name
            return self.current_process
        except pymem.exception.ProcessNotFound:
            print(f"❌ Processo '{process_name}' non trovato")
            return None
        except pymem.exception.CouldNotOpenProcess:
            print(f"❌ Impossibile aprire il processo '{process_name}' - Privilegi amministrativi necessari")
            return None
        except Exception as e:
            print(f"❌ Errore durante l'attacco al processo: {e}")
            return None
    
    def attach_to_pid(self, pid: int) -> Optional[pymem.Pymem]:
        """
        Si attacca a un processo specifico per PID
        
        Args:
            pid: Process ID
            
        Returns:
            Oggetto Pymem se successo, None altrimenti
        """
        try:
            process_name = pymem.process.process_from_id(pid).name
            return self.attach_to_process(process_name)
        except Exception as e:
            print(f"❌ Errore durante l'attacco al PID {pid}: {e}")
            return None
    
    def get_process_info(self) -> Optional[Dict[str, any]]:
        """
        Restituisce informazioni sul processo attualmente connesso
        
        Returns:
            Dizionario con informazioni sul processo
        """
        if not self.current_process:
            return None
            
        try:
            return {
                'name': self.process_name,
                'pid': self.current_process.process_id,
                'base_address': self.current_process.process_base.base_address,
                'handle': self.current_process.process_handle
            }
        except Exception as e:
            print(f"❌ Errore nel recupero informazioni: {e}")
            return None
    
    def close(self):
        """Chiude la connessione al processo"""
        if self.current_process:
            try:
                self.current_process.close_process()
                self.current_process = None
                self.process_name = None
            except Exception as e:
                print(f"⚠️ Errore durante la chiusura: {e}")
    
    def __del__(self):
        """Destructor - chiude automaticamente il processo"""
        self.close()

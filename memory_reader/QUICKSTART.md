# 🚀 Guida Rapida - Memory Reader

## Installazione

1. **Installa Python 3.7+** (se non già installato)

2. **Esegui il setup automatico:**
   ```bash
   python setup.py
   ```
   
   Oppure manualmente:
   ```bash
   pip install -r requirements.txt
   ```

## Primo Utilizzo

### 1. Avvia l'applicazione principale
```bash
python main.py
```

### 2. Oppure prova gli esempi
```bash
python examples/esempio_base.py
```

## Esempi Rapidi

### Leggere un valore intero
```python
from src.core.process_manager import ProcessManager
from src.core.memory_reader import MemoryReader

# Attacca al processo
pm = ProcessManager()
process = pm.attach_to_process("notepad.exe")

# Leggi memoria
reader = MemoryReader(process)
value = reader.read_int(0x12345678)  # Sostituisci con indirizzo reale
print(f"Valore: {value}")
```

### Cercare un valore in memoria
```python
from src.scanners.pattern_scanner import PatternScanner

scanner = PatternScanner(process)
addresses = scanner.scan_for_value(1000)  # Cerca il valore 1000

for addr in addresses:
    print(f"Trovato a: 0x{addr:X}")
```

### Dump della memoria
```python
reader = MemoryReader(process)
dump = reader.dump_memory(0x12345678, 256)
print(dump)
```

## Struttura dei Moduli

### 📦 core/
- **process_manager.py** - Gestione processi
- **memory_reader.py** - Lettura/scrittura memoria

### 🔍 scanners/
- **pattern_scanner.py** - Ricerca pattern e valori

### 🛠️ utils/
- **logger.py** - Sistema di logging
- **helpers.py** - Funzioni utility

## Note Importanti

⚠️ **Privilegi Amministrativi**: Su Windows, potrebbero essere necessari privilegi amministrativi per accedere ad alcuni processi.

⚠️ **Solo Uso Personale**: Usa questo strumento solo per scopi educativi e su software di cui possiedi i diritti.

⚠️ **Anti-Cheat**: Non usare su giochi online con sistemi anti-cheat, potresti essere bannato.

## Prossimi Passi

1. Esplora i file in `examples/` per vedere altri utilizzi
2. Modifica `config/settings.py` per personalizzare l'applicazione
3. Consulta il README.md per informazioni più dettagliate

## Problemi Comuni

### "Processo non trovato"
- Verifica che il processo sia in esecuzione
- Controlla l'ortografia del nome del processo (include .exe su Windows)

### "Permessi insufficienti"
- Esegui il terminale/IDE come amministratore
- Alcuni processi di sistema potrebbero essere protetti

### "Impossibile leggere l'indirizzo"
- Verifica che l'indirizzo sia valido
- L'indirizzo potrebbe essere cambiato (ASLR)
- Usa uno scanner per trovare gli indirizzi corretti

## Risorse Utili

- [Documentazione Pymem](https://pymem.readthedocs.io/)
- [Cheat Engine](https://www.cheatengine.org/) - Per trovare indirizzi
- [Memory Patterns](https://guidedhacking.com/) - Guide avanzate

---

**Buon coding! 🎯**

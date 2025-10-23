# Memory Reader Project

Applicazione Python per leggere e analizzare la memoria di processi in esecuzione.

## 📁 Struttura del Progetto

```
memory_reader/
├── src/
│   ├── core/           # Componenti principali
│   ├── utils/          # Utility e helper
│   └── scanners/       # Scanner per pattern e indirizzi
├── examples/           # Esempi di utilizzo
├── tests/             # Test unitari
├── config/            # File di configurazione
├── logs/              # File di log
└── main.py            # Entry point principale
```

## 🚀 Installazione

```bash
pip install -r requirements.txt
```

## 💻 Utilizzo Base

```python
from src.core.process_manager import ProcessManager
from src.core.memory_reader import MemoryReader

# Gestisci i processi
pm = ProcessManager()
process = pm.attach_to_process("notepad.exe")

# Leggi la memoria
reader = MemoryReader(process)
value = reader.read_int(0x12345678)
```

## 📝 Note

- Richiede privilegi amministrativi su Windows
- Utilizzare solo per scopi personali ed educativi
- Rispettare le leggi sul copyright e i termini di servizio

## 🔧 To-Do

- [ ] Implementare scanner di pattern
- [ ] Aggiungere supporto per strutture dati complesse
- [ ] Creare GUI opzionale
- [ ] Migliorare logging e error handling

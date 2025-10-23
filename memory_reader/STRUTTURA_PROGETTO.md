# 📁 Struttura del Progetto Memory Reader

```
memory_reader/
│
├── 📄 main.py                      # Entry point principale dell'applicazione
├── 📄 setup.py                     # Script di installazione automatica
├── 📄 requirements.txt             # Dipendenze Python
├── 📄 README.md                    # Documentazione principale
├── 📄 QUICKSTART.md               # Guida rapida per iniziare
├── 📄 .gitignore                  # File da escludere da Git
│
├── 📁 src/                         # Codice sorgente principale
│   ├── 📄 __init__.py
│   │
│   ├── 📁 core/                    # Componenti principali
│   │   ├── 📄 __init__.py
│   │   ├── 📄 process_manager.py  # Gestione processi
│   │   └── 📄 memory_reader.py    # Lettura/scrittura memoria
│   │
│   ├── 📁 scanners/                # Scanner per pattern
│   │   ├── 📄 __init__.py
│   │   └── 📄 pattern_scanner.py  # Ricerca pattern e valori
│   │
│   └── 📁 utils/                   # Utility e helper
│       ├── 📄 __init__.py
│       ├── 📄 logger.py           # Sistema di logging
│       └── 📄 helpers.py          # Funzioni helper
│
├── 📁 examples/                    # Esempi di utilizzo
│   └── 📄 esempio_base.py         # Esempi pratici
│
├── 📁 config/                      # File di configurazione
│   └── 📄 settings.py             # Impostazioni applicazione
│
├── 📁 tests/                       # Test unitari (da implementare)
│
└── 📁 logs/                        # File di log (generati automaticamente)
```

## 📋 Descrizione dei Moduli

### 🎯 Core Modules

#### **process_manager.py**
- Gestisce l'attacco ai processi
- Lista processi attivi
- Fornisce informazioni sui processi
- Funzioni principali:
  - `list_processes()` - Lista tutti i processi
  - `attach_to_process(name)` - Attacca per nome
  - `attach_to_pid(pid)` - Attacca per PID
  - `get_process_info()` - Info sul processo corrente

#### **memory_reader.py**
- Lettura di diversi tipi di dati
- Scrittura in memoria
- Dump della memoria
- Funzioni principali:
  - `read_int(address)` - Leggi intero
  - `read_float(address)` - Leggi float
  - `read_bytes(address, length)` - Leggi bytes
  - `read_string(address)` - Leggi stringa
  - `write_int(address, value)` - Scrivi intero
  - `dump_memory(address, size)` - Hex dump

### 🔍 Scanner Modules

#### **pattern_scanner.py**
- Ricerca pattern di bytes
- Scan di valori specifici
- Gestione moduli
- Funzioni principali:
  - `pattern_scan(pattern)` - Cerca pattern
  - `scan_for_value(value)` - Cerca valore
  - `scan_string(text)` - Cerca stringa
  - `list_modules()` - Lista moduli caricati

### 🛠️ Utility Modules

#### **logger.py**
- Sistema di logging centralizzato
- Log su file e console
- Diversi livelli di log

#### **helpers.py**
- Funzioni di utilità varie
- Formattazione indirizzi
- Conversioni hex/int
- Input sicuri

## 🚀 Come Iniziare

1. **Installazione:**
   ```bash
   python setup.py
   ```

2. **Esegui applicazione principale:**
   ```bash
   python main.py
   ```

3. **Prova gli esempi:**
   ```bash
   python examples/esempio_base.py
   ```

## 🔧 Configurazione

Modifica `config/settings.py` per personalizzare:
- Livello di logging
- Dimensioni di lettura
- Timeout degli scan
- Altre impostazioni

## 📝 Espandere il Progetto

### Aggiungi nuovi scanner:
Crea file in `src/scanners/` con nuove funzionalità di ricerca

### Aggiungi nuove utility:
Crea file in `src/utils/` con funzioni helper

### Aggiungi esempi:
Crea file in `examples/` con casi d'uso specifici

### Aggiungi test:
Crea file in `tests/` per test unitari

## 📚 Dipendenze

- **pymem** - Libreria principale per memory reading
- **psutil** - Gestione processi
- **colorama** - Output colorato (opzionale)
- **loguru** - Logging avanzato (opzionale)

## ⚠️ Note Importanti

- Richiede privilegi amministrativi su Windows
- Usa solo per scopi personali e educativi
- Rispetta le leggi e i termini di servizio
- Non usare su giochi online con anti-cheat

---

**Progetto creato con ❤️ per scopi educativi**

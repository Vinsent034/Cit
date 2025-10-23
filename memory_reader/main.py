"""
Memory Reader - Entry Point Principale
Applicazione per leggere e analizzare la memoria di processi con menu interattivo
"""

import sys
from pathlib import Path

# Aggiungi il path src al PYTHONPATH
sys.path.insert(0, str(Path(__file__).parent / "src"))

from menu_manager import MenuManager


def main():
    """Avvia il menu principale dell'applicazione"""
    menu = MenuManager()
    
    try:
        menu.show_main_menu()
    except KeyboardInterrupt:
        print("\n\n👋 Interruzione da utente. Arrivederci!")
    except Exception as e:
        print(f"\n❌ Errore critico: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
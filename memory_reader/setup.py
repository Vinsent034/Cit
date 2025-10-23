"""
Setup Script - Installazione rapida del progetto
"""

import subprocess
import sys
import os


def check_python_version():
    """Verifica la versione di Python"""
    if sys.version_info < (3, 7):
        print("❌ Python 3.7 o superiore è richiesto")
        sys.exit(1)
    print(f"✓ Python {sys.version_info.major}.{sys.version_info.minor} rilevato")


def install_requirements():
    """Installa le dipendenze"""
    print("\n📦 Installazione dipendenze...")
    try:
        subprocess.check_call([
            sys.executable, 
            "-m", 
            "pip", 
            "install", 
            "-r", 
            "requirements.txt"
        ])
        print("✓ Dipendenze installate con successo")
    except subprocess.CalledProcessError:
        print("❌ Errore nell'installazione delle dipendenze")
        sys.exit(1)


def create_directories():
    """Crea le directory necessarie"""
    print("\n📁 Creazione directory...")
    
    directories = ['logs', 'config', 'examples', 'tests']
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
    
    print("✓ Directory create")


def check_admin_privileges():
    """Verifica i privilegi amministrativi (solo Windows)"""
    if sys.platform == "win32":
        try:
            import ctypes
            is_admin = ctypes.windll.shell32.IsUserAnAdmin()
            if not is_admin:
                print("\n⚠️  ATTENZIONE: Privilegi amministrativi potrebbero essere necessari")
                print("   Per accedere alla memoria di alcuni processi, esegui come amministratore")
        except:
            pass


def main():
    """Funzione principale di setup"""
    print("=" * 60)
    print(" MEMORY READER - Setup ".center(60))
    print("=" * 60)
    
    # Controlli
    check_python_version()
    create_directories()
    install_requirements()
    check_admin_privileges()
    
    print("\n" + "=" * 60)
    print(" ✓ Setup completato con successo! ".center(60))
    print("=" * 60)
    print("\n📖 Per iniziare:")
    print("   python main.py")
    print("   oppure")
    print("   python examples/esempio_base.py")
    print("\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Setup interrotto dall'utente")
    except Exception as e:
        print(f"\n❌ Errore durante il setup: {e}")

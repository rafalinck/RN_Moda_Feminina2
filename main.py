import sys
import os

# Garante que o diretório atual está no path do Python
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from gui.app import RnModaApp

def main():
    print("Iniciando R&N Moda Feminina...")
    try:
        app = RnModaApp()
        app.mainloop()
    except Exception as e:
        print(f"Ocorreu um erro ao iniciar a aplicação gráfica: {e}")
        print("Por favor, certifique-se de que o Python e o Tkinter estão configurados corretamente.")
        input("Pressione Enter para sair...")

if __name__ == "__main__":
    main()

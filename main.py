import tkinter as tk
from src.gui import InterfaceGraficaLogistica

def main():
    root = tk.Tk()
    app = InterfaceGraficaLogistica(root)
    root.mainloop()

if __name__ == "__main__":
    main()
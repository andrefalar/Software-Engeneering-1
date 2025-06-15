# Punto de entrada de la aplicación gráfica

import tkinter as tk

def launch_app():
    root = tk.Tk()
    root.title("FortiFile")
    root.geometry("600x400")
    root.mainloop()

if __name__ == "__main__":
    launch_app()
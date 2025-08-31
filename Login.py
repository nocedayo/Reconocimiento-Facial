import tkinter as tk
import os
from tkinter import messagebox

# creamos la ventana
ventana = tk.Tk()
ventana.title("Registro de Usuario")
etiqueta = tk.Label(
    ventana,
    text= "Sistema de reconocimiento facial",
    fg="blue",  # Color del texto
    font=("Arial", 14, "bold") # Fuente, tamaño y estilo
)   
#FORMAMOS LA VENTANA
ancho_ventana = 350
alto_ventana = 250

ancho_pantalla = ventana.winfo_screenwidth()
alto_pantalla = ventana.winfo_screenheight()

x = (ancho_pantalla // 2) - (ancho_ventana // 2)
y = (alto_pantalla // 2) - (alto_ventana // 2)

ventana.geometry(f'{ancho_ventana}x{alto_ventana}+{x}+{y}')
etiqueta.pack(pady=20)

def al_hacer_clic():
    messagebox.showinfo("ATENTO","Asegurate de posicionarte frente a la camara ")
    os.system("python app.py")   
    
boton = tk.Button(ventana, text="Ingresar", command=al_hacer_clic)

boton.pack(pady=10)

ventana.mainloop()


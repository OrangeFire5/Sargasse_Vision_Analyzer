#Crea la barra de menu del la UI
import tkinter as tk

class BarraDeMenu(tk.Menu):
    def __init__(self, master = None):
        super().__init__(master)
        self.master = master
        #Menu general
        self.barra_menus = tk.Menu()
        self.menu_archivo = tk.Menu(self.barra_menus, tearoff=False)
        self.menu_archivo.add_command(label="Abrir",accelerator="Ctrl+A",command=self.prueba,compound=tk.LEFT)
        self.menu_archivo.add_command(label="Guardar",accelerator="Ctrl+G",command=self.prueba,compound=tk.LEFT)
        self.menu_archivo.add_separator()
        self.menu_archivo.add_command(label="Guardar como...",accelerator="Ctrl+G",command=self.prueba,compound=tk.LEFT)
        #Agrega atajo de teclado
        #self.app.bind_all("<Control-g>", prueba)
        self.menu_archivo.add_separator()
        self.menu_archivo.add_command(label="Salir", command=master.destroy)
        
        #Seccion Opciones
        self.menu_opciones = tk.Menu(self.barra_menus, tearoff=False)
        self.menu_opciones.add_command(label="Opcion1",accelerator="",command=self.prueba,compound=tk.LEFT)

        #Se agregan opciones al menu
        self.barra_menus.add_cascade(menu=self.menu_archivo, label="Archivo")
        self.barra_menus.add_cascade(menu=self.menu_opciones, label="Opciones")
        self.master.config(menu=self.barra_menus)
    def prueba(self):
        print("opcion seleccionada")
    

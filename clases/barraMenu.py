#Crea la barra de menu del la UI
import tkinter as tk

class BarraDeMenu(tk.Menu):
    def __init__(self, master = None,controller=None, gestorArchivos=None):
        super().__init__(master)
        self.master.protocol("WM_DELETE_WINDOW", self.salir)
        self.master = master
        self.controller = controller
        self.gestorArchivos = gestorArchivos
        #Menu general
        self.barra_menus = tk.Menu()

        #Seccion Archivo
        self.menu_archivo = tk.Menu(self.barra_menus, tearoff=False)
        self.menu_archivo.add_command(label="Nuevo proyecto",accelerator="Ctrl+N",command=self.nuevoProyecto,compound=tk.LEFT)
        self.menu_archivo.add_separator()
        self.menu_archivo.add_command(label="Abrir proyecto",accelerator="Ctrl+A",command=self.gestorArchivos.abrirProyecto,compound=tk.LEFT)
        self.menu_archivo.add_separator()
        self.menu_archivo.add_command(label="Guardar",accelerator="Ctrl+G",command=self.gestorArchivos.guardar,compound=tk.LEFT)
        self.menu_archivo.add_command(label="Guardar como...",accelerator="Ctrl+G",command=self.gestorArchivos.guardarComo,compound=tk.LEFT)
        self.menu_archivo.add_separator()
        self.menu_archivo.add_command(label="Salir", command=self.salir)
        #Agrega atajo de teclado
        #self.app.bind_all("<Control-g>", prueba)

        #Seccion Opciones
        self.menu_opciones = tk.Menu(self.barra_menus, tearoff=False)
        self.menu_opciones.add_command(label="Exportar..",accelerator="Ctrl+E",command=self.controller.exportarTodasLasAreas,compound=tk.LEFT)
        
        #Seccion Configuraciones
        self.menu_configuraciones = tk.Menu(self.barra_menus, tearoff=False)
        self.menu_configuraciones.add_command(label="Color de Areas",accelerator="",command=self.gestorArchivos.menuColorAreas,compound=tk.LEFT)
        
        #Seccion ayuda
        self.menu_ayuda = tk.Menu(self.barra_menus, tearoff=False)
        self.menu_ayuda.add_command(label="Manual",accelerator="",command=self.prueba,compound=tk.LEFT)
        self.menu_ayuda.add_command(label="Acerca de...",accelerator="",command=self.prueba,compound=tk.LEFT)
        #Se agregan opciones al menu
        self.barra_menus.add_cascade(menu=self.menu_archivo, label="Archivo")
        self.barra_menus.add_cascade(menu=self.menu_opciones, label="Opciones")
        self.barra_menus.add_cascade(menu=self.menu_configuraciones, label="Configuraciones")
        self.barra_menus.add_cascade(menu=self.menu_ayuda, label="Ayuda")
        self.master.config(menu=self.barra_menus)
    def prueba(self):
        print("opcion seleccionada")
    def nuevoProyecto(self):
        self.master.destroy()
        self.gestorArchivos.nuevoProyecto()
    def salir(self):
        self.gestorArchivos.borrarDatosCarpetaTemporal()
        self.master.destroy()
    

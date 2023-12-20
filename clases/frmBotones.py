#Generacion del marco donde se visualizaran las imagenes
import tkinter as tk

class FrmBotones(tk.Frame):
    def __init__(self, master = None,controlador=None):
        super().__init__(master)
        self.master = master
        self.controller = controlador
        self.config(relief="ridge", bd=5)

        self.createButton()

    def createButton(self):
        self.btnExportarSelecciones =  tk.Button(self)
        self.btnExportarSelecciones.config(text="Exportar\nSelecciones",command=self.controller.exportarTodasLasAreas,state="disabled")
        self.btnExportarSelecciones.place(relx=0.05,rely=0.0625, relwidth=0.90, relheight=0.25)

        self.btnExportarSeleccion=  tk.Button(self)
        self.btnExportarSeleccion.config(text="Exportar\nSeleccion",state="disabled", command=self.controller.exportarImagen)
        self.btnExportarSeleccion.place(relx=0.05,rely=0.375,  relwidth=0.90, relheight=0.25)


        self.btnElimnarSelecciones =  tk.Button(self,state="disabled")
        self.btnElimnarSelecciones.config(text="Eliminar\nseleccion",command=self.controller.eliminarSeleccion,state="disabled")
        self.btnElimnarSelecciones.place(relx=0.05,rely=0.6875,  relwidth=0.90, relheight=0.25)
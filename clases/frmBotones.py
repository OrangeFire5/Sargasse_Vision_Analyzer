#Generacion del marco donde se visualizaran las imagenes
import tkinter as tk

class FrmBotones(tk.Frame):
    def __init__(self, master = None):
        super().__init__(master)
        self.master = master
        self.config(relief="ridge", bd=5)

        self.createButton()

    def createButton(self):
        self.btnGuardarArea =  tk.Button(self)
        self.btnGuardarArea.config(text="Guardar area\nde trabajo")
        self.btnGuardarArea.place(relx=0.05,rely=0.0625, relwidth=0.90, relheight=0.25)

        self.btnGuardarSelecciones=  tk.Button(self)
        self.btnGuardarSelecciones.config(text="Guardar\nselecciones")
        self.btnGuardarSelecciones.place(relx=0.05,rely=0.375,  relwidth=0.90, relheight=0.25)

        self.btnElimnarSelecciones =  tk.Button(self,bg="#B02525",fg="white", font=("Arial", 10, "bold"),state="disabled")
        self.btnElimnarSelecciones.config(text="Eliminar\nseleccion")
        self.btnElimnarSelecciones.place(relx=0.05,rely=0.6875,  relwidth=0.90, relheight=0.25)

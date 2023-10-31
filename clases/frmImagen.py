#Generacion del marco donde se visualizaran las imagenes
import tkinter as tk
import os

class FrmImagen(tk.Frame):
    def __init__(self, master = None):
        super().__init__(master,bg="green")
        self.master = master
        self.config(relief="ridge", bd=5)

        master.rowconfigure(0,weight=1)
        master.columnconfigure(0,weight=1)
        master.columnconfigure(1,weight=1)

        self.rowconfigure(0,weight=5)
        self.rowconfigure(1,weight=1)
        self.rowconfigure(2,weight=1)
        self.columnconfigure(0,weight=1)

        self.createIcono()
        self.createLabel()
        self.createButton()

    def createIcono(self):
        path ="{0}/img/imgBruta.png".format(os.getcwd())
        path =  path.replace("\\","/")
        self.icono = tk.PhotoImage(file=path)
        self.lbIcono =  tk.Label(self, image=self.icono)
        self.lbIcono.grid(column=0,row=0,sticky="nsew")

    def createLabel(self):
        self.lbImagen =  tk.Label(self)
        self.lbImagen.config(text="Imagen Sentinel color real")
        self.lbImagen.grid(column=0,row=1,sticky="nsew", padx=20,pady=10)

    def createButton(self):
        self.btnAbrirImagen =  tk.Button(self)
        self.btnAbrirImagen.config(text="Seleccione una imagen")
        self.btnAbrirImagen.grid(column=0,row=2,sticky="nsew", padx=20,pady=10)

#Generacion del marco donde se visualizaran las imagenes
import tkinter as tk
import os
from frmImagen import *
from frmDatos import *
from frmTablaSelecciones import *

class FrmBotones(tk.Frame):
    def __init__(self, master = None):
        super().__init__(master,bg="red")
        self.master = master
        self.config(relief="ridge", bd=5)

        self.createButton()

    def createButton(self):
        self.btnGuardarArea =  tk.Button(self)
        self.btnGuardarArea.config(text="Guardar area\nde trabajo")
        self.btnGuardarArea.place(relx=0.05,rely=0.0625, relwidth=0.90, relheight=0.25)
        #self.btnGuardarArea.grid(column=0,row=0,sticky="nsew")
        self.btnGuardarSelecciones=  tk.Button(self)
        self.btnGuardarSelecciones.config(text="Guardar\nselecciones")
        self.btnGuardarSelecciones.place(relx=0.05,rely=0.375,  relwidth=0.90, relheight=0.25)
        #self.btnGuardarSelecciones.grid(column=0,row=1,sticky="nsew")
        self.btnElimnarSelecciones =  tk.Button(self,bg="#B02525",fg="white", font=("Arial", 10, "bold"),state="disabled")
        self.btnElimnarSelecciones.config(text="Eliminar\nseleccion")
        self.btnElimnarSelecciones.place(relx=0.05,rely=0.6875,  relwidth=0.90, relheight=0.25)
        #self.btnElimnarSelecciones.grid(column=0,row=2,sticky="nsew")




app = tk.Tk()
app.title("Sargasse Vision Analyzer")
app.geometry("800x500")

app.rowconfigure(0,weight=5)
app.rowconfigure(1,weight=1)
app.rowconfigure(2,weight=1)
app.columnconfigure(0,weight=3)
app.columnconfigure(1,weight=3)
app.columnconfigure(2,weight=3)
app.columnconfigure(3,weight=1)
app.columnconfigure(4,weight=3)
app.columnconfigure(5,weight=3)
app.columnconfigure(6,weight=3)


frameImagen1 = FrmImagen(app).grid(row=0, column=0, columnspan=3, sticky="nsew",padx=2,pady=2)
frameImagen2 = FrmImagen(app).grid(row=0, column=4, columnspan=3, sticky="nsew",padx=2,pady=2)
frameDatos = FrmDatos(app).grid(row=1, column=0,columnspan=7, sticky="nsew",padx=2,pady=2)
frameTablaSelecciones = FrmTablaSelecciones(app).grid(row=2, column=0,columnspan=6, sticky="nsew",padx=2,pady=2)
frameBotones = FrmBotones(app).grid(row=2, column=6, sticky="nsew",padx=2,pady=2)
app.mainloop()
import tkinter as tk
from frmImagen import *
from frmDatos import *
from frmTablaSelecciones import *
from frmBotones import *


class FrmBarraDeVista(tk.Frame):
    def __init__(self, master = None):
        super().__init__(master,bg="gray",width=30, height=100)
        self.master = master
        self.config(relief="ridge", bd=2)
        self.crearBotones()
    def crearBotones(self):
        self.btnAumentoZoom = tk.Button(self)
        self.btnAumentoZoom.config(text="+")
        self.btnAumentoZoom.place(relx=0.06, rely=0.04, relwidth=0.9,relheight=0.20)

        self.btnDiminuyeZoom = tk.Button(self)
        self.btnDiminuyeZoom.config(text="-")

        self.btnDiminuyeZoom.place(relx=0.06, rely=0.28,relwidth=0.9,relheight=0.20)
        self.btnAjusteVista = tk.Button(self)
        self.btnAjusteVista.config(text="A")
        self.btnAjusteVista.place(relx=0.06, rely=0.52,relwidth=0.9,relheight=0.20)

        self.btnSincronizar = tk.Button(self)
        self.btnSincronizar.config(text="=")
        self.btnSincronizar.place(relx=0.06, rely=0.76,relwidth=0.9,relheight=0.20)

app = tk.Tk()
app.title("Sargasse Vision Analyzer")
app.geometry("600x500")


app.rowconfigure(0,weight=5)
app.rowconfigure(1,weight=1)
app.rowconfigure(2,weight=1)
app.columnconfigure(0,weight=7)
app.columnconfigure(1,weight=7)
app.columnconfigure(2,weight=7)
app.columnconfigure(3,weight=1)
app.columnconfigure(4,weight=7)
app.columnconfigure(5,weight=7)
app.columnconfigure(6,weight=7)


frameImagen1 = FrmImagen(app).grid(row=0, column=0, columnspan=3, sticky="nsew",padx=2,pady=2)
frameBarraDeVista = FrmBarraDeVista(app).grid(row=0, column=3, sticky="n")
frameImagen2 = FrmImagen(app).grid(row=0, column=4, columnspan=3, sticky="nsew",padx=2,pady=2)
frameDatos = FrmDatos(app).grid(row=1, column=0,columnspan=7, sticky="nsew",padx=2,pady=2)
frameTablaSelecciones = FrmTablaSelecciones(app).grid(row=2, column=0,columnspan=6, sticky="nsew",padx=2,pady=2)
frameBotones = FrmBotones(app).grid(row=2, column=6, sticky="nsew",padx=2,pady=2)
app.mainloop()
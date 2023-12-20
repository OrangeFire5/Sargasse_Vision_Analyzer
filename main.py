import tkinter as tk
from clases.frmImagen import *
from clases.frmTablaSelecciones import *
from clases.frmBotones import *
from clases.barraMenu import *
from funcionalidad.controller import *
from funcionalidad.gestorArchivos import *

app = tk.Tk()
app.title("Sargasse Vision Analyzer")
app.geometry("800x500")
app.iconbitmap("img/iconos/icon.ico")

app.rowconfigure(0,weight=9)
app.rowconfigure(1,weight=1)
app.columnconfigure(0,weight=3)
app.columnconfigure(1,weight=3)
app.columnconfigure(2,weight=3)
app.columnconfigure(3,weight=3)

app.columnconfigure(4,weight=3)
app.columnconfigure(5,weight=3)

controlador = Controller(app)
gestorArchivos = GestorArchivos(controlador)
BarraDeMenu(app,controlador, gestorArchivos)

frameImagen1 = FrmImagen(app,controlador, gestorArchivos,"FrameImagen1")
frameImagen1.grid(row=0, column=0, columnspan=3, sticky="nsew",padx=2,pady=2)

frameImagen2 = FrmImagen(app,controlador,gestorArchivos,"FrameImagen2","Imagen Sentinel procesada","imgProcesada.png")
frameImagen2.grid(row=0, column=3, columnspan=3, sticky="nsew",padx=2,pady=2)
frameTablaSelecciones = FrmTablaSelecciones(app,controlador)
frameTablaSelecciones.grid(row=1, column=0,columnspan=5, sticky="nsew",padx=2,pady=2)
frameBotones = FrmBotones(app,controlador)
frameBotones.grid(row=1, column=5, sticky="nsew",padx=2,pady=2)

controlador.set_frmImagen1(frameImagen1)
controlador.set_frmImagen2(frameImagen2)
controlador.set_frmTablaSelecciones(frameTablaSelecciones)
controlador.set_frmBotones(frameBotones)
controlador.set_gestorArchivos(gestorArchivos)
app.mainloop()
import tkinter as tk
from clases.frmImagen import *
from clases.frmTablaSelecciones import *
from clases.frmBotones import *
from clases.barraMenu import *

app = tk.Tk()
app.title("Sargasse Vision Analyzer")
app.geometry("800x500")
app.iconbitmap("img/icon.ico")

#Barra de menu
BarraDeMenu(app)

app.rowconfigure(0,weight=9)
app.rowconfigure(1,weight=1)
app.columnconfigure(0,weight=3)
app.columnconfigure(1,weight=3)
app.columnconfigure(2,weight=3)
app.columnconfigure(3,weight=3)
app.columnconfigure(4,weight=3)
app.columnconfigure(5,weight=3)

frameImagen1 = FrmImagen(app).grid(row=0, column=0, columnspan=3, sticky="nsew",padx=2,pady=2)
frameImagen2 = FrmImagen(app,"Imagen Sentinel procesada","imgProcesada.ico").grid(row=0, column=3, columnspan=3, sticky="nsew",padx=2,pady=2)
frameTablaSelecciones = FrmTablaSelecciones(app).grid(row=1, column=0,columnspan=5, sticky="nsew",padx=2,pady=2)
frameBotones = FrmBotones(app).grid(row=1, column=5, sticky="nsew",padx=2,pady=2)

app.mainloop()
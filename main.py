import tkinter as tk
from clases.frmImagen import *
from clases.frmDatos import *
from clases.frmTablaSelecciones import *

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


frame1 = FrmImagen(app).grid(row=0, column=0, columnspan=3, sticky="nsew",padx=2,pady=2)
frame2 = FrmImagen(app).grid(row=0, column=4, columnspan=3, sticky="nsew",padx=2,pady=2)
frame3 = FrmDatos(app).grid(row=1, column=0,columnspan=7, sticky="nsew",padx=2,pady=2)
frame4 = FrmTablaSelecciones(app).grid(row=2, column=0,columnspan=6, sticky="nsew",padx=2,pady=2)
app.mainloop()
import tkinter as tk
from clases.frmImagen import *
from clases.frmDatos import *

app = tk.Tk()
app.title("Sargasse Vision Analyzer")
app.geometry("800x500")

app.rowconfigure(0,weight=3)
app.rowconfigure(1,weight=1)
app.columnconfigure(0,weight=3)
app.columnconfigure(1,weight=1)
app.columnconfigure(2,weight=3)


frame1 = FrmImagen(app).grid(row=0, column=0, sticky="nsew",padx=10,pady=10)
frame2 = FrmImagen(app).grid(row=0, column=2, sticky="nsew",padx=10,pady=10)
frame3 = FrmDatos(app).grid(row=1, column=0,columnspan=3, sticky="nsew",padx=10,pady=10)

app.mainloop()
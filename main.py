import tkinter as tk
from clases.frmImagen import *

app = tk.Tk()
app.title("Sargasse Vision Analyzer")
app.geometry("800x500")

app.rowconfigure(0,weight=1)
app.columnconfigure(0,weight=1)
app.columnconfigure(1,weight=1)

frame1 = FrmImagen(app).grid(row=0, column=0, sticky="nsew",padx=10,pady=10)
frame2 = FrmImagen(app).grid(row=0, column=1, sticky="nsew",padx=10,pady=10)

app.mainloop()
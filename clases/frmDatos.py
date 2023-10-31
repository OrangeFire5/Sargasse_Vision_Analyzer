#Generacion de marco con informacion del posicionamiento del cursor
import tkinter as tk

class FrmDatos(tk.Frame):
    def __init__(self, master = None):
        super().__init__(master,bg="yellow")
        self.master = master
        self.config(relief="ridge", bd=5)

        self.rowconfigure(0,weight=1)
        self.rowconfigure(1,weight=1)
        self.rowconfigure(2,weight=1)
        self.columnconfigure(0,weight=1)
        self.columnconfigure(1,weight=1)
        self.columnconfigure(2,weight=1)
        self.columnconfigure(3,weight=1)
        self.columnconfigure(4,weight=1)
        self.columnconfigure(5,weight=1)

        self.createLabels()
        self.createInputs()
    def createLabels(self):
        tk.Label(self,text="Datos \n seleccionados").grid(column=0, row=0, rowspan=3, sticky="nsew",padx=2, pady=2)

        tk.Label(self,text="Coordenadas Geograficas").grid(column=2, row=0, columnspan=2, sticky="nsew",padx=2, pady=2)
        tk.Label(self,text="Coordenadas Locales").grid(column=4, row=0, columnspan=2, sticky="nsew",padx=2, pady=2)

        tk.Label(self,text="Valor").grid(column=1, row=1, sticky="nsew",padx=2, pady=2)
        tk.Label(self,text="Longitud").grid(column=2, row=1, sticky="nsew",padx=2, pady=2)
        tk.Label(self,text="Latitud").grid(column=3, row=1, sticky="nsew",padx=2, pady=2)
        tk.Label(self,text="X").grid(column=4, row=1, sticky="nsew",padx=2, pady=2)
        tk.Label(self,text="Y").grid(column=5, row=1, sticky="nsew",padx=2, pady=2)
    def createInputs(self):
        self.valor = tk.Entry(self,justify=tk.CENTER,state="readonly")
        self.valor.grid(column=1, row=2, sticky="nsew",padx=2, pady=2)

        self.longitud = tk.Entry(self,state="readonly")
        self.longitud.grid(column=2, row=2, sticky="nsew",padx=2, pady=2)

        self.latitud = tk.Entry(self,state="readonly")
        self.latitud.grid(column=3, row=2, sticky="nsew",padx=2, pady=2)

        self.X = tk.Entry(self,state="readonly")
        self.X.grid(column=4, row=2, sticky="nsew",padx=2,pady=2)

        self.Y = tk.Entry(self,state="readonly")
        self.Y.grid(column=5, row=2, sticky="nsew",padx=2,pady=2)

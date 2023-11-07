#Generacion del marco que contine a la tabla que muestra las selecciones
import tkinter as tk
from tkinter import ttk

class FrmTablaSelecciones(tk.Frame):
    def __init__(self, master = None):
        super().__init__(master,bg="blue")
        self.master = master
        self.config(relief="ridge", bd=5)

        self.createTitle()
        self.createTabla()

    def createTitle(self):
        #tk.Label(self, text="Tabla de selecciones").grid(column=0,row=0,columnspan=6, sticky="nsew",padx=10, pady=10)
        tk.Label(self, text="Tabla de selecciones").pack(fill=tk.X)
    def createTabla(self):
        self.hscrollbar = ttk.Scrollbar(self, orient=tk.HORIZONTAL)
        self.vscrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL)
        self.treeview = ttk.Treeview(self
            ,columns=("lat", "long", "x","y","choose") 
            ,xscrollcommand=self.hscrollbar.set
            ,yscrollcommand=self.vscrollbar.set
            ,height=4)
        self.hscrollbar.config(command=self.treeview.xview)
        self.hscrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.vscrollbar.config(command=self.treeview.yview)
        self.vscrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.treeview.heading("#0", text="Id")
        self.treeview.heading("lat", text="Latitud")
        self.treeview.heading("long", text="Longitud")
        self.treeview.heading("x", text="x")
        self.treeview.heading("y", text="y")
        self.treeview.heading("choose", text="F+ / F- / P+")
        self.treeview.column("#0",width=30, stretch=True)
        self.treeview.column("lat",width=30, stretch=True)
        self.treeview.column("long",width=30, stretch=True)
        self.treeview.column("x",width=30, stretch=True)
        self.treeview.column("y",width=30, stretch=True)
        self.treeview.column("choose",width=30, stretch=True)
        self.treeview.pack(fill=tk.BOTH, expand=True)
        #self.treeview.grid(column=0, row=1, columnspan=6, sticky="nsew",padx=10, pady=10)

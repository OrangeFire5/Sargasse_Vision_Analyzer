#Generacion del marco que contine a la tabla que muestra las selecciones
import tkinter as tk
from tkinter import ttk

class FrmTablaSelecciones(tk.Frame):
    def __init__(self, master = None,controller=None):
        super().__init__(master)
        self.master = master
        self.config(relief="ridge", bd=5)
        self.controller = controller
        self.createTitle()
        self.createTabla()
        self.treeview.bind("<<TreeviewSelect>>", self.activarArea)

    def createTitle(self):
        tk.Label(self, text="Tabla de selecciones").pack(fill=tk.X)
    def createTabla(self):
        self.hscrollbar = ttk.Scrollbar(self, orient=tk.HORIZONTAL)
        self.vscrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL)
        self.treeview = ttk.Treeview(self
            ,columns=("ID","puntos", "coord","choose") 
            ,xscrollcommand=self.hscrollbar.set
            ,yscrollcommand=self.vscrollbar.set
            ,height=3)
        self.hscrollbar.config(command=self.treeview.xview)
        self.hscrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.vscrollbar.config(command=self.treeview.yview)
        self.vscrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        #self.treeview.heading("#0", text="Id")
        self.treeview.heading("ID", text="Id")
        self.treeview.heading("puntos", text="Puntos(x,y)")
        self.treeview.heading("coord", text="Coordenadas geograficas (Lat,Lon)")
        self.treeview.heading("choose", text="F+ / F- / P+")
        self.treeview.column("#0", width=0, stretch=tk.NO)
        self.treeview.column("ID",width=35,stretch=tk.NO,anchor="center")
        self.treeview.column("coord",width=0,stretch=tk.YES, anchor="center")
        self.treeview.column("puntos",width=0,stretch=tk.YES,anchor="center")
        self.treeview.column("choose",width=80,stretch=tk.NO,anchor="center")
        self.treeview.pack(fill=tk.BOTH, expand=True)
        self.treeview.tag_configure("datos", font=("", 7))
        #self.treeview.grid(column=0, row=1, columnspan=6, sticky="nsew",padx=10, pady=10)

    def get_id_seleccionado(self):
        seleccion = self.treeview.selection()
        if seleccion:
            return int(self.treeview.item(seleccion, "values")[0])

    def insertarDatos(self,ids,puntos,coord,choose="F+"):
        self.treeview.insert('', 'end', values=(ids,puntos,coord,choose), tags=("datos"),iid=ids)
    def modificarPuntos(self,i,puntos):
        for item in self.treeview.get_children():
            ids = int(self.treeview.item(item, "values")[0]) 
            if i == ids:
                self.treeview.set(item, column="puntos", value=puntos)
    def modificarCoord(self,i,coord):
        for item in self.treeview.get_children():
            ids = int(self.treeview.item(item, "values")[0])
            if i == ids:
                self.treeview.set(item, column="coord", value=coord)
    def modificarChoose(self,i,choose):
        for item in self.treeview.get_children():
            ids = int(self.treeview.item(item, "values")[0]) 
            if i == ids:
                self.treeview.set(item, column="choose", value=choose)
    def activarArea(self,event):
        seleccion = self.treeview.selection()
        if seleccion:
            ids = int(self.treeview.item(seleccion, "values")[0])
            ids =ids-1
            choose=self.treeview.item(seleccion, "values")[3]
            if choose == "F-":
                color="gold"
            if choose == "T+":
                color="limegreen"
            if choose == "F+":
                color="brown"
            self.controller.activarModoEdicion(ids,color)
    def deseleccionar_todo(self):
        items_seleccionados = self.treeview.selection()
        if items_seleccionados:
            self.treeview.selection_remove(items_seleccionados)
    def eliminarArea(self,ids):
        seleccion = self.treeview.selection()
        if seleccion:
            self.treeview.delete(seleccion)

        for item in self.treeview.get_children():
            i = int(self.treeview.item(item, "values")[0]) 
            if i > ids:
                valores = list(self.treeview.item(item, "values"))
                valores[0] = i-1
                self.treeview.delete(i)
                self.treeview.insert("", "end", values=valores,tags=("datos"), iid=i-1)


    

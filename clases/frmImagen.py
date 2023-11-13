#Generacion del marco donde se visualizaran las imagenes
import tkinter as tk
import os
from PIL import ImageTk, Image
from tkinter import filedialog

class FrmImagen(tk.Frame):
    def __init__(self, master = None, barraSelecciones = False, image = "imgBruta.png"):
        super().__init__(master)
        self.master = master
        self.ancho = self.winfo_width()
        self.alto = self.winfo_height()
        self.config(relief="ridge", bd=5)
        
        self.rowconfigure(0,weight=5)
        self.rowconfigure(1,weight=1)
        self.rowconfigure(2,weight=1)
        self.columnconfigure(0,weight=1)

        self.createIcono(image)
        self.createLabel()
        self.createButton()
        if barraSelecciones:
            self.createBarraSelecciones()
            self.lbImagen.config(text="Imagen Sentinel procesada")
            self.createCuadroClasificador() 
            self.ocultarCuadroClasificador()

##Creacion de elementos de la Ul##
    def createIcono(self,image):
        path = os.path.dirname(__file__)
        path = os.path.dirname(path)
        path = os.path.join(path,"img")
        path = os.path.join(path,image)

        self.imgenOriginal = Image.open(path)
        self.image = ImageTk.PhotoImage(self.imgenOriginal)
        self.contenedorImage =  tk.Label(self, image=self.image)
        self.contenedorImage.grid(column=0,row=0,sticky="nsew")

    def createLabel(self):
        self.lbImagen =  tk.Label(self)
        self.lbImagen.config(text="Imagen Sentinel a color real")
        self.lbImagen.grid(column=0,row=1,sticky="nsew", padx=20,pady=5, ipady=3)

    def createButton(self):
        self.btnAbrirImagen =  tk.Button(self)
        self.btnAbrirImagen.config(text="Seleccione una imagen", command=self.AbrirImagen)
        self.btnAbrirImagen.grid(column=0,row=2,sticky="nsew", padx=20,pady=5, ipady=3)
    
    def createBarraSelecciones(self):
        self.BarraSelecciones = tk.Frame(self)
        self.BarraSelecciones.config(background="gray",width=30, height=100,relief="ridge", bd=2)
        self.BarraSelecciones.grid(column=0,row=0,sticky="ne")
        
        self.btnPuntero = tk.Button(self.BarraSelecciones)
        self.btnPuntero.config(text="Point")
        self.btnPuntero.place(relx=0.06, rely=0.0625, relwidth=0.9,relheight=0.25)

        self.btnHand = tk.Button(self.BarraSelecciones)
        self.btnHand.config(text="Hand")
        self.btnHand.place(relx=0.06, rely=0.375,relwidth=0.9,relheight=0.25)

        self.btnAjusteVista = tk.Button(self.BarraSelecciones)
        self.btnAjusteVista.config(text="Area")
        self.btnAjusteVista.place(relx=0.06, rely=0.6875,relwidth=0.9,relheight=0.25)
    
    def createCuadroClasificador(self):
        self.cuadroClasificador = tk.Frame(self)
        self.cuadroClasificador.config(background="gray",relief="ridge", bd=2)
        self.cuadroClasificador.grid(column=0,row=3,sticky="s")

        self.tipoDeSeleccion = tk.IntVar()
        self.tipoDeSeleccion.set(1)

        tk.Label(self.cuadroClasificador,text="F-").grid(column=0,row=0,sticky="nsew")
        self.radio1 = tk.Radiobutton(self.cuadroClasificador,variable=self.tipoDeSeleccion, value=0)
        self.radio1.grid(column=0,row=1,sticky="nsew")

        tk.Label(self.cuadroClasificador,text="T+").grid(column=1,row=0,sticky="nsew")
        self.radio2 = tk.Radiobutton(self.cuadroClasificador,variable=self.tipoDeSeleccion, value=1)
        self.radio2.grid(column=1,row=1,sticky="nsew")

        tk.Label(self.cuadroClasificador,text="F+").grid(column=2,row=0,sticky="nsew")
        self.radio3 = tk.Radiobutton(self.cuadroClasificador,variable=self.tipoDeSeleccion, value=2)
        self.radio3.grid(column=2,row=1,sticky="nsew")

##Funcionalidades##
    
    def ocultarCuadroClasificador(self):
        self.cuadroClasificador.grid_forget()
    def mostrarCuadroClasificador(self):
        self.cuadroClasificador.grid()
    #Abre una imagen
    def AbrirImagen(self):
        filtros=(("Imagenes", ("*.png","*.jpg","*.tif","*.ico")), ("Todos los archivos", "*.*"))
        filename = filedialog.askopenfilename(filetypes=filtros, title="Abrir Imagen")
        if filename:
            self.lbImagen.grid_forget()
            self.btnAbrirImagen.grid_forget()
            self.contenedorImage.grid_forget()
            self.contenedorImage.place(relx=0,rely=0,relwidth=1,relheight=1)
            self.imgenOriginal = Image.open(filename)
            self.AjustarImagen()
            self.bind("<Configure>",self.AjustarPanelImagen)
    #Ajusta tamaño de la imagen de acuerdo al tamaño de la ventana
    def AjustarPanelImagen(self,event):
        if (self.ancho != self.winfo_width()) or (self.alto  != self.winfo_height()):
            self.AjustarImagen()
    def AjustarImagen(self):
            self.ancho = self.winfo_width()
            self.alto = self.winfo_height()
            self.image = ImageTk.PhotoImage(self.imgenOriginal.resize((self.ancho,self.alto)))
            self.contenedorImage.config(image=self.image)
        

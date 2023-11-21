#Generacion del marco para mostrar las opciones para visualizar la imagen(Zoom, ajuste y sincronizar)
import tkinter as tk
import os
from PIL import ImageTk, Image

class FrmBarraDeVista(tk.Frame):
    def __init__(self, master = None):
        super().__init__(master,width=30, height=80)
        self.master = master
        self.config(relief="ridge", bd=2)
        self.crearBotones()
    def crearBotones(self):
        #Rutas
        path = os.path.dirname(__file__)
        path = os.path.dirname(path)
        path = os.path.join(path,"img")
        path = os.path.join(path,"iconos")
        
        #AumentoZoom
        icono = Image.open(os.path.join(path,"zoomMas.ico")).resize((15,15))
        self.iconAumentoZoom = ImageTk.PhotoImage(icono)
        self.btnAumentoZoom = tk.Button(self)
        self.btnAumentoZoom.config(image=self.iconAumentoZoom)
        self.btnAumentoZoom.place(relx=0.06, rely=0.0625, relwidth=0.9,relheight=0.25)
        
        #Disminuye Zoom
        icono = Image.open(os.path.join(path,"zoomMenos.ico")).resize((15,15))
        self.iconDisminuyeZoom = ImageTk.PhotoImage(icono)
        self.btnDiminuyeZoom = tk.Button(self)
        self.btnDiminuyeZoom.config(image=self.iconDisminuyeZoom)
        self.btnDiminuyeZoom.place(relx=0.06, rely=0.375,relwidth=0.9,relheight=0.25)

        #Sincronizar imagenes
        icono = Image.open(os.path.join(path,"ajuste.ico")).resize((15,15))
        self.iconSicronizar = ImageTk.PhotoImage(icono)
        self.btnSincronizar = tk.Button(self)
        self.btnSincronizar.config(text="=")
        self.btnSincronizar.place(relx=0.06, rely=0.6875,relwidth=0.9,relheight=0.25)

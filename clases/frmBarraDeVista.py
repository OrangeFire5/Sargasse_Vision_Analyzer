#Generacion del marco para mostrar las opciones para visualizar la imagen(Zoom, ajuste y sincronizar)
import tkinter as tk

class FrmBarraDeVista(tk.Frame):
    def __init__(self, master = None):
        super().__init__(master,bg="gray",width=30, height=100)
        self.master = master
        self.config(relief="ridge", bd=2)
        self.crearBotones()
    def crearBotones(self):
        self.btnAumentoZoom = tk.Button(self)
        self.btnAumentoZoom.config(text="+")
        self.btnAumentoZoom.place(relx=0.06, rely=0.04, relwidth=0.9,relheight=0.20)

        self.btnDiminuyeZoom = tk.Button(self)
        self.btnDiminuyeZoom.config(text="-")

        self.btnDiminuyeZoom.place(relx=0.06, rely=0.28,relwidth=0.9,relheight=0.20)
        self.btnAjusteVista = tk.Button(self)
        self.btnAjusteVista.config(text="A")
        self.btnAjusteVista.place(relx=0.06, rely=0.52,relwidth=0.9,relheight=0.20)

        self.btnSincronizar = tk.Button(self)
        self.btnSincronizar.config(text="=")
        self.btnSincronizar.place(relx=0.06, rely=0.76,relwidth=0.9,relheight=0.20)

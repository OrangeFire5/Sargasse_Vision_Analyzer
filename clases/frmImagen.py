#Generacion del marco donde se visualizaran las imagenes
import tkinter as tk

class FrmImagen(tk.Frame):
    def __init__(self, master = None, barraSelecciones = False, image = "img/imgBruta.png"):
        super().__init__(master,bg="green")
        self.master = master
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

    def createIcono(self,image):
        self.icono = tk.PhotoImage(file=image)
        self.lbIcono =  tk.Label(self, image=self.icono)
        self.lbIcono.grid(column=0,row=0,sticky="nsew")

    def createLabel(self):
        self.lbImagen =  tk.Label(self)
        self.lbImagen.config(text="Imagen Sentinel a color real")
        self.lbImagen.grid(column=0,row=1,sticky="nsew", padx=20,pady=5, ipady=3)

    def createButton(self):
        self.btnAbrirImagen =  tk.Button(self)
        self.btnAbrirImagen.config(text="Seleccione una imagen")
        self.btnAbrirImagen.grid(column=0,row=2,sticky="nsew", padx=20,pady=5, ipady=3)
    
    def createBarraSelecciones(self):
        self.marco = tk.Frame(self)
        self.marco.config(background="gray",width=30, height=100,relief="ridge", bd=2)
        self.marco.grid(column=0,row=0,sticky="ne")
        
        self.btnPuntero = tk.Button(self.marco)
        self.btnPuntero.config(text="Point")
        self.btnPuntero.place(relx=0.06, rely=0.0625, relwidth=0.9,relheight=0.25)

        self.btnHand = tk.Button(self.marco)
        self.btnHand.config(text="Hand")
        self.btnHand.place(relx=0.06, rely=0.375,relwidth=0.9,relheight=0.25)

        self.btnAjusteVista = tk.Button(self.marco)
        self.btnAjusteVista.config(text="Area")
        self.btnAjusteVista.place(relx=0.06, rely=0.6875,relwidth=0.9,relheight=0.25)
    
    def createCuadroClasificador(self):
        self.marco = tk.Frame(self)
        self.marco.config(background="gray",relief="ridge", bd=2)
        self.marco.grid(column=0,row=3,sticky="s")

        self.tipoDeSeleccion = tk.IntVar()
        self.tipoDeSeleccion.set(1)

        tk.Label(self.marco,text="F-").grid(column=0,row=0,sticky="nsew")
        self.radio1 = tk.Radiobutton(self.marco,variable=self.tipoDeSeleccion, value=0)
        self.radio1.grid(column=0,row=1,sticky="nsew")

        tk.Label(self.marco,text="T+").grid(column=1,row=0,sticky="nsew")
        self.radio2 = tk.Radiobutton(self.marco,variable=self.tipoDeSeleccion, value=1)
        self.radio2.grid(column=1,row=1,sticky="nsew")

        tk.Label(self.marco,text="F+").grid(column=2,row=0,sticky="nsew")
        self.radio3 = tk.Radiobutton(self.marco,variable=self.tipoDeSeleccion, value=2)
        self.radio3.grid(column=2,row=1,sticky="nsew")

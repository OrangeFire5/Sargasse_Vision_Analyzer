#Generacion del marco donde se visualizaran las imagenes
import tkinter as tk
import os
from PIL import ImageTk, Image
import matplotlib.image as mpimg
from tkinter import filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
#from controller import *

class FrmImagen(tk.Frame):
    def __init__(self, master = None, controlador=None,gestorArchivos=None, nombre="", textoLabel = "Imagen Sentinel a color real", image = "imgColorReal.png"):
        super().__init__(master)
        self.master = master
        self.controller = controlador
        self.gestorArchivos = gestorArchivos
        self.nombre = nombre
        self.ImagenCargada = False
        self.config(relief="ridge", bd=5)
        self.ancho = self.winfo_width()
        self.alto = self.winfo_height()
        
        ##Configuraciones##
        self.grid_propagate(False)
        self.rowconfigure(0,weight=5)
        self.rowconfigure(1,weight=1)
        self.rowconfigure(2,weight=1)
        self.columnconfigure(0,weight=1)

        self.createIcono(image)
        self.createLabel(textoLabel)
        self.createButton()

##Creacion de elementos de la Ul##
    def createIcono(self,image):
        path = os.path.dirname(__file__)
        path = os.path.dirname(path)
        path = os.path.join(path,"img")
        path = os.path.join(path,"iconos")
        path = os.path.join(path,image)

        self.imgenOriginal = Image.open(path).resize((100,100))
        self.image = ImageTk.PhotoImage(self.imgenOriginal)
        self.contenedorImage =  tk.Label(self, image=self.image)
        self.contenedorImage.grid(column=0,row=0,sticky="nsew")

    def createLabel(self, textoLabel):
        self.lbImagen =  tk.Label(self)
        self.lbImagen.config(text=textoLabel)
        self.lbImagen.grid(column=0,row=1,sticky="nsew", padx=20,pady=5, ipady=3)

    def createButton(self):
        self.btnAbrirImagen =  tk.Button(self)
        self.btnAbrirImagen.config(text="Seleccione una imagen", command=self.AbrirImagen)
        self.btnAbrirImagen.grid(column=0,row=2,sticky="nsew", padx=20,pady=5, ipady=3)
    
    def createBarraSelecciones(self):
        self.herramientaSeleccionada = ""
        self.sincronizar = False
        self.BarraSelecciones = tk.Frame(self)
        self.BarraSelecciones.config(background="gray",width=30, height=175,relief="ridge", bd=2)
        self.BarraSelecciones.grid(column=0,row=0,sticky="ne")
        
        #Rutas
        path = os.path.dirname(__file__)
        path = os.path.dirname(path)
        path = os.path.join(path,"img")
        path = os.path.join(path,"iconos")

        #Puntero - 0
        icono = Image.open(os.path.join(path,"puntero.png")).resize((15,15))
        self.iconPuntero = ImageTk.PhotoImage(icono)
        self.btnPuntero = tk.Button(self.BarraSelecciones)
        self.btnPuntero.config(image=self.iconPuntero)
        self.btnPuntero.place(relx=0.06, rely=0.02, relwidth=0.9,relheight=0.12)
        
        #Hand - 1
        icono = Image.open(os.path.join(path,"hand.png")).resize((15,15))
        self.iconHand = ImageTk.PhotoImage(icono)
        self.btnHand = tk.Button(self.BarraSelecciones)
        self.btnHand.config(image=self.iconHand,command=self.handTool)
        self.btnHand.place(relx=0.06, rely=0.16,relwidth=0.9,relheight=0.12)

        #AumentoZoom - 2
        icono = Image.open(os.path.join(path,"zoomMas.png")).resize((15,15))
        self.iconAumentoZoom = ImageTk.PhotoImage(icono)
        self.btnAumentoZoom = tk.Button(self.BarraSelecciones)
        self.btnAumentoZoom.config(image=self.iconAumentoZoom, command=self.aumentoZoomTool)
        self.btnAumentoZoom.place(relx=0.06, rely=0.3, relwidth=0.9,relheight=0.12)
        
        #Disminuye Zoom - 3
        icono = Image.open(os.path.join(path,"zoomMenos.png")).resize((15,15))
        self.iconDisminuyeZoom = ImageTk.PhotoImage(icono)
        self.btnDiminuyeZoom = tk.Button(self.BarraSelecciones)
        self.btnDiminuyeZoom.config(image=self.iconDisminuyeZoom, command=self.disminuyeZoomTool)
        self.btnDiminuyeZoom.place(relx=0.06, rely=0.44,relwidth=0.9,relheight=0.12)

        #Ajustar vista - 4
        icono = Image.open(os.path.join(path,"ajuste.png")).resize((15,15))
        self.iconAjusteVista = ImageTk.PhotoImage(icono)
        self.btnAjusteVista = tk.Button(self.BarraSelecciones)
        self.btnAjusteVista.config(image=self.iconAjusteVista, command=self.ajustarVista)
        self.btnAjusteVista.place(relx=0.06, rely=0.58,relwidth=0.9,relheight=0.12)

        #Area - 5 
        icono = Image.open(os.path.join(path,"area.png")).resize((15,15))
        self.iconArea = ImageTk.PhotoImage(icono)
        self.btnArea = tk.Button(self.BarraSelecciones)
        self.btnArea.config(image =self.iconArea)
        self.btnArea.place(relx=0.06, rely=0.72,relwidth=0.9,relheight=0.12)

        #Sincronizar imagenes - 6
        icono = Image.open(os.path.join(path,"sincro.png")).resize((15,15))
        self.iconSicronizar = ImageTk.PhotoImage(icono)
        self.btnSincronizar = tk.Button(self.BarraSelecciones)
        self.btnSincronizar.config(image=self.iconSicronizar, command=self.sincronizarTool)
        self.btnSincronizar.place(relx=0.06, rely=0.86,relwidth=0.9,relheight=0.12)

    def createBarraDeDatos(self, nombre):
        self.BarraDeDatos = tk.Frame(self)
        self.BarraDeDatos.config(background="gray",relief=None)
        self.BarraDeDatos.place(relx=0, rely=0.935,relwidth=1,relheight=0.065)

        if self.nombre == "FrameImagen1":
            #Etiquetas de nombre
            self.EtiquetaDeDatos = tk.Label(self.BarraDeDatos)
            self.datosPixel = tk.StringVar()
            self.datosPixel.set(nombre)
            self.EtiquetaDeDatos.config(bg="lightgrey", textvariable=self.datosPixel, anchor=tk.W)
            self.EtiquetaDeDatos.place(relx=0, rely=0,relwidth=0.3,relheight=1)

            #Etiquetas de datos
            self.EtiquetaDeDatos = tk.Label(self.BarraDeDatos)
            self.datosPixel = tk.StringVar()
            self.datosPixel.set("Lon:--, Lat:--, x:--, y:--")
            self.EtiquetaDeDatos.config(bg="lightgrey", textvariable=self.datosPixel, anchor=tk.E)
            self.EtiquetaDeDatos.place(relx=0.3, rely=0,relwidth=0.55,relheight=1)

            #Rutas
            path = os.path.dirname(__file__)
            path = os.path.dirname(path)
            path = os.path.join(path,"img")
            path = os.path.join(path,"iconos")

            #Boton RGB
            self.modoDeColoracion = "rgb"
            self.btnRGB = tk.Button(self.BarraDeDatos)
            self.btnRGB.config(text="RGB", font=("Consolas", 7, "bold"), fg="white" ,bg="gray40",relief="sunken",cursor="arrow",command=self.cambiarArgb)
            self.btnRGB.place(relx=0.85, rely=0,relwidth=0.05,relheight=1)

            #Boton FC
            self.btnFC = tk.Button(self.BarraDeDatos)
            self.btnFC.config(text="FC",font=("Consolas", 7, "bold"), bg="gray92", relief="raised",cursor="arrow",command=self.cambiarAfc)
            self.btnFC.place(relx=0.9, rely=0,relwidth=0.05,relheight=1)

            #Modos de iluminacion
            if self.gestorArchivos.getTipoImgBruta()=="SEN2":
                self.modoIluminacion = 12
            else:
                self.modoIluminacion = 14
            icono = Image.open(os.path.join(path,"sol1.png")).resize((14,14))
            self.iconIluminacion = ImageTk.PhotoImage(icono)
            self.btnIluminacion = tk.Button(self.BarraDeDatos)
            self.btnIluminacion.config(image=self.iconIluminacion, bg="gray92", relief="raised",cursor="arrow",command=self.cambiarModoIluminacion)
            self.btnIluminacion.place(relx=0.95, rely=0,relwidth=0.05,relheight=1)
        else:
            #Etiquetas de nombre
            self.EtiquetaDeDatos = tk.Label(self.BarraDeDatos)
            self.datosPixel = tk.StringVar()
            self.datosPixel.set(nombre)
            self.EtiquetaDeDatos.config(bg="lightgrey", textvariable=self.datosPixel, anchor=tk.W)
            self.EtiquetaDeDatos.place(relx=0, rely=0,relwidth=0.4,relheight=1)

            #Etiquetas de datos
            self.EtiquetaDeDatos = tk.Label(self.BarraDeDatos)
            self.datosPixel = tk.StringVar()
            self.datosPixel.set("Value:--, Lon:--, Lat:--, x:--, y:--")
            self.EtiquetaDeDatos.config(bg="lightgrey", textvariable=self.datosPixel, anchor=tk.E)
            self.EtiquetaDeDatos.place(relx=0.4, rely=0,relwidth=0.6,relheight=1)


    def createCuadroClasificador(self):
        self.cuadroClasificador = tk.Frame(self)
        self.cuadroClasificador.config(background="gray",relief="ridge", bd=2)
        self.cuadroClasificador.grid(column=0,row=3,sticky="sw")

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
    def mostrarCuadroClasificador(self):
        self.cuadroClasificador.grid(sticky="sw")
    def ocultarCuadroClasificador(self):
        self.cuadroClasificador.grid_forget()
    def mostrarBarraSelecciones(self):
        self.BarraSelecciones.grid(column=0,row=0,sticky="ne")
    def ocultarBarraSelecciones(self):
        self.BarraSelecciones.grid_forget()
    #Abre una imagen
    def AbrirImagen(self):
        filename = self.gestorArchivos.abrirImagen(self.nombre)
        if filename:
            self.lbImagen.grid_forget()
            self.btnAbrirImagen.grid_forget()
            self.contenedorImage.grid_forget()
            self.contenedorImage.place(relx=0,rely=0,relwidth=1,relheight=0.935)
            ##Abre imagen##
            self.image = Image.open(filename)
            self.cargarImagen()
            ##Crea elementos para trabajar la imagen##
            self.ImagenCargada=True        
            self.createBarraSelecciones()
            self.createBarraDeDatos(self.gestorArchivos.getNombreImg(self.nombre))
            self.createCuadroClasificador()
            self.ocultarCuadroClasificador()
            #self.mostrarCuadroClasificador()           
            self.handTool()
    def cargarImagen(self):
        if hasattr(self, 'canvas'):
            self.canvas_widget.destroy()
        self.anchoImagen, self.altoImagen = self.image.size
        ##Configuracion de figura de mathplotlib##
        self.fig = Figure()
        self.ax = self.fig.add_subplot(111)
        self.ax.set_adjustable("datalim")
        self.ax.set_position([0, 0, 1, 1])
        self.ax.set_xlim(0,self.anchoImagen)
        self.ax.set_ylim(self.altoImagen, 0)
        self.ax.imshow(self.image)  
        ## Crear un lienzo de Matplotlib en el frame##
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.contenedorImage)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(fill=tk.BOTH, expand=True)
        self.canvas_widget.bind("<MouseWheel>", self.zoomRuedaRaton)
        self.canvas.mpl_connect("motion_notify_event", self.CoordenadasImagen)

    def CoordenadasImagen(self, event):
        # Obtener las coordenadas del puntero
        self.x = round(event.xdata) if event.xdata is not None  else None
        self.y = round(event.ydata) if event.ydata is not None else None
        # Mostrar las coordenadas en la consola
        if self.nombre== "FrameImagen1":
            self.datosPixel.set(f"Lon:--, Lat:--, x:{self.x}, y:{self.y}")
        elif self.nombre== "FrameImagen2":
            self.datosPixel.set(f"Value:--, Lon:--, Lat:--, x:{self.x}, y:{self.y}")

    ### Inicio funciones Zoom ###
    def zoomRuedaRaton(self, event):
        zoom_factor = 1.2 if event.delta <= 0 else (1/1.2)
        self.aplicarZoom(zoom_factor)
    def zoomMas(self, event):
        zoom_factor = 1/1.5
        self.aplicarZoom(zoom_factor)
    def zoomMenos(self, event):
        zoom_factor = 1.5
        self.aplicarZoom(zoom_factor)   
    def aplicarZoom(self,zoom_factor):
        x, y = self.x, self.y
        limX = (x - (x - self.ax.get_xlim()[0]) * zoom_factor, x + (self.ax.get_xlim()[1] - x) * zoom_factor)
        limY = (y - (y - self.ax.get_ylim()[0]) * zoom_factor, y + (self.ax.get_ylim()[1] - y) * zoom_factor)
        self.ax.set_xlim(limX)
        self.ax.set_ylim(limY)
        if self.sincronizar:
            self.controller.ajustarVista(self.nombre,limX,limY)
        self.canvas.draw()
    ### Fin de funciones Zoom ###

    def ajustarVista(self):
        self.ax.set_xlim(0,self.anchoImagen)
        self.ax.set_ylim(self.altoImagen, 0)
        if self.sincronizar:
            self.controller.aplicarAjuste(self.nombre)
        self.canvas.draw()

    def click(self, event):
        self.x= event.x
        self.y= event.y
        
    def arrastre(self, event):   
        x= event.x
        y= event.y
        factor_x = (self.ax.get_xlim()[1] - self.ax.get_xlim()[0])/self.canvas.get_width_height()[0]
        factor_y = (self.ax.get_ylim()[0] - self.ax.get_ylim()[1])/self.canvas.get_width_height()[1]
        limX=(self.ax.get_xlim()[0]-((x - self.x)*factor_x) ,self.ax.get_xlim()[1]-((x - self.x)*factor_x))
        limY=(self.ax.get_ylim()[0]-((y - self.y)*factor_y) ,self.ax.get_ylim()[1]-((y - self.y)*factor_y))
        self.ax.set_xlim(limX)
        self.ax.set_ylim(limY)
        self.x= x
        self.y= y
        if self.sincronizar:
            self.controller.ajustarVista(self.nombre,limX,limY)
        self.canvas.draw()

 ### Botones de tools ###  
    def handTool(self):
        if self.herramientaSeleccionada == "Hand":
            self.desactivarHerramienta()
        else:
            self.activarHerramienta("Hand")                   
    def aumentoZoomTool(self):
        if self.herramientaSeleccionada == "ZoomMas":
            self.desactivarHerramienta()
        else:
            self.activarHerramienta("ZoomMas")
    def disminuyeZoomTool(self):
        if self.herramientaSeleccionada == "ZoomMenos":
            self.desactivarHerramienta()
        else:
            self.activarHerramienta("ZoomMenos")
    def sincronizarTool(self):
        if self.controller.existeImagenEnOtroFrame(self.nombre):
            if self.sincronizar:
                self.btnSincronizar.config(bg="gray92", relief="raised")
                self.sincronizar = False
            else:
                self.btnSincronizar.config(bg="gray40",relief="sunken")
                self.sincronizar = True
            self.controller.sincronizarTool(self.nombre)

 ### Controladores de tools ###           
    def desactivarHerramienta(self):
        match self.herramientaSeleccionada:
            case "Hand":
                self.canvas_widget.unbind("<ButtonPress-1>")
                self.canvas_widget.unbind("<B1-Motion>")
                self.btnHand.config(bg="gray92", relief="raised")
            case "ZoomMas":
                self.canvas_widget.unbind("<ButtonPress-1>")
                self.btnAumentoZoom.config(bg="gray92", relief="raised")
            case "ZoomMenos":
                self.canvas_widget.unbind("<ButtonPress-1>")
                self.btnDiminuyeZoom.config(bg="gray92", relief="raised")
            case "ZoomMenos":
                self.canvas_widget.unbind("<ButtonPress-1>")
                self.btnDiminuyeZoom.config(bg="gray92", relief="raised")
            case "":
                exit
        self.herramientaSeleccionada = ""
        self.config(cursor="arrow")
    def activarHerramienta(self, herramienta):
        self.desactivarHerramienta()
        match herramienta:
            case "Hand":
                self.canvas_widget.bind("<ButtonPress-1>", self.click)
                self.canvas_widget.bind("<B1-Motion>", self.arrastre)
                self.btnHand.config(bg="gray40",relief="sunken")
                self.config(cursor="hand2")
            case "ZoomMas":
                self.canvas_widget.bind("<ButtonPress-1>", self.zoomMas)
                self.btnAumentoZoom.config(bg="gray40",relief="sunken")
                self.config(cursor="plus")
            case "ZoomMenos":
                self.canvas_widget.bind("<ButtonPress-1>", self.zoomMenos)
                self.btnDiminuyeZoom.config(bg="gray40",relief="sunken")
                self.config(cursor="cross_reverse")
            case "":
                exit
        self.herramientaSeleccionada = herramienta

    #Funciones de barra de datos
    def cambiarModoIluminacion(self):
        ruta = self.gestorArchivos.getRutaImgBruta_img()
        tipoImgBruta = self.gestorArchivos.getTipoImgBruta()
        self.modoIluminacion += 1
        if self.modoIluminacion > 14 and tipoImgBruta =="SEN2":
            self.modoIluminacion = 12
        if self.modoIluminacion > 16 and tipoImgBruta=="SEN3":
            self.modoIluminacion = 14
        self.image = Image.open(f'{ruta}/{self.modoDeColoracion}_{self.modoIluminacion}bits.tif')
        self.cargarImagen()

        path = os.path.dirname(__file__)
        path = os.path.dirname(path)
        path = os.path.join(path,"img/iconos")

        if tipoImgBruta=="SEN2":
            noIcon = self.modoIluminacion - 11
        else:
            noIcon = self.modoIluminacion - 13
        icono = Image.open(os.path.join(path,f"sol{noIcon}.png")).resize((14,14))
        self.iconIluminacion = ImageTk.PhotoImage(icono)
        self.btnIluminacion.config(image=self.iconIluminacion)


    def cambiarArgb(self):
        if not self.modoDeColoracion == "rgb":
            self.modoDeColoracion = "rgb"
            ruta = self.gestorArchivos.getRutaImgBruta_img()
            self.image = Image.open(f'{ruta}/{self.modoDeColoracion}_{self.modoIluminacion}bits.tif')
            self.cargarImagen()
            self.btnRGB.config(fg="white",bg="gray40", relief="sunken")
            self.btnFC.config(fg="black",bg="gray92",relief="raised")
    
    def cambiarAfc(self):
        if not self.modoDeColoracion == "fc":
            self.modoDeColoracion = "fc"
            ruta = self.gestorArchivos.getRutaImgBruta_img()
            self.image = Image.open(f'{ruta}/{self.modoDeColoracion}_{self.modoIluminacion}bits.tif')
            self.cargarImagen()
            self.btnFC.config(fg="white",bg="gray40", relief="sunken")
            self.btnRGB.config(fg="black",bg="gray92",relief="raised")

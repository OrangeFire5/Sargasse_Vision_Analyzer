#Generacion del marco donde se visualizaran las imagenes
import tkinter as tk
import os
from PIL import ImageTk, Image
import matplotlib.image as mpimg
from tkinter import filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure

class FrmImagen(tk.Frame):
    def __init__(self, master = None, textoLabel = "Imagen Sentinel a color real", image = "imgColorReal.png"):
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
        self.createBarraSelecciones()
        self.ocultarBarraSelecciones()
        self.lbImagen.config(text=textoLabel)
        self.createCuadroClasificador() 
        self.ocultarCuadroClasificador()

##Creacion de elementos de la Ul##
    def createIcono(self,image):
        path = os.path.dirname(__file__)
        path = os.path.dirname(path)
        path = os.path.join(path,"img")
        path = os.path.join(path,"iconos")
        path = os.path.join(path,image)

        self.imgenOriginal = Image.open(path).resize((125,125))
        self.image = ImageTk.PhotoImage(self.imgenOriginal)
        self.contenedorImage =  tk.Label(self, image=self.image)
        self.contenedorImage.grid(column=0,row=0,sticky="nsew")

    def createLabel(self):
        self.lbImagen =  tk.Label(self)
        #self.lbImagen.config()
        self.lbImagen.grid(column=0,row=1,sticky="nsew", padx=20,pady=5, ipady=3)

    def createButton(self):
        self.btnAbrirImagen =  tk.Button(self)
        self.btnAbrirImagen.config(text="Seleccione una imagen", command=self.AbrirImagen)
        self.btnAbrirImagen.grid(column=0,row=2,sticky="nsew", padx=20,pady=5, ipady=3)
    
    def createBarraSelecciones(self):
        self.herramientaSeleccionada = ""
        self.BarraSelecciones = tk.Frame(self)
        self.BarraSelecciones.config(background="gray",width=30, height=100,relief="ridge", bd=2)
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
        self.btnPuntero.place(relx=0.06, rely=0.04, relwidth=0.9,relheight=0.20)
        
        #Hand - 1
        icono = Image.open(os.path.join(path,"hand.png")).resize((15,15))
        self.iconHand = ImageTk.PhotoImage(icono)
        self.btnHand = tk.Button(self.BarraSelecciones)
        self.btnHand.config(image=self.iconHand,command=self.handTool)
        self.btnHand.place(relx=0.06, rely=0.28,relwidth=0.9,relheight=0.20)

        #Ajustar vista
        icono = Image.open(os.path.join(path,"ajuste.ico")).resize((15,15))
        self.iconAjusteVista = ImageTk.PhotoImage(icono)
        self.btnAjusteVista = tk.Button(self.BarraSelecciones)
        self.btnAjusteVista.config(image=self.iconAjusteVista, command=self.ajustarVista)
        self.btnAjusteVista.place(relx=0.06, rely=0.52,relwidth=0.9,relheight=0.20)

        #Area -2
        icono = Image.open(os.path.join(path,"ajuste.ico")).resize((15,15))
        self.iconArea = ImageTk.PhotoImage(icono)
        self.btnArea = tk.Button(self.BarraSelecciones)
        self.btnArea.config(text="Area")
        self.btnArea.place(relx=0.06, rely=0.76,relwidth=0.9,relheight=0.20)
    
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
    def mostrarCuadroClasificador(self):
        self.cuadroClasificador.grid()
    def ocultarCuadroClasificador(self):
        self.cuadroClasificador.grid_forget()
    def mostrarBarraSelecciones(self):
        self.BarraSelecciones.grid(column=0,row=0,sticky="ne")
    def ocultarBarraSelecciones(self):
        self.BarraSelecciones.grid_forget()

    #Abre una imagen
    def AbrirImagen(self):
        filtros=(("Imagenes", ("*.png","*.jpg","*.tif","*.ico")), ("Todos los archivos", "*.*"))
        filename = filedialog.askopenfilename(filetypes=filtros, title="Abrir Imagen")
        if filename:
            self.lbImagen.grid_forget()
            self.btnAbrirImagen.grid_forget()
            self.contenedorImage.grid_forget()
            self.contenedorImage.config()
            self.contenedorImage.place(relx=0,rely=0,relwidth=1,relheight=1)
            
            self.image = Image.open(filename)
            
            # Crear la figura de Matplotlib
            self.fig = Figure()
            self.ax = self.fig.add_subplot(111)
            # Mostrar la imagen en la gráfica
            self.anchoImagen, self.altoImagen = self.image.size
            self.ax.set_xlim(0,self.anchoImagen)
            self.ax.set_ylim(self.altoImagen, 0)
            self.ax.set_adjustable("datalim")
            self.ax.set_position([0, 0, 1, 1])
            self.ax.margins(0.5)
            self.ax.use_sticky_edges = False;
            self.ax.axis("off")#Deshabilita los ejes
            self.ax.imshow(self.image)
            
            # Crear un lienzo de Matplotlib en el frame
            self.canvas = FigureCanvasTkAgg(self.fig, master=self.contenedorImage)

            #Inicio creacion de barra de herramientas
            #self.toolbar = NavigationToolbar2Tk(self.canvas, self.contenedorImage, pack_toolbar=True)
            #self.toolbar.update()
            #self.toolbar.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
            #Fin de Creacion de barra de herramientas
            self.canvas_widget = self.canvas.get_tk_widget()
            self.canvas_widget.pack(fill=tk.BOTH, expand=True)
            self.canvas_widget.bind("<MouseWheel>", self.zoomRuedaRaton)
            self.canvas.mpl_connect("motion_notify_event", self.CoordenadasImagen)
            self.mostrarBarraSelecciones()
            self.handTool()
    def CoordenadasImagen(self, event):
        # Obtener las coordenadas del puntero
        self.x = int(event.xdata) if event.xdata is not None  else None
        self.y = int(event.ydata) if event.ydata is not None else None
        # Mostrar las coordenadas en la consola
        print(f"Coordenadas del puntero: ({self.x}, {self.y})")
    def zoomRuedaRaton(self, event):
        # Obtener el factor de zoom
        zoom_factor = 1.2 if event.delta <= 0 else (1/1.2)
        # Obtener las coordenadas del evento
        x, y = self.x, self.y
        # Realizar el zoom
        self.ax.set_xlim(x - (x - self.ax.get_xlim()[0]) * zoom_factor, x + (self.ax.get_xlim()[1] - x) * zoom_factor)
        self.ax.set_ylim(y - (y - self.ax.get_ylim()[0]) * zoom_factor, y + (self.ax.get_ylim()[1] - y) * zoom_factor)
        # Redibujar la figura
        self.canvas.draw()
    def ajustarVista(self):
        self.ax.set_xlim(0,self.anchoImagen)
        self.ax.set_ylim(self.altoImagen, 0)
        self.canvas.draw()
    def click(self, event):
        self.x= event.x
        self.y= event.y
    def arrastre(self, event):   
        x= event.x
        y= event.y
        factor_x = (self.ax.get_xlim()[1] - self.ax.get_xlim()[0])/self.canvas.get_width_height()[0]
        factor_y = (self.ax.get_ylim()[0] - self.ax.get_ylim()[1])/self.canvas.get_width_height()[1]
        self.ax.set_xlim(self.ax.get_xlim()[0]-((x - self.x)*factor_x) ,self.ax.get_xlim()[1]-((x - self.x)*factor_x))
        self.ax.set_ylim(self.ax.get_ylim()[0]-((y - self.y)*factor_y) ,self.ax.get_ylim()[1]-((y - self.y)*factor_y))
        self.x= x
        self.y= y
        self.canvas.draw()
    def handTool(self):
        if self.herramientaSeleccionada == "Hand":
            self.canvas_widget.unbind("<ButtonPress-1>")
            self.canvas_widget.unbind("<B1-Motion>")
            self.btnHand.config(bg="#f0f0f0")
            self.config(cursor="arrow")
            self.herramientaSeleccionada = ""
        else:
            
            self.canvas_widget.bind("<ButtonPress-1>", self.click)
            self.canvas_widget.bind("<B1-Motion>", self.arrastre)
            self.btnHand.config(bg="#8a989a")
            self.config(cursor="hand2")
            self.herramientaSeleccionada ="Hand"
        

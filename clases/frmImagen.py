#Generacion del marco donde se visualizaran las imagenes
import os
import tkinter as tk
import rasterio
import matplotlib.patches as patches

from PIL import ImageTk, Image
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from pyproj import Transformer

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
        #Areas
        self.Areas=[]

##Creacion de elementos de la Ul##
    def createIcono(self,image):
        path = os.path.dirname(__file__)
        path = os.path.dirname(path)
        path = os.path.join(path,f"img/iconos/{image}")

        self.image = ImageTk.PhotoImage(Image.open(path).resize((100,100)))
        self.contenedorImage =  tk.Label(self, image=self.image)
        self.contenedorImage.grid(column=0,row=0,sticky="nsew")

    def createLabel(self, textoLabel):
        self.lbImagen =  tk.Label(self,text=textoLabel)
        self.lbImagen.grid(column=0,row=1,sticky="nsew", padx=20,pady=5, ipady=3)

    def createButton(self):
        self.btnAbrirImagen =  tk.Button(self,text="Seleccione una imagen", command=self.AbrirImagen)
        self.btnAbrirImagen.grid(column=0,row=2,sticky="nsew", padx=20,pady=5, ipady=3)
    
    def createBarraSelecciones(self):
        self.herramientaSeleccionada = ""
        self.sincronizar = False
        self.BarraSelecciones = tk.Frame(self,background="gray",width=30, height=175,relief="ridge", bd=2)
        self.BarraSelecciones.grid(column=0,row=0,sticky="ne")
        
        #Rutas
        path = os.path.dirname(__file__)
        path = os.path.dirname(path)
        path = os.path.join(path,"img/iconos")

        #Pointer - 0
        self.rectContorno = None
        self.rectRelleno =None
        self.iconPointer = ImageTk.PhotoImage(Image.open(os.path.join(path,"puntero.png")).resize((15,15)))
        self.btnPointer = tk.Button(self.BarraSelecciones,image=self.iconPointer,command=self.pointerTool)
        self.btnPointer.place(relx=0.06, rely=0.02, relwidth=0.9,relheight=0.12)
        
        #Hand - 1
        self.iconHand = ImageTk.PhotoImage(Image.open(os.path.join(path,"hand.png")).resize((15,15)))
        self.btnHand = tk.Button(self.BarraSelecciones,image=self.iconHand,command=self.handTool)
        self.btnHand.place(relx=0.06, rely=0.16,relwidth=0.9,relheight=0.12)

        #AumentoZoom - 2
        self.iconAumentoZoom = ImageTk.PhotoImage(Image.open(os.path.join(path,"zoomMas.png")).resize((15,15)))
        self.btnAumentoZoom = tk.Button(self.BarraSelecciones,image=self.iconAumentoZoom, command=self.aumentoZoomTool)
        self.btnAumentoZoom.place(relx=0.06, rely=0.3, relwidth=0.9,relheight=0.12)
        
        #Disminuye Zoom - 3
        self.iconDisminuyeZoom = ImageTk.PhotoImage(Image.open(os.path.join(path,"zoomMenos.png")).resize((15,15)))
        self.btnDiminuyeZoom = tk.Button(self.BarraSelecciones,image=self.iconDisminuyeZoom, command=self.disminuyeZoomTool)
        self.btnDiminuyeZoom.place(relx=0.06, rely=0.44,relwidth=0.9,relheight=0.12)

        #Ajustar vista - 4
        self.iconAjusteVista = ImageTk.PhotoImage(Image.open(os.path.join(path,"ajuste.png")).resize((15,15)))
        self.btnAjusteVista = tk.Button(self.BarraSelecciones,image=self.iconAjusteVista, command=self.ajustarVista)
        self.btnAjusteVista.place(relx=0.06, rely=0.58,relwidth=0.9,relheight=0.12)

        #Area - 5 
        self.area = None
        self.pointersArea = []
        self.vertices = []
        self.trazandoArea = False
        self.EditMode=False
        self.modificandoArea =False
        self.areaModificada = 0
        #Define las variables de tipo de seleccion actual
        self.color = self.controller.get_colorTP()
        self.iconArea = ImageTk.PhotoImage(Image.open(os.path.join(path,"area.png")).resize((15,15)))
        self.btnArea = tk.Button(self.BarraSelecciones,image =self.iconArea, command=self.areaTool)
        self.btnArea.place(relx=0.06, rely=0.72,relwidth=0.9,relheight=0.12)

        #Sincronizar imagenes - 6
        self.iconSicronizar = ImageTk.PhotoImage(Image.open(os.path.join(path,"sincro.png")).resize((15,15)))
        self.btnSincronizar = tk.Button(self.BarraSelecciones,image=self.iconSicronizar, command=self.sincronizarTool)
        self.btnSincronizar.place(relx=0.06, rely=0.86,relwidth=0.9,relheight=0.12)

    def createBarraDeDatos(self, nombre):
        self.BarraDeDatos = tk.Frame(self,background="gray",relief=None)
        self.BarraDeDatos.place(relx=0, rely=0.935,relwidth=1,relheight=0.065)
        
        #Etiquetas de nombre
        self.datosPixel = tk.StringVar()
        self.datosPixel.set(nombre)
        self.EtiquetaDeNombre = tk.Label(self.BarraDeDatos,bg="lightgrey",cursor="arrow",font=("", 7), textvariable=self.datosPixel, anchor=tk.W)

        #Etiquetas de datos
        self.EtiquetaDeDatos = tk.Label(self.BarraDeDatos,bg="lightgrey",cursor="arrow",font=("", 7), textvariable=self.datosPixel, anchor=tk.E)
        self.datosPixel = tk.StringVar()
        self.datosPixel.set("Lon:--, Lat:--, x:--, y:--")

        #Rutas
        path = os.path.dirname(__file__)
        path = os.path.dirname(path)
        path = os.path.join(path,"img/iconos")
        #Boton RGB
        self.modoDeColoracion = "rgb"
        self.btnRGB = tk.Button(self.BarraDeDatos,text="RGB", font=("Consolas", 7, "bold"), fg="white" ,bg="gray40",relief="sunken",cursor="arrow",command=self.cambiarArgb)
        #Boton FC
        self.btnFC = tk.Button(self.BarraDeDatos,text="FC",font=("Consolas", 7, "bold"), bg="gray92", relief="raised",cursor="arrow",command=self.cambiarAfc)

        #Modos de iluminacion
        self.modoIluminacion = 12 if self.gestorArchivos.getTipoImgBruta()=="SEN2" else 14
        self.iconIluminacion = ImageTk.PhotoImage(Image.open(os.path.join(path,"sol1.png")).resize((14,14)))
        self.btnIluminacion = tk.Button(self.BarraDeDatos,image=self.iconIluminacion, bg="gray92", relief="raised",cursor="arrow",command=self.cambiarModoIluminacion)
        
        self.EtiquetaDeNombre.place(relx=0, rely=0,relwidth=0.3,relheight=1)
        if self.nombre == "FrameImagen1":         
            self.EtiquetaDeDatos.place(relx=0.3, rely=0,relwidth=0.55,relheight=1)
            self.btnRGB.place(relx=0.85, rely=0,relwidth=0.05,relheight=1)
            self.btnFC.place(relx=0.9, rely=0,relwidth=0.05,relheight=1)
            self.btnIluminacion.place(relx=0.95, rely=0,relwidth=0.05,relheight=1)
        else:
            self.EtiquetaDeDatos.place(relx=0.3, rely=0,relwidth=0.7,relheight=1)

    def createCuadroClasificador(self,area):  
        self.EtiquetaDeNombre.place_forget()
        self.cuadroClasificador = tk.Frame(self.BarraDeDatos,bg="lightgrey",relief=None)
        self.cuadroClasificador.place(relx=0, rely=0,relwidth=0.3,relheight=1)

        self.tipoDeSeleccion = tk.IntVar()
        self.tipoDeSeleccion.set(self.controller.get_tipo(self.nombre,area))
        self.tipoDeSeleccion.trace_add("write", self.cambioDeTipo)
        
        self.radio1 = tk.Radiobutton(self.cuadroClasificador,variable=self.tipoDeSeleccion, value=0,bg="lightgrey")
        self.radio1.place(relx=0.03, rely=0,relwidth=0.15,relheight=1)
        tk.Label(self.cuadroClasificador,text="F-",bg="lightgrey").place(relx=0.18, rely=0,relwidth=0.15,relheight=1)
        
        self.radio2 = tk.Radiobutton(self.cuadroClasificador,variable=self.tipoDeSeleccion, value=1,bg="lightgrey")
        self.radio2.place(relx=0.35, rely=0,relwidth=0.15,relheight=1)
        tk.Label(self.cuadroClasificador,text="T+",bg="lightgrey").place(relx=0.5, rely=0,relwidth=0.15,relheight=1)
        
        self.radio3 = tk.Radiobutton(self.cuadroClasificador,variable=self.tipoDeSeleccion, value=2,bg="lightgrey")
        self.radio3.place(relx=0.67, rely=0,relwidth=0.15,relheight=1)
        tk.Label(self.cuadroClasificador,text="F+",bg="lightgrey").place(relx=0.82, rely=0,relwidth=0.15,relheight=1)

##Funcionalidades##
    def cambioDeTipo(self,*args):
        self.color,choose = self.controller.colorearArea(self.Areas[self.areaModificada],self.tipoDeSeleccion.get())
        for vertice in self.vertices:
            vertice.set_facecolor(self.color)
            vertice.set_edgecolor(self.color)
        self.controller.modificarChooseTabla(self.nombre,self.areaModificada,choose)
        self.canvas.draw()
    
    def ajustarLimites(self,limX,limY):
        self.ax.set_xlim(limX)
        self.ax.set_ylim(limY) 

    #Abre una imagen
    def AbrirImagen(self):
        filename = self.gestorArchivos.abrirImagen(self.nombre)
        if filename:
            self.lbImagen.destroy()
            self.btnAbrirImagen.destroy()
            self.contenedorImage.grid_forget()
            ##Abre imagen##
            self.image = Image.open(filename)
            self.anchoImagen, self.altoImagen = self.image.size
            self.cargarImagen()
            self.contenedorImage.place(relx=0,rely=0,relwidth=1,relheight=0.935) 
            # Abrir la imagen con rasterio
            with rasterio.open(filename) as src:
                self.src = src
            #Crea elementos para trabajar la imagen
            self.ImagenCargada=True        
            self.createBarraSelecciones()
            self.createBarraDeDatos(self.gestorArchivos.getNombreImg(self.nombre))
            self.handTool()
    def cargarImagen(self,conservarSize=False):
        if conservarSize:
            limX=self.ax.get_xlim()
            limY=self.ax.get_ylim()
        else:
            limX = (0,self.anchoImagen)
            limY = (self.altoImagen,0)
        if hasattr(self, 'canvas'):
            self.canvas_widget.destroy()
        ##Configuracion de figura de mathplotlib##
        self.fig = Figure()
        self.ax = self.fig.add_subplot(111)
        self.ax.set_adjustable("datalim")
        self.ax.set_position([0, 0, 1, 1])
        self.ax.imshow(self.image)
        self.ajustarLimites(limX,limY)
        ## Crear un lienzo de Matplotlib en el frame##
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.contenedorImage)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(fill=tk.BOTH, expand=True)
        self.canvas_widget.bind("<MouseWheel>", self.zoomRuedaRaton)
        self.canvas.mpl_connect("motion_notify_event", self.CoordenadasImagen)

    def CoordenadasImagen(self, event):
        # Obtener las coordenadas locales del puntero
        self.x = round(event.xdata) if event.xdata is not None  else exit
        self.y = round(event.ydata) if event.ydata is not None else exit
        #Obtiene las coordenadas geograficas del pixel
        coord = self.consultarCoord(self.x,self.y)
        if self.nombre== "FrameImagen2" and self.x >=0 and self.x<self.anchoImagen and self.y >=0 and self.y<self.altoImagen:    
            self.value = round(self.image.getpixel((self.x,self.y)))
        else:
            self.value = 0
        # Mostrar las coordenadas en la consola
        if self.nombre== "FrameImagen1":
            self.datosPixel.set(f"Lat:{coord[0]}, Lon:{coord[1]}, x:{self.x}, y:{self.y}")
        elif self.nombre== "FrameImagen2":
            self.datosPixel.set(f"Value:{self.value}, Lat:{coord[0]}, Lon:{coord[1]}, x:{self.x}, y:{self.y}")
        if self.trazandoArea:
            self.actualizarAreaDeConstruccion()
        if self.modificandoArea:
            self.modificarArea()
    def consultarCoord(self,x,y):
        lon, lat = self.src.transform * (x,y)
        if self.src.crs == "EPSG:32616":
            transformer = Transformer.from_crs('epsg:32616', 'epsg:4326')
            lon, lat = transformer.transform(lon, lat)
        return (round(lat,6),round(lon,6))

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
        self.ajustarLimites(limX,limY)
        if self.sincronizar:
            self.controller.ajustarVista(self.nombre,limX,limY)
        self.canvas.draw()
    def zoomManual(self):
        x2, y2 =self.x,self.y
        x1, y1 = self.pointersArea[0]
        x = (x1,x2) if x1 < x2 else (x2,x1)
        y = (y2,y1) if y1 < y2 else (y1,y2)
        self.ajustarLimites(x,y)
        self.cancelarContruccionArea()
        self.canvas.draw()
    ### Fin de funciones Zoom ###

    def ajustarVista(self):
        self.ajustarLimites((0,self.anchoImagen),(self.altoImagen, 0))
        if self.sincronizar:
            self.controller.aplicarAjuste(self.nombre)
        self.canvas.draw()

    def click(self, event):
        self.x= event.x
        self.y= event.y

    def arrastre(self, event):
        xy = event.x, event.y
        xlim = self.ax.get_xlim()
        ylim = self.ax.get_ylim()
        canvas_width, canvas_height = self.canvas.get_width_height()
        factor_xy = ((xlim[1] - xlim[0]) / canvas_width,(ylim[0] - ylim[1]) / canvas_height) 
        delta_xy = (xy[0] - self.x,xy[1] - self.y)
        limX = (xlim[0] - delta_xy[0] * factor_xy[0], xlim[1] - delta_xy[0] * factor_xy[0])
        limY = (ylim[0] - delta_xy[1] * factor_xy[1], ylim[1] - delta_xy[1] * factor_xy[1])
        self.ajustarLimites(limX, limY)
        self.x, self.y = xy
        if self.sincronizar:
            self.controller.ajustarVista(self.nombre, limX, limY)
        self.canvas.draw()
    
    def trazarSeleccion(self,event,x=None,y=None):
        if self.rectRelleno is not None:
            self.rectRelleno.remove()
        if self.rectContorno is not None:
            self.rectContorno.remove()
        xlim = self.ax.get_xlim()
        ylim = self.ax.get_ylim()
        factor = min((xlim[1] - xlim[0]) * 0.05, (ylim[0] - ylim[1]) * 0.05)
        factor = factor if factor > 1 else 0.5
        x1 = (self.x) - factor
        y1 = (self.y) - factor
        if x == None and y == None:
            x=self.x
            y=self.y
        self.rectContorno = patches.Rectangle((x1, y1), factor*2, factor*2, linewidth=1, edgecolor='r',fc='none')
        self.rectRelleno = patches.Rectangle((x -0.5, y-0.5), 1, 1, linewidth=1, edgecolor='none', fc="green", alpha=0.1)
        self.ax.add_patch(self.rectRelleno)
        self.ax.add_patch(self.rectContorno)
        self.canvas.draw()
        self.idDraw_Event=self.canvas.mpl_connect('draw_event',self.ajustarContornoDeSeleccion)
        
    def ajustarContornoDeSeleccion(self,event):
        self.rectContorno.remove()
        xlim = self.ax.get_xlim()
        ylim = self.ax.get_ylim()
        factor = min((xlim[1] - xlim[0]) * 0.05, (ylim[0] - ylim[1]) * 0.05)
        factor = factor if factor > 1 else 0.5
        x = (self.rectRelleno.get_x()+0.5) - factor
        y = (self.rectRelleno.get_y()+0.5)  - factor
        self.rectContorno = patches.Rectangle((x, y), factor*2, factor*2, linewidth=1, edgecolor='r',fc='none')
        self.ax.add_patch(self.rectContorno)

    def eliminarSeleccion(self,event):    
        if self.rectContorno is not None:
            self.canvas.mpl_disconnect(self.idDraw_Event)
            self.rectContorno.remove()
            self.rectContorno = None
        if self.rectRelleno is not None:
            self.rectRelleno.remove()
            self.rectRelleno = None
        self.canvas.draw()

 #Creacion de Areas#
    def iniciarConstruccionArea(self,event):
        if not self.trazandoArea:
            xy=(self.x,self.y)
            self.pointersArea.append(xy)
            self.trazandoArea = True
            if self.herramientaSeleccionada == "ZoomMas":
                self.canvas_widget.unbind("<ButtonPress-1>")
                self.canvas_widget.unbind("<ButtonPress-3>")
                self.canvas_widget.bind("<ButtonPress-1>", self.iniciarConstruccionArea)
                self.canvas_widget.bind("<ButtonPress-3>", self.iniciarConstruccionArea)            
        else:
            self.trazandoArea = False
            if self.herramientaSeleccionada == "ZoomMas":
                self.activarHerramienta(self.herramientaSeleccionada)
                self.zoomManual()
            else:
                self.construirArea()

    def actualizarAreaDeConstruccion(self):
        xy2 =self.x,self.y
        xy1 = self.pointersArea[0]
        if self.area is not None:
            self.area.remove()
        self.area = patches.Polygon([xy1,(xy1[0],xy2[1]),xy2,(xy2[0],xy1[1])], closed=True, edgecolor='dimgrey', facecolor='white', alpha=0.5, linestyle='dashed',linewidth=2)
        self.ax.add_patch(self.area)
        self.canvas.draw()

    def construirArea(self,event=None):
        x2 = round(self.x)
        y2 = round(self.y)
        x1, y1 = self.pointersArea[0]
        xmin,xmax = (x1,x2) if x1<x2 else (x2,x1)
        ymin,ymax = (y1,y2) if y1<y2 else (y2,y1)
        self.pointersArea.clear()
        self.pointersArea=[(xmin,ymin),(xmin,ymax),(xmax,ymax),(xmax,ymin)]
        latmin,lonmin = self.consultarCoord(xmin,ymin)
        latmax,lonmax = self.consultarCoord(xmax,ymax)
        puntosDatos=f"({xmin},{ymin}),({xmin},{ymax}),({xmax},{ymax}),({xmax},{ymin})"
        coord =f"({latmin},{lonmin}),({latmin},{lonmax}),({latmax},{lonmax}),({latmax},{lonmin})"
        self.Areas.append(patches.Polygon(self.pointersArea, closed=True, edgecolor=self.color , facecolor=self.color , alpha=0.3,linewidth=2))
        self.ax.add_patch(self.Areas[-1])
        self.controller.set_Area(len(self.Areas)-1,self,self.Areas[-1],"T+")
        self.controller.agregarAreaATablaSelecciones(puntosDatos,coord,"T+")
        self.modoEdicion(self.pointersArea, (len(self.Areas)-1))
        self.cancelarContruccionArea()

    def cargarAreas(self,puntos,tipo):
        xmin,ymin = puntos[0]
        xmax,ymax = puntos[1]
        pointersArea=[(xmin,ymin),(xmin,ymax),(xmax,ymax),(xmax,ymin)]
        latmin,lonmin = self.consultarCoord(xmin,ymin)
        latmax,lonmax = self.consultarCoord(xmax,ymax)
        puntosDatos=f"({xmin},{ymin}),({xmin},{ymax}),({xmax},{ymax}),({xmax},{ymin})"
        coord =f"({latmin},{lonmin}),({latmin},{lonmax}),({latmax},{lonmax}),({latmax},{lonmin})"
        self.Areas.append(patches.Polygon(pointersArea, closed=True, edgecolor=self.color , facecolor=self.color , alpha=0.3,linewidth=2))
        self.ax.add_patch(self.Areas[-1])
        self.controller.colorearArea(self.Areas[-1],tipo)
        self.controller.set_Area(len(self.Areas)-1,self,self.Areas[-1],tipo)
        self.controller.agregarAreaATablaSelecciones(puntosDatos,coord,tipo)
        self.canvas.draw()

    def cancelarContruccionArea(self,event=None):
        if self.herramientaSeleccionada == "ZoomMas":
                self.activarHerramienta(self.herramientaSeleccionada)
        self.trazandoArea =False
        if self.area is not None:
            self.area.remove()
            self.area = None
            self.pointersArea.clear()
        self.canvas.draw()

    def modoEdicion(self,puntos,area):
        self.EditMode =True
        self.createCuadroClasificador(area)
        factor_x = (self.ax.get_xlim()[1] - self.ax.get_xlim()[0])*0.015
        factor_y = (self.ax.get_ylim()[0] - self.ax.get_ylim()[1])*0.015
        factor = factor_x if factor_x < factor_y else factor_y
        for point in puntos:
            self.vertices.append(patches.Circle(point, factor, edgecolor=self.color, facecolor=self.color))
            self.ax.add_patch(self.vertices[-1])
        self.canvas.draw()
        self.areaModificada = area 
        self.canvas_widget.unbind("<ButtonPress-1>")
        self.canvas_widget.unbind("<ButtonPress-3>")
        self.canvas_widget.bind("<ButtonPress-1>", self.dentroCirculo)
        
    def dentroCirculo(self,event):
        x,y = self.x,self.y
        radio = self.vertices[0].get_radius()
        for i in range(0,4):
            punto = self.vertices[i].center
            if x>=(punto[0]-radio)  and x<=(punto[0]+radio) and y>=(punto[1]-radio) and y<=(punto[1]+radio):
                self.verticeModificado = i
                self.editando()
                return
        self.controller.desactivarSelecciones()
        self.desactivarModoEdicion()

    def modificarArea(self):
        x,y = self.x,self.y
        puntos = self.Areas[self.areaModificada].get_xy()
        xmin, ymin= round(puntos[0][0]),round(puntos[0][1])
        xmax, ymax= round(puntos[2][0]),round(puntos[2][1])
        if self.verticeModificado == 0:
            xmin=x
            ymin=y
        elif self.verticeModificado == 1:
            xmin=x
            ymax=y
        elif self.verticeModificado == 2:
            xmax=x
            ymax=y
        elif self.verticeModificado == 3:
            xmax=x
            ymin=y
        xmin,xmax = (xmin,xmax) if xmin<xmax else (xmax,xmin)
        ymin,ymax = (ymin,ymax) if ymin<ymax else (ymax,ymin)
        nuevos_puntos = [(xmin,ymin),(xmin,ymax),(xmax,ymax),(xmax,ymin)]
        self.Areas[self.areaModificada].set_xy(nuevos_puntos)
        for i in range(0,4):
            self.vertices[i].set_center(nuevos_puntos[i])
        self.canvas.draw()

    def editando(self,event = None):
        if self.modificandoArea:
            self.modificandoArea =False
            puntos = self.Areas[self.areaModificada].get_xy()
            xmin, ymin= round(puntos[0][0]),round(puntos[0][1])
            xmax, ymax= round(puntos[2][0]),round(puntos[2][1])
            xmin,xmax = (xmin,xmax) if xmin<xmax else (xmax,xmin)
            ymin,ymax = (ymin,ymax) if ymin<ymax else (ymax,ymin)
            xmin,xmax = (xmin,xmax) if xmin<xmax else (xmax,xmin)
            ymin,ymax = (ymin,ymax) if ymin<ymax else (ymax,ymin)
            nuevos_puntos = [(xmin,ymin),(xmin,ymax),(xmax,ymax),(xmax,ymin)]
            self.Areas[self.areaModificada].set_xy(nuevos_puntos)
            latmin,lonmin = self.consultarCoord(xmin,ymin)
            latmax,lonmax = self.consultarCoord(xmax,ymax)
            puntosDatos=f"({xmin},{ymin}),({xmin},{ymax}),({xmax},{ymax}),({xmax},{ymin})"
            coord =f"({latmin},{lonmin}),({latmin},{lonmax}),({latmax},{lonmax}),({latmax},{lonmin})"
            self.controller.modificarPuntosTabla(self.nombre,(self.areaModificada),puntosDatos)
            self.controller.modificarCoordTabla(self.nombre,(self.areaModificada),coord)
            for i in range(0,4):
                self.vertices[i].set_center(nuevos_puntos[i])
            self.canvas_widget.unbind("<ButtonPress-1>")
            self.canvas_widget.bind("<ButtonPress-1>", self.dentroCirculo)
        else:
            self.modificandoArea =True
            self.canvas_widget.unbind("<ButtonPress-1>")
            self.canvas_widget.bind("<ButtonPress-1>", self.editando)

    def desactivarModoEdicion(self):
        self.EditMode =False
        self.color = self.controller.get_colorTP()
        for vertice in self.vertices:
            vertice.remove()
        self.canvas.draw()
        self.vertices.clear()
        self.areaModificada = 0
        self.canvas_widget.unbind("<ButtonPress-1>")
        self.activarHerramienta("Area")
        self.cuadroClasificador.destroy()
        self.EtiquetaDeNombre.place(relx=0, rely=0,relwidth=0.3,relheight=1)
        self.controller.desactivarSelecciones(True)

    def activarModoEdicion(self,area,color):
        if (self.EditMode and not area == self.areaModificada) or (not self.EditMode):
            if not area == self.areaModificada:
                try:
                    self.desactivarModoEdicion()
                except:
                    exit
            self.color = color
            xy = self.Areas[area].get_xy()
            xmin, ymin= round(xy[0][0]),round(xy[0][1])
            xmax, ymax= round(xy[2][0]),round(xy[2][1])
            puntos = [(xmin,ymin),(xmin,ymax),(xmax,ymax),(xmax,ymin)]
            self.modoEdicion(puntos,area)
    def eliminarArea(self,ids):
        self.trazandoArea =False
        self.modificandoArea = False
        self.desactivarModoEdicion()
        self.Areas[ids].remove()
        del self.Areas[ids]
        self.canvas.draw()

 ### Botones de tools ###  
    def pointerTool(self):
        if self.herramientaSeleccionada == "Pointer":
            self.desactivarHerramienta()
        else:
            self.activarHerramienta("Pointer")  
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
    def areaTool(self):
        if self.herramientaSeleccionada == "Area":
            self.desactivarHerramienta()
        else:
            self.activarHerramienta("Area")
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
    def activarHerramienta(self, herramienta):
        self.desactivarHerramienta()
        match herramienta:
            case "Pointer":
                self.canvas_widget.bind("<Double-Button-1>", self.trazarSeleccion)
                self.canvas_widget.bind("<ButtonPress-3>", self.eliminarSeleccion)
                self.btnPointer.config(bg="gray40",relief="sunken")
                self.config(cursor="arrow")
            case "Hand":
                self.canvas_widget.bind("<ButtonPress-1>", self.click)
                self.canvas_widget.bind("<B1-Motion>", self.arrastre)
                self.btnHand.config(bg="gray40",relief="sunken")
                self.config(cursor="hand2")
            case "ZoomMas":
                self.canvas_widget.bind("<ButtonPress-1>", self.zoomMas)
                self.canvas_widget.bind("<ButtonPress-3>", self.iniciarConstruccionArea)
                self.canvas_widget.bind("<Escape>", self.cancelarContruccionArea)      
                self.btnAumentoZoom.config(bg="gray40",relief="sunken")
                self.config(cursor="plus")
            case "ZoomMenos":
                self.canvas_widget.bind("<ButtonPress-1>", self.zoomMenos)
                self.btnDiminuyeZoom.config(bg="gray40",relief="sunken")
                self.config(cursor="cross_reverse")
            case "Area":            
                self.canvas_widget.bind("<ButtonPress-1>",self.iniciarConstruccionArea)
                self.canvas_widget.bind("<ButtonPress-3>", self.cancelarContruccionArea)
                self.canvas_widget.bind("<Escape>", self.cancelarContruccionArea)      
                self.btnArea.config(bg="gray40", relief="sunken")
            case "":
                exit
        self.herramientaSeleccionada = herramienta


    def desactivarHerramienta(self):
        match self.herramientaSeleccionada:
            case "Pointer":
                self.canvas_widget.unbind("<Double-Button-1>")
                self.canvas_widget.unbind("<ButtonPress-3>")
                self.btnPointer.config(bg="gray92", relief="raised")
            case "Hand":
                self.canvas_widget.unbind("<ButtonPress-1>")
                self.canvas_widget.unbind("<B1-Motion>")
                self.btnHand.config(bg="gray92", relief="raised")
            case "ZoomMas":
                self.canvas_widget.unbind("<ButtonPress-1>")
                self.canvas_widget.unbind("<ButtonPress-3>")
                self.canvas_widget.unbind("<Escape>")    
                self.btnAumentoZoom.config(bg="gray92", relief="raised")
            case "ZoomMenos":
                self.canvas_widget.unbind("<ButtonPress-1>")
                self.btnDiminuyeZoom.config(bg="gray92", relief="raised")
            case "Area":
                self.canvas_widget.unbind("<ButtonPress-1>")
                self.canvas_widget.unbind("<ButtonPress-3>")
                self.canvas_widget.unbind("<Escape>")    
                self.cancelarContruccionArea()
                self.btnArea.config(bg="gray92", relief="raised")
            case "":
                exit
        self.herramientaSeleccionada = ""
        self.config(cursor="arrow")

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
        self.cargarImagen(True)

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
            self.cargarImagen(True)
            self.btnRGB.config(fg="white",bg="gray40", relief="sunken")
            self.btnFC.config(fg="black",bg="gray92",relief="raised")
    
    def cambiarAfc(self):
        if not self.modoDeColoracion == "fc":
            self.modoDeColoracion = "fc"
            ruta = self.gestorArchivos.getRutaImgBruta_img()
            self.image = Image.open(f'{ruta}/{self.modoDeColoracion}_{self.modoIluminacion}bits.tif')
            self.cargarImagen(True)
            self.btnFC.config(fg="white",bg="gray40", relief="sunken")
            self.btnRGB.config(fg="black",bg="gray92",relief="raised")
import os
import zipfile
import shutil
import json
import tkinter as tk
import re
import shutil
import sys
import subprocess

from osgeo import gdal
from tkinter import filedialog
from PIL import ImageTk, Image
from funcionalidad.procesamientoSEN3 import procesarImagenBrutaSEN3, exportacionSEN3
from funcionalidad.procesamientoSEN2 import procesarImagenBrutaSEN2, exportacionSEN2


class GestorArchivos:
    def __init__(self,controller=None):
        self.controller = controller
        self.rutaProyecto = os.path.join(os.path.expanduser("~"),".savia")
        self.rutaImgBruta = ""
        self.rutaImgProcesada = ""
        self.rutaImgBruta_bands = ""
        self.rutaImgBruta_img = ""
        self.rutaImgBruta_temp= ""
        self.diretoriosCreados =False
        self.abrirArchivo =False
        #Variable a guardar
        self.nomImg1= ""
        self.nombreImgFrame1 = ""
        self.nombreImgFrame2 = ""
        self.tipoImgBruta = ""
        #colores
        self.Inicializar()

    def Inicializar(self):
        #Revisa si existe la carpeta del proyecto
        if not os.path.exists(self.rutaProyecto):
            os.makedirs(self.rutaProyecto)
        self.cargarColoresAreas()
                
    def crearDirTrabajo(self):
        if not self.abrirArchivo:
            i=1
            while os.path.exists(os.path.join(self.rutaProyecto,f"proyect{i}")):
                i += 1
            self.rutaProyecto = os.path.join(self.rutaProyecto,f"proyect{i}")
            os.makedirs(self.rutaProyecto)            
        self.rutaImgBruta = os.path.join(self.rutaProyecto,"imgBruta")
        self.rutaImgProcesada = os.path.join(self.rutaProyecto,"imgProcesada")
        #Directorios en imagen Bruta
        self.rutaImgBruta_bands = os.path.join(self.rutaImgBruta,"bands")
        self.rutaImgBruta_img = os.path.join(self.rutaImgBruta,"img")
        self.rutaImgBruta_temp = os.path.join(self.rutaImgBruta,"temp")
        #Directorios en imagen Procesada
        self.rutaImgProcesada_img = os.path.join(self.rutaImgProcesada,"img")
        if not self.abrirArchivo:
            os.makedirs(self.rutaImgBruta)
            os.makedirs(self.rutaImgProcesada)
            os.makedirs(self.rutaImgProcesada_img)

    def abrirImagen(self,nombre):
        if self.abrirArchivo:
            if nombre == "FrameImagen1":
                return os.path.join(self.rutaImgBruta_img,self.nomImg1)
            else:
                return os.path.join(self.rutaImgProcesada_img,self.nombreImgFrame2)
        else:
            if nombre == "FrameImagen1":
                filtros=(("Sentinel-3", ("*.zip","S3A*.zip")),("Sentinel-2", ("*.zip","S2A*.zip")))
            elif nombre == "FrameImagen2":
                filtros=(("Imagen Procesada", "*.tif"),)
            else:
                return "" 
            filename = filedialog.askopenfilename(filetypes=filtros, title="Seleccione imagen")
            if filename:
                if not self.diretoriosCreados:
                    self.crearDirTrabajo()
                    self.diretoriosCreados=True
                nombre, ext = os.path.splitext(filename)
                nombre = os.path.basename(nombre)
                if ext == ".zip":
                    self.nombreImgFrame1 =f'{nombre}{ext}'
                    #Descomprime en carpeta 
                    with zipfile.ZipFile(filename, 'r') as zip_ref:
                        zip_ref.extractall(self.rutaImgBruta)
                    rutaImgDescomprimida = os.path.join(self.rutaImgBruta,os.listdir(self.rutaImgBruta)[0])
                    os.makedirs(self.rutaImgBruta_bands)
                    os.makedirs(self.rutaImgBruta_img)
                    os.makedirs(self.rutaImgBruta_temp)
                    #Identifica tipo de imagen y compruba la existencia de todas los archivos necesarios
                    if procesarImagenBrutaSEN3(rutaImgDescomprimida,self.rutaImgBruta_bands,self.rutaImgBruta_temp,self.rutaImgBruta_img):
                        self.tipoImgBruta = "SEN3"
                        #Modos de color = 14,15,16 bits
                        filename = os.path.join(self.rutaImgBruta_img,"RGB_14bits.tif")
                        self.nomImg1 ="RGB_14bits.tif"
                        return filename
                    elif procesarImagenBrutaSEN2(rutaImgDescomprimida,self.rutaImgBruta_bands,self.rutaImgBruta_temp,self.rutaImgBruta_img):
                        self.tipoImgBruta = "SEN2"
                        #Modos de color = 12,13,14 bits
                        filename = os.path.join(self.rutaImgBruta_img,"RGB_12bits.tif")
                        self.nomImg1 = "RGB_12bits.tif"
                        return filename
                    else:
                        print("El documento no cuenta con la informacion necesaria para generar la imagen")
                elif ext == ".tif":
                    self.nombreImgFrame2 =f'{nombre}{ext}'
                    shutil.copy(filename, self.rutaImgProcesada_img)
                    return filename
    def nuevoProyecto(self):
        subprocess.run(["python", sys.argv[0]])


    def abrirProyecto(self):
        filename = filedialog.askdirectory()
        if filename:
            self.abrirArchivo = True
            self.rutaProyecto = filename
            self.crearDirTrabajo()
            with open(os.path.join(filename,'datos.json'), 'r') as archivo_json:
                datos = json.load(archivo_json)
            self.nomImg1= datos['nombreImgArchivo1']
            self.nombreImgFrame1 = datos['nombreImgFrame1']
            self.nombreImgFrame2 = datos['nombreImgFrame2']
            self.tipoImgBruta = datos['tipoImgBruta']
            self.areas = datos['areas']
            if not self.nomImg1 == '':
                self.controller.frmImagen1.AbrirImagen()
            if not self.nombreImgFrame2 == '':
                self.controller.frmImagen2.AbrirImagen()           
            self.abrirArchivo = False
            for area in self.areas:
                self.controller.cargarAreas(area[0], area[1], area[2])
        
    def guardar(self):
        areas=[]
        for area in self.controller.Areas:
            puntos = area[3].get_xy()
            xmin, ymin= round(puntos[0][0]),round(puntos[0][1])
            xmax, ymax= round(puntos[2][0]),round(puntos[2][1])
            areas.append((area[2].nombre,[(xmin,ymin),(xmax,ymax)],area[4]))
        datos={'nombreImgArchivo1': self.nomImg1,
               'nombreImgFrame1':self.nombreImgFrame1,
               'tipoImgBruta':self.tipoImgBruta,
               'nombreImgFrame2':self.nombreImgFrame2,
               'areas':areas}
        with open(os.path.join(self.rutaProyecto,'datos.json'), 'w') as archivo_json:
            json.dump(datos, archivo_json)

    def guardarComo(self):
        filtros=(("Nombre directorio", ("")),)
        filename = filedialog.asksaveasfilename(filetypes=filtros)
        if filename:
            self.rutaProyecto = filename
            if not os.path.exists(self.rutaProyecto):
                os.makedirs(self.rutaProyecto)
            #Image Bruta
            self.rutaImgBruta = os.path.join(self.rutaProyecto,"imgBruta")
            os.makedirs(self.rutaImgBruta)
            shutil.copytree(self.rutaImgBruta_bands,os.path.join(self.rutaImgBruta,"bands"))
            shutil.copytree(self.rutaImgBruta_img,os.path.join(self.rutaImgBruta,"img"))
            shutil.copytree(self.rutaImgBruta_temp,os.path.join(self.rutaImgBruta,"temp"))
            self.rutaImgBruta_bands = os.path.join(self.rutaImgBruta,"bands")
            self.rutaImgBruta_img = os.path.join(self.rutaImgBruta,"img")
            self.rutaImgBruta_temp = os.path.join(self.rutaImgBruta,"temp")
            #Image Procesada
            self.rutaImgProcesada = os.path.join(self.rutaProyecto,"imgProcesada")
            os.makedirs(self.rutaImgProcesada)
            shutil.copytree(self.rutaImgProcesada_img,os.path.join(self.rutaImgProcesada,"img"))
            self.rutaImgProcesada_img = os.path.join(self.rutaImgProcesada,"img")
            self.guardar()

    def borrarDatosCarpetaTemporal(self):
        dir = os.path.join(os.path.expanduser("~"),".savia")
        if os.path.exists(dir):
            for f in os.listdir(dir):
                shutil.rmtree(os.path.join(dir, f))

#Menu colores#
    def cargarColoresAreas(self):
        try:
            with open('config.json', 'r') as archivo_json:
                datos = json.load(archivo_json)
            self.colorFN = datos['colorFN']
            self.colorTP = datos['colorTP']
            self.colorFP = datos['colorFP']
        except:
            self.colorFN = "gold"
            self.colorTP = "limegreen"
            self.colorFP = "brown"
    def menuColorAreas(self):
        app = tk.Toplevel() 
        app.title("Colores de Area")
        app.geometry("270x200")
        app.resizable(width=False, height=False)
        app.iconbitmap("img/iconos/icon.ico")
        for i in range(0,8):
            app.rowconfigure(i,weight=1)
        app.columnconfigure(0,weight=5)
        app.columnconfigure(1,weight=1)
        app.columnconfigure(2,weight=4)
        #Titulo
        tk.Label(app,text="Agrega el valor del color en hexadecimal",font=("",8,"bold")).grid(row=0,column=0,columnspan=3,pady=10)
        #colorFN
        tk.Label(app,text="Color de falso negativo(ColorFN/F-)").grid(row=1,column=0,columnspan=3,sticky="w",padx=5,pady=2)
        lbColorFN = tk.Label(app,bg=self.colorFN)
        lbColorFN.grid(row=2,column=0,sticky="ew",padx=12)
        tk.Label(app,text="#",font=("",9,"bold")).grid(row=2,column=1,sticky="e")
        colorFN = tk.Entry(app,width=6,validate="key",validatecommand=(app.register(self.validacionEntry), "%P"))     
        colorFN.grid(row=2,column=2,padx=10,sticky="ew")
        colorFN.insert(0,self.colorFN.replace("#",""))
        colorFN.bind("<FocusOut>", lambda event, entry=colorFN, lb=lbColorFN: self.presentarColor(event, entry, lb))
        #colorTP
        tk.Label(app,text="Color de verdadero positivo(ColorTP/T+)").grid(row=3,column=0,columnspan=3,sticky="w",padx=5,pady=2)  
        lbColorTP = tk.Label(app,bg=self.colorTP)
        lbColorTP.grid(row=4,column=0,sticky="ew",padx=12)
        tk.Label(app,text="#",font=("",9,"bold")).grid(row=4,column=1,sticky="e")
        colorTP = tk.Entry(app,width=6,validate="key",validatecommand=(app.register(self.validacionEntry), "%P"))  
        colorTP.grid(row=4,column=2,padx=10,sticky="ew")
        colorTP.insert(0,self.colorTP.replace("#",""))
        colorTP.bind("<FocusOut>", lambda event, entry=colorTP, lb=lbColorTP: self.presentarColor(event, entry, lb))
        #colorFP
        tk.Label(app,text="Color de falso positivo(ColorFP/F+)").grid(row=5,column=0,columnspan=3,sticky="w",padx=5,pady=2)
        lbColorFP = tk.Label(app,bg=self.colorFP)
        lbColorFP.grid(row=6,column=0,sticky="ew",padx=12)
        tk.Label(app,text="#",font=("",9,"bold")).grid(row=6,column=1,sticky="e")
        colorFP = tk.Entry(app,width=6,validate="key",validatecommand=(app.register(self.validacionEntry), "%P"))  
        colorFP.grid(row=6,column=2,padx=10,sticky="ew")
        colorFP.insert(0,self.colorFP.replace("#",""))
        colorFP.bind("<FocusOut>", lambda event, entry=colorFP, lb=lbColorFP: self.presentarColor(event, entry, lb))

        colores=[colorFN,colorTP,colorFP]
        buttonGuardar = tk.Button(app,text="Guardar",command=lambda: self.guardarColores(colores,app))
        buttonGuardar.grid(row=7,column=2,pady=10,padx=5,sticky="ew")
        app.mainloop()
    def acercaDe(self):
        app = tk.Toplevel()   
        app.title("Acerca de...")
        app.geometry("300x300")
        #app.resizable(width=False, height=False)
        app.iconbitmap("img/iconos/icon.ico")
        for i in range(0,8):
            app.rowconfigure(i,weight=1)
        app.columnconfigure(0,weight=5)
        app.columnconfigure(1,weight=1)
        app.columnconfigure(2,weight=4)
        #Titulo
        path = os.path.dirname(__file__)
        path = os.path.dirname(path)
        path = os.path.join(path,"img")
        path = os.path.join(path,"iconos")
        path = os.path.join(path,"logo.png")
        print(path)
        image = Image.open(path).resize((100,100))
        icon = ImageTk.PhotoImage(image)

        tk.Label(app,image=icon).place(relx=0.025,rely=0,relwidth=0.3,relheight=0.3)
        tk.Label(app,text="Sargasse Vision Analyzer",fg="#996600",font=("",13,"bold")).place(relx=0.3,rely=0,relwidth=0.7,relheight=0.175)
        tk.Label(app,text="Versión: 1.1",fg="#3C5C26",font=("",10,"italic")).place(relx=0.3,rely=0.175,relwidth=0.7,relheight=0.05)

        tk.Label(app,text="¡Gracias por utilizar nuestro producto!",fg="#EB9E03",font=("",11,"bold")).place(relx=0,rely=0.3,relwidth=1,relheight=0.15)

        tk.Label(app,text="Creado por:",font=("",8,"bold"),fg="#D09500",anchor=tk.W).place(relx=0.05,rely=0.45,relwidth=10.9,relheight=0.05)
        tk.Label(app,text="Ing. Linda Vázquez Erasmo",fg="#3C5C26",font=("",8,"bold"),anchor=tk.E).place(relx=0.1,rely=0.5,relwidth=0.8,relheight=0.05)
        tk.Label(app,text="Ing. Irvin Ulises González Leal",fg="#3C5C26",font=("",8,"bold"),anchor=tk.E).place(relx=0.1,rely=0.55,relwidth=0.8,relheight=0.05)
        tk.Label(app,text="En colaboración con:",fg="#D09500",font=("",8,"bold"),anchor=tk.W).place(relx=0.05,rely=0.6,relwidth=0.9,relheight=0.05)
        tk.Label(app,text="Agencia Espacial Mexicana",fg="#3C5C26",font=("",8,"bold"),anchor=tk.E).place(relx=0.1,rely=0.65,relwidth=0.8,relheight=0.05)
        tk.Label(app,text="Universidad Politecnica de Atlacomulco",fg="#3C5C26",font=("",8,"bold"),anchor=tk.E).place(relx=0.1,rely=0.7,relwidth=0.8,relheight=0.05)
        tk.Label(app,text="Asesores:",fg="#D09500",font=("",8,"bold"),anchor=tk.W).place(relx=0.05,rely=0.75,relwidth=0.9,relheight=0.05)
        tk.Label(app,text="Dr. Adán Salazar Garibay ",fg="#3C5C26",font=("",8,"bold"),anchor=tk.E).place(relx=0.1,rely=0.8,relwidth=0.8,relheight=0.05)
        tk.Label(app,text="M. en C. Serafín Chávez Barranco",fg="#3C5C26",font=("",8,"bold"),anchor=tk.E).place(relx=0.1,rely=0.85,relwidth=0.8,relheight=0.05)
        tk.Label(app,text="Ing. Marco Antonio López Paredes",fg="#3C5C26",font=("",8,"bold"),anchor=tk.E).place(relx=0.1,rely=0.9,relwidth=0.8,relheight=0.05)

        #tk.Label(app,text="Savia es desarrollado como un proyecto de Estadia para obtener un grado en",font=("",8,"bold")).grid()
        #tk.Label(app,text="ingenieria en sistemas computacionales.",font=("",8,"bold")).grid()
        #tk.Label(app,text="El proyecto es resultado de la colaboracion entre la Universidad Politecnica de Atlacomulco y la Agencia Espacial Mexicana",font=("",8,"bold")).grid()
        app.mainloop()
         

#Getters#
    def getNombreImg(self,nombre):
        if nombre == "FrameImagen1":
            return self.nombreImgFrame1
        else:
            return self.nombreImgFrame2
    def getRutaImgBruta_img (self):
        return self.rutaImgBruta_img
    def getTipoImgBruta(self):
        return self.tipoImgBruta
    def getAbrirArchivo(self):
        return self.abrirArchivo
#   Configurar Colores #
    def validacionEntry(self,contenido):
        patron_hex = re.compile(r'^[0-9A-Fa-f]*$')
        caracterValido = bool(re.match(patron_hex, contenido))
        return len(contenido)<=6 and caracterValido
    def presentarColor(self,event,entry,lb):
        valor = entry.get()
        if len(valor)<3:
            for i in range(len(valor),3):
                valor=f"{valor}0"
                entry.insert(tk.END,"0")
        elif len(valor)<6 and not len(valor) == 3:
            for i in range(len(valor),6):
                valor=f"{valor}0"
                entry.insert(tk.END,"0")
        color =f"#{valor}"
        lb.config(bg=color)

    def guardarColores(self,colors,ventana):
        color = []
        for i in range(0,3):
            color.append(colors[i].get())
            if color[i]== "":
                match i:
                    case 0:
                        color[i] = "gold"
                    case 1:
                        color[i] = "limegreen"
                    case 2:
                        color[i] = "brown"
            else:
                if len(color[i])<3:
                    for j in range(len(color[i]),3):
                        color[i]=f"{color[i]}0"
                elif len(color[i])<6 and not len(color[i]) == 3:
                    for j in range(len(color[i]),6):
                        color[i]=f"{color[i]}0"
                color[i] =f"#{color[i]}"
        datos={'colorFN': color[0],'colorTP':color[1],'colorFP':color[2]}
        with open('config.json', 'w') as archivo_json:
            json.dump(datos, archivo_json)
        self.colorFN = color[0]
        self.colorTP = color[1]
        self.colorFP = color[2]
        self.controller.recolorearAreas()
        ventana.destroy()


# Exportar imagen#        
    def exportarImagen(self,filename,coord,iid): 
        if self.tipoImgBruta == "SEN3":
            exportacionSEN3(self.rutaImgBruta_bands,self.rutaImgBruta_temp,filename,iid,coord)
        elif self.tipoImgBruta == "SEN2":
            exportacionSEN2(self.rutaImgBruta_bands,self.rutaImgBruta_temp,filename,iid,coord)
        print("Exportacion terminada!")
import os
import zipfile
import shutil
import json

from osgeo import gdal
from tkinter import filedialog
from funcionalidad.procesamientoSEN3 import procesarImagenBrutaSEN3
from funcionalidad.procesamientoSEN2 import procesarImagenBrutaSEN2

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

        self.Inicializar()

    def Inicializar(self):
        #Revisa si existe la carpeta del proyecto
        if not os.path.exists(self.rutaProyecto):
            os.makedirs(self.rutaProyecto)
        
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

            if not self.nomImg1 == '':
                self.controller.frmImagen1.AbrirImagen()
            if not self.nombreImgFrame2 == '':
                self.controller.frmImagen2.AbrirImagen()           
            self.abrirArchivo = False
        
    def guardar(self):
        datos={'nombreImgArchivo1': self.nomImg1,
               'nombreImgFrame1':self.nombreImgFrame1,
               'tipoImgBruta':self.tipoImgBruta,
               'nombreImgFrame2':self.nombreImgFrame2}
        print(f'Guadado en:{os.path.join(self.rutaProyecto,'datos.json')}')
        with open(os.path.join(self.rutaProyecto,'datos.json'), 'w') as archivo_json:
            json.dump(datos, archivo_json)
            
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
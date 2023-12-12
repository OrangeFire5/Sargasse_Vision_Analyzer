import os
import glob
import zipfile
from osgeo import gdal
from tkinter import filedialog

class GestorArchivos:
    def __init__(self):
        self.rutaProyecto = os.path.expanduser("~")
        self.rutaProyecto = os.path.join(self.rutaProyecto,"savia")
        self.rutaImgBruta = ""
        self.rutaImgProcesada = ""
        self.rutaBandas = ""
        self.rutaImg = ""
        self.temp = ""
        self.allBands=[]
        self.Inicializar()

    def Inicializar(self):
        #Revisa si existe la carpeta 
        if not os.path.exists(self.rutaProyecto):
            os.makedirs(self.rutaProyecto)
        i=1
        print(os.path.join(self.rutaProyecto,f"proyect{i}"))
        while os.path.exists(os.path.join(self.rutaProyecto,f"proyect{i}")):
            i += 1
        self.rutaProyecto = os.path.join(self.rutaProyecto,f"proyect{i}")
        os.makedirs(self.rutaProyecto)
        self.rutaImgBruta = os.path.join(self.rutaProyecto,"imgBruta")
        self.rutaImgProcesada = os.path.join(self.rutaProyecto,"imgProcesada")
        self.rutaBandas = os.path.join(self.rutaImgBruta,"bands")
        self.rutaImg = os.path.join(self.rutaImgBruta,"img")
        self.temp = os.path.join(self.rutaImgBruta,"temp")
        os.makedirs(self.rutaImgBruta)
        os.makedirs(self.rutaImgProcesada)

    def abrirImagen(self):
        filtros=(("Sentinel-3", ("*.zip","S3A*.zip")),("Sentinel-2", ("*.zip","S2A*.zip")), ("Imagen Procesada", "*.tif"))
        filename = filedialog.askopenfilename(filetypes=filtros, title="Seleccione imagen")
        if filename:
            nombre, ext = os.path.splitext(filename)
            nombre = os.path.basename(nombre)
            if ext == ".zip":
                #Descomprime en carpeta temporal
                with zipfile.ZipFile(filename, 'r') as zip_ref:
                    zip_ref.extractall(self.rutaImgBruta)
                rutaImgDescomprimida = os.path.join(self.rutaImgBruta,os.listdir(self.rutaImgBruta)[0])
                os.makedirs(self.rutaBandas)
                os.makedirs(self.rutaImg)
                os.makedirs(self.temp)
                #Identifica tipo de imagen y compruba la existencia de todas los archivos necesarios
                if self.comprobacionSEN3(rutaImgDescomprimida):
                    self.procesarImagenBrutaSEN3(rutaImgDescomprimida)
                    filename = os.path.join(self.rutaImg,"RGB_15bits.tif")
                    return filename
                elif self.comprobacionSEN2(rutaImgDescomprimida):
                    self.construirCapasSEN2(rutaImgDescomprimida)
                    self.construirImgSen2()
                    filename = os.path.join(self.rutaImg,"RGB_13bits.tif")
                    return filename
                else:
                    print("El documento no cuenta con la informacion necesaria para generar la imagen")
            elif ext == ".tif":
                return filename
            return ""

    def comprobacionSEN3(self,ruta):
        if not os.path.exists(os.path.join(ruta, "geo_coordinates.nc")):
            return False
        for i in range(1,22):
            if i< 10:
                if not os.path.exists(os.path.join(ruta, f"Oa0{i}_radiance.nc")):
                    return False
                else:
                    self.allBands.append(os.path.join(ruta, f"Oa0{i}_radiance.nc"))
            elif i>=10:
                if not os.path.exists(os.path.join(ruta, f"Oa{i}_radiance.nc")):
                    return False
                else:
                    self.allBands.append(os.path.join(ruta, f"Oa{i}_radiance.nc"))
        return True
    
    def procesarImagenBrutaSEN3(self,ruta):
        #<--Capas-->
        # Definir la lista de archivos de entrada y otras opciones de fusión
        input_files = [f'{os.path.join(ruta,"Oa04_radiance.nc")}', f'{os.path.join(ruta,"Oa06_radiance.nc")}',f'{os.path.join(ruta,"Oa08_radiance.nc")}',f'{os.path.join(ruta,"Oa17_radiance.nc")}']
        #Modos de color = 14,15,16 bits
        self.obtenerLatYLon(ruta)
        self.construirCapasSen3(self.allBands)
        self.construirImgYGeoRefSen3()
        self.construirImgYGeoRefSen3("FC")
        for i in range(14,16):
            self.construirCapasSen3(input_files,i)
            self.construirImgYGeoRefSen3(i)
            self.construirImgYGeoRefSen3(i,"FC")
        

    def construirCapasSen3(self,input_files,bits=16):
        gdal_translate_options = ['-of', 'GTiff','-ot', 'Byte','-scale', '0', f'{2**bits}', '0', '255']
        for file in input_files:
            # Construir el comando gdal_translate
            nombre = os.path.splitext(file)[0]
            nombre = os.path.basename(nombre)
            if bits == 16:
                gdal.Translate(os.path.join(self.rutaBandas,f'{nombre}.tif'), gdal.Open(file), options=gdal_translate_options)
            else:    
                gdal.Translate(os.path.join(self.rutaBandas,f'{nombre}_{bits}bits.tif'), gdal.Open(file), options=gdal_translate_options)
    def obtenerLatYLon(self,ruta):
        gdal_translate_options = ['-of', 'VRT']
        gdal.Translate(os.path.join(self.temp,'lat.vrt'), gdal.Open(f'NETCDF:"{os.path.join(ruta,'geo_coordinates.nc')}":latitude'), options=gdal_translate_options)
        gdal.Translate(os.path.join(self.temp,'lon.vrt'), gdal.Open(f'NETCDF:"{os.path.join(ruta,'geo_coordinates.nc')}":longitude'), options=gdal_translate_options)
    
    def construirImgYGeoRefSen3(self,bits=16,mode="RGB"): 
        pathLat = os.path.join(self.temp,'lat.vrt')
        pathLon =  os.path.join(self.temp,'lon.vrt')
        pathGeo = os.path.join(self.temp,'geo.tif')
        pathCoord = os.path.join(self.temp,'coord.vrt')
        pathInfo = os.path.join(self.temp,'info.txt')
        
        if mode == "RGB":
            if bits == 16:
                bandRed= os.path.join(self.rutaBandas,f'Oa08_radiance.tif')
                bandVerde= os.path.join(self.rutaBandas,f'Oa06_radiance.tif')
                bandAzul= os.path.join(self.rutaBandas,f'Oa04_radiance.tif')
            else:
                bandRed= os.path.join(self.rutaBandas,f'Oa08_radiance_{bits}bits.tif')
                bandVerde= os.path.join(self.rutaBandas,f'Oa06_radiance_{bits}bits.tif')
                bandAzul= os.path.join(self.rutaBandas,f'Oa04_radiance_{bits}bits.tif')
            pathImage= os.path.join(self.rutaImg,f'rgb_{bits}bits.tif')
        elif mode == "FC":
            if bits == 16:
                bandRed= os.path.join(self.rutaBandas,f'Oa17_radiance.tif')
                bandVerde= os.path.join(self.rutaBandas,f'Oa08_radiance.tif')
                bandAzul= os.path.join(self.rutaBandas,f'Oa06_radiance.tif')
            else:
                bandRed= os.path.join(self.rutaBandas,f'Oa17_radiance_{bits}bits.tif')
                bandVerde= os.path.join(self.rutaBandas,f'Oa08_radiance.tif')
                bandAzul= os.path.join(self.rutaBandas,f'Oa06_radiance.tif')
            pathImage= os.path.join(self.rutaImg,f'fc_{bits}bits.tif')

        contenido_vrt = f"""
        <VRTDataset rasterXSize="4865" rasterYSize="4090">
         <metadata domain="GEOLOCATION">
         <mdi key="X_DATASET">{pathLon}</mdi>
         <mdi key="X_BAND">1</mdi>
         <mdi key="Y_DATASET">{pathLat}</mdi>
         <mdi key="Y_BAND">1</mdi>
         <mdi key="PIXEL_OFFSET">0</mdi>
         <mdi key="LINE_OFFSET">0</mdi>
         <mdi key="PIXEL_STEP">1</mdi>
         <mdi key="LINE_STEP">1</mdi>
         </metadata> 
           <VRTRasterBand dataType="Byte" band="1">
           <ColorInterp>Red</ColorInterp> 
            <SimpleSource>
              <SourceFilename relativeToVRT="1">{bandRed}</SourceFilename>
              <SourceBand>1</SourceBand>
              <SourceProperties RasterXSize="4865" RasterYSize="4091" dataType="Byte"/>
              <SrcRect xOff="0" yOff="0" xSize="4865" ySize="4091" />
              <DstRect xOff="0" yOff="0" xSize="4865" ySize="4091" />
            </SimpleSource>
          </VRTRasterBand>

           <VRTRasterBand dataType="Byte" band="2">
           <ColorInterp>Green</ColorInterp> 
            <SimpleSource>
              <SourceFilename relativeToVRT="1">{bandVerde}</SourceFilename>
              <SourceBand>1</SourceBand>
              <SourceProperties RasterXSize="4865" RasterYSize="4091" dataType="Byte"/>
              <SrcRect xOff="0" yOff="0" xSize="4865" ySize="4091" />
              <DstRect xOff="0" yOff="0" xSize="4865" ySize="4091" />
            </SimpleSource>
          </VRTRasterBand>

          <VRTRasterBand dataType="Byte" band="3">
           <ColorInterp>Blue</ColorInterp> 
            <SimpleSource>
              <SourceFilename relativeToVRT="1">{bandAzul}</SourceFilename>
              <SourceBand>1</SourceBand>
              <SourceProperties RasterXSize="4865" RasterYSize="4091" dataType="Byte"/>
              <SrcRect xOff="0" yOff="0" xSize="4865" ySize="4091" />
              <DstRect xOff="0" yOff="0" xSize="4865" ySize="4091" />
            </SimpleSource>
          </VRTRasterBand>
        </VRTDataset>
        """
        # Escribir el contenido en el archivo        
        with open(pathCoord, 'w') as archivo_vrt:
            archivo_vrt.write(contenido_vrt) 
        
        gdal_warp_options  = gdal.WarpOptions(format='GTiff',dstSRS='EPSG:4326',srcNodata=0,multithread=True,geoloc=True)
        gdal.Warp(pathGeo, pathCoord, options=gdal_warp_options ,overwrite=True)

        with open(pathInfo, 'w') as output_file:
            output_file.write(gdal.Info(f'{pathGeo}'))
            info = gdal.Info(pathGeo)

        with open(pathInfo) as info:
            lineas = info.readlines()
            for linea in lineas:
                if "Upper Left" in linea:
                    upper_txt = linea
                if "Lower Right" in linea:
                    lower_txt = linea
        lon1 = ""
        lat1 = ""
        lon2 = ""
        lat2 = ""

        for i in range(upper_txt.find("(")+1,upper_txt.find(",")):
            if upper_txt[i] != ".":
                lon1 = lon1 +  upper_txt[i]
        for i in range(upper_txt.find(",")+1,upper_txt.find(")")):
            if upper_txt[i] != ".":
                lat1 = lat1 +  upper_txt[i]
        for i in range(lower_txt.find("(")+1,lower_txt.find(",")):
            if lower_txt[i] != ".":
                lon2 = lon2 +  lower_txt[i]
        for i in range(lower_txt.find(",")+1,lower_txt.find(")")):
            if lower_txt[i] != ".":
                lat2 = lat2 +  lower_txt[i]

        def convert(val):
            pre = 9
            nbl = len(val)
            ent = val[:-pre]
            pos = nbl - pre
            dec = val[pos:pos + pre]
            return f"{ent}.{dec}"

        lon1 = convert(lon1)
        lat1 = convert(lat1)
        lon2 = convert(lon2)
        lat2 = convert(lat2)

        gdal_translate_options = ['-of', 'GTiff', '-a_ullr',lon1, lat1, lon2, lat2, "-a_srs", "EPSG:4326"]
        gdal.Translate(pathImage, gdal.Open(pathGeo), options=gdal_translate_options)

    def comprobacionSEN2(self,ruta):
        path = os.path.join(ruta, f"GRANULE/*/IMG_DATA")
        self.resEspacial=["R10m","R20m","R60m"]
        self.bandas = [['*B02_10m.jp2','*B03_10m.jp2','*B04_10m.jp2','*B08_10m.jp2'],
                  ['*B05_20m.jp2','*B06_20m.jp2','*B07_20m.jp2','*B11_20m.jp2','*B12_20m.jp2','*B8A_20m.jp2'],
                  ['*B01_60m.jp2','*B09_60m.jp2']]
        for i in range(0,3):
            pathActual = os.path.join(path,self.resEspacial[i])
            for band in self.bandas[i]:
                if len(glob.glob(os.path.join(pathActual,band))) == 0:
                    return False
                print(f"{band}banda existente")
        return True
    def construirCapasSEN2(self,ruta):
        path = os.path.join(ruta, f"GRANULE/*/IMG_DATA")
        #Contruccion de todas las capas para su entrada a la red neuronal(a 16bits - 65536):
        gdal_translate_options = ['-of', 'GTiff','-ot', 'Uint16']
        for i in range(0,3):
            pathActual = os.path.join(path,self.resEspacial[i])
            for band in self.bandas[i]:
                rutaCompleta = glob.glob(os.path.join(pathActual,band))[0]
                nombre = band.replace('*','')
                nombre = nombre.split('_',1)[0]
                gdal.Translate(os.path.join(self.rutaBandas,f'{nombre}.tif'), gdal.Open(rutaCompleta), options=gdal_translate_options)

        #Contruccion de bandas para obtencion de imagen:
        self.bandasRGBYFC =['*B02_10m.jp2','*B03_10m.jp2','*B04_10m.jp2','*B08_10m.jp2']
        path = os.path.join(path, "R10m")
        for i in range(12,15):
            gdal_translate_options = ['-of', 'GTiff','-ot', 'Byte','-scale', '0', f'{2**i}', '0', '255']
            for band in self.bandasRGBYFC:
                rutaCompleta = glob.glob(os.path.join(path,band))[0]
                nombre = band.replace('*','')
                nombre = nombre.split('_',1)[0]
                gdal.Translate(os.path.join(self.rutaBandas,f'{nombre}_{i}bits.tif'), gdal.Open(rutaCompleta), options=gdal_translate_options)
        gdal_translate_options = ['-b', '1'] 
    def construirImgSen2(self):
        gdal_translate_options = ['-b', '1']
        bandas = ['B02','B03','B04','B08']
        #Combinacion de coloeres rgb('B04','B03','B02'),FC('B08','B04','B03')
        for i in range(12,15):
            for band in bandas:
                rutaBanda = os.path.join(self.rutaBandas,f'{band}_{i}bits.tif')  
                gdal.Translate(os.path.join(self.temp,f'{band}.vrt'), rutaBanda, options=gdal_translate_options)
            #Construccion de imagen RGB
            gdal_buildvrt_options = ['-separate']
            gdal.BuildVRT(os.path.join(self.temp,'rgb.vrt'),[os.path.join(self.temp,'B04.vrt'), os.path.join(self.temp,'B03.vrt'), os.path.join(self.temp,'B02.vrt')],options=gdal_buildvrt_options)
            gdal_translate_options = ['-of', 'GTiff', '-ot', 'Byte']   
            gdal.Translate(os.path.join(self.rutaImg,f'rgb_{i}bits.tif'),os.path.join(self.temp,'rgb.vrt'), options=gdal_translate_options)    
            #Construccion de imagen FC
            gdal_buildvrt_options = ['-separate']
            gdal.BuildVRT(os.path.join(self.temp,'fc.vrt'),[os.path.join(self.temp,'B08.vrt'), os.path.join(self.temp,'B04.vrt'), os.path.join(self.temp,'B03.vrt')],options=gdal_buildvrt_options)
            gdal_translate_options = ['-of', 'GTiff', '-ot', 'Byte']   
            gdal.Translate(os.path.join(self.rutaImg,f'fc_{i}bits.tif'),os.path.join(self.temp,'fc.vrt'), options=gdal_translate_options)

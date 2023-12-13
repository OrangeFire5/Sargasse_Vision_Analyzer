import os
from osgeo import gdal

#Realiza todos los procesos para generar las imagenes Sentinel-3
def procesarImagenBrutaSEN3(ruta,rutaImgBruta_bands,rutaImgBruta_temp,rutaImgBruta_img):
#<-- COMPROBACION DE Imagen SEN-3 -->
    if not os.path.exists(os.path.join(ruta, "geo_coordinates.nc")):
        return False
    #Comprueba la existencia de las bandas y almacena los nombre en una lista
    allBands=[]
    for i in range(1,22):
        banda = f"Oa0{i}_radiance.nc" if i < 10 else f"Oa{i}_radiance.nc"
        if not os.path.exists(os.path.join(ruta, banda)):
            return False
        allBands.append(os.path.join(ruta, banda))
#<-- COMPROBACION DE Imagen SEN-3 -->
    # Definir la lista de archivos de entrada y otras opciones de fusión
    input_files = [f'{os.path.join(ruta,"Oa04_radiance.nc")}', f'{os.path.join(ruta,"Oa06_radiance.nc")}',f'{os.path.join(ruta,"Oa08_radiance.nc")}',f'{os.path.join(ruta,"Oa17_radiance.nc")}']
    #Modos de color = 14,15,16 bits
    obtenerLatYLon(ruta,rutaImgBruta_temp)
    construirCapasSen3(allBands,rutaImgBruta_bands)
    for i in range(14,17):
        construirCapasSen3(input_files,rutaImgBruta_bands,i)
        construirImgYGeoRefSen3(rutaImgBruta_bands,rutaImgBruta_temp,rutaImgBruta_img,i)
        construirImgYGeoRefSen3(rutaImgBruta_bands,rutaImgBruta_temp,rutaImgBruta_img,i,"FC")
    return True

def construirCapasSen3(input_files,rutaImgBruta_bands,bits=16):
    gdal_translate_options = ['-of', 'GTiff','-ot', 'Byte','-scale', '0', f'{2**bits}', '0', '255']
    for file in input_files:
        # Construir el comando gdal_translate
        nombre = os.path.splitext(file)[0]
        nombre = os.path.basename(nombre)
        gdal.Translate(os.path.join(rutaImgBruta_bands,f'{nombre}.tif') if bits == 16 else os.path.join(rutaImgBruta_bands,f'{nombre}_{bits}bits.tif'), gdal.Open(file), options=gdal_translate_options)


def obtenerLatYLon(ruta,rutaImgBruta_temp):
        gdal_translate_options = ['-of', 'VRT']
        gdal.Translate(os.path.join(rutaImgBruta_temp,'lat.vrt'), gdal.Open(f'NETCDF:"{os.path.join(ruta,'geo_coordinates.nc')}":latitude'), options=gdal_translate_options)
        gdal.Translate(os.path.join(rutaImgBruta_temp,'lon.vrt'), gdal.Open(f'NETCDF:"{os.path.join(ruta,'geo_coordinates.nc')}":longitude'), options=gdal_translate_options)

def construirImgYGeoRefSen3(rutaImgBruta_bands,rutaImgBruta_temp,rutaImgBruta_img,bits=16,mode="RGB"): 
    pathLat = os.path.join(rutaImgBruta_temp,'lat.vrt')
    pathLon =  os.path.join(rutaImgBruta_temp,'lon.vrt')
    pathGeo = os.path.join(rutaImgBruta_temp,'geo.tif')
    pathCoord = os.path.join(rutaImgBruta_temp,'coord.vrt')
    pathInfo = os.path.join(rutaImgBruta_temp,'info.txt')
    
    if mode == "RGB":
        bandRed= os.path.join(rutaImgBruta_bands,f'Oa08_radiance.tif') if bits == 16 else os.path.join(rutaImgBruta_bands,f'Oa08_radiance_{bits}bits.tif')
        bandVerde= os.path.join(rutaImgBruta_bands,f'Oa06_radiance.tif') if bits == 16 else os.path.join(rutaImgBruta_bands,f'Oa06_radiance_{bits}bits.tif')
        bandAzul= os.path.join(rutaImgBruta_bands,f'Oa04_radiance.tif') if bits == 16 else os.path.join(rutaImgBruta_bands,f'Oa04_radiance_{bits}bits.tif')
        pathImage= os.path.join(rutaImgBruta_img,f'rgb_{bits}bits.tif')
    elif mode == "FC":
        bandRed= os.path.join(rutaImgBruta_bands,f'Oa17_radiance.tif') if bits == 16 else os.path.join(rutaImgBruta_bands,f'Oa17_radiance_{bits}bits.tif')
        bandVerde= os.path.join(rutaImgBruta_bands,f'Oa08_radiance.tif') if bits == 16 else os.path.join(rutaImgBruta_bands,f'Oa08_radiance_{bits}bits.tif')
        bandAzul= os.path.join(rutaImgBruta_bands,f'Oa06_radiance.tif') if bits == 16 else os.path.join(rutaImgBruta_bands,f'Oa06_radiance_{bits}bits.tif')
        pathImage= os.path.join(rutaImgBruta_img,f'fc_{bits}bits.tif')

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
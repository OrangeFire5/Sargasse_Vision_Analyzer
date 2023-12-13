import os
import glob
from osgeo import gdal
#Funcion ejecutora
def procesarImagenBrutaSEN2(ruta,rutaImgBruta_bands,rutaImgBruta_temp,rutaImgBruta_img):
    path = os.path.join(ruta, f"GRANULE/*/IMG_DATA")
    resEspacial=["R10m","R20m","R60m"]
    bandasRGBYFC =['*B02_10m.jp2','*B03_10m.jp2','*B04_10m.jp2','*B08_10m.jp2']
    bandas = [['*B02_10m.jp2','*B03_10m.jp2','*B04_10m.jp2','*B08_10m.jp2'],
              ['*B05_20m.jp2','*B06_20m.jp2','*B07_20m.jp2','*B11_20m.jp2','*B12_20m.jp2','*B8A_20m.jp2'],
              ['*B01_60m.jp2','*B09_60m.jp2']]
    #<-- COMPROBACION DE Imagen SEN-3 -->
    for i in range(0,3):
        pathActual = os.path.join(path,resEspacial[i])
        for band in bandas[i]:
            if len(glob.glob(os.path.join(pathActual,band))) == 0:
                return False
    #<-- COMPROBACION DE Imagen SEN-3 -->        
    construirCapasSEN2(path, rutaImgBruta_bands,resEspacial,bandas,bandasRGBYFC)
    bandasRGBYFC = ['B02','B03','B04','B08']
    construirImgSen2(bandasRGBYFC,rutaImgBruta_bands,rutaImgBruta_temp,rutaImgBruta_img)

    return True
#Contructor de bandas
def construirCapasSEN2(path, rutaImgBruta_bands,resEspacial,bandas,bandasRGBYFC):
    gdal_translate_options = ['-of', 'GTiff','-ot', 'Uint16']
    #Obtencion de bandas de 16 bits
    for i in range(0,3):
        pathActual = os.path.join(path,resEspacial[i])
        for band in bandas[i]:
            rutaCompleta = glob.glob(os.path.join(pathActual,band))[0]
            nombre = band.replace('*','')
            nombre = nombre.split('_',1)[0]
            gdal.Translate(os.path.join(rutaImgBruta_bands,f'{nombre}.tif'), gdal.Open(rutaCompleta), options=gdal_translate_options)
    #Contruccion de bandas para obtencion de imagen:
    path = os.path.join(path, "R10m")
    for i in range(12,15):
        gdal_translate_options = ['-of', 'GTiff','-ot', 'Byte','-scale', '0', f'{2**i}', '0', '255']
        for band in bandasRGBYFC:
            rutaCompleta = glob.glob(os.path.join(path,band))[0]
            nombre = band.replace('*','')
            nombre = nombre.split('_',1)[0]
            gdal.Translate(os.path.join(rutaImgBruta_bands,f'{nombre}_{i}bits.tif'), gdal.Open(rutaCompleta), options=gdal_translate_options)
#Constructor de imagenes
def construirImgSen2(bandas,rutaImgBruta_bands,rutaImgBruta_temp,rutaImgBruta_img):
    gdal_translate_options = ['-b', '1']
    #Combinacion de coloeres rgb('B04','B03','B02'),FC('B08','B04','B03')
    for i in range(12,15):
        for band in bandas:
            rutaBanda = os.path.join(rutaImgBruta_bands,f'{band}_{i}bits.tif')  
            gdal.Translate(os.path.join(rutaImgBruta_temp,f'{band}.vrt'), rutaBanda, options=gdal_translate_options)
        #Construccion de imagen RGB
        gdal_buildvrt_options = ['-separate']
        gdal.BuildVRT(os.path.join(rutaImgBruta_temp,'rgb.vrt'),[os.path.join(rutaImgBruta_temp,'B04.vrt'), os.path.join(rutaImgBruta_temp,'B03.vrt'), os.path.join(rutaImgBruta_temp,'B02.vrt')],options=gdal_buildvrt_options)
        gdal_translate_options = ['-of', 'GTiff', '-ot', 'Byte']   
        gdal.Translate(os.path.join(rutaImgBruta_img,f'rgb_{i}bits.tif'),os.path.join(rutaImgBruta_temp,'rgb.vrt'), options=gdal_translate_options)    
        #Construccion de imagen FC
        gdal_buildvrt_options = ['-separate']
        gdal.BuildVRT(os.path.join(rutaImgBruta_temp,'fc.vrt'),[os.path.join(rutaImgBruta_temp,'B08.vrt'), os.path.join(rutaImgBruta_temp,'B04.vrt'), os.path.join(rutaImgBruta_temp,'B03.vrt')],options=gdal_buildvrt_options)
        gdal_translate_options = ['-of', 'GTiff', '-ot', 'Byte']   
        gdal.Translate(os.path.join(rutaImgBruta_img,f'fc_{i}bits.tif'),os.path.join(rutaImgBruta_temp,'fc.vrt'), options=gdal_translate_options)
from tkinter import filedialog
class Controller:
    def __init__(self, master):
        self.master = master
        self.frmImagen1 = None
        self.frmImagen2 = None
        self.frmTablaSelecciones = None
        self.frmBotones = None
        self.frmGestorArchivos =None
        self.Areas =[]

    def set_frmImagen1(self, frmImagen):
        self.frmImagen1 = frmImagen
    def set_frmImagen2(self, frmImagen):
        self.frmImagen2 = frmImagen
    def set_frmTablaSelecciones(self, frmTablaSelecciones):
        self.frmTablaSelecciones= frmTablaSelecciones
    def set_frmBotones(self, frmBotones):
        self.frmBotones = frmBotones
    def set_gestorArchivos(self,frmGestorArchivos):
        self.frmGestorArchivos = frmGestorArchivos

    ##  Sincronizar ##
    def existeImagenEnOtroFrame(self,nombre):
        if nombre == "FrameImagen1":
            return self.frmImagen2.ImagenCargada
        elif nombre == "FrameImagen2":
            return self.frmImagen1.ImagenCargada   
    def sincronizarTool(self,nombre):
        if nombre == "FrameImagen1":
            if self.frmImagen1.sincronizar != self.frmImagen2.sincronizar:
                self.frmImagen2.sincronizarTool()
                if self.frmImagen2.sincronizar:
                    self.ajustarVista(nombre,self.frmImagen1.ax.get_xlim(),self.frmImagen1.ax.get_ylim())
        elif nombre == "FrameImagen2":
            if self.frmImagen1.sincronizar != self.frmImagen2.sincronizar:
                self.frmImagen1.sincronizarTool()
                if self.frmImagen1.sincronizar:
                    self.ajustarVista(nombre,self.frmImagen2.ax.get_xlim(),self.frmImagen2.ax.get_ylim())
    def ajustarVista(self,nombre,limX,limY):
        if nombre == "FrameImagen1":
            self.frmImagen2.ax.set_xlim(limX[0],limX[1])
            self.frmImagen2.ax.set_ylim(limY[0],limY[1])
            self.frmImagen2.canvas.draw()
        elif nombre == "FrameImagen2":
            self.frmImagen1.ax.set_xlim(limX[0],limX[1])
            self.frmImagen1.ax.set_ylim(limY[0],limY[1])
            self.frmImagen1.canvas.draw()
    def aplicarAjuste(self,nombre):
        if nombre == "FrameImagen1":
            self.frmImagen2.sincronizar = False
            self.frmImagen2.ajustarVista()
            self.frmImagen2.sincronizar = True
        elif nombre == "FrameImagen2":
            self.frmImagen1.sincronizar = False
            self.frmImagen1.ajustarVista()
            self.frmImagen1.sincronizar = True
    ## Fin - Sincronizar ##
            
    ## AREAS ##
    #Construccion de Areas#
    def set_Area(self,idLocal,frmImagen,area,tipo):
        a=[]
        a.append(len(self.Areas))
        a.append(idLocal)
        a.append(frmImagen)
        a.append(area)
        a.append(tipo)
        self.Areas.append(a)
    def agregarAreaATablaSelecciones(self,puntos,coord,choose="F+"):
        self.frmTablaSelecciones.insertarDatos(len(self.Areas),puntos,coord,choose)
        self.activarBtnEliminarSelecciones()
        self.activarBtnExportarSeleccion()
        self.activarBtnExportarSelecciones()

    #Modo edicion#
    def desactivarSelecciones(self,newArea=False):
        if not newArea:
            self.frmTablaSelecciones.deseleccionar()
        self.desactivarBtnEliminarSelecciones()
        self.desactivarBtnExportarSeleccion()   
    def activarModoEdicion(self,ids,color):
        self.Areas[ids][2].activarModoEdicion(self.Areas[ids][1],color)
        self.activarBtnEliminarSelecciones()
        self.activarBtnExportarSeleccion()
    # Editando #
    def modificarPuntosTabla(self,nombre,ids,puntos):
        for a in self.Areas:
            print(f"{nombre} == {a[2].nombre} and {ids} == {a[1]}:")
            if nombre == a[2].nombre and ids == a[1]:
                self.frmTablaSelecciones.modificarPuntos(a[0]+1,puntos)
                return  
    def modificarCoordTabla(self,nombre,ids,coord):
        for a in self.Areas:
            if nombre == a[2].nombre and ids == a[1]:
                self.frmTablaSelecciones.modificarCoord(a[0]+1,coord)
                return
    def modificarChooseTabla(self,nombre,ids,choose):
        for a in self.Areas:
            if nombre == a[2].nombre and ids == a[1]:
                a[4] = choose
                self.frmTablaSelecciones.modificarChoose(a[0]+1,choose)
                return
    # Eliminando #         
    def eliminarSeleccion(self):
        ids=self.get_Id_Seleccionado()
        self.frmTablaSelecciones.eliminarArea(ids)
        ids=ids-1
        self.Areas[ids][2].eliminarArea(self.Areas[ids][1])
        del self.Areas[ids]
        frm1=0
        frm2=0
        for i in range(0,len(self.Areas)):
            self.Areas[i][0] = i
            if self.Areas[i][2].nombre == "FrameImagen1":
                self.Areas[i][1]=frm1
                frm1=frm1+1
            else: 
                self.Areas[i][1]=frm2
                frm2=frm2+1
        if len(self.Areas) == 0 :
            self.desactivarBtnExportarSelecciones()
    #Colorear Areas#
    def recolorearAreas(self):
        if self.frmImagen1.EditMode:
            self.frmImagen1.desactivarModoEdicion()
        if self.frmImagen2.EditMode:
            self.frmImagen2.desactivarModoEdicion()
        for area in self.Areas:
            color = self.colorearArea(area[3],area[4])
        self.frmImagen1.canvas.draw()
        self.frmImagen2.canvas.draw()
    def colorearArea(self,area,choose):  
        if choose == "F-" or choose ==0:
            color = self.get_colorFN()
            choose = "F-"
        elif choose == "T+" or choose ==1:
            color = self.get_colorTP()
            choose = "T+"
        elif choose == "F+" or choose ==2:
            color = self.get_colorFP()
            choose = "F+"
        else:
            color = self.get_colorTP()
            choose = "T+"
        area.set_facecolor(color)
        area.set_edgecolor(color)
        return (color,choose)

    # Obtencion de colores #
    def get_colorFN(self):
        return self.frmGestorArchivos.colorFN
    def get_colorTP(self):
        return self.frmGestorArchivos.colorTP
    def get_colorFP(self):
        return self.frmGestorArchivos.colorFP
    
    #frmBotones#
    def activarBtnExportarSelecciones(self):
        self.frmBotones.btnExportarSelecciones.config(state="active")
    def desactivarBtnExportarSelecciones(self):
        self.frmBotones.btnExportarSelecciones.config(state="disabled")
    def activarBtnExportarSeleccion(self):
        self.frmBotones.btnExportarSeleccion.config(state="active")
    def desactivarBtnExportarSeleccion(self):
        self.frmBotones.btnExportarSeleccion.config(state="disabled")
    def activarBtnEliminarSelecciones(self):
        self.frmBotones.btnElimnarSelecciones.config(state="active")
    def desactivarBtnEliminarSelecciones(self):
        self.frmBotones.btnElimnarSelecciones.config(state="disabled")
    
    #Importacion#
    def get_Id_Seleccionado(self):
        return self.frmTablaSelecciones.get_id_seleccionado()
    def exportarImagen(self):
        filename = filedialog.askdirectory()
        if filename:
            iid=self.get_Id_Seleccionado()-1
            puntos = self.Areas[iid][3].get_xy()
            xmin, ymin= round(puntos[0][0]),round(puntos[0][1])
            xmax, ymax= round(puntos[2][0]),round(puntos[2][1])

            if self.frmGestorArchivos.tipoImgBruta == "SEN3":
                latmin,lonmin = self.frmImagen1.consultarCoord(xmin,ymin)
                latmax,lonmax = self.frmImagen1.consultarCoord(xmax,ymax)
                coord =[latmin,lonmin,latmax,lonmax]
            elif self.frmGestorArchivos.tipoImgBruta == "SEN2":
                coord =[xmin,ymin,xmax-xmin,xmax-xmin]
            print(coord)
            self.frmGestorArchivos.exportarImagen(filename,coord,(iid+1))

    def exportarTodasLasAreas(self):
        filename = filedialog.askdirectory()
        if filename:
            for i in range(0,len(self.Areas)):
                puntos = self.Areas[i][3].get_xy()
                xmin, ymin= round(puntos[0][0]),round(puntos[0][1])
                xmax, ymax= round(puntos[2][0]),round(puntos[2][1])

                if self.frmGestorArchivos.tipoImgBruta == "SEN3":
                    latmin,lonmin = self.frmImagen1.consultarCoord(xmin,ymin)
                    latmax,lonmax = self.frmImagen1.consultarCoord(xmax,ymax)
                    coord =[latmin,lonmin,latmax,lonmax]
                elif self.frmGestorArchivos.tipoImgBruta == "SEN2":
                    coord =[xmin,ymin,xmax-xmin,xmax-xmin]
                self.frmGestorArchivos.exportarImagen(filename,coord,(i+1))
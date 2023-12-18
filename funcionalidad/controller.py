class Controller:
    def __init__(self, master):
        self.master = master
        self.frmImagen1 = None
        self.frmImagen2 = None
        self.frmTablaSelecciones = None
        self.frmBotones = None
        self.frmGestorArchivos =None
        self.frmArea = []

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
    #Funciones de manejo de Tabla de selecciones
    def agregarAreaATablaSelecciones(self,ids,puntos,coord,choose="F+"):
        self.frmTablaSelecciones.insertarDatos(ids,puntos,coord,choose)
    def modificarPuntosTabla(self,ids,puntos):
        self.frmTablaSelecciones.modificarPuntos(ids,puntos)
    def modificarCoordTabla(self,ids,coord):
        self.frmTablaSelecciones.modificarCoord(ids,coord)
    def modificarChooseTabla(self,ids,choose):
        self.frmTablaSelecciones.modificarChoose(ids,choose)
    def set_frmArea(self,nombre):
        self.frmArea.append(nombre)
    def desactivarSelecciones(self): 
        self.frmTablaSelecciones.deseleccionar_todo()
        self.desactivarBtnEliminarSelecciones()
        self.desactivarBtnExportarSeleccion()
    def activarModoEdicion(self,ids,color):
        self.activarBtnEliminarSelecciones()
        self.activarBtnExportarSeleccion()
        if self.frmArea[ids] == "FrameImagen1": 
            self.frmImagen1.activarEdicionArea(ids,color)
        elif self.frmArea[ids] == "FrameImagen2":
            self.frmImagen2.activarEdicionArea(ids,color)
    def eliminarSeleccion(self):
        ids=self.frmTablaSelecciones.get_id_seleccionado()
        self.frmTablaSelecciones.eliminarArea(ids)
        ids=ids-1
        if self.frmArea[ids] == "FrameImagen1": 
            self.frmImagen1.eliminarSeleccion(ids)
        elif self.frmArea[ids] == "FrameImagen2":
            self.frmImagen2.eliminarSeleccion(ids)
        del self.frmArea[ids]
    def seleccionar(self,ids):
        self.frmTablaSelecciones.treeview.selection_set(ids)
        self.activarBtnEliminarSelecciones()
        self.activarBtnExportarSeleccion()
    def activarBtnEliminarSelecciones(self):
        self.frmBotones.btnElimnarSelecciones.config(state="active")
    def desactivarBtnEliminarSelecciones(self):
        self.frmBotones.btnElimnarSelecciones.config(state="disabled")
    def activarBtnExportarSeleccion(self):
        self.frmBotones.btnExportarSeleccion.config(state="active")
    def desactivarBtnExportarSeleccion(self):
        self.frmBotones.btnExportarSeleccion.config(state="disabled")

            


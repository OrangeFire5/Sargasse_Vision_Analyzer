class Controller:
    def __init__(self, master):
        self.master = master
        self.frmImagen1 = None
        self.frmImagen2 = None

    def set_frmImagen1(self, frmImagen):
        self.frmImagen1 = frmImagen
    def set_frmImagen2(self, frmImagen):
        self.frmImagen2 = frmImagen

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
from gl import Bitmap

bmp = Bitmap(800, 800)

def glInit():
    return bmp


if __name__ == '__main__':

    #Inicializa obj
    bmp = glInit()

    #Cambia todos los pixeles de un color
    bmp.glClear()

    #Colores de pixeles
    bmp.glColor(1, 1, 0)

    bmp.glLoadObjModel('face.obj', (0, 0), (0.03, 0.03))
    
    #Output BMP
    bmp.glWrite("out.bmp")

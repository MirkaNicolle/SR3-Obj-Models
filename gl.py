#Mirka Monzon 18139
#SR3 - OBJ models

import struct
from obj import ObjReader

#Definicion
def char(c):
    return struct.pack('=c', c.encode('ascii'))

def word(w):
    return struct.pack('=h', w)

def dword(d):
    return struct.pack('=l', d)

def color(r,g,b):
    return bytes([b, g, r])

#Constructor
class Bitmap(object):
    
    def __init__(self, height, width):

        self.height = height
        self.width = width
        self.framebuffer = []
        self.clear_color = color(0, 0, 0)
        self.vertex_color = color(255, 0, 0)
        self.glClear()

    #Inicializacion de software render 
    def glInit(self):
        pass

#Funciones de render 
    #Inicializacion de framebuffer
    def glCreateWindow(self, height, width):
        self.height = height
        self.width = width
        self.glClear()

    #Creacion de espacio para dibujar
    def glViewPort(self, x, y, width, height):
        self.x = x
        self.y = y
        self.vpx = width
        self.vpy = height

     #Mapa de bits de un solo color
    def glClear(self):
        self.framebuffer = [
            [self.clear_color for x in range(self.width)] for y in range(self.height)
        ]
    
    #Cambio de color de glClear
    def glClearColor(self, r, g, b):
        try:
            self.rc = round(255*r)
            self.gc = round(255*g)
            self.bc = round(255*b)
            self.clear_color = color(self.rc, self.rg, self.rb)
        except ValueError:
            print('\nERROR: Ingrese un número entre 1 y 0\n')
    
    #Cambio de color de punto en pantalla
    def glVertex(self, x, y):
        if x <= 1 and x>= -1 and y >= -1 and y <= 1:
                
                if x > 0:
                        self.vx = self.x + round(round(self.vpx/2)*x) - 1
                if y > 0:
                        self.vy = self.y + round(round(self.vpy/2)*y) - 1
                if x <= 0:
                        self.vx = self.x + round(round(self.vpx/2)*x)
                if y <= 0:
                        self.vy = self.y + round(round(self.vpy/2)*y)
                
                self.glPoint(self.vx,self.vy, self.vertex_color)
        else:
                pass
    
    #Cambio de color con el que funciona glVertex
    def glColor(self, r, g, b):
        try:
            self.rv = round(255*r)
            self.gv = round(255*g)
            self.bv = round(255*b)
            self.vertex_color = color(self.rv,self.gv,self.bv)
        except ValueError:
                print('\nERROR: Ingrese un número entre 1 y 0\n')

    #Da el color al punto en pantalla 
    def glPoint(self, x, y, color):
        x = int(round((x+1) * self.width / 2))
        y = int(round((y+1) * self.height / 2))
        try:
                self.framebuffer[y][x] = color
        except IndexError:
                print("\nEl pixel está fuera de los límites de la imagen.\n")
    
     #Funcion para linea 
    def glLine(self, x0, y0, x1, y1):
        #Convierte los valores entre -1 a 1 a cordenadas DMC
        x0 = int(round((x0 + 1) * self.width / 2))
        y0 = int(round((y0 + 1) * self.height / 2))
        x1 = int(round((x1 + 1) * self.width / 2))
        y1 = int(round((y1 + 1) * self.height / 2))

        dy = abs(y1 - y0)
        dx = abs(x1 - x0)

        steep = dy > dx
        
        #Si dy es mayor que dx entonces intercambiamos cada una de las coordenadas
        if steep:
            x0, y0 = y0, x0
            x1, y1 = y1, x1
        
        #Si el punto de inicio en x es mayor que el punto final, intercambia los puntos
        if x0 > x1:
            x0, x1 = x1, x0
            y0, y1 = y1, y0
        
        dy = abs(y1 - y0)
        dx = abs(x1 - x0)

        #Determina los puntos que formarán la línea
        offset = 0.5 * 2 * dx
        threshold = 0.5 * 2 * dx
        y = y0

        #Rellena la línea con puntos sin dejar espacios
        for x in range(x0, x1 + 1):
            if steep:
                self.glPoint((float(y)/(float(self.width)/2))-1,(float(x)/(float(self.height)/2))-1,self.vertex_color)
            else:
                self.glPoint((float(x)/(float(self.width)/2))-1,(float(y)/(float(self.height)/2))-1,self.vertex_color)
            offset += dy

            if offset >= threshold:
                y += 1 if y0 < y1 else -1
                threshold += 1 * dx

    def glFillPolygon(self, polygon):
        #Point-in-Polygon (PIP) Algorithm
        for y in range(self.height):
            for x in range(self.width):
                i = 0
                j = len(polygon) - 1
                draw_point = False
                #Verifica si el punto está entre los límites
                for i in range(len(polygon)):
                    if (polygon[i][1] < y and polygon[j][1] >= y) or (polygon[j][1] < y and polygon[i][1] >= y):
                        if polygon[i][0] + (y - polygon[i][1]) / (polygon[j][1] - polygon[i][1]) * (polygon[j][0] - polygon[i][0]) < x:
                            draw_point = not draw_point
                    j = i
                if draw_point:
                    self.glPoint((float(x)/(float(self.width)/2))-1,(float(y)/(float(self.height)/2))-1,self.vertex_color)

    #Lee y renderiza archivos .obj 
    def glLoadObjModel(self, file_name, translate=(0,0), scale=(1,1)):
        #Lector .obj
        model = ObjReader(file_name)
        model.readLines()
        
        for face in model.faces:
            vertices_ctr = len(face)
            for j in range(vertices_ctr):
                f1 = face[j][0]
                f2 = face[(j+1) % vertices_ctr][0]
                
                v1 = model.vertices[f1 - 1]
                v2 = model.vertices[f2 - 1]

                x1 = (v1[0] + translate[0]) * scale[0]
                y1 = (v1[1] + translate[1]) * scale[1]
                x2 = (v2[0] + translate[0]) * scale[0]
                y2 = (v2[1] + translate[1]) * scale[1]

                self.glLine(x1, y1, x2, y2)


    def glWrite(self, file_name):
        bmp_file = open(file_name, 'wb')

        #Header
        bmp_file.write(char('B'))
        bmp_file.write(char('M'))
        bmp_file.write(dword(14 + 40 + self.width * self.height))
        bmp_file.write(dword(0))
        bmp_file.write(dword(14 + 40))
        
        #image header 
        bmp_file.write(dword(40))
        bmp_file.write(dword(self.width))
        bmp_file.write(dword(self.height))
        bmp_file.write(word(1))
        bmp_file.write(word(24))
        bmp_file.write(dword(0))
        bmp_file.write(dword(self.width * self.height * 3))
        bmp_file.write(dword(0))
        bmp_file.write(dword(0))
        bmp_file.write(dword(0))
        bmp_file.write(dword(0))

        for x in range(self.height):
            for y in range(self.width):
                bmp_file.write(self.framebuffer[x][y])
            
        bmp_file.close()
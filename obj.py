#Mirka Monzon 18139
#SR3 - OBJ models


#Lector .obj
class ObjReader(object):
    
    #Constructor
    def __init__(self, filename):
        #Lee y renderiza archivos .obj 
        with open(filename) as obj_file:
            self.lines = obj_file.read().splitlines()
        
        self.vertices = []
        self.normals = []
        self.tex_coords = []
        self.faces = []

        #Lee lineas individuales de .obj
        self.readLines()
    
    #Remueve espacios vacios
    def removeSpaces(self, face):

        store_data = face.split('/')

        if ("") in store_data:
            store_data.remove("")
        
        return map(int, store_data)

    #Lee lineas individuales de .obj
    def readLines(self):
        for line in self.lines:
            if line:
                prefix, value = line.split(' ', 1)
                if prefix == 'v':
                    self.vertices.append(list(map(float,value.split(' '))))
                elif prefix == 'vn':
                    self.normals.append(list(map(float,value.split(' '))))
                elif prefix == 'vt':
                    self.tex_coords.append(list(map(float,value.split(' '))))
                elif prefix == 'f':
                    self.faces.append([list(self.removeSpaces(face)) for face in value.split(' ')])
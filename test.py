import pandas as pd
import numpy as np
from pandas.tseries.offsets import BusinessDay


'''
PPG_Planning_Class
Item
Plant
Required_Completion_Date
'''
# PRUEBAS DE AQUI HACIA ABAJO
class Color:
    def __init__(self, nombre, planta, fecha_fin, standar_prod_time, routing_code):
        self.nombre = nombre
        self.planta = planta
        self.fecha_fin = fecha_fin
        self.standar_prod_time = standar_prod_time
        self.routing_code = routing_code
    
    def insertarMezclaNueva(self, nombre, planta, fecha_fin, standar_prod_time, routing_code):
        self.nombre = nombre
        self.planta = planta
        self.fecha = fecha_fin
        self.standar_prod_time = standar_prod_time
        self.routing_code = routing_code

    def __repr__(self):
        return f"Color(nombre={self.nombre}, planta={self.planta}, fecha_fin={self.fecha_fin}, standar_prod_time={self.standar_prod_time}, routing_code={self.routing_code})"


    # faltaria poner los getters, porque setters ponemos lo de arriba


class Equipo:
    def __init__(self, color: Color, planta, tecnologia, capacidad):
        self.color = color
        self.planta = planta
        self.tecnologia = tecnologia
        self.capacidad = capacidad
        self.working = True # mirar esto porque alomejor no hace falta si tenemos fechas de inicio y fin
        # mirar si tengo que poner fechas de inicio y final

    def isWorking(self):
        if self.working == False:
            return False
        return True
    
    def __repr__(self):
        return f"Equipo(planta={self.planta}, tecnologia={self.tecnologia}, color={self.color}, capacidad={self.capacidad})"

    #falta poner los getters para devolver cosas


def crear_lista_colores(datos_pinturas):
    lista_colores = []
    for _, fila in datos_pinturas.iterrows():
        if pd.isnull(fila["Item"]):
            continue
         
        color_obj = Color(
            nombre=fila["Item"],
            planta=fila["Plant"],
            fecha_fin=fila["Required_Completion_Date"],
            standar_prod_time=fila["Standard_Prod_Time"],
            routing_code=fila["Routing_Code"]
        )
        lista_colores.append(color_obj)
    return lista_colores

def print_lista_colores(lista_colores):
    for color in lista_colores:
        print(color)

def crear_lista_equipos(datos_equipos, datos_diluidores):
    lista_equipos = []
    
    # Convertimos datos_diluidores en un diccionario para acceder rápido a la cantidad de equipos
    diluidores_dict = pd.Series(datos_diluidores["Nº Equipos"].values, index=datos_diluidores["Etiquetas de fila"]).to_dict()
    
    for _, fila in datos_equipos.iterrows():
        # Obtenemos el tipo de equipo y su cantidad desde datos_diluidores
        equipo_tipo = fila["Equipo"]
        cantidad = diluidores_dict.get(equipo_tipo, 1)  # Si no hay cantidad especificada, asumimos 1

        # Creamos los objetos Equipo según la cantidad especificada
        for _ in range(cantidad):
            equipo_obj = Equipo(
                planta=fila["Planta"],
                tecnologia=fila["Tecnología"],
                color=fila["Planning Class"],
                capacidad=fila["Capacidad (lote/semana)"]
            )
            lista_equipos.append(equipo_obj)

    return lista_equipos

def print_lista_equipos(lista_equipos):
    for equipo in lista_equipos:
        print(equipo)

#-----------------------------------

def print_pinturas(datos_pinturas):
    #datos_pinturas["Tecnologia"].fillna("-", inplace=True)

    # esto lo tengo por ahora para hacer pruebas
    for i in datos_pinturas["Routing_Code"]:
        if i.split("-")[2] == "PPIMM" or i.split("-")[2] == "ZPIMM":
            print(f"ES METALICO - {i}")
        elif i.split("-")[2] == "PPISC" or i.split("-")[2] == "ZPISC":
            print(f"ES OPACO - {i}")
        else:
            print("broma")

    # Muestra los primeros registros
    print("\n\n" + str(datos_pinturas))

def print_equipos(datos_equipos):
    # cambiar despues esto porque da warning de que esta deprecated
    datos_equipos.fillna("-", inplace=True)

    print(datos_equipos)

def print_diluidores(datos_diluidores):
    # cambiar despues esto porque da warning de que esta deprecated
    datos_diluidores.fillna("-", inplace=True)

    print(datos_diluidores)


if __name__=="__main__":
    ruta_archivo = "./plan.xlsx"
    datos_pinturas = pd.read_excel(ruta_archivo, sheet_name="prod", usecols=["PPG_Planning_Class", "Item", "Plant","Required_Completion_Date", "Standard_Prod_Time", "Routing_Code"])
    datos_equipos = pd.read_excel(ruta_archivo, sheet_name="equipos", usecols=["Planning Class", "Planta", "Tecnología", "Equipo", "Capacidad (lote/semana)"])
    datos_diluidores = pd.read_excel(ruta_archivo, sheet_name="maquinas", usecols=["Etiquetas de fila", "Nº Equipos"])
    #print_pinturas(datos_pinturas)
    lista_colores = crear_lista_colores(datos_pinturas)
    print_lista_colores(lista_colores)
    lista_equipos = crear_lista_equipos(datos_equipos, datos_diluidores)
    print_lista_equipos(lista_equipos)


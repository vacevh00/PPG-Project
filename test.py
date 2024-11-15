import pandas as pd
import numpy as np
from pandas.tseries.offsets import BusinessDay
from collections import defaultdict
import datetime

'''
PPG_Planning_Class
Item
Plant
Required_Completion_Date
'''
# Clase para representar cada lote de un color
class Color:
    def __init__(self, nombre, planta, fecha_fin, standar_prod_time, routing_code):
        self.nombre = nombre
        self.planta = planta
        self.fecha_fin = fecha_fin
        #self.fecha_required = fecha_required
        self.standar_prod_time = standar_prod_time
        self.routing_code = routing_code
    
    def insertarMezclaNueva(self, nombre, planta, fecha_fin, standar_prod_time, routing_code):
        self.nombre = nombre
        self.planta = planta
        self.fecha = fecha_fin
        #self.fecha_required = fecha_required
        self.standar_prod_time = standar_prod_time
        self.routing_code = routing_code
    
    def getNombre(self):
        return self.nombre

    def __repr__(self):
        return f"Color(nombre={self.nombre}, planta={self.planta}, fecha_fin={self.fecha_fin}, standar_prod_time={self.standar_prod_time}, routing_code={self.routing_code})"


# Clase que representa cada máquina
class Equipo:
    def __init__(self, clases, planta, tecnologia, capacidad, nombre, cantidad):
        self.clases = set(clases)
        self.nombre = nombre
        self.planta = planta
        self.tecnologia = tecnologia
        self.capacidad = capacidad
        self.cantidad = cantidad

    def add_color(self, color):
        self.colores.add(color)
    
    def have_color(self, color):
        return color in self.colores
    
    def to_string_set(self):
        result = ""
        for i in self.clases:
            result += i + ", "
        return result
    
    def __repr__(self):
        return f"Equipo(nombre={self.nombre}, planta={self.planta}, tecnologia={self.tecnologia}, clases={self.to_string_set()}, capacidad={self.capacidad}, cantidad={self.cantidad})"


# Lista con los pedidos que tenemos que fabricar
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
        color_obj.fecha_fin = color_obj.fecha_fin.date()
        if color_obj.routing_code.split("-")[2] == "PPIMM" or color_obj.routing_code.split("-")[2] == "ZPIMM":
            color_obj.routing_code ="Metalico"
        elif color_obj.routing_code.split("-")[2] == "PPISC" or color_obj.routing_code.split("-")[2] == "ZPISC":
            color_obj.routing_code ="Opaco"
        lista_colores.append(color_obj)
    return lista_colores

# toString de una lista de colores
def print_lista_colores(lista_colores):
    for color in lista_colores:
        print(color)

# Lista con los equipos que tenemos en la fábrica
'''def crear_lista_equipos(datos_equipos, datos_diluidores, lista_colores):
    lista_equipos = []
    
    # Convertimos datos_diluidores en un diccionario para acceder rápido a la cantidad de equipos
    diluidores_dict = pd.Series(datos_diluidores["Nº Equipos"].values, index=datos_diluidores["Etiquetas de fila"]).to_dict()
    colores2 = set()
    equipo_ant = ""
    planta2 = ""
    tecnologia2 = ""
    equipo_tipo2 = ""
    capacidad2 = ""
    for _, fila in datos_equipos.iterrows():
        # Obtenemos el tipo de equipo y su cantidad desde datos_diluidores
        equipo_tipo2 = fila["Equipo"]
        if(equipo_ant==""):
            equipo_ant = equipo_tipo2
            colores2.add(fila["Planning Class"])
        if(equipo_tipo2==equipo_ant):
            colores2.add(fila["Planning Class"])
        else:
            for _ in range(diluidores_dict[equipo_ant]):
                equipo_obj = Equipo(
                    planning-classes=colores2,
                    planta=planta2,
                    tecnologia=tecnologia2,
                    equipo_tipo=equipo_tipo2,
                    capacidad=capacidad2
                )
                if pd.isna(equipo_obj.capacidad):
                    equipo_obj.capacidad = fila["Capacidad(Lote/dia)"]*5
                lista_equipos.append(equipo_obj)
            equipo_ant=equipo_tipo2
            planta2=fila["Planta"]
            tecnologia2=fila["Tecnología"]
            capacidad2=fila["Capacidad (lote/semana)"]
            colores2 = set()
    return lista_equipos'''

def crear_lista_equipos(datos_equipos, datos_diluidores, lista_colores):
    lista_equipos = []
    diluidores_dict = pd.Series(datos_diluidores["Nº Equipos"].values, index=datos_diluidores["Etiquetas de fila"]).to_dict()

    for _, fila in datos_equipos.iterrows():
        # Obtenemos el tipo de equipo y su cantidad desde datos_diluidores
        nombreEq = fila["Equipo"]
        cant = diluidores_dict.get(nombreEq, 1)  # Si no hay cantidad especificada, asumimos 1
        
        # Buscamos si ya existe un equipo del mismo tipo en la lista
        equipo_existente = next((eq for eq in lista_equipos if eq.nombre == nombreEq), None)

        if equipo_existente:
            # Si existe, añadimos la clase si no está repetida
            if fila["Planning Class"] not in equipo_existente.clases:
                equipo_existente.clases.add(fila["Planning Class"])
        else:
            # Si no existe, creamos un nuevo equipo
            equipo_obj = Equipo(
                planta=fila["Planta"],
                tecnologia=fila["Tecnología"],
                clases={fila["Planning Class"]},  # Usamos un conjunto para evitar duplicados
                capacidad=fila["Capacidad (lote/semana)"],
                nombre=nombreEq,
                cantidad=cant
            )
            if pd.isna(equipo_obj.capacidad):
                equipo_obj.capacidad = fila["Capacidad(Lote/dia)"] * 5 #Teniendo en cuenta que la semana son 5 dias
            lista_equipos.append(equipo_obj)

    return lista_equipos


# toString de los equipos
def print_lista_equipos(lista_equipos):
    for equipo in lista_equipos:
        print(equipo)

# ordena de más urgente a menos
def ordenamiento_color(colores):
    colores_ordenados = sorted(colores, key=lambda color: color.fecha_fin, reverse=False)
    return colores_ordenados

'''def planificar_produccion(lista_colores, lista_equipos):
    lista_colores = ordenamiento_color(lista_colores)  # Ordenar colores por fecha_fin (descendente)

    calendario_equipos = defaultdict(list)  # {equipo: [(inicio, fin), ...]}
    cronograma = []  # [(color, equipo, inicio, fin)]

    for color in lista_colores:
        asignado = False

        for equipo in lista_equipos:
            if color.nombre not in equipo.colores:
                continue  # Este equipo no puede fabricar este color

            # Calcular el intervalo permitido para la producción
            fecha_inicio_permitido, fecha_terminacion_minima, fecha_terminacion_maxima = calcular_intervalo_produccion(
                color.fecha_fin, color.standar_prod_time
            )

            # Buscar un intervalo disponible para este equipo
            intervalo_disponible = buscar_intervalo_disponible(
                calendario_equipos[equipo],
                fecha_inicio_permitido,
                fecha_terminacion_maxima,
                color.standar_prod_time
            )

            if intervalo_disponible:
                # Asignar el color a este equipo
                inicio, fin = intervalo_disponible
                calendario_equipos[equipo].append((inicio, fin))
                calendario_equipos[equipo].sort()  # Mantener ordenado el calendario
                cronograma.append((color, equipo, inicio, fin))
                asignado = True
                print("Asignado")
                break

        if not asignado:
            print(f"Advertencia: No se pudo asignar el color {color.nombre}")

    return cronograma


def buscar_intervalo_disponible(calendario, fecha_inicio, fecha_fin, duracion_dias):
    duracion = BusinessDay(duracion_dias)
    inicio_actual = fecha_inicio
    while inicio_actual <= fecha_fin - duracion:
        fin_actual = inicio_actual + duracion
        # Verificar conflictos en el calendario
        if all(fin_actual <= inicio or inicio_actual >= fin for inicio, fin in calendario):
            return (inicio_actual, fin_actual)
        # Avanzar al siguiente día hábil
        inicio_actual += BusinessDay()
    return None

def print_cronograma(cronograma):
    for color, equipo, inicio, fin in cronograma:
        print(f"Color {color.nombre} -> Equipo {equipo.equipo_tipo}: {inicio} - {fin}")

def calcular_intervalo_produccion(fecha_fin, duracion_dias):
    business_day_offset = BusinessDay()
    fecha_terminacion_minima = fecha_fin - 2 * business_day_offset
    fecha_terminacion_maxima = fecha_fin + 2 * business_day_offset
    fecha_inicio_ideal = fecha_fin - duracion_dias * business_day_offset
    fecha_inicio_permitido = max(fecha_inicio_ideal, fecha_terminacion_minima - duracion_dias * business_day_offset)
    return fecha_inicio_permitido, fecha_terminacion_minima, fecha_terminacion_maxima
'''

# main
if __name__=="__main__":
    ruta_archivo = "./plan.xlsx"
    datos_pinturas = pd.read_excel(ruta_archivo, sheet_name="prod", usecols=["PPG_Planning_Class", "Item", "Plant","Required_Completion_Date", "Standard_Prod_Time", "Routing_Code"])
    datos_equipos = pd.read_excel(ruta_archivo, sheet_name="equipos", usecols=["Planning Class", "Planta", "Tecnología", "Equipo", "Capacidad (lote/semana)", "Capacidad(Lote/dia)"])
    datos_diluidores = pd.read_excel(ruta_archivo, sheet_name="maquinas", usecols=["Etiquetas de fila", "Nº Equipos"])
    #print_pinturas(datos_pinturas)
    lista_colores = crear_lista_colores(datos_pinturas)
    lista_colores = ordenamiento_color(lista_colores)
    print_lista_colores(lista_colores)
    lista_equipos = crear_lista_equipos(datos_equipos, datos_diluidores, lista_colores)
    print_lista_equipos(lista_equipos)
    #cronograma = planificar_produccion(lista_colores, lista_equipos)
    #print_cronograma(cronograma)

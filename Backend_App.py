import pandas as pd
import numpy as np
from pandas.tseries.offsets import BusinessDay
from collections import defaultdict
from workalendar.europe import CastileAndLeon
from datetime import timedelta
from collections import defaultdict
import matplotlib.pyplot as plt
import matplotlib.dates as mdates



'''
PPG_Planning_Class
Item
Plant
Required_Completion_Date
'''
# Clase para representar cada lote de un color
class Lote:
    def __init__(self, nombre, planta, fecha_required, standar_prod_time, routing_code, item):
        self.nombre = nombre
        self.planta = planta
        #self.fecha_fin = fecha_fin
        self.fecha_required = fecha_required
        self.standar_prod_time = standar_prod_time
        self.routing_code = routing_code
        self.item = item
    
    def insertarMezclaNueva(self, nombre, planta, fecha_required, standar_prod_time, routing_code, item):
        self.nombre = nombre
        self.planta = planta
        #self.fecha = fecha_fin
        self.fecha_required = fecha_required
        self.standar_prod_time = standar_prod_time
        self.routing_code = routing_code
        self.item = item
    
    def getNombre(self):
        return self.nombre

    def __repr__(self):
        return f"Lote(nombre={self.nombre}, planta={self.planta}, fecha_required={self.fecha_required}, standar_prod_time={self.standar_prod_time}, routing_code={self.routing_code} item={self.item})"


# Clase que representa cada máquina
class Equipo:
    def __init__(self, colores, planta, tecnologia, equipo_tipo, id):
        self.colores = set(colores)
        self.equipo_tipo = equipo_tipo
        self.planta = planta
        self.tecnologia = tecnologia
        self.disponibilidad = defaultdict(lambda: True)  # Fechas inicializadas como disponibles
        self.id = id

    def esta_disponible(self, fecha_inicio, fecha_fin):
        # Verifica si el equipo está disponible en todas las fechas del rango
        return all(self.disponibilidad[fecha] for fecha in self.generar_rango(fecha_inicio, fecha_fin))


    def asignar_lote(self, fecha_inicio, fecha_fin, dias_laborables):
        fecha_fin = self.calcular_fecha_fin(fecha_inicio, dias_laborables)
        for fecha in self.generar_rango(fecha_inicio, fecha_fin):
            self.disponibilidad[fecha] = False

    def liberar_lote(self, fecha_inicio, fecha_fin):
        # Libera las fechas ocupadas por un lote
        for fecha in self.generar_rango(fecha_inicio, fecha_fin):
            self.disponibilidad[fecha] = True

    @staticmethod
    def generar_rango(fecha_inicio, fecha_fin):
        cal = CastileAndLeon()
        rango = [
            fecha_inicio + timedelta(days=i)
            for i in range((fecha_fin - fecha_inicio).days + 1)
        ]
        return [fecha for fecha in rango if cal.is_working_day(fecha)]

    @staticmethod
    def calcular_fecha_fin(fecha_inicio, dias_laborales):
        cal = CastileAndLeon() 
        dias_contados = 0
        fecha_actual = fecha_inicio

        while dias_contados < dias_laborales:
            if cal.is_working_day(fecha_actual):
                dias_contados += 1
                fecha_actual += timedelta(days=1) 
            elif fecha_actual.weekday() == 6 and cal.is_holiday(fecha_actual):
                fecha_actual += timedelta(days=2) 
            else:
                fecha_actual += timedelta(days=1) 
        return fecha_actual

    def add_color(self, color):
        self.colores.add(color)
    
    def have_color(self, color):
        return color in self.colores
    
    def to_string_set(self):
        result = ""
        for i in self.colores:
            result += i + ", "
        return result
    
    def __repr__(self):
        return f"Equipo(nombre={self.equipo_tipo}, id={self.id} planta={self.planta}, tecnologia={self.tecnologia}, color={self.to_string_set()})"


# Lista con los pedidos que tenemos que fabricar
def crear_lista_colores(datos_pinturas):
    lista_colores = []
    for _, fila in datos_pinturas.iterrows():
        if pd.isnull(fila["Item"]):
            continue
         
        color_obj = Lote(
            nombre=fila["PPG_Planning_Class"],
            planta=fila["Plant"],
            fecha_required=fila["Required_Completion_Date"],
            standar_prod_time=fila["Standard_Prod_Time"],
            routing_code=fila["Routing_Code"],
            item=fila["Item"]
        )
        lista_colores.append(color_obj)
    return lista_colores

# toString de una lista de colores
def print_lista_colores(lista_colores):
    for color in lista_colores:
        print(color)

# Lista con los equipos que tenemos en la fábrica
def crear_lista_equipos(datos_equipos, datos_diluidores, lista_colores):
    lista_equipos = []
    
    # Convertimos datos_diluidores en un diccionario para acceder rápido a la cantidad de equipos
    diluidores_dict = pd.Series(datos_diluidores["Nº Equipos"].values, index=datos_diluidores["Etiquetas de fila"]).to_dict()
    colores2 = set()
    equipo_ant = ""
    planta2 = ""
    tecnologia2 = ""
    equipo_tipo2 = ""
    for _, fila in datos_equipos.iterrows():
        # Obtenemos el tipo de equipo y su cantidad desde datos_diluidores
        equipo_tipo2 = fila["Equipo"]
        if(equipo_ant==""):
            equipo_ant = equipo_tipo2
            colores2.add(fila["Planning Class"])
            planta2=fila["Planta"]
            tecnologia2=fila["Tecnología"]
        elif(equipo_tipo2==equipo_ant):
            colores2.add(fila["Planning Class"])
            planta2=fila["Planta"]
            tecnologia2=fila["Tecnología"]
        else:
            for i in range(diluidores_dict[equipo_ant]):
                equipo_obj = Equipo(
                    colores=colores2,
                    planta=planta2,
                    tecnologia=tecnologia2,
                    equipo_tipo=equipo_ant,
                    id=i
                )
                lista_equipos.append(equipo_obj)
            equipo_ant=equipo_tipo2
            planta2=fila["Planta"]
            tecnologia2=fila["Tecnología"]
            colores2 = set()
            colores2.add(fila["Planning Class"])
    for i in range(diluidores_dict[equipo_ant]):
        equipo_obj = Equipo(
            colores=colores2,
            planta=planta2,
            tecnologia=tecnologia2,
            equipo_tipo=equipo_ant,
            id=i
        )
        lista_equipos.append(equipo_obj)
    return lista_equipos

# toString de los equipos
def print_lista_equipos(lista_equipos):
    for equipo in lista_equipos:
        print(equipo)

# ordena de más urgente a menos
def ordenamiento_color(colores):
    colores_ordenados = sorted(colores, key=lambda color: color.fecha_required, reverse=False)
    return colores_ordenados

#-----------------------------------------
def asignar_lotes_backtracking_max(lotes, equipos):
    # Ordena los lotes por urgencia (fecha requerida más cercana primero)
    lotes = sorted(lotes, key=lambda lote: lote.fecha_required)
    mejor_plan = {}  # Para almacenar el plan con más lotes asignados
    backtrack_max(lotes, 0, equipos, {}, mejor_plan)
    return mejor_plan


def backtrack_max(lotes, index, equipos, plan_actual, mejor_plan):
    # Caso base: hemos procesado todos los lotes
    if index == len(lotes):
        # Actualiza el mejor plan si el actual tiene más lotes asignados
        if len(plan_actual) > len(mejor_plan):
            mejor_plan.clear()
            mejor_plan.update(plan_actual)
        return True

    lote_actual = lotes[index]
    fecha_fin = lote_actual.fecha_required
    duracion = lote_actual.standar_prod_time

    # Genera las fechas posibles considerando ±2 días alrededor de la required_date
    posibles_fechas_inicio = [
        fecha_fin - timedelta(days=duracion + offset)
        for offset in range(-2, 3)
    ]

    # Intentar asignar el lote a cada equipo compatible
    for equipo in equipos:
        #print_lista_colores(equipo.colores)
        if lote_actual.nombre not in equipo.colores:
            continue  # Saltar si el equipo no puede manejar este tipo de lote
        for fecha_inicio in posibles_fechas_inicio:
            fecha_fin_real = Equipo.calcular_fecha_fin(fecha_inicio, duracion)

            if equipo.esta_disponible(fecha_inicio, fecha_fin_real):
                # Asigna temporalmente el lote al equipo
                equipo.asignar_lote(fecha_inicio, fecha_fin_real, duracion)
                plan_actual[lote_actual] = (equipo, fecha_inicio, fecha_fin_real)

                # Llama recursivamente para el siguiente lote
                exito = backtrack_max(lotes, index + 1, equipos, plan_actual, mejor_plan)

                if(exito==False):
                    # Deshace la asignación si no tuvo éxito
                    equipo.liberar_lote(fecha_inicio, fecha_fin_real)
                    del plan_actual[lote_actual]
                else:
                    return True
    return False
#-----------------------------------------------------

def visualizar_gantt(plan, titulo="Plan de Producción"):
    fig, ax = plt.subplots(figsize=(12, 8))
    colores = plt.cm.tab20.colors  # Colores predefinidos para diferenciar lotes
    equipo_y_pos = {}  # Mapear equipos a posiciones en el eje Y

    # Calcular la posición en el eje Y para cada equipo
    equipos = sorted(set((equipo.equipo_tipo, equipo.id) for equipo, _, _ in plan.values()))
    for i, (equipo_tipo, equipo_id) in enumerate(equipos):
        equipo_y_pos[(equipo_tipo, equipo_id)] = i

    for i, (lote, (equipo, inicio, fin)) in enumerate(plan.items()):
        y_pos = equipo_y_pos[(equipo.equipo_tipo, equipo.id)]
        color = colores[i % len(colores)]  # Selecciona un color para el lote

        # Agregar barra para el lote
        ax.barh(y_pos, (fin - inicio).days, left=inicio, color=color, edgecolor="black", align="center")

        # Agregar etiqueta en la barra
        ax.text(inicio + timedelta(days=1), y_pos, f"{lote.item} ({equipo.equipo_tipo})", va='center', fontsize=8)

    # Configurar eje Y con nombres de los equipos
    ax.set_yticks(list(equipo_y_pos.values()))
    ax.set_yticklabels([f"{equipo_tipo} (ID: {equipo_id})" for equipo_tipo, equipo_id in equipo_y_pos.keys()])
    ax.set_xlabel("Fechas")
    ax.set_ylabel("Equipos")
    ax.set_title(titulo)

    # Configurar formato de fechas en el eje X
    ax.xaxis.set_major_locator(mdates.DayLocator(interval=2))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
    plt.xticks(rotation=45)

    plt.tight_layout()
    plt.show()

# main
def main_app():
    ruta_archivo = "./plan.xlsx"
    datos_pinturas = pd.read_excel(ruta_archivo, sheet_name="prod", usecols=["PPG_Planning_Class", "Item", "Plant","Required_Completion_Date", "Standard_Prod_Time", "Routing_Code"])
    datos_equipos = pd.read_excel(ruta_archivo, sheet_name="equipos", usecols=["Planning Class", "Planta", "Tecnología", "Equipo", "Capacidad (lote/semana)"])
    #print(datos_equipos)
    datos_diluidores = pd.read_excel(ruta_archivo, sheet_name="maquinas", usecols=["Etiquetas de fila", "Nº Equipos"])
    #print(datos_diluidores)
    lista_colores = crear_lista_colores(datos_pinturas)
    #print_lista_colores(lista_colores)
    lista_equipos = crear_lista_equipos(datos_equipos, datos_diluidores, lista_colores)
    #print_lista_equipos(lista_equipos)
    plan = asignar_lotes_backtracking_max(lista_colores, lista_equipos)
    if plan:
        # for lote, (equipo, inicio, fin) in plan.items():
        #     print(f"{lote.nombre} asignado a {equipo.equipo_tipo} id {equipo.id} desde {inicio} hasta {fin}")
        # visualizar_gantt(plan)
        return plan, lista_equipos
    return None
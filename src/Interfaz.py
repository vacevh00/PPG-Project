import tkinter as tk
from tkinter import TclError
from tkinter import messagebox
from datetime import date, timedelta
from tkinter import filedialog
from workalendar.europe import CastileAndLeon
import random
from tkinter import ttk
from datetime import datetime
import Backend_App
import pandas as pd
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.style = ttk.Style("superhero")
        self.root.title("MAIN")
        self.root.geometry("600x500")
        self.root.resizable(False, False)
        self.version = "v 1.3"

        self.ruta = "../docs/plan.xlsx"
        self.label = tk.Label(root, text="Sin archivo seleccionado")
        self.label.place(x=270, y=15)
        # Cambiar el color de fondo de la ventana principal
        #self.root.configure(bg="#c4c4c4")  # Fondo gris claro
        # Crear estilos personalizados para los botones
        #self.style = ttk.Style()
        #self.style.theme_use("clam")
        # Estilo para el botón "Iniciar aplicación"
        """self.style.configure(
            "Start.TButton",
            font=("Arial", 12, "bold"),
            foreground="white",
            background="#007bff",  # Verde
            padding=10
        )
        self.style.map("Start.TButton", background=[("active", "#0056b3")])  # Hover
        # Estilo para el botón "Añadir nuevo lote"
        self.style.configure(
            "Add.TButton",
            font=("Arial", 10, "bold"),
            foreground="white",
            background="#007bff",  # Azul
            padding=10
        )
        self.style.map("Add.TButton", background=[("active", "#0056b3")])
"""
        # Botón "Iniciar aplicación"
        self.button = ttk.Button(
            text="Iniciar aplicación",
            bootstyle=SUCCESS,  # Botón con estilo moderno
            command=self.on_button_click
        )

        # Botón "Añadir nuevo lote"
        self.button2 = ttk.Button(
            text="Añadir nuevo lote",
            bootstyle=INFO,  # Estilo moderno con color informativo
            command=self.on_button_click2
        )

        # Botón "Información"
        self.button3 = ttk.Button(
            text="i",
            bootstyle=INFO,  # Botón estilo advertencia
            command=self.on_button_click3
        )

        self.button4 = ttk.Button(
            text="Seleccionar archivo",
            bootstyle=INFO,
            command=self.on_button_click4
        )


        # Posicionar botones
        self.button4.place(x=140, y=10)
        self.button2.place(x=10, y=10)
        self.button3.place(x=560, y=10, width=30)
        self.button.place(relx=0.5, rely=0.5, anchor="center")

    def on_button_click(self):
        self.button.config(state="disabled")
        self.root.after(1200, self.change_window)

    def change_window(self):
        # Ocultar la ventana principal
        self.root.withdraw()
        new_window = tk.Toplevel()  # Usa tk.Toplevel para crear una nueva ventana
        new_window.title("Nueva Ventana")
        new_window.geometry("1200x900")
        #style = ttk.Style("superhero")  # Cambiar el estilo aquí
        new_window.configure(bg="#4f4f4f")  # Fondo opcional para la nueva ventana

        # Crear y mostrar el contenido de la nueva ventana
        app = App(new_window, self.root, self.button, self.ruta)
        try:
            new_window.state('zoomed')  # Maximizar la ventana si es posible
        except TclError:
            pass
        new_window.protocol("WM_DELETE_WINDOW", app.on_close)
        new_window.mainloop()

    def on_button_click2(self):
        self.button2.config(state="disabled")
        self.root.after(500, self.change_window2)

    def on_button_click3(self):
        # Usar el método `messagebox` de ttkbootstrap
        ttk.dialogs.Messagebox.show_info(
            title="Información",
            message=f"Grupo 2 de Dirección de Proyectos\n\n"
                    f"Trabajo final para PPG\n"
                    f"Versión {self.version}"
        )
    def on_button_click4(self):
        ruta_archivo = filedialog.askopenfilename(
            title="Seleccionar archivo",
            filetypes=[("Hojas de calculo", "*.xlsx")]
        )
        if ruta_archivo:
            self.ruta = ruta_archivo
            nombre = ruta_archivo.split("/")[-1]
            self.label.config(text=f"Seleccionado: {nombre}")

    def change_window2(self):
        # Crear una nueva ventana de configuración
        new_window = tk.Toplevel()  # Crea una nueva ventana de nivel superior
        new_window.title("Configuración")
        new_window.geometry("600x450")

        # Configurar fondo opcional
        #new_window.configure(bg="#4f4f4f")

        # Crear y mostrar el contenido de la nueva ventana
        config = Configuration(new_window, self.root, self.button2)
        new_window.protocol("WM_DELETE_WINDOW", config.on_close)
        new_window.mainloop()

class Configuration:
    def __init__(self, root, main_window, main_button):
        self.root = root
        self.root.title("Añadir Lote")
        self.main_window = main_window
        self.main_button = main_button
        self.root.geometry("500x600")
        self.root.resizable(False, False)

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        # Crear los widgets
        self.create_widgets()

    def create_widgets(self):
        # Etiqueta de título
        ttk.Label(self.root, text="Añadir Lote", font=("Arial", 16, "bold"), bootstyle=INFO).pack(pady=10)

        # Campo para ID del lote
        ttk.Label(self.root, text="ID de Lote:", bootstyle="info").pack(anchor="w", padx=20, pady=5)
        self.lote_id_entry = ttk.Entry(self.root, bootstyle="info")
        self.lote_id_entry.pack(fill="x", padx=20)

        # Campo para Routing Code
        ttk.Label(self.root, text="Routing Code:", bootstyle="info").pack(anchor="w", padx=20, pady=5)
        self.routing_code_entry = ttk.Entry(self.root, bootstyle="info")
        self.routing_code_entry.pack(fill="x", padx=20)

        # Selección de Planta (Lista Desplegable)
        ttk.Label(self.root, text="Planta:", bootstyle="info").pack(anchor="w", padx=20, pady=5)
        self.planta_options = ["VDC", "VDD", "VDW", "VDM"]
        self.planta_combo = ttk.Combobox(self.root, values=self.planta_options, state="readonly")
        self.planta_combo.pack(fill="x", padx=20)
        self.planta_combo.set("Seleccionar Planta")  # Placeholder inicial

        # Selección de Planning Class (Lista Desplegable)
        ttk.Label(self.root, text="Planning Class:", bootstyle="info").pack(anchor="w", padx=20, pady=5)
        self.planning_class_options = ["VD-APA", "VDCBE1", "VDCBM1", "VD-N4A", "VDWBBC"]
        self.planning_class_combo = ttk.Combobox(self.root, values=self.planning_class_options, state="readonly")
        self.planning_class_combo.pack(fill="x", padx=20)
        self.planning_class_combo.set("Seleccionar Clase")  # Placeholder inicial

        # Selección de Fecha de Inicio
        ttk.Label(self.root, text="Introduce la fecha (dd/mm/YYYY):", bootstyle="info").pack(anchor="w", padx=20, pady=5)
        self.start_date = ttk.Entry(self.root, bootstyle="info")
        self.start_date.pack(fill="x", padx=20)

        # Duración Estimada
        ttk.Label(self.root, text="Duración Estimada (días):", bootstyle="info").pack(anchor="w", padx=20, pady=5)
        self.duracion_entry = ttk.Entry(self.root, bootstyle="info")
        self.duracion_entry.pack(fill="x", padx=20)

        # Botón de Guardar
        self.save_button = ttk.Button(self.root, text="Guardar", bootstyle=SUCCESS, command=self.save_data)
        self.save_button.pack(pady=20)

    def save_data(self):
        # Obtener los datos del formulario
        lote_id = self.lote_id_entry.get()
        routing_code = self.routing_code_entry.get()
        planta = self.planta_combo.get()
        planning_class = self.planning_class_combo.get()
        start_date = self.start_date.get()
        duracion = self.duracion_entry.get()

        # Validar datos
        if not lote_id or not routing_code or planta == "Seleccionar Planta" or planning_class == "Seleccionar Clase" or not duracion.isdigit() or self.correctDate(start_date) == False:
            ttk.dialogs.Messagebox.show_error(
                title="Error",
                message="Por favor, complete todos los campos correctamente."
            )
            return

        # Simular guardar datos (puedes reemplazar esto con lógica real)
        ttk.dialogs.Messagebox.show_info(
            title="Guardado",
            message=f"Datos guardados:\n\n"
                    f"ID de Lote: {lote_id}\n"
                    f"Routing Code: {routing_code}\n"
                    f"Planta: {planta}\n"
                    f"Planning Class: {planning_class}\n"
                    f"Fecha de Inicio: {start_date}\n"
                    f"Duración Estimada: {duracion} días"
        )
        self.root.destroy()  # Cerrar la ventana después de guardar
        self.main_button.config(state="normal")

    def correctDate(self, startDate):
        try:
            parsed_date = datetime.strptime(startDate, "%d/%m/%Y").date()
            today = datetime.today().date()
            # Verifica si la fecha es hoy o posterior
            if parsed_date < today:
                return False
            else:
                return True
        except ValueError:
            messagebox.showerror("Error", "Formato incorrecto. Usa dd/mm/YYYY.")

    def on_close(self):
        # Confirmación para cerrar
        response = ttk.dialogs.Messagebox.show_question(
            title="Confirmar salida",
            message="¿Está seguro de que quiere salir?"
        )
        if response == "Yes":
            self.root.destroy()
            self.main_window.deiconify()
            self.main_button.config(state="normal")



class App:
    def __init__(self, root, main_window, main_button, ruta):
        self.root = root
        self.root.title("PPG-DEV")
        self.plan, self.lista_equipos = Backend_App.main_app(ruta)
        self.main_window = main_window
        self.main_button = main_button
        self.current_month = date.today().month + 1
        self.current_year = date.today().year
        # Frame principal
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill="both", expand=True)

        # Crear el espacio central
        self.center_frame = tk.Frame(self.main_frame)
        self.center_frame.pack(fill="both", expand=True)

        # Crear los botones o menús para las secciones
        self.buttons_frame = tk.Frame(self.main_frame)
        self.buttons_frame.pack(fill="x")
        
        # Botones para cambiar de vista 
        self.button1 = tk.Button(self.buttons_frame, text="        VDW        ", command=lambda: self.show_section_1(self.current_month, self.current_year))
        self.button1.pack(side="left", padx=10)
        self.button2 = tk.Button(self.buttons_frame, text="        VDC        ", command=lambda: self.show_section_2(self.current_month, self.current_year))
        self.button2.pack(side="left", padx=10)
        self.button3 = tk.Button(self.buttons_frame, text="        VDM        ", command=lambda: self.show_section_3(self.current_month, self.current_year))
        self.button3.pack(side="left", padx=10)
        self.button4 = tk.Button(self.buttons_frame, text="        VDD        ", command=lambda: self.show_section_4(self.current_month, self.current_year))
        self.button4.pack(side="left", padx=10)


        # MESES DESPLEGABLE
        self.months = [
            "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
            "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
        ]

        current_month_index = date.today().month - 1  # Los meses de datetime van de 1 a 12
        current_month_name = self.months[current_month_index]   # Nombre del mes actual

        self.month_combobox = ttk.Combobox(self.buttons_frame, values=self.months, state="readonly", width=12)
        self.month_combobox.set("Mes")
        self.month_combobox.pack(side="right", padx=20)
        self.month_combobox.bind("<<ComboboxSelected>>", self.on_month_selected)


        # Definir cada sección
        self.section_1 = tk.Frame(self.center_frame)
        self.section_2 = tk.Frame(self.center_frame)
        self.section_3 = tk.Frame(self.center_frame)
        self.section_4 = tk.Frame(self.center_frame)

        #self.on_month_selected()
        #self.show_section_2(self.current_month, self.current_year)
        

    # TO-DO Meses
    def on_month_selected(self, event=None, section=1):
        """
        Callback que se ejecuta al seleccionar un mes desde el combobox.
        Actualiza la tabla con los festivos y tareas correspondientes al mes seleccionado.
        """
        selected_month = self.month_combobox.get()
        mes = self.months.index(selected_month) + 1  # Convertir a índice de mes (1-12)
        anio = date.today().year
        self.current_month = mes
        self.current_year= anio
        # Redibujar la tabla para el mes seleccionado
        self.clear_center_frame()  # Limpiar la tabla actual
        if section==1:
            self.show_section_1(mes, anio) 
        elif section==2:
            self.show_section_2(mes, anio) 
        elif section==3:
            self.show_section_3(mes, anio) 
        else:
            self.show_section_4(mes, anio)

    def pintar_festivos_tabla(self, dia, num_rows):
        # Obtener el índice del día en la cuadrícula
        dia_indice = dia.day  # Usamos el atributo `.day` del objeto `date`

        # Definir el tamaño de las celdas (debe coincidir con el tamaño usado en show_section_1)
        cell_width = max(self.root.winfo_width() // 20, 80)
        cell_height = max(self.root.winfo_height() // 30, 30)

        # Pintar el fondo de las celdas de los días no lectivos
        for i in range(num_rows):
            x1 = cell_width * dia_indice
            y1 = cell_height * (i + 1)  # Las filas de datos empiezan en la segunda fila
            x2 = x1 + cell_width
            y2 = y1 + cell_height

            self.canvas.create_rectangle(x1, y1, x2, y2, fill="gray", outline="black")

    def dias_del_mes_siguiente(self, ):
        hoy = date.today()

        mes_siguiente = hoy.month + 1 if hoy.month < 12 else 1
        año_siguiente = hoy.year if hoy.month < 12 else hoy.year + 1
        

        primer_dia_mes_siguiente = date(año_siguiente, mes_siguiente, 1)
        

        if mes_siguiente < 12:
            primer_dia_mes_posterior = date(año_siguiente, mes_siguiente + 1, 1)
        else:
            primer_dia_mes_posterior = date(año_siguiente + 1, 1, 1)
        

        return (primer_dia_mes_posterior - primer_dia_mes_siguiente).days

    def pintar_festivos(self, num_rows, mes):
        """
        Calcula y pinta los días festivos del mes seleccionado en la tabla.
        """
        # Crear una instancia del calendario de Castilla y León
        cal = CastileAndLeon()

        # Obtener el rango de fechas del mes seleccionado
        hoy = date.today()
        anio = hoy.year
        primer_dia = date(anio, mes, 1)
        ultimo_dia = self.ultimo_dia_mes(mes)

        # Calcular los días festivos y fines de semana
        dias_no_lectivos = []
        dia_actual = primer_dia
        while dia_actual <= ultimo_dia:
            if cal.is_holiday(dia_actual) or dia_actual.weekday() in [5, 6]:  # Sábado o domingo
                dias_no_lectivos.append(dia_actual)
                # Añadir el lunes siguiente si es domingo festivo
                if dia_actual.weekday() == 6 and cal.is_holiday(dia_actual):
                    lunes_siguiente = dia_actual + timedelta(days=1)
                    if lunes_siguiente not in dias_no_lectivos:
                        dias_no_lectivos.append(lunes_siguiente)
            dia_actual += timedelta(days=1)

        # Pintar los días no lectivos en la tabla
        for dia in dias_no_lectivos:
            self.pintar_festivos_tabla(dia, num_rows)

    def ultimo_dia_mes(self, mes):
        """
        Devuelve el último día del mes especificado.
        """
        hoy = date.today()
        anio = hoy.year
        if mes == 12:
            return date(anio, 12, 31)
        else:
            return date(anio, mes + 1, 1) - timedelta(days=1)

    
    def generar_color_aleatorio(self):

        while True:
            r, g, b = random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
            
            avg_intensity = (r + g + b) // 3
            
            if 50 <= avg_intensity <= 150 and abs(r - g) < 30 and abs(g - b) < 30 and abs(b - r) < 30:
                continue
            
            return "#{:02x}{:02x}{:02x}".format(r, g, b)


    # segundo y cuarto parametro tienen que ser el mismo, nº de la fila
    # primero y tercero son los valores que coge para sacar los dias que dura
    # no se ya ni que es j ni i, osea, que seguir esquema de arriba xd
    def pintar_tareas(self, j, i, j2, i2, nombre_var):
        """
        Pinta una tarea en el canvas, ajustándose dinámicamente al tamaño de las celdas.

        Args:
            j: Día de inicio (columna inicial).
            i: Índice de la fila (equipo).
            j2: Día de fin (columna final).
            i2: Mismo valor que `i` (se puede eliminar en futuras versiones).
            nombre_var: Nombre de la tarea a mostrar.
        """
        # Obtener dimensiones de las celdas dinámicamente
        cell_width = max(self.root.winfo_width() // 20, 80)  # Ancho mínimo de 80 px
        cell_height = max(self.root.winfo_height() // 30, 30)  # Alto mínimo de 30 px

        # Coordenadas iniciales y finales de la tarea
        x1 = j * cell_width
        y1 = i * cell_height
        x2 = j2 * cell_width + cell_width  # Final de la tarea, suma una celda más
        y2 = i2 * cell_height + cell_height  # Final de la fila

        # Dibujar rectángulo de la tarea
        self.canvas.create_rectangle(x1, y1, x2, y2, fill=self.generar_color_aleatorio(), outline="black")

        # Dibujar texto centrado en el rectángulo
        self.canvas.create_text(
            (x1 + x2) / 2, (y1 + y2) / 2,  # Coordenadas centradas
            text=nombre_var,
            fill="black",
            font=("Arial", 10, "bold")
        )

    def segregar_eventos(self, equipos_total, planta, mes, anio):
        # print(f"mes={mes}, anio={anio}, planta={planta}")
        primer_dia_mes = pd.Timestamp(year=anio, month=mes, day=1)
        ultimo_dia_mes = primer_dia_mes + pd.offsets.MonthEnd(0)
        # i = 0
        for lote, (equipo, inicio, fin) in self.plan.items():
            
            # print(f"{lote.nombre} asignado a {equipo.equipo_tipo} id {equipo.id} desde {inicio} hasta {fin}")
            inicio = pd.Timestamp(inicio) if not isinstance(inicio, pd.Timestamp) else inicio
            fin = pd.Timestamp(fin) if not isinstance(fin, pd.Timestamp) else fin

            # print(type(inicio))

            if equipo.planta != planta:
                continue

            if fin < primer_dia_mes:
                continue

            if inicio > ultimo_dia_mes:
                continue

            # Recortar inicio y fin para pintar solo dentro del mes seleccionado
            if inicio < primer_dia_mes:
                inicio = primer_dia_mes

            if fin > ultimo_dia_mes:
                fin = ultimo_dia_mes

            # Encontrar el índice del equipo en la lista
            resultado = next(((i, e) for i, e in enumerate(equipos_total) if e.id == equipo.id), None)
            if resultado is None:
                continue

            indice, equipo_encontrado = resultado
            # i +=1
            # print(inicio)
            # print(fin)
            #print(f"{lote.nombre} asignado a {equipo.equipo_tipo} id {equipo.id} desde {inicio} hasta {fin}")
            # Pintar la tarea en el canvas
            self.pintar_tareas(inicio.day, indice + 1, fin.day, indice + 1, lote.item)
        # print(i)
               
    def primer_dia_mes_siguiente(self):
        hoy = datetime.now()

        # Calcular el primer día del mes siguiente
        if hoy.month == 12:  # Si es diciembre, avanzamos al siguiente año
            primer_dia = datetime(hoy.year + 1, 1, 1)
        else:
            primer_dia = datetime(hoy.year, hoy.month + 1, 1)

        return primer_dia

    def ultimo_dia_mes_siguiente(self):
        hoy = datetime.now()

        # Calcular el primer día del mes siguiente
        if hoy.month == 12:  # Si es diciembre, avanzamos al siguiente año
            primer_dia_mes_siguiente = datetime(hoy.year + 1, 1, 1)
        else:
            primer_dia_mes_siguiente = datetime(hoy.year, hoy.month + 1, 1)

        # Calcular el primer día del mes después del siguiente
        if primer_dia_mes_siguiente.month == 12:  # Si es diciembre, pasamos al siguiente año
            primer_dia_mes_despues = datetime(primer_dia_mes_siguiente.year + 1, 1, 1)
        else:
            primer_dia_mes_despues = datetime(primer_dia_mes_siguiente.year, primer_dia_mes_siguiente.month + 1, 1)

        # Restar un día para obtener el último día del mes siguiente
        ultimo_dia = primer_dia_mes_despues - timedelta(days=1)

        return ultimo_dia

    def es_del_proximo_mes(self,fecha):
        # Obtener la fecha actual
        hoy = datetime.now()

        # Calcular el próximo mes y el año correspondiente
        if hoy.month == 12:  # Si es diciembre, el próximo mes es enero del siguiente año
            proximo_mes = 1
            anio = hoy.year + 1
        else:
            proximo_mes = hoy.month + 1
            anio = hoy.year

        # Verificar si la fecha pertenece al próximo mes y año
        return fecha.month == proximo_mes and fecha.year == anio

    def show_section_1(self, mes=date.today().month, anio=date.today().year):
        self.clear_center_frame()

        if not hasattr(self, 'canvas'):
            # Crear un marco para el canvas y scrollbars
            self.canvas_frame = tk.Frame(self.section_1)
            self.canvas_frame.pack(fill="both", expand=True)

            # Crear el canvas para dibujar la tabla
            self.canvas = tk.Canvas(self.canvas_frame, bg="white")
            self.canvas.grid(row=0, column=0, sticky="nsew")

            # Crear scrollbars y vincularlas al canvas
            self.scroll_x = tk.Scrollbar(self.canvas_frame, orient="horizontal", command=self.canvas.xview)
            self.scroll_y = tk.Scrollbar(self.canvas_frame, orient="vertical", command=self.canvas.yview)
            self.scroll_x.grid(row=1, column=0, sticky="ew")
            self.scroll_y.grid(row=0, column=1, sticky="ns")

            # Configurar el canvas con las scrollbars
            self.canvas.configure(xscrollcommand=self.scroll_x.set, yscrollcommand=self.scroll_y.set)
            self.canvas_frame.grid_rowconfigure(0, weight=1)
            self.canvas_frame.grid_columnconfigure(0, weight=1)

        else:
            # Limpiar el canvas si ya existe
            self.canvas.delete("all")

        # Ajustar dinámicamente el tamaño de las celdas según el tamaño de la ventana
        cell_width = max(self.root.winfo_width() // 20, 80)  # Mínimo 80 px de ancho por celda
        cell_height = max(self.root.winfo_height() // 30, 30)  # Mínimo 30 px de alto por celda

        #print(f"mes={mes}, anio={anio}")

        # Filtrar equipos para esta sección
        lista_sec1 = [equipo for equipo in self.lista_equipos if equipo.planta == "VDW"]

        if mes == 12:  # Caso especial: diciembre
            primer_dia_mes = date(anio, mes, 1)
            ultimo_dia_mes = date(anio + 1, 1, 1) - timedelta(days=1)
        else:
            primer_dia_mes = date(anio, mes, 1)
            ultimo_dia_mes = date(anio, mes + 1, 1) - timedelta(days=1)
        num_dias_mes = (ultimo_dia_mes - primer_dia_mes).days + 1

        # Número de filas y columnas basado en los datos
        num_rows = len(lista_sec1) + 1  # Una fila extra para encabezados
        num_cols = num_dias_mes + 1  # Una columna extra para encabezados

        # Ajustar dinámicamente el área desplazable del canvas
        self.canvas.config(scrollregion=(0, 0, num_cols * cell_width, num_rows * cell_height))

        # Dibujar encabezados de columnas (días)
        for i in range(num_cols):
            x = i * cell_width
            self.canvas.create_line(x, 0, x, num_rows * cell_height, fill="gray", width=1)
            if i > 0:  # Encabezados de días (omitir primera columna)
                self.canvas.create_text(x + cell_width // 2, cell_height // 2, text=f"Día {i}", anchor="center", fill="white", font=("Arial", 10, "bold"))

        # Dibujar encabezados de filas (equipos)
        for j in range(num_rows):
            y = j * cell_height
            self.canvas.create_line(0, y, num_cols * cell_width, y, fill="gray", width=1)
            if j > 0:  # Encabezados de equipos (omitir primera fila)
                self.canvas.create_text(cell_width // 2, y + cell_height // 2, text=f"{lista_sec1[j-1].equipo_tipo}", anchor="center", fill="white", font=("Arial", 10, "bold"))

        # Dibujar eventos y festivos
        self.segregar_eventos(lista_sec1, "VDW", mes, anio)  # Eventos
        self.pintar_festivos(len(lista_sec1), self.current_month)  # Festivos

        # Mostrar la sección
        self.section_1.pack(fill="both", expand=True)



    # COPIAR SHOW_SECTION_1 EN LOS 3 DE ABAJO (aun no esta acabado)
    def show_section_2(self, mes=date.today().month, anio=date.today().year):
        self.clear_center_frame()

        if not hasattr(self, 'canvas'):
            # Crear un marco para el canvas y scrollbars
            self.canvas_frame = tk.Frame(self.section_1)
            self.canvas_frame.pack(fill="both", expand=True)

            # Crear el canvas para dibujar la tabla
            self.canvas = tk.Canvas(self.canvas_frame, bg="white")
            self.canvas.grid(row=0, column=0, sticky="nsew")

            # Crear scrollbars y vincularlas al canvas
            self.scroll_x = tk.Scrollbar(self.canvas_frame, orient="horizontal", command=self.canvas.xview)
            self.scroll_y = tk.Scrollbar(self.canvas_frame, orient="vertical", command=self.canvas.yview)
            self.scroll_x.grid(row=1, column=0, sticky="ew")
            self.scroll_y.grid(row=0, column=1, sticky="ns")

            # Configurar el canvas con las scrollbars
            self.canvas.configure(xscrollcommand=self.scroll_x.set, yscrollcommand=self.scroll_y.set)
            self.canvas_frame.grid_rowconfigure(0, weight=1)
            self.canvas_frame.grid_columnconfigure(0, weight=1)

        else:
            # Limpiar el canvas si ya existe
            self.canvas.delete("all")

        # Ajustar dinámicamente el tamaño de las celdas según el tamaño de la ventana
        cell_width = max(self.root.winfo_width() // 20, 80)  # Mínimo 80 px de ancho por celda
        cell_height = max(self.root.winfo_height() // 30, 30)  # Mínimo 30 px de alto por celda

        # Filtrar equipos para esta sección
        lista_sec1 = [equipo for equipo in self.lista_equipos if equipo.planta == "VDC"]

        if mes == 12:  # Caso especial: diciembre
            primer_dia_mes = date(anio, mes, 1)
            ultimo_dia_mes = date(anio + 1, 1, 1) - timedelta(days=1)
        else:
            primer_dia_mes = date(anio, mes, 1)
            ultimo_dia_mes = date(anio, mes + 1, 1) - timedelta(days=1)
        num_dias_mes = (ultimo_dia_mes - primer_dia_mes).days + 1

        # Número de filas y columnas basado en los datos
        num_rows = len(lista_sec1) + 1  # Una fila extra para encabezados
        num_cols = num_dias_mes + 1  # Una columna extra para encabezados

        # Ajustar dinámicamente el área desplazable del canvas
        self.canvas.config(scrollregion=(0, 0, num_cols * cell_width, num_rows * cell_height))

        # Dibujar encabezados de columnas (días)
        for i in range(num_cols):
            x = i * cell_width
            self.canvas.create_line(x, 0, x, num_rows * cell_height, fill="gray", width=1)
            if i > 0:  # Encabezados de días (omitir primera columna)
                self.canvas.create_text(x + cell_width // 2, cell_height // 2, text=f"Día {i}", anchor="center", fill="white", font=("Arial", 10, "bold"))

        # Dibujar encabezados de filas (equipos)
        for j in range(num_rows):
            y = j * cell_height
            self.canvas.create_line(0, y, num_cols * cell_width, y, fill="gray", width=1)
            if j > 0:  # Encabezados de equipos (omitir primera fila)
                self.canvas.create_text(cell_width // 2, y + cell_height // 2, text=f"{lista_sec1[j-1].equipo_tipo}", anchor="center", fill="white", font=("Arial", 10, "bold"))

        # Dibujar eventos y festivos
        self.segregar_eventos(lista_sec1, "VDC", mes, anio)  # Eventos
        self.pintar_festivos(len(lista_sec1), self.current_month)  # Festivos

        # Mostrar la sección
        self.section_1.pack(fill="both", expand=True)

    # COPIAR SHOW_SECTION_1 EN LOS 3 DE ABAJO (aun no esta acabado)
    def show_section_3(self, mes=date.today().month, anio=date.today().year):
        self.clear_center_frame()

        if not hasattr(self, 'canvas'):
            # Crear un marco para el canvas y scrollbars
            self.canvas_frame = tk.Frame(self.section_1)
            self.canvas_frame.pack(fill="both", expand=True)

            # Crear el canvas para dibujar la tabla
            self.canvas = tk.Canvas(self.canvas_frame, bg="white")
            self.canvas.grid(row=0, column=0, sticky="nsew")

            # Crear scrollbars y vincularlas al canvas
            self.scroll_x = tk.Scrollbar(self.canvas_frame, orient="horizontal", command=self.canvas.xview)
            self.scroll_y = tk.Scrollbar(self.canvas_frame, orient="vertical", command=self.canvas.yview)
            self.scroll_x.grid(row=1, column=0, sticky="ew")
            self.scroll_y.grid(row=0, column=1, sticky="ns")

            # Configurar el canvas con las scrollbars
            self.canvas.configure(xscrollcommand=self.scroll_x.set, yscrollcommand=self.scroll_y.set)
            self.canvas_frame.grid_rowconfigure(0, weight=1)
            self.canvas_frame.grid_columnconfigure(0, weight=1)

        else:
            # Limpiar el canvas si ya existe
            self.canvas.delete("all")

        # Ajustar dinámicamente el tamaño de las celdas según el tamaño de la ventana
        cell_width = max(self.root.winfo_width() // 20, 80)  # Mínimo 80 px de ancho por celda
        cell_height = max(self.root.winfo_height() // 30, 30)  # Mínimo 30 px de alto por celda

        # Filtrar equipos para esta sección
        lista_sec1 = [equipo for equipo in self.lista_equipos if equipo.planta == "VDM"]

        if mes == 12:  # Caso especial: diciembre
            primer_dia_mes = date(anio, mes, 1)
            ultimo_dia_mes = date(anio + 1, 1, 1) - timedelta(days=1)
        else:
            primer_dia_mes = date(anio, mes, 1)
            ultimo_dia_mes = date(anio, mes + 1, 1) - timedelta(days=1)
        num_dias_mes = (ultimo_dia_mes - primer_dia_mes).days + 1

        # Número de filas y columnas basado en los datos
        num_rows = len(lista_sec1) + 1  # Una fila extra para encabezados
        num_cols = num_dias_mes + 1  # Una columna extra para encabezados

        # Ajustar dinámicamente el área desplazable del canvas
        self.canvas.config(scrollregion=(0, 0, num_cols * cell_width, num_rows * cell_height))

        # Dibujar encabezados de columnas (días)
        for i in range(num_cols):
            x = i * cell_width
            self.canvas.create_line(x, 0, x, num_rows * cell_height, fill="gray", width=1)
            if i > 0:  # Encabezados de días (omitir primera columna)
                self.canvas.create_text(x + cell_width // 2, cell_height // 2, text=f"Día {i}", anchor="center", fill="white", font=("Arial", 10, "bold"))

        # Dibujar encabezados de filas (equipos)
        for j in range(num_rows):
            y = j * cell_height
            self.canvas.create_line(0, y, num_cols * cell_width, y, fill="gray", width=1)
            if j > 0:  # Encabezados de equipos (omitir primera fila)
                self.canvas.create_text(cell_width // 2, y + cell_height // 2, text=f"{lista_sec1[j-1].equipo_tipo}", anchor="center", fill="white", font=("Arial", 10, "bold"))

        # Dibujar eventos y festivos
        self.segregar_eventos(lista_sec1, "VDM", mes, anio)  # Eventos
        self.pintar_festivos(len(lista_sec1), self.current_month)  # Festivos

        # Mostrar la sección
        self.section_1.pack(fill="both", expand=True)


    def show_section_4(self, mes=date.today().month, anio=date.today().year):
        self.clear_center_frame()

        if not hasattr(self, 'canvas'):
            # Crear un marco para el canvas y scrollbars
            self.canvas_frame = tk.Frame(self.section_1)
            self.canvas_frame.pack(fill="both", expand=True)

            # Crear el canvas para dibujar la tabla
            self.canvas = tk.Canvas(self.canvas_frame, bg="white")
            self.canvas.grid(row=0, column=0, sticky="nsew")

            # Crear scrollbars y vincularlas al canvas
            self.scroll_x = tk.Scrollbar(self.canvas_frame, orient="horizontal", command=self.canvas.xview)
            self.scroll_y = tk.Scrollbar(self.canvas_frame, orient="vertical", command=self.canvas.yview)
            self.scroll_x.grid(row=1, column=0, sticky="ew")
            self.scroll_y.grid(row=0, column=1, sticky="ns")

            # Configurar el canvas con las scrollbars
            self.canvas.configure(xscrollcommand=self.scroll_x.set, yscrollcommand=self.scroll_y.set)
            self.canvas_frame.grid_rowconfigure(0, weight=1)
            self.canvas_frame.grid_columnconfigure(0, weight=1)

        else:
            # Limpiar el canvas si ya existe
            self.canvas.delete("all")

        # Ajustar dinámicamente el tamaño de las celdas según el tamaño de la ventana
        cell_width = max(self.root.winfo_width() // 20, 80)  # Mínimo 80 px de ancho por celda
        cell_height = max(self.root.winfo_height() // 30, 30)  # Mínimo 30 px de alto por celda

        # Filtrar equipos para esta sección
        lista_sec1 = [equipo for equipo in self.lista_equipos if equipo.planta == "VDD"]

        if mes == 12:  # Caso especial: diciembre
            primer_dia_mes = date(anio, mes, 1)
            ultimo_dia_mes = date(anio + 1, 1, 1) - timedelta(days=1)
        else:
            primer_dia_mes = date(anio, mes, 1)
            ultimo_dia_mes = date(anio, mes + 1, 1) - timedelta(days=1)
        num_dias_mes = (ultimo_dia_mes - primer_dia_mes).days + 1

        # Número de filas y columnas basado en los datos
        num_rows = len(lista_sec1) + 1  # Una fila extra para encabezados
        num_cols = num_dias_mes + 1  # Una columna extra para encabezados

        # Ajustar dinámicamente el área desplazable del canvas
        self.canvas.config(scrollregion=(0, 0, num_cols * cell_width, num_rows * cell_height))

        # Dibujar encabezados de columnas (días)
        for i in range(num_cols):
            x = i * cell_width
            self.canvas.create_line(x, 0, x, num_rows * cell_height, fill="gray", width=1)
            if i > 0:  # Encabezados de días (omitir primera columna)
                self.canvas.create_text(x + cell_width // 2, cell_height // 2, text=f"Día {i}", anchor="center", fill="white", font=("Arial", 10, "bold"))

        # Dibujar encabezados de filas (equipos)
        for j in range(num_rows):
            y = j * cell_height
            self.canvas.create_line(0, y, num_cols * cell_width, y, fill="gray", width=1)
            if j > 0:  # Encabezados de equipos (omitir primera fila)
                self.canvas.create_text(cell_width // 2, y + cell_height // 2, text=f"{lista_sec1[j-1].equipo_tipo}", anchor="center", fill="white", font=("Arial", 10, "bold"))

        # Dibujar eventos y festivos
        self.segregar_eventos(lista_sec1, "VDD", mes, anio)  # Eventos
        self.pintar_festivos(len(lista_sec1), self.current_month)  # Festivos

        # Mostrar la sección
        self.section_1.pack(fill="both", expand=True)



    def clear_center_frame(self):
        for widget in self.center_frame.winfo_children():
            widget.pack_forget()

    def on_close(self):
        # Mostrar popup para salir de la aplicacion
        response = messagebox.askyesno("Confirmar salida", "¿Estas seguro de que quieres salir?")
        if response:
            self.root.destroy()
            self.main_window.deiconify()
            self.main_button.config(state="normal")


if __name__ == "__main__":
    
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()
    
"""

    plan, lista_equipos = Backend_App.main_app()

    for i in plan:
         print(i)

    print("\n\n\n")

    for i in lista_equipos:
         print(i)


    for lote, (equipo, inicio, fin) in plan.items():
         print(f"{lote.nombre} asignado a {equipo.equipo_tipo} planta {equipo.planta} id {equipo.id} desde {inicio} hasta {fin}")
         
"""
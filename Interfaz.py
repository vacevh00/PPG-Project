import tkinter as tk
from tkinter import messagebox
from datetime import date, timedelta
from workalendar.europe import CastileAndLeon
import random
from tkinter import ttk
from datetime import datetime
import Backend_App


class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("MAIN")
        self.root.geometry("600x500")
        self.root.resizable(False, False)

        # Cambiar el color de fondo de la ventana principal
        self.root.configure(bg="#c4c4c4")  # Fondo gris claro

        # Crear estilos personalizados para los botones
        self.style = ttk.Style()
        self.style.theme_use("clam")

        # Estilo para el botón "Iniciar aplicación"
        self.style.configure(
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

        # Botón "Iniciar aplicación"
        self.button = ttk.Button(
            text="Iniciar aplicación",
            style="Start.TButton",
            command=self.on_button_click
        )

        # Botón "Añadir nuevo lote"
        self.button2 = ttk.Button(
            text="Añadir nuevo lote",
            style="Add.TButton",
            command=self.on_button_click2
        )

        self.button2.place(x=10, y=10)
        self.button.place(relx=0.5, rely=0.5, anchor="center")

    def on_button_click(self):
        self.button.config(state="disabled")
        self.root.after(2000, self.change_window)

    def change_window(self):
        # Ocultar la ventana principal
        self.root.withdraw()

        new_window = tk.Tk()
        app = App(new_window, self.root, self.button)
        new_window.state('zoomed')
        new_window.geometry("1200x900")
        new_window.protocol("WM_DELETE_WINDOW", app.on_close)
        new_window.mainloop()

    def on_button_click2(self):
        self.button2.config(state="disabled")
        self.root.after(1500, self.change_window2)
    
    def change_window2(self):
        # Ocultar la ventana principal
        new_window = tk.Tk()
        config = Configuration(new_window, self.root, self.button2)
        new_window.geometry("600x450")
        new_window.protocol("WM_DELETE_WINDOW", config.on_close)
        new_window.mainloop()
        
class Configuration:
    def __init__(self, root, main_window, main_button):
        self.root = root
        self.root.title("Añadir Lote")
        self.main_window = main_window
        self.main_button = main_button

        # Configurar la ventana con el mismo color de fondo que en MainWindow
        self.root.configure(bg="#c4c4c4")  # Fondo gris claro
        self.root.geometry("500x900")
        self.root.resizable(False, False)

        # Crear los estilos para los botones de la misma manera que en MainWindow
        self.style = ttk.Style()
        self.style.theme_use("clam")

        # Estilo para el botón "Guardar" (similar al botón "Iniciar aplicación")
        self.style.configure(
            "Save.TButton",
            font=("Arial", 12, "bold"),
            foreground="white",
            background="#007bff",  # Azul
            padding=10
        )
        self.style.map("Save.TButton", background=[("active", "#0056b3")])  # Hover

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        # Crear los widgets
        self.create_widgets()

    def create_widgets(self):
        # Etiqueta de título
        tk.Label(self.root, text="Añadir Lote", font=("Arial", 16), bg="#c4c4c4").pack(pady=10)

        # Campo para ID del lote
        tk.Label(self.root, text="ID de Lote:", bg="#c4c4c4").pack(anchor="w", padx=20, pady=5)
        self.lote_id_entry = tk.Entry(self.root)
        self.lote_id_entry.pack(fill="x", padx=20)

        # Campo para Routing Code
        tk.Label(self.root, text="Routing Code:", bg="#c4c4c4").pack(anchor="w", padx=20, pady=5)
        self.routing_code_entry = tk.Entry(self.root)
        self.routing_code_entry.pack(fill="x", padx=20)

        # Selección de Planta (Lista Desplegable)
        tk.Label(self.root, text="Planta:", bg="#c4c4c4").pack(anchor="w", padx=20, pady=5)
        self.planta_options = ["VDC", "VDD", "VDW", "VDM"]
        self.planta_combo = ttk.Combobox(self.root, values=self.planta_options, state="readonly")
        self.planta_combo.pack(fill="x", padx=20)
        self.planta_combo.set("Seleccionar Planta")  # Placeholder inicial

        # Selección de Planning Class (Lista Desplegable)
        tk.Label(self.root, text="Planning Class:", bg="#c4c4c4").pack(anchor="w", padx=20, pady=5)
        self.planning_class_options = ["VD-APA", "VDCBE1", "VDCBM1", "VD-N4A", "VDWBBC"]
        self.planning_class_combo = ttk.Combobox(self.root, values=self.planning_class_options, state="readonly")
        self.planning_class_combo.pack(fill="x", padx=20)
        self.planning_class_combo.set("Seleccionar Clase")  # Placeholder inicial

        # Selección de Fecha de Inicio
        tk.Label(self.root, text="Introduce la fecha (dd/mm/YYYY):", bg="#c4c4c4").pack(anchor="w", padx=20, pady=5)
        self.start_date = tk.Entry(self.root)
        self.start_date.pack(fill="x", padx=20)

        # Duración Estimada
        tk.Label(self.root, text="Duración Estimada (días):", bg="#c4c4c4").pack(anchor="w", padx=20, pady=5)
        self.duracion_entry = tk.Entry(self.root)
        self.duracion_entry.pack(fill="x", padx=20)

        # Botón de Guardar con el estilo configurado
        self.save_button = ttk.Button(self.root, text="Guardar", style="Save.TButton", command=self.save_data)
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
            messagebox.showerror("Error", "Por favor, complete todos los campos correctamente.")
            return
        # Simular guardar datos (puedes reemplazar esto con lógica real)
        messagebox.showinfo("Guardado", f"Datos guardados:\n\n"
                                        f"ID de Lote: {lote_id}\n"
                                        f"Routing Code: {routing_code}\n"
                                        f"Planta: {planta}\n"
                                        f"Planning Class: {planning_class}\n"
                                        f"Fecha de Inicio: {start_date}\n"
                                        f"Duración Estimada: {duracion} días")
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
        response = messagebox.askyesno("Confirmar salida", "¿Está seguro de que quiere salir?")
        if response:
            self.root.destroy()
            self.main_window.deiconify()
            self.main_button.config(state="normal")


class App:
    def __init__(self, root, main_window, main_button):
        self.root = root
        self.root.title("PPG-DEV")
        self.plan, self.lista_equipos = Backend_App.main_app()
        self.main_window = main_window
        self.main_button = main_button
        
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
        self.button1 = tk.Button(self.buttons_frame, text="        VDW        ", command=self.show_section_1)
        self.button1.pack(side="left", padx=10)
        self.button2 = tk.Button(self.buttons_frame, text="        VDC        ", command=self.show_section_2)
        self.button2.pack(side="left", padx=10)
        self.button3 = tk.Button(self.buttons_frame, text="        VDM        ", command=self.show_section_3)
        self.button3.pack(side="left", padx=10)
        self.button4 = tk.Button(self.buttons_frame, text="        VDD        ", command=self.show_section_4)
        self.button4.pack(side="left", padx=10)


        # MESES DESPLEGABLE
        self.months = [
            "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
            "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
        ]

        self.month_combobox = ttk.Combobox(self.buttons_frame, values=self.months, state="readonly", width=12)
        self.month_combobox.set("Mes")  # Texto inicial del desplegable
        self.month_combobox.pack(side="right", padx=20)
        self.month_combobox.bind("<<ComboboxSelected>>", self.on_month_selected)


        # Definir cada sección
        self.section_1 = tk.Frame(self.center_frame)
        self.section_2 = tk.Frame(self.center_frame)
        self.section_3 = tk.Frame(self.center_frame)
        self.section_4 = tk.Frame(self.center_frame)

        self.show_section_1()

    # TO-DO Meses
    def on_month_selected(self,event):
        selected_month = self.month_combobox.get()
        # CAMBIAR A MES SELECCIONADO

    # CON ESTA FUNCION VAMOS A PINTAR, SE VA A LLAMAR DESPUES X VECES
    def pintar_festivos_tabla(self, dia, num_rows):
        # Ejemplo de una tarea como gantt
        aux = dia.day
        #self.canvas.create_rectangle(100, 80, 500, 120, fill="blue", outline="black")
        #self.canvas.create_rectangle(100*aux, 80, 100+100*aux, 120, fill="gray", outline="black")
        #self.canvas.create_text(200, 60, text="Tarea_1", fill="white", font=("Arial", 10))

        for i in range(num_rows):
            self.canvas.create_rectangle(100*aux, 40*i, 100+100*aux, 80*i, fill="gray", outline="black")

    def dias_del_mes_siguiente(self):
        hoy = date.today()

        mes_siguiente = hoy.month + 1 if hoy.month < 12 else 1
        año_siguiente = hoy.year if hoy.month < 12 else hoy.year + 1
        

        primer_dia_mes_siguiente = date(año_siguiente, mes_siguiente, 1)
        

        if mes_siguiente < 12:
            primer_dia_mes_posterior = date(año_siguiente, mes_siguiente + 1, 1)
        else:
            primer_dia_mes_posterior = date(año_siguiente + 1, 1, 1)
        

        return (primer_dia_mes_posterior - primer_dia_mes_siguiente).days

    def pintar_festivos(self, num_rows):
        # Crear una instancia del calendario de Castilla y Leon
        cal = CastileAndLeon()

        # Obtener el mes y el año actual
        hoy = date.today()
        mes_siguiente = hoy.month % 12 + 1
        anio_siguiente = hoy.year + (1 if mes_siguiente == 1 else 0)

        # Calcular el rango de fechas para el mes siguiente
        primer_dia = date(anio_siguiente, mes_siguiente, 1)
        if mes_siguiente == 12:  # Caso especial: diciembre
            primer_dia_siguiente = date(anio_siguiente + 1, 1, 1)
        else:
            primer_dia_siguiente = date(anio_siguiente, mes_siguiente + 1, 1)

        # Recorrer todos los días del mes siguiente
        dia_actual = primer_dia
        dias_no_lectivos = []

        while dia_actual < primer_dia_siguiente:
            if cal.is_holiday(dia_actual) or dia_actual.weekday() in [5, 6]:  # Sábado (5) o domingo (6)
                dias_no_lectivos.append(dia_actual)
                # Si el día es domingo y festivo, añadir el lunes como festivo
                if dia_actual.weekday() == 6 and cal.is_holiday(dia_actual):  # Domingo festivo
                    lunes_siguiente = dia_actual + timedelta(days=1)
                    if lunes_siguiente not in dias_no_lectivos:  # Evitar duplicados
                        dias_no_lectivos.append(lunes_siguiente)
            dia_actual += timedelta(days=1)

        # pinta dias no lectivos
        for dia in dias_no_lectivos:
            self.pintar_festivos_tabla(dia, num_rows)

    
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
        # MODIFICACIONES FUTURAS QUITAR "i2", no sirve de nada, con i vale
        '''
        Valores:
            - donde empieza en X (pintar 1 dia mas +100)
            - donde empieza en Y (pintar 1 diluidor mas abajo +40)
            - hasta donde llega X (pintar 1 dia mas +100)
            - hasta donde llega Y (pintar 1 diluidor mas abajo +40)
        '''
        self.canvas.create_rectangle(100*j, 40*i, 100+100*j2, 40+40*i2, fill=self.generar_color_aleatorio(), outline="black")
        self.canvas.create_text(((100*j) + (100+100*j2))/2, 20+40*i, text=nombre_var, fill="black", font=("Arial", 10, "bold"))

    def segregar_eventos(self, equipos_total, planta):

        for lote, (equipo, inicio, fin) in self.plan.items():
            # print(f"{lote.nombre} asignado a {equipo.equipo_tipo} id {equipo.id} desde {inicio} hasta {fin}")

            if equipo.planta != planta:
                continue

            if fin < self.primer_dia_mes_siguiente():
                continue

            if not self.es_del_proximo_mes(fin):
                fin = None

            if not self.es_del_proximo_mes(inicio):
                inicio = None

            if fin is None and inicio is None:
                continue
            else:
                if fin == None:
                    fin = self.ultimo_dia_mes_siguiente()
                elif inicio == None:
                    inicio = self.primer_dia_mes_siguiente()

            resultado = next(((i, e) for i, e in enumerate(equipos_total) if e.id == equipo.id), None)

            # Siempre lo encuentra, si no lo encuentra pues a bailar
            indice, equipo_encontrado = resultado

            self.pintar_tareas(inicio.day,indice+1,fin.day,indice+1,lote.nombre)

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

    def show_section_1(self):
        self.clear_center_frame()

        if not hasattr(self, 'canvas'):
            self.canvas_frame = tk.Frame(self.section_1)
            self.canvas_frame.pack(fill="both", expand=True)

            self.canvas = tk.Canvas(self.canvas_frame, bg="white", scrollregion=(0, 0, 2000, 1000))
            self.scroll_x = tk.Scrollbar(self.canvas_frame, orient="horizontal", command=self.canvas.xview)
            self.scroll_y = tk.Scrollbar(self.canvas_frame, orient="vertical", command=self.canvas.yview)
            
            self.canvas.configure(xscrollcommand=self.scroll_x.set, yscrollcommand=self.scroll_y.set)
            self.canvas.grid(row=0, column=0, sticky="nsew")
            self.scroll_x.grid(row=1, column=0, sticky="ew")
            self.scroll_y.grid(row=0, column=1, sticky="ns")
            
            self.canvas_frame.grid_rowconfigure(0, weight=1)
            self.canvas_frame.grid_columnconfigure(0, weight=1)
        
        else:
            # Limpiar canvas si ya existe
            self.canvas.delete("all")

        # Dibujar tipo Excel
        cell_width = 100
        cell_height = 40

        lista_sec1 = [equipo for equipo in self.lista_equipos if equipo.planta == "VDW"]

        num_rows = len(lista_sec1) # preguntar si me pueden devolver el array con todos los de esta seccion
        num_cols = self.dias_del_mes_siguiente()+1 # esto se cambia en base al numero de dias del siguiente mes
        

        # Ajustar dinámicamente el scrollregion según el contenido
        self.canvas.config(scrollregion=(0, 0, num_cols * cell_width, num_rows * cell_height))

        # Dibujar columnas y encabezados de días
        for i in range(num_cols):
            x = i * cell_width
            self.canvas.create_line(x, 0, x, num_rows * cell_height, fill="gray")
            if i > 0:  # Encabezados para fechas (omitir primera columna)
                self.canvas.create_text(x + cell_width // 2, 15, text=f"Dia {i}", anchor="center")

        # Dibujar filas y encabezados de tareas
        for j in range(num_rows):
            y = j * cell_height
            self.canvas.create_line(0, y, num_cols * cell_width, y, fill="gray")
            if j > 0:  # Encabezados para tareas (omitir primera fila)
                self.canvas.create_text(50, y + cell_height // 2, text=f"{lista_sec1[j].equipo_tipo}", anchor="center")

        # Primero escribo los eventos y luego los sobreescribo con los festivos para no tener que hacer magia
        self.segregar_eventos(lista_sec1, "VDW")
        # bucle para pintar el array de tareas
        self.pintar_festivos(num_rows)


        # EJEMPLOS DE PRUEBA
        # segundo y cuarto parametro tienen que ser el mismo, nº de la fila
        # primero y tercero son los valores que coge para sacar los dias que dura
        # self.pintar_tareas(2,1,3,1, "Nombre3")
        # self.pintar_tareas(4,1,5,1, "Nombre2")
        # self.pintar_tareas(2,2,4,2, "Nombre1") # j i j2 i2
        # self.pintar_tareas(2,3,5,3, "Nombre4")

        self.section_1.pack(fill="both", expand=True)






    # COPIAR SHOW_SECTION_1 EN LOS 3 DE ABAJO (aun no esta acabado)
    def show_section_2(self):
        # self.clear_center_frame()
        # self.section_2.pack(expand=True)

        self.clear_center_frame()

        if not hasattr(self, 'canvas'):
            self.canvas_frame = tk.Frame(self.section_2)
            self.canvas_frame.pack(fill="both", expand=True)

            self.canvas = tk.Canvas(self.canvas_frame, bg="white", scrollregion=(0, 0, 2000, 1000))
            self.scroll_x = tk.Scrollbar(self.canvas_frame, orient="horizontal", command=self.canvas.xview)
            self.scroll_y = tk.Scrollbar(self.canvas_frame, orient="vertical", command=self.canvas.yview)
            
            self.canvas.configure(xscrollcommand=self.scroll_x.set, yscrollcommand=self.scroll_y.set)
            self.canvas.grid(row=0, column=0, sticky="nsew")
            self.scroll_x.grid(row=1, column=0, sticky="ew")
            self.scroll_y.grid(row=0, column=1, sticky="ns")
            
            self.canvas_frame.grid_rowconfigure(0, weight=1)
            self.canvas_frame.grid_columnconfigure(0, weight=1)
        
        else:
            # Limpiar canvas si ya existe
            self.canvas.delete("all")

        # Dibujar tipo Excel
        cell_width = 100
        cell_height = 40

        lista_sec1 = [equipo for equipo in self.lista_equipos if equipo.planta == "VDC"]

        num_rows = len(lista_sec1) # preguntar si me pueden devolver el array con todos los de esta seccion
        num_cols = self.dias_del_mes_siguiente()+1 # esto se cambia en base al numero de dias del siguiente mes
        

        # Ajustar dinámicamente el scrollregion según el contenido
        self.canvas.config(scrollregion=(0, 0, num_cols * cell_width, num_rows * cell_height))

        # Dibujar columnas y encabezados de días
        for i in range(num_cols):
            x = i * cell_width
            self.canvas.create_line(x, 0, x, num_rows * cell_height, fill="gray")
            if i > 0:  # Encabezados para fechas (omitir primera columna)
                self.canvas.create_text(x + cell_width // 2, 15, text=f"Dia {i}", anchor="center")

        # Dibujar filas y encabezados de tareas
        for j in range(num_rows):
            y = j * cell_height
            self.canvas.create_line(0, y, num_cols * cell_width, y, fill="gray")
            if j > 0:  # Encabezados para tareas (omitir primera fila)
                self.canvas.create_text(50, y + cell_height // 2, text=f"{lista_sec1[j].equipo_tipo}", anchor="center")

        # Primero escribo los eventos y luego los sobreescribo con los festivos para no tener que hacer magia
        self.segregar_eventos(lista_sec1, "VDC")
        # bucle para pintar el array de tareas
        self.pintar_festivos(num_rows)


        self.section_1.pack(fill="both", expand=True)

    def show_section_3(self):
        # self.clear_center_frame()
        # self.section_3.pack(expand=True)

        self.clear_center_frame()

        if not hasattr(self, 'canvas'):
            self.canvas_frame = tk.Frame(self.section_3)
            self.canvas_frame.pack(fill="both", expand=True)

            self.canvas = tk.Canvas(self.canvas_frame, bg="white", scrollregion=(0, 0, 2000, 1000))
            self.scroll_x = tk.Scrollbar(self.canvas_frame, orient="horizontal", command=self.canvas.xview)
            self.scroll_y = tk.Scrollbar(self.canvas_frame, orient="vertical", command=self.canvas.yview)
            
            self.canvas.configure(xscrollcommand=self.scroll_x.set, yscrollcommand=self.scroll_y.set)
            self.canvas.grid(row=0, column=0, sticky="nsew")
            self.scroll_x.grid(row=1, column=0, sticky="ew")
            self.scroll_y.grid(row=0, column=1, sticky="ns")
            
            self.canvas_frame.grid_rowconfigure(0, weight=1)
            self.canvas_frame.grid_columnconfigure(0, weight=1)
        
        else:
            # Limpiar canvas si ya existe
            self.canvas.delete("all")

        # Dibujar tipo Excel
        cell_width = 100
        cell_height = 40

        lista_sec1 = [equipo for equipo in self.lista_equipos if equipo.planta == "VDM"]

        num_rows = len(lista_sec1) # preguntar si me pueden devolver el array con todos los de esta seccion
        num_cols = self.dias_del_mes_siguiente()+1 # esto se cambia en base al numero de dias del siguiente mes
        

        # Ajustar dinámicamente el scrollregion según el contenido
        self.canvas.config(scrollregion=(0, 0, num_cols * cell_width, num_rows * cell_height))

        # Dibujar columnas y encabezados de días
        for i in range(num_cols):
            x = i * cell_width
            self.canvas.create_line(x, 0, x, num_rows * cell_height, fill="gray")
            if i > 0:  # Encabezados para fechas (omitir primera columna)
                self.canvas.create_text(x + cell_width // 2, 15, text=f"Dia {i}", anchor="center")

        # Dibujar filas y encabezados de tareas
        for j in range(num_rows):
            y = j * cell_height
            self.canvas.create_line(0, y, num_cols * cell_width, y, fill="gray")
            if j > 0:  # Encabezados para tareas (omitir primera fila)
                self.canvas.create_text(50, y + cell_height // 2, text=f"{lista_sec1[j].equipo_tipo}", anchor="center")

        # Primero escribo los eventos y luego los sobreescribo con los festivos para no tener que hacer magia
        self.segregar_eventos(lista_sec1, "VDM")
        # bucle para pintar el array de tareas
        self.pintar_festivos(num_rows)

        self.section_1.pack(fill="both", expand=True)



    def show_section_4(self):
        # self.clear_center_frame()
        # self.section_4.pack(expand=True)
        self.clear_center_frame()

        if not hasattr(self, 'canvas'):
            self.canvas_frame = tk.Frame(self.section_4)
            self.canvas_frame.pack(fill="both", expand=True)

            self.canvas = tk.Canvas(self.canvas_frame, bg="white", scrollregion=(0, 0, 2000, 1000))
            self.scroll_x = tk.Scrollbar(self.canvas_frame, orient="horizontal", command=self.canvas.xview)
            self.scroll_y = tk.Scrollbar(self.canvas_frame, orient="vertical", command=self.canvas.yview)
            
            self.canvas.configure(xscrollcommand=self.scroll_x.set, yscrollcommand=self.scroll_y.set)
            self.canvas.grid(row=0, column=0, sticky="nsew")
            self.scroll_x.grid(row=1, column=0, sticky="ew")
            self.scroll_y.grid(row=0, column=1, sticky="ns")
            
            self.canvas_frame.grid_rowconfigure(0, weight=1)
            self.canvas_frame.grid_columnconfigure(0, weight=1)
        
        else:
            # Limpiar canvas si ya existe
            self.canvas.delete("all")

        # Dibujar tipo Excel
        cell_width = 100
        cell_height = 40

        lista_sec1 = [equipo for equipo in self.lista_equipos if equipo.planta == "VDD"]

        num_rows = len(lista_sec1) # preguntar si me pueden devolver el array con todos los de esta seccion
        num_cols = self.dias_del_mes_siguiente()+1 # esto se cambia en base al numero de dias del siguiente mes
        

        # Ajustar dinámicamente el scrollregion según el contenido
        self.canvas.config(scrollregion=(0, 0, num_cols * cell_width, num_rows * cell_height))

        # Dibujar columnas y encabezados de días
        for i in range(num_cols):
            x = i * cell_width
            self.canvas.create_line(x, 0, x, num_rows * cell_height, fill="gray")
            if i > 0:  # Encabezados para fechas (omitir primera columna)
                self.canvas.create_text(x + cell_width // 2, 15, text=f"Dia {i}", anchor="center")

        # Dibujar filas y encabezados de tareas
        for j in range(num_rows):
            y = j * cell_height
            self.canvas.create_line(0, y, num_cols * cell_width, y, fill="gray")
            if j > 0:  # Encabezados para tareas (omitir primera fila)
                self.canvas.create_text(50, y + cell_height // 2, text=f"{lista_sec1[j].equipo_tipo}", anchor="center")

        # Primero escribo los eventos y luego los sobreescribo con los festivos para no tener que hacer magia
        self.segregar_eventos(lista_sec1, "VDD")
        # bucle para pintar el array de tareas
        self.pintar_festivos(num_rows)

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
    

    plan, lista_equipos = Backend_App.main_app()

"""     for i in plan:
         print(i)

    print("\n\n\n")

    for i in lista_equipos:
         print(i)


    for lote, (equipo, inicio, fin) in plan.items():
         print(f"{lote.nombre} asignado a {equipo.equipo_tipo} planta {equipo.planta} id {equipo.id} desde {inicio} hasta {fin}") """


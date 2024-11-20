import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from datetime import date, timedelta
from workalendar.europe import Spain
import random
from datetime import datetime


class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("MAIN")
        self.root.geometry("600x500")
        self.root.resizable(False, False)

        self.button = tk.Button(self.root, text="Iniciar aplicación", command=self.on_button_click)
        self.button2 = tk.Button(self.root, text="Añadir nuevo lote", command=self.on_button_click2)
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
        new_window.geometry("1200x900")
        new_window.protocol("WM_DELETE_WINDOW", app.on_close)
        new_window.mainloop()
    
    def on_button_click2(self):
        self.button2.config(state="disabled")
        self.root.after(1500, self.change_window2)
    
    def change_window2(self):
        # Ocultar la ventana principal
        self.root.withdraw()

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

        # Configurar la ventana
        self.root.geometry("500x900")
        self.root.resizable(False, False)
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        # Crear elementos de la interfaz
        self.create_widgets()

    def create_widgets(self):
        # Etiqueta de título
        tk.Label(self.root, text="Añadir Lote", font=("Arial", 16)).pack(pady=10)

        # Campo para ID del lote
        tk.Label(self.root, text="ID de Lote:").pack(anchor="w", padx=20, pady=5)
        self.lote_id_entry = tk.Entry(self.root)
        self.lote_id_entry.pack(fill="x", padx=20)

        # Campo para Routing Code
        tk.Label(self.root, text="Routing Code:").pack(anchor="w", padx=20, pady=5)
        self.routing_code_entry = tk.Entry(self.root)
        self.routing_code_entry.pack(fill="x", padx=20)

        # Selección de Planta (Lista Desplegable)
        tk.Label(self.root, text="Planta:").pack(anchor="w", padx=20, pady=5)
        self.planta_options = ["VDC", "VDD", "VDW"]
        self.planta_combo = ttk.Combobox(self.root, values=self.planta_options, state="readonly")
        self.planta_combo.pack(fill="x", padx=20)
        self.planta_combo.set("Seleccionar Planta")  # Placeholder inicial

        # Selección de Planning Class (Lista Desplegable)
        tk.Label(self.root, text="Planning Class:").pack(anchor="w", padx=20, pady=5)
        self.planning_class_options = ["VD-APA", "VDCBE1", "VDCBM1", "VD-N4A", "VDWBBC"]
        self.planning_class_combo = ttk.Combobox(self.root, values=self.planning_class_options, state="readonly")
        self.planning_class_combo.pack(fill="x", padx=20)
        self.planning_class_combo.set("Seleccionar Clase")  # Placeholder inicial

        # Selección de Fecha de Inicio
        tk.Label(self.root, text="Introduce la fecha (dd/mm/YYYY):").pack(anchor="w", padx=20, pady=5)
        self.start_date = tk.Entry(self.root)
        self.start_date.pack(fill="x", padx=20)

        # Duración Estimada
        tk.Label(self.root, text="Duración Estimada (días):").pack(anchor="w", padx=20, pady=5)
        self.duracion_entry = tk.Entry(self.root)
        self.duracion_entry.pack(fill="x", padx=20)

        # Botón de Guardar
        self.save_button = tk.Button(self.root, text="Guardar", command=self.save_data)
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
        # PONER NOMBRE EQUIPOS EN VEZ DE "APARTADO X"
        self.button1 = tk.Button(self.buttons_frame, text="Apartado 1", command=self.show_section_1)
        self.button1.pack(side="left", padx=10)
        self.button2 = tk.Button(self.buttons_frame, text="Apartado 2", command=self.show_section_2)
        self.button2.pack(side="left", padx=10)
        self.button3 = tk.Button(self.buttons_frame, text="Apartado 3", command=self.show_section_3)
        self.button3.pack(side="left", padx=10)
        self.button4 = tk.Button(self.buttons_frame, text="Apartado 4", command=self.show_section_4)
        self.button4.pack(side="left", padx=10)
        
        # Definir cada sección
        self.section_1 = tk.Frame(self.center_frame)
        self.section_2 = tk.Label(self.center_frame, text="En progreso...", font=("Arial", 20))
        self.section_3 = tk.Label(self.center_frame, text="En progreso...", font=("Arial", 20))
        self.section_4 = tk.Label(self.center_frame, text="En progreso...", font=("Arial", 20))

        self.show_section_1()

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
        # Crear una instancia del calendario de España
        cal = Spain()

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
    def pintar_tareas(self, j, i, j2, i2):
        # MODIFICACIONES FUTURAS QUITAR "i2", no sirve de nada, con i vale
        '''
        Valores:
            - donde empieza en X (pintar 1 dia mas +100)
            - donde empieza en Y (pintar 1 diluidor mas abajo +40)
            - hasta donde llega X (pintar 1 dia mas +100)
            - hasta donde llega Y (pintar 1 diluidor mas abajo +40)
        '''
        self.canvas.create_rectangle(100*j, 40*i, 100+100*j2, 40+40*i2, fill=self.generar_color_aleatorio(), outline="black")

    def show_section_1(self):
        self.clear_center_frame()

        if not hasattr(self, 'canvas'):
            self.canvas_frame = tk.Frame(self.section_1)
            self.canvas_frame.pack(fill="both", expand=True)

            # Canvas y Scrollbars
            self.canvas = tk.Canvas(self.canvas_frame, bg="white", scrollregion=(0, 0, 2000, 1000))
            self.scroll_x = tk.Scrollbar(self.canvas_frame, orient="horizontal", command=self.canvas.xview)
            self.scroll_y = tk.Scrollbar(self.canvas_frame, orient="vertical", command=self.canvas.yview)
            
            self.canvas.configure(xscrollcommand=self.scroll_x.set, yscrollcommand=self.scroll_y.set)
            self.canvas.grid(row=0, column=0, sticky="nsew")
            self.scroll_x.grid(row=1, column=0, sticky="ew")
            self.scroll_y.grid(row=0, column=1, sticky="ns")
            
            self.canvas_frame.grid_rowconfigure(0, weight=1)
            self.canvas_frame.grid_columnconfigure(0, weight=1)

            # Dibujar tipo Excel
            cell_width = 100
            cell_height = 40
            num_rows = 30 # preguntar si me pueden devolver el array con todos los de esta seccion
            num_cols = self.dias_del_mes_siguiente()+1 # esto se cambia en base al numero de dias del siguiente mes
            # print("DIAS: " + str(num_cols))

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
                    self.canvas.create_text(50, y + cell_height // 2, text=f"Tarea {j}", anchor="center")


            # bucle para pintar el array de tareas
            self.pintar_festivos(num_rows)


            # EJEMPLOS DE PRUEBA
            # segundo y cuarto parametro tienen que ser el mismo, nº de la fila
            # primero y tercero son los valores que coge para sacar los dias que dura
            self.pintar_tareas(2,1,3,1)
            self.pintar_tareas(4,1,5,1)
            self.pintar_tareas(2,2,4,2) # j i j2 i2
            # self.pintar_tareas(2,1,2,1)
            # self.pintar_tareas(2,2,2,3)

        self.section_1.pack(fill="both", expand=True)






    # COPIAR SHOW_SECTION_1 EN LOS 3 DE ABAJO (aun no esta acabado)
    def show_section_2(self):
        self.clear_center_frame()
        self.section_2.pack(expand=True)

    def show_section_3(self):
        self.clear_center_frame()
        self.section_3.pack(expand=True)

    def show_section_4(self):
        self.clear_center_frame()
        self.section_4.pack(expand=True)




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


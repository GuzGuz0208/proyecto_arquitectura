import customtkinter as ctk
import tkinter as tk
import time
from Class.constantes import *


class InterfazBus:
    def __init__(self, canvas, cpu_height):
        self.canvas =  canvas
        self.color_datos = COLOR_BUS_DE_DATOS
        self.color_direcciones = COLOR_BUS_DE_DIRECCIONES
        self.color_control = COLOR_BUS_DE_CONTROL
        self.font = ("Arial", 10, "bold")
        self.buses = {}
        self.line_ids = {} 
        self.cpu_height = cpu_height  # Altura de la CPU

        # Asegurar que el dibujo se haga después de que el Canvas esté renderizado
        self.canvas.bind("<Configure>", self.on_configure)
        self.inicializar_buses()
        self.dibujar()

    def on_configure(self, event=None):
        """Se ejecuta cuando el Canvas cambia de tamaño."""
        # Validar que el canvas tenga dimensiones válidas
        if self.canvas.winfo_width() > 0 and self.canvas.winfo_height() > 0:
            self.inicializar_buses()
            self.dibujar()

    def inicializar_buses(self):
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        # Definir los límites de la región rosada
        pink_start_x = canvas_width * 0.7  
        pink_end_x = canvas_width * 0.9    
        bus_start_y = self.cpu_height * 0.37 
        bus_end_y = canvas_height * 0.70   # Límite inferior del área rosada

        # Coordenadas base de los buses dentro de la región rosada
        base_x = (pink_start_x + pink_end_x) / 2
        separation = (pink_end_x - pink_start_x) / 2  # Aumentar la separación entre buses
        bus_width = separation / 6  # Ajustar el ancho proporcionalmente

        # Calcular posiciones escaladas para los buses
        self.buses = {
            "datos": {
                "color": self.color_datos,
                "start": (base_x - separation,bus_start_y + (bus_end_y * 0.05)),
                "end": (base_x - separation, bus_end_y * 0.85),
                "label": "Bus de Datos",
                "width": bus_width,
                "estado": "Activo",
            },
            "direcciones": {
                "label": "Bus de Direcciones",
                "color": self.color_direcciones,
                "start": (base_x, bus_start_y + (bus_end_y * 0.1)), 
                "end": (base_x, bus_end_y * 0.90),
                "width": bus_width,
                "estado": "Inactivo",
            },
            "control": {
                "color": self.color_control,
                "start": (base_x + separation, bus_start_y + (bus_end_y * 0.15)),  
                "end": (base_x + separation, bus_end_y * 0.95),
                "label": "Bus de Control",
                "width": bus_width,
                "estado": "Activo",
            },
        }

    def dibujar(self):
        # Limpiar el canvas antes de dibujar
        self.canvas.delete("all")
        
        # Diccionario para almacenar los IDs de las líneas por bus
        self.line_ids = {}
        
        # Dibujar los buses
        for bus_name, bus_data in self.buses.items():
            color = bus_data["color"]
            start = bus_data["start"]
            end = bus_data["end"]
            width = bus_data["width"]
            
            # Almacenar el ID de la línea en el diccionario
            self.line_ids[bus_name] = {
                "Bus_principal": self.canvas.create_line(start[0], start[1], end[0], end[1], fill=color, width=int(width)),
                "label": self.draw_vertical_label(bus_data["label"], start[0] - 30, start[1], color),
                "Conexion_memoria_datos": self.crear_conexion_memoria_datos(start, end, color, width),
                "Conexion_memoria_programa": self.crear_conexion_memoria_programa(start, end, color, width),
                "Conexion_i_o": self.crear_conexion_i_o(start, end, color, width),
            }

    def draw_vertical_label(self, text, x, y, color):
        """Dibuja la etiqueta vertical para un bus."""
        if text:
            for i, char in enumerate(text):
                self.canvas.create_text(x, y + i * 10, text=char, fill=color, font=self.font)

    def draw_bus_status(self, estado, x, y, color):
        """Dibuja el estado del bus."""
        if estado:
            self.canvas.create_text(x, y, text=f"Estado: {estado}", fill=color, font=("Arial", 12, "bold"))

    def crear_conexion_memoria_datos(self, start, end, color, width):
        """
        Crea la conexión horizontal superior (relacionada con memoria/datos).
        La línea comienza desde el final del bus y se extiende hacia el borde derecho del canvas.
        
        :param start: Coordenadas de inicio del bus (x, y).
        :param end: Coordenadas de fin del bus (x, y).
        :param color: Color de la línea.
        :param width: Grosor de la línea.
        :return: ID de la línea creada.
        """
        canvas_width = self.canvas.winfo_width()  # Obtener el ancho actual del canvas
        # Crear la línea y devolver su ID
        return self.canvas.create_line(end[0] - int(width / 2), start[1], canvas_width, start[1], fill=color, width=int(width))

    def crear_conexion_i_o(self, start, end, color, width):
        """
        Crea la conexión horizontal inferior (relacionada con I/O).
        La línea comienza desde el borde izquierdo del canvas y termina al inicio del bus.
        
        :param start: Coordenadas de inicio del bus (x, y).
        :param end: Coordenadas de fin del bus (x, y).
        :param color: Color de la línea.
        :param width: Grosor de la línea.
        :return: ID de la línea creada.
        """
        # Crear la línea y devolver su ID
        return self.canvas.create_line(0, end[1], start[0] + int(width / 2), end[1], fill=color, width=int(width))

    def crear_conexion_memoria_programa(self, start, end, color, width):
        """
        Crea la conexión horizontal para la memoria del programa.
        La línea comienza al final del bus y se extiende hasta el borde derecho del canvas.
        
        :param start: Coordenadas de inicio del bus (x, y).
        :param end: Coordenadas de fin del bus (x, y).
        :param color: Color de la línea.
        :param width: Grosor de la línea.
        :return: ID de la línea creada.
        """
        frame_width = self.canvas.winfo_width()  # Obtener el ancho actual del canvas
        # Crear la línea y devolver su ID
        return self.canvas.create_line(end[0], end[1], frame_width, end[1], fill=color, width=int(width))

    def actualizar_color_linea(self, bus_name, new_color):
        """
        Resalta temporalmente las líneas de un bus y restaura su color original.
        
        :param bus_name: El nombre del bus (clave en self.line_ids) cuyo color se desea cambiar.
        :param new_color: El nuevo color que se aplicará temporalmente a las líneas del bus.
        """
        # Resaltar las líneas del bus con el nuevo color
        self.highlight_bus(bus_name, new_color)

        # Restaurar el color original después de 2 segundos
        if bus_name in self.buses:
            self.canvas.after(2000, lambda: self.reset_bus_color(bus_name))
        else:
            print(f"El bus '{bus_name}' no tiene un color original definido.")

    def highlight_bus(self, bus_name, color):
        """
        Cambia el color de las líneas asociadas a un bus.
        
        :param bus_name: El nombre del bus (clave en self.line_ids) cuyo color se desea resaltar.
        :param color: El color que se aplicará a las líneas del bus.
        """
        # Verificar si el bus existe en el diccionario line_ids
        if bus_name in self.line_ids:
            # Cambiar el color de todas las líneas asociadas al bus
            for key, line_id in self.line_ids[bus_name].items():
                if isinstance(line_id, int):  # Verificar que sea un ID válido
                    self.canvas.itemconfig(line_id, fill=color)
        else:
            print(f"El bus '{bus_name}' no existe o no tiene líneas asociadas.")


    def reset_bus_color(self, bus_name):
        """
        Restaura el color original de las líneas asociadas a un bus.
        
        :param bus_name: El nombre del bus (clave en self.line_ids) cuyo color se desea restaurar.
        """
        # Verificar si el bus existe en el diccionario line_ids y buses
        if bus_name in self.line_ids and bus_name in self.buses:
            original_color = self.buses[bus_name]["color"]  # Obtener el color original del bus
            # Restaurar el color de todas las líneas asociadas al bus
            for key, line_id in self.line_ids[bus_name].items():
                if isinstance(line_id, int):  # Verificar que sea un ID válido
                    self.canvas.itemconfig(line_id, fill=original_color)
        else:
            print(f"El bus '{bus_name}' no existe o no tiene líneas asociadas.")


    
    def activar_componente(self, bus_name, componente):
        pass

    def activar_bus_datos_conexion_io(self):
        """
        Activa las líneas del bus de datos y cambia su color a COLOR_BUS_DE_DATOS_ACTIVO.
        Después de 2 segundos, vuelve a su color original COLOR_BUS_DE_DATOS.
        """
        #time.sleep(2)
        # Obtener las líneas asociadas al bus 'datos'
        line_datos = self.line_ids.get("datos", {})  # Usamos .get() para evitar errores si no existe
        
        if line_datos:
            # Definir las líneas específicas a activar
            lineas_a_activar = ['Conexion_i_o', 'Bus_principal']
            
            # Cambiar el color de las líneas específicas a COLOR_BUS_DE_DATOS_ACTIVO
            for linea in lineas_a_activar:
                if linea in line_datos:
                    line_id = line_datos[linea]
                    # Asegúrate de que sea un número entero (ID válido de línea)
                    if isinstance(line_id, int):
                        self.canvas.itemconfig(line_id, fill=COLOR_BUS_DE_DATOS_ACTIVO)
                        self.canvas.after(2000, lambda line=line_id: self.canvas.itemconfig(line, fill='red'))
                
        else:
            print(f"El bus 'datos' no existe o no tiene las líneas especificadas.")
        
    def restaurar_color(self, line):
        self.canvas.itemconfig(line, fill="red")
    
    def activar_bus_direcciones(self):
        self.highlight_bus("direcciones", COLOR_BUS_DE_DIRECCIONES_ACTIVO)
    
    def activar_bus_control(self):
        self.highlight_bus("control", COLOR_BUS_DE_CONTROL_ACTIVO)
    
    def activar_bus_datos(self):
        self.highlight_bus("datos", COLOR_BUS_DE_DATOS_ACTIVO)
    
    def desactivar_bus_direcciones(self):
        self.highlight_bus("direcciones", COLOR_BUS_DE_DIRECCIONES)
    
    def desactivar_bus_control(self):
        self.highlight_bus("control", COLOR_BUS_DE_CONTROL)
    
    def desactivar_bus_datos(self):
        self.highlight_bus("datos", COLOR_BUS_DE_DATOS)

if __name__ == "_main_":
    COLOR_BACKGROUND = "white"
    COLOR_BUS_DE_DATOS = "red"

    # Crear la ventana principal
    root = ctk.CTk()
    root.geometry("800x600")
    root.title("Prueba de InterfazBus")

    # Crear un marco y pasar la clase InterfazBus
    frame = ctk.CTkFrame(root, width=800, height=600)
    frame.pack(fill="both", expand=True)

    interfaz = InterfazBus(frame, cpu_height=100)

    root.after(2000, lambda: interfaz.activar_bus_datos_conexion_io)
        # Crear un botón para cambiar el color
    boton_cambiar_color = ctk.CTkButton(root, text="Cambiar Color Bus de Datos", command=interfaz.activar_bus_datos_conexion_io)
    boton_cambiar_color.pack(pady=10)

    # Ejecutar el bucle principal
    root.mainloop()


    # Función para cambiar el color del bus 'datos'
def cambiar_color_datos():
    interfaz.actualizar_color_linea("datos", "blue")
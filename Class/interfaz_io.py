import customtkinter as ctk
from tkinter import filedialog
import os

class InterfazIO:
    def __init__(self, parent, cpu_main):
        # Configuración inicial de customtkinter
        ctk.set_appearance_mode("System")  # Modo: "System", "Dark" o "Light"
        ctk.set_default_color_theme("blue")  # Tema: "blue", "green", "dark-blue"

        # Crear el marco principal para la interfaz
        self.frame = ctk.CTkFrame(parent, width=0.2 * 1280, height=800, corner_radius=15)
        self.frame.pack(side="left", fill="y", padx=10, pady=10)

        # Etiqueta para el campo de entrada
        self.input_label = ctk.CTkLabel(
            self.frame, text="Campo de Entrada", font=("Arial", 14, "bold")
        )
        self.input_label.place(relx=0.05, rely=0.0)  # Letrero más visible

        # Campo de entrada (INPUT)
        self.input_text = ctk.CTkTextbox(self.frame, width=int(0.9 * 1280 * 0.2), height=220, corner_radius=10)
        self.input_text.place(relx=0.05, rely=0.05)  # Bajado ligeramente para que el letrero sea visible

        # Botones
        self.execute_button = ctk.CTkButton(
            self.frame, text="Comenzar", width=int(0.9 * 1280 * 0.2), height=40,
            fg_color="#4caf50",  # Color verde
            text_color="white",
            corner_radius=10,
            command=cpu_main.load_instructions
        )
        self.execute_button.place(relx=0.05, rely=0.35)  # Subir ligeramente el botón

        self.load_button = ctk.CTkButton(
            self.frame, text="Cargar Archivo", width=int(0.9 * 1280 * 0.2), height=40,
            fg_color="#2196f3",  # Color azul
            text_color="white",
            corner_radius=10,
            command=self.load_file
        )
        self.load_button.place(relx=0.05, rely=0.43)  # Subir ligeramente el botón

        self.save_button = ctk.CTkButton(
            self.frame, text="Guardar Instrucciones", width=int(0.9 * 1280 * 0.2), height=40,
            fg_color="#ff9800",  # Color naranja
            text_color="white",
            corner_radius=10,
            command=self.save_file
        )
        self.save_button.place(relx=0.05, rely=0.51)  # Subir ligeramente el botón

        # Nuevo botón: Cargar Instrucción
        self.load_instruction_button = ctk.CTkButton(
            self.frame, text="Cargar Instrucción", width=int(0.9 * 1280 * 0.2), height=40,
            fg_color="#9c27b0",  # Color púrpura
            text_color="white",
            corner_radius=10,
            command=cpu_main.load_single_instructions  # Cambiar al método adecuado
        )
        self.load_instruction_button.place(relx=0.05, rely=0.59)  # Subir ligeramente el botón

        # Etiqueta para el campo de salida
        self.output_label = ctk.CTkLabel(
            self.frame, text="Campo de Salida", font=("Arial", 14, "bold")
        )
        self.output_label.place(relx=0.05, rely=0.68)  # Mover el letrero más arriba

        # Campo de salida (OUTPUT)
        self.output_text = ctk.CTkTextbox(self.frame, width=int(0.9 * 1280 * 0.2), height=200, corner_radius=10)
        self.output_text.place(relx=0.05, rely=0.73)  # Ajustar ligeramente para que esté debajo del letrero
        self.output_text.configure(state="disabled")


    def execute_output(self):
        """Copia el contenido de INPUT al OUTPUT."""
        input_content = self.input_text.get("1.0", "end-1c")  # Obtener texto de INPUT
        self.output_text.configure(state="normal")  # Habilitar edición
        self.output_text.delete("1.0", "end")  # Limpiar OUTPUT
        self.output_text.insert("1.0", input_content)  # Insertar texto en OUTPUT
        self.output_text.configure(state="disabled")  # Deshabilitar edición

    def load_file(self):
        """Carga un archivo .jjj de ../ejemplos_programas en el campo INPUT."""
        file_path = filedialog.askopenfilename(
            initialdir="../ejemplos_programas",
            title="Seleccionar archivo .jjj",
            filetypes=(("Archivos .jjj", "*.jjj"), ("Todos los archivos", "*.*"))
        )
        if file_path:
            with open(file_path, "r") as file:
                content = file.read()
                self.input_text.delete("1.0", "end")  # Limpiar INPUT
                self.input_text.insert("1.0", content)  # Cargar contenido en INPUT

    def save_file(self):
        """Guarda el contenido de INPUT en un archivo .jjj en ../ejemplos_programas."""
        folder_path = "../ejemplos_programas"
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        file_path = filedialog.asksaveasfilename(
            initialdir=folder_path,
            title="Guardar archivo como",
            defaultextension=".jjj",
            filetypes=(("Archivos .jjj", "*.jjj"),)
        )
        if file_path:
            input_content = self.input_text.get("1.0", "end-1c")
            with open(file_path, "w") as file:
                file.write(input_content)

if __name__ == "__main__":
    # Crear la ventana principal
    root = ctk.CTk()
    root.geometry("1280x800")  # Definir tamaño de la ventana
    root.title("Interfaz de Entrada/Salida")

    # Inicializar la clase InterfazIO
    interfaz_io = InterfazIO(root)

    # Ejecutar el bucle principal
    root.mainloop()
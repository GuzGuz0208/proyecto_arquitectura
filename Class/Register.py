# Clase Register (Registro)
# Responsabilidades:
# - Representa un registro en la computadora.
# - Almacena un valor y lo muestra en el lienzo.

class Register:
    def __init__(self, canvas, x, y, name):
        self.value = 0
        self.canvas = canvas
        self.x = x
        self.y = y
        self.name = str(name)  # Convertir a cadena para evitar errores

        if self.name == "PSW":
            # Configuración para PSW
            self.rect_id = canvas.create_rectangle(
                x, y, x + 200, y + 30, fill="lightgray", outline="black")
            
            self.text_id = canvas.create_text(
                x + 100, y + 15, text=f"{self.name}: {self.value}", fill="black", font=("Arial", 12, "bold"))
        
        elif self.name == "ALU":
            # Configuración para ALU (triángulo invertido)
            self.triangle_id = canvas.create_polygon(
                x, y,               # Vértice superior izquierdo
                x + 200, y,         # Vértice superior derecho
                x + 100, y + 150,    # Vértice inferior centrado
                fill="lightblue", outline="black"
            )

            self.text_id = canvas.create_text(
                x + 80, y + 25, text=f"{self.name}: {self.value}", fill="black", font=("Arial", 12, "bold")
            )
        
        elif self.name.startswith("R") and self.name[1:].isdigit() and 1 <= int(self.name[1:]) <= 9:
            # Configuración especial para registros "R1" a "R9"
            self.rect_id = canvas.create_rectangle(
                x, y, x + 120, y + 25, fill="lightgreen", outline="black"
            )

            self.text_id = canvas.create_text(
                x + 60, y + 12, text=f"{self.name}: {self.value}", fill="black", font=("Arial", 10, "bold")
            )
        
        else:
            # Configuración para otros registros
            self.rect_id = canvas.create_rectangle(
                x, y, x + 150, y + 30, fill="lightgray", outline="black"
            )

            self.text_id = canvas.create_text(
                x + 75, y + 15, text=f"{self.name}: {self.value}", fill="black", font=("Arial", 12, "bold")
            )

    def set_value(self, value):
        self.value = value

        if self.name == "ALU":
            self.canvas.itemconfig(self.text_id, text=f"{self.name}: \n{self.value}")
        else:
            self.canvas.itemconfig(self.text_id, text=f"{self.name}: {self.value}")
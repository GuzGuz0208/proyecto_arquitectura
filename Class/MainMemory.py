from Class.Memory import Memory

class MainMemory:
    def __init__(self, canvas):
        self.canvas = canvas
        self.memory = Memory(self.canvas, 850, 70, 32)
        # Se ha comentado la creación de texto ya que no parece tener un propósito activo
        # self.memory_text = self.canvas.create_text(660, 80, text="", fill="white", anchor="nw", font=("Arial", 12, "bold"))

    def update_memory_display(self, instructions):
        """
        Actualiza la visualización de la memoria en el canvas.
        Este método actualiza los valores de las instrucciones en la memoria
        (Memoria de instrucciones y datos) y los dibuja en el lienzo.

        :param instructions: Lista de instrucciones que se deben visualizar.
        """
        # Este es un ejemplo de cómo se podría realizar la actualización visual.
        # Si quieres mostrar las instrucciones de manera visual:
        memory_contents = "\n".join(f"{i}: {instr}" for i, instr in enumerate(instructions))
        
        # Actualizamos el texto en el lienzo (descomentamos si es necesario usar el `self.memory_text`)
        # self.canvas.itemconfig(self.memory_text, text=memory_contents)
        print("Actualización de memoria: ", memory_contents)

    def reset(self):
        """
        Restablece la memoria y la visualización de los valores en el canvas.
        Limpia los valores de la memoria y actualiza la vista.
        """
        self.memory.clear_registers()
        self.update_memory_display([])  # Limpiar la visualización de memoria
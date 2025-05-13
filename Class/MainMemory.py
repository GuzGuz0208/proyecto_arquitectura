from Class.Memory import Memory

class MainMemory:
    def __init__(self, canvas):
        self.canvas = canvas
        self.memory = Memory(self.canvas, 850, 70, 32)
        #self.memory_text = self.canvas.create_text(660, 80, text="", fill="white", anchor="nw", font=("Arial", 12, "bold"))

    def update_memory_display(self, instructions):
        pass
        #memory_contents = "\n".join(f"{i} - {instr}" for i, instr in enumerate(instructions))
        #self.canvas.itemconfig(self.memory_text, text=memory_contents)

    def reset(self):
        self.memory.clear_registers()
        self.update_memory_display([])
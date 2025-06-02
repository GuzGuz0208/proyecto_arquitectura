from Class.ALU import ALU
from Class.Register import Register
from Class.RegisterBank import RegisterBank
from Class.ControlUnit import ControlUnit
from Class.WiredControlUnit import WiredControlUnit
import tkinter as tk

class CPU:
    def __init__(self, canvas):
        self.canvas = canvas
        self.inner_canvas = tk.Canvas(canvas, width=400, height=400, bg="#1C1C1C")  # Crear un nuevo Canvas como widget
        self.inner_canvas.place(x=20, y=20)  # Posicionar el nuevo Canvas dentro del principal

        self.alu = ALU()
        self.register_bank = RegisterBank(self.inner_canvas, 15, 250) #300, 45
        self.pc_register = Register(self.inner_canvas, 230, 200, "PC")
        self.mar_register = Register(self.inner_canvas, 230, 50, "MAR")
        self.ir_register = Register(self.inner_canvas, 230, 100, "IR")
        self.mbr_register = Register(self.inner_canvas, 230, 150, "MBR")
        self.alu_text = Register(self.inner_canvas, 15, 70, "ALU")
        self.psw_register = Register(self.inner_canvas, 100, 350, "PSW")

        # Instancia de la Unidad de Control
        self.control_unit = ControlUnit()
        self.wired_control_unit = WiredControlUnit(canvas)  # O usa otra implementación si corresponde

    def reset(self):
        self.alu = ALU()
        self.pc_register.set_value(0)
        self.mar_register.set_value(0)
        self.ir_register.set_value(0)
        self.mbr_register.set_value(0)
        self.psw_register.set_value("Z: 0, C: 0, S: 0, O: 0 ")
        self.alu_text.set_value(0)
        self.register_bank.clear_registers()

    def update_psw_display(self):
        psw_text = f"Z: {self.alu.psw['Z']} C: {self.alu.psw['C']} S: {self.alu.psw['S']} O: {self.alu.psw['O']}"
        self.psw_register.set_value(psw_text)
    

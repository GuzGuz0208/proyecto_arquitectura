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

        # Componentes principales de la CPU
        self.alu = ALU()  # Unidad aritmético-lógica
        self.register_bank = RegisterBank(self.inner_canvas, 15, 250)  # Banco de registros
        self.pc_register = Register(self.inner_canvas, 230, 200, "PC")  # Contador de programa (PC)
        self.mar_register = Register(self.inner_canvas, 230, 50, "MAR")  # Registro de dirección de memoria (MAR)
        self.ir_register = Register(self.inner_canvas, 230, 100, "IR")  # Registro de instrucción (IR)
        self.mbr_register = Register(self.inner_canvas, 230, 150, "MBR")  # Registro de buffer de memoria (MBR)
        self.alu_text = Register(self.inner_canvas, 15, 70, "ALU")  # Texto de salida para ALU
        self.psw_register = Register(self.inner_canvas, 100, 350, "PSW")  # Registro de bandera de estado del programa (PSW)

        # Instancia de la Unidad de Control
        self.control_unit = ControlUnit()
        self.wired_control_unit = WiredControlUnit(canvas)  # Unidad de control conectada al canvas

    def reset(self):
        """Restablecer todos los componentes de la CPU a su estado inicial"""
        self.alu = ALU()
        self.pc_register.set_value(0)
        self.mar_register.set_value(0)
        self.ir_register.set_value(0)
        self.mbr_register.set_value(0)
        self.psw_register.set_value("Z: 0, C: 0, N: 0, O: 0 ")  # Reset de las banderas
        self.alu_text.set_value(0)
        self.register_bank.clear_registers()

    def update_psw_display(self):
        """Actualizar la visualización de las banderas en el PSW"""
        psw_text = f"Z: {self.alu.psw['Z']} C: {self.alu.psw['C']} N: {self.alu.psw['N']} O: {self.alu.psw['O']}"
        self.psw_register.set_value(psw_text)

    def get_register_value(self, reg_name):
        """Obtener el valor de un registro del banco de registros"""
        return self.register_bank.get(reg_name)

    def set_register_value(self, reg_name, value):
        """Establecer el valor de un registro en el banco de registros"""
        self.register_bank.set(reg_name, value)
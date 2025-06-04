import tkinter as tk
from Class.constantes import *
from Class.Dictionary import OPCODES  # asumo que está definido aquí

# Diccionario inverso para mapear opcode int a nombre string
OPCODE_NAMES = {v: k for k, v in OPCODES.items()}

class WiredControlUnit:
    """
    Clase que gestiona la generación de señales de control y su visualización en un canvas.
    """

    def __init__(self, main_canvas):
        self.control_signals = {}
        self.instruction_register = None
        self.main_canvas = main_canvas

    def initialize_internal_canvas(self):
        self.main_canvas.update_idletasks()
        canvas_width = self.main_canvas.winfo_width()
        canvas_height = self.main_canvas.winfo_height()

        self.internal_canvas = tk.Canvas(
            self.main_canvas,
            bg=COLOR_COMPONENTES,
            width=canvas_width,
            height=int(canvas_height * 0.2),
            highlightthickness=0
        )
        self.internal_canvas.place(x=0, y=int(canvas_height * 0.7), width=canvas_width, height=int(canvas_height * 0.2))

    def fetch(self, memory, pc):
        instruction = memory.load_instruction(pc)
        self.instruction_register = instruction
        return instruction

    def decode(self):
        if not self.instruction_register:
            raise ValueError("No instruction loaded in the instruction register")
        parts = self.instruction_register.split(maxsplit=1)
        opcode = parts[0]
        if len(parts) > 1:
            operands = parts[1].split(',')
            reg1 = operands[0].strip()
            reg2 = operands[1].strip() if len(operands) > 1 else ''
        else:
            reg1, reg2 = '', ''
        return opcode, reg1, reg2

    def generate_control_signals(self, opcode):

        self.control_signals = {
            'fetch': True,
            'decode': True,
            'execute': False,
            'memory_read': False,
            'memory_write': False,
            'register_read': False,
            'register_write': False,
            'alu_operation': None,
        }
        if isinstance(opcode, int):
            opcode = OPCODE_NAMES.get(opcode, 'UNKNOWN')
        if opcode in ['ADD', 'SUB', 'MUL', 'DIV', 'AND', 'OR', 'NOT', 'XOR']:
            self.control_signals['execute'] = True
            self.control_signals['alu_operation'] = opcode
            self.control_signals['register_read'] = True
            self.control_signals['register_write'] = True
        elif opcode == 'LOAD':
            self.control_signals['memory_read'] = True
            self.control_signals['register_write'] = True
        elif opcode == 'STORE':
            self.control_signals['memory_write'] = True
        elif opcode == 'MOVE':
            self.control_signals['register_read'] = True
            self.control_signals['register_write'] = True
        elif opcode == 'JP':  # Jump
            self.control_signals['execute'] = True
            self.control_signals['alu_operation'] = 'JP'
        elif opcode == 'JPZ':  # Jump if Zero
            self.control_signals['execute'] = True
            self.control_signals['alu_operation'] = 'JPZ'
        elif opcode == 'CALL':
            self.control_signals['execute'] = True
            self.control_signals['alu_operation'] = 'CALL'
        elif opcode == 'HALT':
            self.control_signals['execute'] = False  # Halt no hace nada, solo detiene la ejecución

        return self.control_signals

    def update_control_signals_display(self):
        self.internal_canvas.delete("all")

        signals = list(self.control_signals.items())
        mid_index = len(signals) // 2

        x_start_col1 = 10
        x_start_col2 = 220
        y_offset = 10
        row_height = 30

        text_font = ("Arial", 12)
        text_color = "white"

        for i, (signal, value) in enumerate(signals[:mid_index]):
            if signal == "alu_operation":
                text = f"{signal}: {value or 'N/A'}"
                self.internal_canvas.create_rectangle(x_start_col1, y_offset, x_start_col1 + 190, y_offset + 20, fill="gray")
                self.internal_canvas.create_text(x_start_col1 + 95, y_offset + 10, text=text, anchor="center", font=text_font, fill=text_color)
            else:
                color = "#FFD580" if value else "#D3D3D3"
                self.internal_canvas.create_text(x_start_col1, y_offset, text=f"{signal}: ", anchor="w", font=text_font, fill=text_color)
                self.internal_canvas.create_oval(x_start_col1 + 120, y_offset - 5, x_start_col1 + 140, y_offset + 15, fill=color)
            y_offset += row_height

        y_offset = 10

        for i, (signal, value) in enumerate(signals[mid_index:]):
            if signal == "alu_operation":
                text = f"{signal}: {value or 'N/A'}"
                self.internal_canvas.create_rectangle(x_start_col2, y_offset, x_start_col2 + 190, y_offset + 20, fill="gray")
                self.internal_canvas.create_text(x_start_col2 + 95, y_offset + 10, text=text, anchor="center", font=text_font, fill=text_color)
            else:
                color = "#FFD580" if value else "#D3D3D3"
                self.internal_canvas.create_text(x_start_col2, y_offset, text=f"{signal}: ", anchor="w", font=text_font, fill=text_color)
                self.internal_canvas.create_oval(x_start_col2 + 120, y_offset - 5, x_start_col2 + 140, y_offset + 15, fill=color)
            y_offset += row_height
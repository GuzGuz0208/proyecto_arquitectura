import tkinter as tk
from tkinter import Canvas
from Class.input_outpout import InputOutput
from Class.interfaz_bus import InterfazBus
from Class.MainMemory import MainMemory
from Class.CPU import CPU
from Class.interfaz_io import InterfazIO
from Class.interfaz_memoria import InterfazMemoria
from Class.constantes import *



# Clase ComputerSimulator (Simulador de Computadora)
# Responsabilidades:
# - Controla la simulación de la computadora.
# - Interactúa con los elementos de la interfaz gráfica de usuario (GUI) para mostrar la simulación.
class ComputerSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Proyecto Final Arquitectura")
        self.root.configure(bg=COLOR_BACKGROUND)
        self.canvas = Canvas(self.root, width=700, height=500,  highlightthickness=0)

        self.cpu = CPU(self.canvas)
        self.system_buses = InterfazBus(self.canvas ,0)

        self.create_widgets()
        self.create_layout()
        self.cpu.wired_control_unit.initialize_internal_canvas()



        self.main_memory = MainMemory(self.canvas)

        self.instructions = []
        self.control_signals_text = {}
        self.create_control_signals_display()
        self.cpu.update_psw_display()

    def create_widgets(self):
        # Cambiar colores a llamativos y ajustar tamaños
        
        self.io = InterfazIO(self.root, self)
        self.memorias = InterfazMemoria(self.root)
        self.input_output = InputOutput(self.io.output_text, self.cpu.register_bank, self.memorias)  # Instancia de InputOutput
        self.text_widget = self.io.input_text      


    def create_layout(self):

        # Posicionar el canvas al lado derecho
        self.canvas.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH, padx=0, pady=10)
        self.canvas.configure(bg=COLOR_MODULOS)  # Establecer fondo como prueba visual
       
    def create_control_signals_display(self):
        signals = ['fetch', 'decode', 'execute', 'memory_read', 'memory_write', 'register_read', 'register_write', 'alu_operation']
        y_position = 60
        for idx, signal in enumerate(signals):
            text_id = self.canvas.create_text(1050, y_position + idx * 30, text=f"{signal}: Off", fill="white", font=("Arial", 12, "bold"), anchor="w")
            self.control_signals_text[signal] = text_id

    def reset(self):
        self.cpu.reset()
        self.main_memory.reset()
        self.instructions = []
        self.main_memory.update_memory_display(self.instructions)
        self.memorias.cargar_instruccion(self.instructions)

    def load_instructions(self):
        self.reset()
        instructions = self.text_widget.get("1.0", tk.END).strip().split('\n')
        for idx, instruction in enumerate(instructions):
            if instruction.strip():
                if len(self.instructions) >= self.main_memory.memory.size // 2:
                    print("There is no space in memory to load more instructions.")
                    break

                 # Verificar si la instrucción contiene la palabra SHOW
                if "SHOW" in instruction.upper():  
                    print("Instrucción SHOW detectada")
                    print("Instrucción: ", instruction.strip())
                    self.input_output.process_instruction(instruction)  # Procesar instrucción SHOW
                    #self.output()  # Llamar al método de salida

                self.main_memory.memory.store_instruction(idx, instruction.strip())
                self.instructions.append(instruction.strip())
        self.main_memory.update_memory_display(self.instructions)
        self.memorias.cargar_instruccion(self.instructions)
        self.execute_all_instructions()

    def load_single_instructions(self):
        self.reset()
        instructions = self.text_widget.get("1.0", tk.END).strip().split('\n')
        for idx, instruction in enumerate(instructions):
            if instruction.strip():
                if len(self.instructions) >= self.main_memory.memory.size // 2:
                    print("There is no space in memory to load more instructions.")
                    break
                self.main_memory.memory.store_instruction(idx, instruction.strip())
                self.instructions.append(instruction.strip())
        self.main_memory.update_memory_display(self.instructions)
        self.memorias.cargar_instruccion(self.instructions)

    def fetch_cycle(self):
        pc_value = self.cpu.pc_register.value
        self.cpu.mar_register.set_value(pc_value)
        mar_value = self.cpu.mar_register.value
        #instruction = self.cpu.control_unit.fetch(self.main_memory.memory, mar_value)
        instruction = self.cpu.wired_control_unit.fetch(self.main_memory.memory, pc_value)


        if not instruction:
            raise ValueError("No instruction found at PC address")
        self.cpu.mbr_register.set_value(instruction)
        self.cpu.ir_register.set_value(instruction)
        self.cpu.pc_register.set_value(pc_value + 1)
        self.cpu.mar_register.set_value(self.cpu.pc_register.value)
        #opcode, reg1, reg2 = self.cpu.control_unit.decode()
        opcode, reg1, reg2 = self.cpu.wired_control_unit.decode()
        operand1 = int(reg1) if reg1.isdigit() else self.cpu.register_bank.get(reg1) if reg1 in self.cpu.register_bank.registers else None
        operand2 = None
        if reg2.startswith('*'):
            address_register = reg2[1:]
            if address_register in self.cpu.register_bank.registers:
                address = self.cpu.register_bank.get(address_register)
                operand2 = self.main_memory.memory.load_data(address).value
            else:
                raise ValueError(f"Invalid register for indirect addressing: {address_register}")
        elif reg2.isdigit():
            operand2 = int(reg2)
        elif reg2 in self.cpu.register_bank.registers:
            operand2 = self.cpu.register_bank.get(reg2)
        control_signals = self.cpu.wired_control_unit.generate_control_signals(opcode)
        self.cpu.wired_control_unit.update_control_signals_display()
        self.system_buses.activar_bus_direcciones()
        self.root.after(500, self.system_buses.desactivar_bus_direcciones)
        self.root.after(500, self.execute_cycle, opcode, reg1, reg2, operand1, operand2, control_signals)

    def execute_cycle(self, opcode, reg1, reg2, operand1, operand2, control_signals):
        self.reset_data_travel()
        if control_signals['alu_operation']:
            self.cpu.alu.execute(control_signals['alu_operation'], int(operand1), int(operand2))
            result = self.cpu.alu.value
            if opcode in ['ADD', 'SUB', 'MUL', 'DIV', 'AND', 'OR', 'NOT', 'XOR']:
                self.cpu.alu_text.set_value(f"{operand1} {opcode} {operand2 if operand2 is not None else ''} = {self.cpu.alu.value}")
                self.cpu.register_bank.set(reg1, result)
        elif opcode == 'JP':
            self.cpu.pc_register.set_value(operand1)
        elif opcode == 'JPZ':
            if operand2 != 0:
                self.cpu.pc_register.set_value(operand1)
        elif opcode == 'LOAD':
            if reg2.startswith('*'):
                address = self.cpu.register_bank.get(reg2[1:])
                value = self.main_memory.memory.load_data(address).value
                self.highlight_data_travel()
                self.cpu.mbr_register.set_value(value)
                value = self.main_memory.memory.load_data(address).value
            elif reg2.startswith("[") and reg2.endswith("]") and reg2[1:-1].isdigit():
                # Cargar el valor de la dirección de memoria usando el método load_data
                value = self.memorias.load_data(int(reg2[1:-1]))  # Asegúrate de convertir la dirección a entero

            else:
                if operand2 > 0x3FFF or operand2 < -0x4000:
                    raise ValueError('Operands out of range')
                value = operand2
                self.cpu.mbr_register.set_value(value)
                self.highlight_data_travel()

            self.cpu.register_bank.set(reg1, value)
        elif opcode == 'STORE':
            self.highlight_data_travel()
            print(f"Storing {operand1} in {operand2}")
            self.memorias.store_data(operand2, operand1)
        elif opcode == 'MOVE':
            self.cpu.register_bank.set(reg1, self.cpu.register_bank.get(reg2))
        elif opcode == 'SHOW':
            self.highlight_data_travel()
        self.root.update()
        self.cpu.wired_control_unit.update_control_signals_display()

    def reset_data_travel(self):
        self.root.after(500, self.system_buses.desactivar_bus_control)
        self.root.after(1000, self.system_buses.desactivar_bus_datos)

    def highlight_data_travel(self):
        self.system_buses.activar_bus_control()
        self.system_buses.activar_bus_datos()

    def highlight_output_travel(self):
        self.system_buses.activar_bus_control()
        self.system_buses.activar_bus_datos()

    def execute_all_instructions(self):
        if self.cpu.pc_register.value < len(self.instructions):
            self.fetch_cycle()
            self.root.after(2000, self.execute_all_instructions)
        else:
            print("Execution completed.")
        self.cpu.update_psw_display()

    def execute_single_instruction(self):
        if self.cpu.pc_register.value < len(self.instructions):
            self.fetch_cycle()
        else:
            print("Execution completed.")
        self.cpu.update_psw_display()
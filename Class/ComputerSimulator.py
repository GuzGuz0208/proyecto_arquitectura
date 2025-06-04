import tkinter as tk
from tkinter import Canvas
from Class.InputOutput import InputOutput
from Class.interfaz_bus import InterfazBus
from Class.MainMemory import MainMemory
from Class.CPU import CPU
from Class.interfaz_io import InterfazIO
from Class.interfaz_memoria import InterfazMemoria
from Class.constantes import *
from Class.Instruction import parse_assembly_line
from Class.Dictionary import OPCODES, OPCODE_TO_ALU_OP, MODE_DIRECT, MODE_INDIRECT, MODE_IMMEDIATE, MODE_REGISTER

class ComputerSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulación Computador")
        self.root.configure(bg=COLOR_BACKGROUND)
        self.canvas = Canvas(self.root, highlightthickness=0)

        # Instanciación de los componentes
        self.cpu = CPU(self.canvas)
        self.system_buses = InterfazBus(self.canvas, 0)
        self.main_memory = MainMemory(self.canvas)

        self.create_widgets()
        self.create_layout()
        self.cpu.wired_control_unit.initialize_internal_canvas()

        self.instructions = []
        self.control_signals_text = {}
        self.create_control_signals_display()
        self.cpu.update_psw_display()

    def create_widgets(self):
        """Crear los widgets de la interfaz"""
        self.io = InterfazIO(self.root, self)
        self.memorias = InterfazMemoria(self.root)
        self.input_output = InputOutput(self.io.output_text, self.cpu.register_bank, self.memorias)
        self.text_widget = self.io.input_text

    def create_layout(self):
        """Configurar el diseño y la posición de los elementos en la interfaz"""
        self.canvas.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH, padx=0, pady=10)
        self.canvas.configure(bg=COLOR_MODULOS)

    def create_control_signals_display(self):
        """Crear y mostrar las señales de control en la interfaz"""
        signals = ['fetch', 'decode', 'execute', 'memory_read', 'memory_write', 'register_read', 'register_write', 'alu_operation']
        y_position = 60
        for idx, signal in enumerate(signals):
            text_id = self.canvas.create_text(1050, y_position + idx * 30, text=f"{signal}: Off", fill="white", font=("Arial", 12, "bold"), anchor="w")
            self.control_signals_text[signal] = text_id

    def reset(self):
        """Reiniciar el simulador y limpiar las instrucciones cargadas"""
        self.cpu.reset()
        self.main_memory.reset()
        self.instructions = []
        self.main_memory.update_memory_display(self.instructions)
        self.memorias.cargar_instruccion(self.instructions)

    def load_instructions(self):
        """Cargar instrucciones desde el widget de entrada (text_widget)"""
        self.reset()
        lines = self.text_widget.get("1.0", tk.END).strip().split('\n')
        self.instructions = []
        for idx, line in enumerate(lines):
            if line.strip():
                try:
                    instr = parse_assembly_line(line)
                    if instr is None:
                        continue
                    self.main_memory.memory.store_instruction(idx, f"{instr.raw:08X}")
                    self.instructions.append(instr)
                    print(f"[INFO] Instrucción #{idx+1}: {instr}")
                except Exception as e:
                    print(f"[ERROR] Línea {idx+1}: {e}")
                    break
        self.main_memory.update_memory_display([f"{i.raw:08X}" for i in self.instructions])
        self.memorias.cargar_instruccion([f"{i.raw:08X}" for i in self.instructions])
        self.execute_all_instructions()

    def load_single_instructions(self):
        """Cargar una sola instrucción desde el widget de entrada"""
        self.reset()
        instructions = self.text_widget.get("1.0", tk.END).strip().split('\n')
        for idx, instruction in enumerate(instructions):
            if instruction.strip():
                if len(self.instructions) >= self.main_memory.memory.size // 2:
                    print("No hay espacio en memoria para cargar más instrucciones.")
                    break
                self.main_memory.memory.store_instruction(idx, instruction.strip())
                self.instructions.append(instruction.strip())
        self.main_memory.update_memory_display(self.instructions)
        self.memorias.cargar_instruccion(self.instructions)

    def fetch_cycle(self):
        """Ciclo de búsqueda de la instrucción"""
        pc_value = self.cpu.pc_register.value
        self.cpu.mar_register.set_value(pc_value)

        if pc_value >= len(self.instructions):
            raise ValueError("PC fuera de rango de instrucciones cargadas")

        instr = self.instructions[pc_value]
        self.cpu.mbr_register.set_value(instr.raw)
        self.cpu.ir_register.set_value(instr.raw)

        self.cpu.pc_register.set_value(pc_value + 1)
        self.cpu.mar_register.set_value(self.cpu.pc_register.value)

        opcode = instr.opcode
        reg1 = instr.operand1
        reg2 = instr.operand2
        mode = instr.mode
        extra = instr.extra

        operand1 = reg1
        operand2 = reg2

        if mode == MODE_INDIRECT:
            reg_name = f"R{reg2}"
            address = self.cpu.register_bank.get(reg_name)
            operand2 = self.main_memory.memory.load_data(address).value

        elif mode == MODE_DIRECT:
            pass

        elif mode == MODE_IMMEDIATE:
            pass

        elif mode == MODE_REGISTER:
            pass

        control_signals = self.cpu.wired_control_unit.generate_control_signals(opcode)
        self.cpu.wired_control_unit.update_control_signals_display()

        self.system_buses.activar_bus_direcciones()
        self.root.after(500, self.system_buses.desactivar_bus_direcciones)
        self.root.after(500, self.execute_cycle, opcode, reg1, reg2, operand1, operand2, control_signals)

    def execute_cycle(self, opcode, reg1, reg2, operand1, operand2, control_signals):
        """Ejecutar el ciclo de instrucción según el opcode y los operandos"""
        print(f"[DEBUG] Ejecutando ciclo de instrucción con los parámetros:")
        print(f"[DEBUG] Opcode: 0x{opcode:02X} ({OPCODES.get(opcode, 'Desconocido')})")
        print(f"[DEBUG] reg1: {reg1}, reg2: {reg2}")
        print(f"[DEBUG] operand1: {operand1}, operand2: {operand2}")
        print(f"[DEBUG] control_signals: {control_signals}")

        self.reset_data_travel()
        reg_name1 = f"R{reg1}"
        reg_name2 = f"R{reg2}"

        # Aquí intentamos obtener la instrucción actual desde la lista de instrucciones
        instr = None
        try:
            instr = self.instructions[self.cpu.pc_register.value - 1]
            print(f"[DEBUG] Instrucción cargada: {instr}")
        except IndexError:
            print("[ERROR] PC fuera de rango de instrucciones")
            return

        # Verificar el modo de la instrucción cargada
        print(f"[DEBUG] Modo de la instrucción: {instr.mode}")

        # Ejecutar ALU solo si hay operación y si opcode está en la lista
        if control_signals.get('alu_operation', False) and opcode in OPCODE_TO_ALU_OP:
            alu_op = OPCODE_TO_ALU_OP.get(opcode)
            print(f"[DEBUG] ALU operation: {alu_op}")

            val1 = self.cpu.register_bank.get(reg_name1)
            val2 = self.cpu.register_bank.get(reg_name2)
            print(f"[DEBUG] ALU operando con: {val1} {alu_op} {val2}")

            self.cpu.alu.execute(alu_op, val1, val2)
            result = self.cpu.alu.value
            self.cpu.register_bank.set(reg_name1, result)
            self.cpu.alu_text.set_value(f"{val1} {alu_op} {val2} = {result}")

            # Actualizar indicador visual
            self.canvas.itemconfig(self.control_signals_text['alu_operation'], fill="yellow")
        else:
            # Desactivar indicador si no hay operación ALU
            self.canvas.itemconfig(self.control_signals_text['alu_operation'], fill="gray")

        # Aquí continúa con el resto de instrucciones
        if opcode == OPCODES['LOADI']:
            print(f"[DEBUG] Cargando valor inmediato en {reg_name1}: {operand2}")
            self.cpu.register_bank.set(reg_name1, operand2)

        elif opcode == OPCODES['LOAD']:
            print(f"[DEBUG] Cargando desde memoria (directo o indirecto) a {reg_name1}")
            if instr.mode == MODE_DIRECT:
                value = self.main_memory.memory.load_data(operand2).value
            elif instr.mode == MODE_INDIRECT:
                addr = self.cpu.register_bank.get(reg_name2)
                value = self.main_memory.memory.load_data(addr).value
            else:
                raise ValueError(f"Modo inválido para LOAD: {instr.mode}")
            self.cpu.register_bank.set(reg_name1, value)

        elif opcode == OPCODES['STORE']:
            print(f"[DEBUG] Almacenando en memoria desde {reg_name1} hacia {operand2}")
            if instr.mode == MODE_DIRECT:
                addr = operand2
            elif instr.mode == MODE_INDIRECT:
                addr = self.cpu.register_bank.get(reg_name2)
            else:
                raise ValueError(f"Modo inválido para STORE: {instr.mode}")
            value = self.cpu.register_bank.get(reg_name1)
            self.highlight_data_travel()
            self.memorias.store_data(addr, value)

        elif opcode == OPCODES['MOVE']:
            print(f"[DEBUG] Moviendo valor de {reg_name2} a {reg_name1}")
            value = self.cpu.register_bank.get(reg_name2)
            self.cpu.register_bank.set(reg_name1, value)

        elif opcode == OPCODES['JP']:
            print(f"[DEBUG] Salto incondicional a {operand1}")
            self.cpu.pc_register.set_value(operand1)

        elif opcode == OPCODES['JPZ']:
            print(f"[DEBUG] Salto si {reg_name1} es 0")
            val = self.cpu.register_bank.get(reg_name1)
            if val == 0:
                self.cpu.pc_register.set_value(operand2)

        elif opcode == OPCODES['JNZ']:
            print(f"[DEBUG] Salto si {reg_name1} no es 0")
            val = self.cpu.register_bank.get(reg_name1)
            if val != 0:
                self.cpu.pc_register.set_value(operand2)

        elif opcode == OPCODES['SHOW']:
            instruction_str = f"SHOW {reg_name1}"
            self.input_output.process_instruction(instruction_str)

        elif opcode == OPCODES['HALT']:
            print("[INFO] Ejecución detenida por HALT.")
            # Aquí puedes detener la simulación si tienes bandera o lógica

        else:
            print(f"[WARN] Opcode no implementado: {opcode}")

        self.root.update()
        self.cpu.wired_control_unit.update_control_signals_display()

        print(f"[DEBUG] Ejecutado opcode={opcode}, reg1={reg1}, reg2={reg2}, operand1={operand1}, operand2={operand2}")

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
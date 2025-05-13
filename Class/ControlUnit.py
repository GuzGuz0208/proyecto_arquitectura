# Clase ControlUnit (Unidad de Control)
# Responsabilidades:
# - Coordina el flujo de instrucciones.
# - Carga las instrucciones desde la memoria y las decodifica.
class ControlUnit:
    def __init__(self):
        # El registro de instrucción almacena la instrucción actualmente cargada.
        self.instruction_register = None

    # Método fetch: Carga la instrucción desde la memoria en función del contador de programa (PC).
    # Parámetros:
    # - memory: Objeto de memoria desde el cual se carga la instrucción.
    # - pc: Contador de programa que indica la dirección de memoria de la siguiente instrucción.
    # - Devuelve la instrucción cargada.
    def fetch(self, memory, pc):
        instruction = memory.load_instruction(pc)
        self.instruction_register = instruction
        return instruction

    # Método decode: Decodifica la instrucción actualmente cargada en el registro de instrucción.
    # Devuelve el opcode, y opcionalmente los operandos.
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

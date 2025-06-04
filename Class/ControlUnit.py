from Class.Instruction import Instruction

class ControlUnit:
    def __init__(self):
        """
        Inicializa el registro de instrucciones (instruction_register).
        Este registro almacenará la instrucción cargada en el ciclo de Fetch.
        """
        self.instruction_register = None

    def fetch(self, memory, pc):
        """
        Carga la instrucción codificada (entero de 32 bits) desde la memoria utilizando el contador de programa (PC),
        y crea un objeto Instruction con ella. La instrucción se almacena en el registro de instrucción.
        
        :param memory: Objeto de memoria con el método load_instruction(direccion).
        :param pc: Dirección actual del contador de programa (PC).
        :return: Objeto Instruction cargado.
        :raises ValueError: Si no se encuentra una instrucción en la dirección especificada.
        """
        raw_instr = memory.load_instruction(pc)  # Cargar instrucción desde la memoria usando PC.
        if raw_instr is None:
            raise ValueError(f"No instruction found at address {pc}")  # Si no se encuentra instrucción.
        self.instruction_register = Instruction(raw_instr)  # Crear objeto Instruction.
        return self.instruction_register

    def decode(self):
        """
        Devuelve los campos decodificados de la instrucción cargada en el registro de instrucción.
        
        :return: Tuple(opcode:int, operand1:int, operand2:int, mode:int, extra:int).
        :raises ValueError: Si no hay ninguna instrucción cargada en el registro.
        """
        if not self.instruction_register:
            raise ValueError("No instruction loaded in the instruction register")  # Verifica que haya una instrucción cargada.
        
        # Extraer los valores de la instrucción cargada.
        instr = self.instruction_register
        return instr.opcode, instr.operand1, instr.operand2, instr.mode, instr.extra
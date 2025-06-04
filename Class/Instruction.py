import re
from Class.Dictionary import OPCODES, ALLOWED_MODES, MODE_REGISTER, MODE_IMMEDIATE, MODE_DIRECT, MODE_INDIRECT

class Instruction:
    def __init__(self, raw_value: int):
        """
        Representa una instrucción de 32 bits.

        Args:
            raw_value (int): valor entero de 32 bits que codifica la instrucción.
        """
        self.raw = raw_value & 0xFFFFFFFF  # asegurarse de 32 bits

        # Extraer campos
        self.opcode = (self.raw >> 24) & 0xFF
        self.operand1 = (self.raw >> 16) & 0xFF
        self.operand2 = (self.raw >> 8) & 0xFF
        self.extension = self.raw & 0xFF

        # Modo de direccionamiento (2 bits más altos de extensión)
        self.mode = (self.extension >> 6) & 0b11

        # Bits restantes para flags u opciones
        self.extra = self.extension & 0b00111111

    def __str__(self):
        return (f"Instruction(opcode=0x{self.opcode:02X}, operand1=0x{self.operand1:02X}, "
                f"operand2=0x{self.operand2:02X}, mode={self.mode}, extra=0x{self.extra:02X})")


def parse_register(reg_str):
    """
    Convierte una cadena como 'R1' a un valor entero.
    """
    reg_str = reg_str.strip().upper()
    if reg_str.startswith("R") and reg_str[1:].isdigit():
        return int(reg_str[1:])
    else:
        raise ValueError(f"Registro inválido: {reg_str}")


def detect_mode(operand_str):
    """
    Detecta el modo de direccionamiento basado en la cadena del operando.
    """
    operand_str = operand_str.strip()
    if operand_str.startswith("R"):
        return MODE_REGISTER
    elif operand_str.isdigit() or (operand_str.startswith("-") and operand_str[1:].isdigit()):
        return MODE_IMMEDIATE
    elif operand_str.startswith("[") and operand_str.endswith("]"):
        return MODE_DIRECT
    elif operand_str.startswith("*R"):
        return MODE_INDIRECT
    else:
        raise ValueError(f"Modo de direccionamiento no reconocido para operando: {operand_str}")


def parse_assembly_line(line):
    """
    Analiza una línea de código ensamblador y devuelve una instrucción.
    """
    line = line.strip()
    if not line or line.startswith(";"):
        return None  # comentario o línea vacía

    parts = re.split(r'[ ,]+', line.upper())
    opcode_str = parts[0]
    opcode = OPCODES.get(opcode_str)
    if opcode is None:
        raise ValueError(f"Opcode desconocido: {opcode_str}")

    operand1 = 0
    operand2 = 0
    mode = 0
    extra = 0

    # Validar cantidad de operandos y modos según instrucción
    allowed_modes = ALLOWED_MODES.get(opcode_str, [])

    if opcode_str in ["RET", "IRET", "HALT", "NOP"]:
        # Instrucciones sin operandos
        mode = 0
    elif opcode_str == "SHOW":
        # Solo un operando: registro
        if len(parts) < 2:
            raise ValueError("SHOW requiere un operando")
        operand1 = parse_register(parts[1])
        mode = MODE_REGISTER
    else:
        # Operandos habituales
        if len(parts) < 2:
            raise ValueError(f"{opcode_str} requiere al menos un operando")
        operand1 = parse_register(parts[1])

        if len(parts) >= 3:
            operand2_str = parts[2]
            mode = detect_mode(operand2_str)

            # Validar modo permitido
            if mode not in allowed_modes:
                raise ValueError(f"Modo {bin(mode)} no permitido para la instrucción {opcode_str}")

            if mode == MODE_REGISTER:
                operand2 = parse_register(operand2_str)
            elif mode == MODE_IMMEDIATE:
                operand2 = int(operand2_str)
            elif mode == MODE_DIRECT:
                # Extraer dirección sin corchetes
                operand2 = int(operand2_str[1:-1])
            elif mode == MODE_INDIRECT:
                # Asume sintaxis *R#
                operand2 = parse_register(operand2_str[2:])

        else:
            # Para instrucciones con un solo operando y modo permitido
            if allowed_modes:
                if allowed_modes[0] != MODE_REGISTER:
                    mode = allowed_modes[0]
                else:
                    mode = MODE_REGISTER

    # Validar modo también para instrucciones con un solo operando
    if opcode_str not in ["SHOW", "RET", "IRET", "HALT", "NOP"]:
        if mode not in allowed_modes:
            raise ValueError(f"Modo {bin(mode)} no permitido para la instrucción {opcode_str}")

    # Crear la instrucción final
    extension = (mode << 6) | extra
    raw = (opcode << 24) | (operand1 << 16) | (operand2 << 8) | extension

    return Instruction(raw)
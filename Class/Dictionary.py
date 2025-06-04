# Modos de direccionamiento
MODE_REGISTER = 0b00
MODE_IMMEDIATE = 0b01
MODE_DIRECT = 0b10
MODE_INDIRECT = 0b11

# Diccionario de opcodes
OPCODES = {
    "NOP": 0x00,
    "LOAD": 0x01,
    "STORE": 0x02,
    "LOADI": 0x03,
    "MOVE": 0x04,
    "ADD": 0x05,
    "SUB": 0x06,
    "MUL": 0x07,
    "DIV": 0x08,
    "AND": 0x09,
    "OR": 0x0A,
    "XOR": 0x0B,
    "NOT": 0x0C,
    "CMP": 0x0D,
    "JP": 0x0E,
    "JPZ": 0x0F,
    "JNZ": 0x10,
    "CALL": 0x11,
    "RET": 0x12,
    "INT": 0x13,
    "IRET": 0x14,
    "MOD": 0x15,
    "INC": 0x16,
    "DEC": 0x17,
    "IN": 0x18,
    "OUT": 0x19,
    "SHOW": 0x1A,
    "HALT": 0xFF
}

# Modos permitidos por instrucción
ALLOWED_MODES = {
    "LOAD": [MODE_DIRECT, MODE_INDIRECT],
    "STORE": [MODE_DIRECT, MODE_INDIRECT],
    "LOADI": [MODE_IMMEDIATE],
    "MOVE": [MODE_REGISTER],
    "ADD": [MODE_REGISTER],
    "SUB": [MODE_REGISTER],
    "MUL": [MODE_REGISTER],
    "DIV": [MODE_REGISTER],
    "AND": [MODE_REGISTER],
    "OR": [MODE_REGISTER],
    "XOR": [MODE_REGISTER],
    "NOT": [MODE_REGISTER],
    "CMP": [MODE_REGISTER],
    "JP": [MODE_DIRECT],
    "JPZ": [MODE_DIRECT],
    "JNZ": [MODE_DIRECT],
    "CALL": [MODE_IMMEDIATE, MODE_DIRECT],
    "RET": [],
    "INT": [MODE_IMMEDIATE, MODE_DIRECT],
    "IRET": [],
    "SHOW": [MODE_REGISTER],
    "HALT": [],
    "MOD": [MODE_REGISTER],
    "INC": [MODE_REGISTER],
    "DEC": [MODE_REGISTER],
    "IN": [MODE_REGISTER],
    "OUT": [MODE_REGISTER],
}

# Mapeo para que ALU reciba string con operación según opcode numérico
OPCODE_TO_ALU_OP = {
    OPCODES['ADD']: 'ADD',
    OPCODES['SUB']: 'SUB',
    OPCODES['MUL']: 'MUL',
    OPCODES['DIV']: 'DIV',
    OPCODES['AND']: 'AND',
    OPCODES['OR']: 'OR',
    OPCODES['NOT']: 'NOT',
    OPCODES['XOR']: 'XOR',
    OPCODES['MOD']: 'MOD',
    OPCODES['INC']: 'INC',
    OPCODES['DEC']: 'DEC',
    OPCODES['JP']: 'JP',
    OPCODES['JPZ']: 'JPZ',
    OPCODES['JNZ']: 'JNZ',
}

# Para cada instrucción, se valida si el modo es permitido y si el opcode está bien definido
def validate_instruction(opcode, operand1, operand2):
    if opcode not in OPCODES.values():
        raise ValueError(f"Opcode {opcode} no válido")
    
    # Validar modos permitidos
    if opcode in ALLOWED_MODES:
        allowed_modes = ALLOWED_MODES[opcode]
        # Aquí validar los modos de direccionamiento si es necesario
        if operand2 not in allowed_modes:
            raise ValueError(f"Modo no permitido para {opcode}: {operand2}")
    else:
        raise ValueError(f"No se definieron modos permitidos para {opcode}")
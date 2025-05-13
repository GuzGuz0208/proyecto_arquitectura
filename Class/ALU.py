# Clase ALU (Unidad Aritmético-Lógica)
# Responsabilidades:
# - Realiza operaciones aritméticas (suma, resta, multiplicación, división) en función del opcode recibido.
# - Almacena el resultado de la operación en su atributo `value`.
class ALU:
    def __init__(self):
        self.value = 0
        self.psw = {
            'Z': 0,  # Zero flag
            'C': 0,  # Carry flag
            'S': 0,  # Sign(+/-) flag
            'O': 0  # Overflow flag
        }

    # Método execute: Ejecuta una operación aritmética basada en el opcode y los operandos recibidos.
    # Parámetros:
    # - opcode: Código de operación que especifica qué operación realizar.
    # - operand1: Primer operando para la operación.
    # - operand2: Segundo operando para la operación.
    # - Almacena el resultado de la operación en el atributo `value`.
    def execute(self, opcode, operand1, operand2):
        if (operand1 > 0x3FFF or operand1 < -
           0x4000 or operand2 > 0x3FFF or operand2 < -0x4000):
            self.psw['O'] = 1
            raise ValueError('Operands out of range')
        else:
            if opcode == 'ADD':
                self.value = operand1 + operand2
                self.psw['C'] = int(self.value > 0x3FFF)
                self.psw['O'] = int(((operand1 & 0x2000) == (operand2 & 0x2000)) and (
                    (self.value & 0x2000) != (operand1 & 0x2000)))
            elif opcode == 'SUB':
                self.value = operand1 - operand2
                self.psw['C'] = int(operand1 < operand2)
                self.psw['O'] = int(((operand1 & 0x2000) != (operand2 & 0x2000)) and (
                    (self.value & 0x2000) != (operand1 & 0x2000)))
            elif opcode == 'MUL':
                self.value = operand1 * operand2
                self.psw['C'] = int(self.value > 0x3FFF)
            elif opcode == 'DIV':
                if operand2 == 0:
                    self.value = 0
                    self.psw['Z'] = 1
                else:
                    self.value = operand1 // operand2
            elif opcode == 'AND':
                self.value = operand1 & operand2
            elif opcode == 'OR':
                self.value = operand1 | operand2
            elif opcode == 'NOT':
                self.value = ~operand2
            elif opcode == 'XOR':
                self.value = operand1 ^ operand2
            elif opcode == 'JP':
                self.value = operand1
            elif opcode == 'JPZ':
                self.value = operand1 if operand2 == 0 else None

        # Actualiza los flags del PSW
        self.psw['Z'] = int(self.value == 0)
        self.psw['S'] = int(self.value < 0)

    def get_psw(self):
        return self.psw

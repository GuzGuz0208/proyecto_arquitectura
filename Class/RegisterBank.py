from Class.Register import Register

# Clase RegisterBank (Banco de Registros)
# Responsabilidades:
# - Organiza y gestiona registros en una matriz 3x3.
# - Cada registro tiene un nombre único y un tamaño apropiado.
class RegisterBank:
    def __init__(self, canvas, x, y):
        """
        Inicializa un banco de registros en forma de matriz 3x3 sin espacios entre ellos.
        
        :param canvas: Lienzo donde se dibujarán los registros.
        :param x: Coordenada X inicial.
        :param y: Coordenada Y inicial.
        """
        self.registers = {}
        rows, cols = 3, 3  # Configurar la matriz 3x3
        register_width = 100  # Ancho estándar para registros
        register_height = 30  # Altura estándar para registros

        for row in range(rows):
            for col in range(cols):
                reg_index = row * cols + col + 1  # Índice de registro (1 a 9)
                reg_name = f"R{reg_index}"  # Crear nombre del registro (R1 a R9)
                reg_x = x + col * register_width  # Posición X basada en la columna
                reg_y = y + row * register_height  # Posición Y basada en la fila

                # Crear y almacenar el registro en la posición calculada
                self.registers[reg_name] = Register(canvas, reg_x, reg_y, reg_name)

    def get(self, reg_name):
        """
        Obtiene el valor de un registro por su nombre.
        """
        if reg_name not in self.registers:
            raise KeyError(f"Register {reg_name} not found")
        return self.registers[reg_name].value

    def set(self, reg_name, value):
        """
        Establece el valor de un registro por su nombre.
        """
        if reg_name not in self.registers:
            raise KeyError(f"Register {reg_name} not found")
        self.registers[reg_name].set_value(value)

    def clear_registers(self):
        """
        Limpia todos los registros estableciendo su valor a 0.
        """
        for register in self.registers.values():
            register.set_value(0)

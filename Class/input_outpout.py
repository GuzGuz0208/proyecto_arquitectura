from Class.RegisterBank import RegisterBank
from Class.interfaz_memoria import InterfazMemoria

class InputOutput:
    def __init__(self, output_widget, register_bank, memory_interface):
        """
        Inicializa la clase InputOutput.
        :param output_widget: Widget de salida donde se mostrarán los resultados.
        :param register_bank: Instancia compartida del banco de registros.
        """
        self.output_widget = output_widget
        self.register_bank = register_bank
        self.memory_interface = memory_interface

    def process_instruction(self, instruction):
        """
        Procesa la instrucción después de encontrar 'SHOW' y realiza la acción correspondiente.
        :param instruction: Instrucción completa como cadena.
        """
        # Limpiar la instrucción y verificar si contiene 'SHOW'
        instruction = instruction.strip()
        if not instruction.upper().startswith("SHOW "):
            print("Instrucción inválida: No contiene 'SHOW'.")
            return

        # Extraer el argumento después de 'SHOW'
        argument = instruction[5:].strip()  # Obtén todo después de "SHOW "
        
        # Verificar si el argumento es un número entero
        if argument.isdigit():
            self._handle_number(int(argument))
        elif argument.startswith("R") and argument[1:].isdigit():  # Verificar formato R1, R2, etc.
            self._handle_register(argument)
        elif argument.startswith("[") and argument.endswith("]") and argument[1:-1].isdigit():
            self._handle_memory_address(int(argument[1:-1]))
        else:
            self._handle_invalid(argument)

    def _handle_number(self, number):
        """Maneja el caso donde el argumento es un número entero."""
        self._update_output(f"Cargando número: {number}", clear=True)

    def _handle_register(self, register):
        """Maneja el caso donde el argumento es un registro (R1, R2, etc.)."""
        if register in self.register_bank.registers:
            value = self.register_bank.get(register)
            self._update_output(f"Valor del registro {register}: {value}", clear=True)
        else:
            self._update_output(f"Registro {register} no encontrado.", clear=True)
            self._update_output(f"Registro {register} no encontrado.", clear=True)

    def _handle_memory_address(self, address):
        """Maneja el caso donde el argumento es una dirección de memoria ([1], [2], etc.)."""
        self._update_output(f"Cargando valor de la dirección de memoria: [{address}]", clear=True)
        try:
            # Cargar el valor de la dirección de memoria usando el método load_data
            valor = self.memory_interface.load_data(int(address))  # Asegúrate de convertir la dirección a entero

            print("ESTE ES EL VALOR", valor)
            if valor is not None:
                self._update_output(f"Valor en la dirección de memoria [{address}]: {valor}", clear=True)
            else:
                self._update_output(f"Dirección de memoria [{address}] inválida o vacía.", clear=True)
        except ValueError:
            self._update_output(f"Error: La dirección [{address}] no es válida.", clear=True)

    def _handle_invalid(self, argument):
        """Maneja el caso donde el argumento no cumple con ningún formato válido."""
        self._update_output(f"Formato inválido: {argument}", clear=True)
        

    def _update_output(self, message, clear=False):
        """
        Actualiza el contenido del campo de salida (OUTPUT) con el mensaje proporcionado.
        :param message: Mensaje a mostrar en el campo de salida.
        :param clear: Si es True, limpia el campo antes de insertar el nuevo mensaje.
        """
        self.output_widget.configure(state="normal")  # Habilitar edición en el widget de salida
        if clear:
            self.output_widget.delete("1.0", "end")  # Limpiar el contenido del OUTPUT
        self.output_widget.insert("end", message + "\n")  # Agregar el mensaje
        self.output_widget.configure(state="disabled")  # Deshabilitar edición


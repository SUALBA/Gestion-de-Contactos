import re
import os

class Contacto:
    """
    Representa un contacto con nombre, teléfono y correo electrónico.
    """
    def __init__(self, nombre: str, telefono: str, email: str):
        self.nombre = nombre.strip()
        self.telefono = telefono.strip()
        self.email = email.strip()

    def __str__(self):
        return f"Nombre: {self.nombre}, Teléfono: {self.telefono}, Email: {self.email}"

    def to_line(self) -> str:
        """
        Convierte el contacto a una línea de texto para almacenamiento.
        """
        return f"{self.nombre};{self.telefono};{self.email}\n"

    @staticmethod
    def from_line(line: str):
        """
        Crea un objeto Contacto a partir de una línea de texto.
        """
        partes = line.strip().split(';')
        if len(partes) != 3:
            raise ValueError("Línea de contacto con formato inválido")
        return Contacto(partes[0], partes[1], partes[2])

class GestionContactos:
    """
    Gestión de una lista de contactos con persistencia en archivo.
    """
    def __init__(self, archivo: str = 'contactos.txt'):
        self.archivo = archivo
        self.contactos = []
        self._cargar_contactos()

    def _cargar_contactos(self):
        """
        Carga los contactos desde el archivo de texto.
        """
        if not os.path.exists(self.archivo):
            return
        try:
            with open(self.archivo, 'r', encoding='utf-8') as f:
                for linea in f:
                    try:
                        contacto = Contacto.from_line(linea)
                        self.contactos.append(contacto)
                    except ValueError:
                        print(f"Advertencia: línea ignorada por formato inválido: {linea.strip()}")
        except IOError as e:
            print(f"Error al leer el archivo: {e}")

    def _guardar_contactos(self):
        """
        Guarda la lista de contactos en el archivo.
        """
        try:
            with open(self.archivo, 'w', encoding='utf-8') as f:
                for c in self.contactos:
                    f.write(c.to_line())
        except IOError as e:
            print(f"Error al escribir en el archivo: {e}")

    def agregar_contacto(self, nombre: str, telefono: str, email: str):
        """
        Agrega un nuevo contacto tras validar datos.
        """
        if not nombre or not telefono or not email:
            raise ValueError("Todos los campos son obligatorios")
        if not self._validar_email(email):
            raise ValueError("Formato de correo electrónico inválido")
        if any(c.nombre.lower() == nombre.lower() for c in self.contactos):
            raise ValueError("El contacto ya existe")
        nuevo = Contacto(nombre, telefono, email)
        self.contactos.append(nuevo)
        self._guardar_contactos()

    def mostrar_todos(self):
        """
        Muestra por pantalla todos los contactos.
        """
        if not self.contactos:
            print("No hay contactos en la lista.")
            return
        for c in self.contactos:
            print(c)

    def buscar_contacto(self, nombre: str) -> Contacto:
        """
        Busca un contacto por nombre (case-insensitive).
        """
        for c in self.contactos:
            if c.nombre.lower() == nombre.lower():
                return c
        raise LookupError("Contacto no encontrado")

    def eliminar_contacto(self, nombre: str):
        """
        Elimina un contacto de la lista.
        """
        for i, c in enumerate(self.contactos):
            if c.nombre.lower() == nombre.lower():
                del self.contactos[i]
                self._guardar_contactos()
                return
        raise LookupError("Contacto no encontrado")

    @staticmethod
    def _validar_email(email: str) -> bool:
        """
        Valida el formato del correo electrónico con regex.
        """
        patron = r'^[\w\.-]+@[\w\.-]+\.\w{2,}$'
        return re.match(patron, email) is not None


def menu():
    gestor = GestionContactos()
    opciones = {
        '1': 'Agregar contacto',
        '2': 'Mostrar todos',
        '3': 'Buscar contacto',
        '4': 'Eliminar contacto',
        '5': 'Salir'
    }
    while True:
        print("\n=== Menú de Gestión de Contactos ===")
        for clave, desc in opciones.items():
            print(f"{clave}. {desc}")
        eleccion = input("Seleccione una opción: ").strip()

        try:
            if eleccion == '1':
                nombre = input("Nombre: ")
                telefono = input("Teléfono: ")
                email = input("Email: ")
                gestor.agregar_contacto(nombre, telefono, email)
                print("Contacto agregado exitosamente.")

            elif eleccion == '2':
                print("\nLista de contactos:")
                gestor.mostrar_todos()

            elif eleccion == '3':
                nombre = input("Nombre a buscar: ")
                contacto = gestor.buscar_contacto(nombre)
                print("Contacto encontrado:")
                print(contacto)

            elif eleccion == '4':
                nombre = input("Nombre a eliminar: ")
                gestor.eliminar_contacto(nombre)
                print("Contacto eliminado exitosamente.")

            elif eleccion == '5':
                print("Saliendo del programa.")
                break

            else:
                print("Opción no válida. Intente de nuevo.")

        except ValueError as ve:
            print(f"Error: {ve}")
        except LookupError as le:
            print(f"Error: {le}")

if __name__ == '__main__':
    menu()

import re
import os

class Contacto:
    """
    Representa un contacto con nombre, teléfono y correo electrónico.
    """

    def __init__(self, nombre: str, telefono: str, email: str):
        # Almacena los atributos, eliminando espacios en los extremos
        self.nombre = nombre.strip()
        self.telefono = telefono.strip()
        self.email = email.strip()

    def __str__(self):
        # Define cómo se muestra un contacto por pantalla
        return f"Nombre: {self.nombre}, Teléfono: {self.telefono}, Email: {self.email}"

    def to_line(self) -> str:
        """
        Convierte el contacto en una línea de texto con formato:
        nombre;telefono;email\n
        para poder guardarlo en un archivo.
        """
        return f"{self.nombre};{self.telefono};{self.email}\n"

    @staticmethod
    def from_line(line: str):
        """
        Crea un objeto Contacto a partir de una línea del archivo.
        Separa la línea por ';' y espera exactamente 3 partes.
        """
        partes = line.strip().split(';')
        if len(partes) != 3:
            raise ValueError("Línea de contacto con formato inválido")
        return Contacto(partes[0], partes[1], partes[2])


class GestionContactos:
    """
    Gestiona una lista de contactos con persistencia en un archivo de texto.
    """

    def __init__(self, archivo: str = 'contactos.txt'):
        self.archivo = archivo
        self.contactos = []             # Lista interna de objetos Contacto
        self._cargar_contactos()        # Al iniciar, intenta cargar contactos previos

    def _cargar_contactos(self):
        """
        Lee todas las líneas del archivo (si existe) y crea un Contacto
        por cada línea válida. Ignora líneas mal formateadas.
        """
        if not os.path.exists(self.archivo):
            return  # Si no existe el archivo, no hace nada
        try:
            with open(self.archivo, 'r', encoding='utf-8') as f:
                for linea in f:
                    try:
                        contacto = Contacto.from_line(linea)
                        self.contactos.append(contacto)
                    except ValueError:
                        # Aviso si hay una línea con error de formato
                        print(f"Advertencia: línea ignorada por formato inválido: {linea.strip()}")
        except IOError as e:
            print(f"Error al leer el archivo: {e}")

    def _guardar_contactos(self):
        """
        Sobrescribe el archivo entero con la lista actual de contactos,
        usando el método to_line de cada uno.
        """
        try:
            with open(self.archivo, 'w', encoding='utf-8') as f:
                for c in self.contactos:
                    f.write(c.to_line())
        except IOError as e:
            print(f"Error al escribir en el archivo: {e}")

    def agregar_contacto(self, nombre: str, telefono: str, email: str):
        """
        Valida los datos y agrega un nuevo contacto a la lista.
        Luego guarda los cambios en el archivo.
        """
        # 1. Campos obligatorios
        if not nombre or not telefono or not email:
            raise ValueError("Todos los campos son obligatorios")
        # 2. Validación de formato de email
        if not self._validar_email(email):
            raise ValueError("Formato de correo electrónico inválido")
        # 3. Comprobar duplicado (case-insensitive)
        if any(c.nombre.lower() == nombre.lower() for c in self.contactos):
            raise ValueError("El contacto ya existe")
        # 4. Crear y añadir
        nuevo = Contacto(nombre, telefono, email)
        self.contactos.append(nuevo)
        # 5. Persistir en disco
        self._guardar_contactos()

    def mostrar_todos(self):
        """
        Muestra por pantalla todos los contactos. Si la lista está vacía,
        informa al usuario.
        """
        if not self.contactos:
            print("No hay contactos en la lista.")
            return
        for c in self.contactos:
            print(c)

    def buscar_contacto(self, nombre: str) -> Contacto:
        """
        Busca un contacto por nombre exacto (sin importar mayúsculas/minúsculas).
        Devuelve el objeto Contacto o lanza LookupError si no existe.
        """
        for c in self.contactos:
            if c.nombre.lower() == nombre.lower():
                return c
        raise LookupError("Contacto no encontrado")

    def eliminar_contacto(self, nombre: str):
        """
        Elimina de la lista el primer contacto cuyo nombre coincida
        (case-insensitive). Guarda los cambios o lanza LookupError si no existe.
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
        Comprueba mediante una expresión regular que el email
        tenga un formato básico válido: algo@algo.algo
        """
        patron = r'^[\w\.-]+@[\w\.-]+\.\w{2,}$'
        return re.match(patron, email) is not None


def menu():
    """
    Bucle principal de interacción: muestra un menú con opciones numeradas
    y llama a los métodos correspondientes de GestionContactos.
    Captura y muestra errores de validación o búsqueda.
    """
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
            print(f"Error: {ve}")    # Errores de validación de entrada
        except LookupError as le:
            print(f"Error: {le}")   # Errores de búsqueda o eliminación

if __name__ == '__main__':
    menu()

# registro_de_productos
tienda con python mysql xammp
Código
1. Importación de Bibliotecas
python
Copiar código
import flet as ft
import mysql.connector
from mysql.connector import Error
import pandas as pd
•	flet: Se utiliza para crear la interfaz gráfica de usuario (GUI). Permite la creación de aplicaciones interactivas con componentes como botones, entradas de texto, listas, etc.
•	mysql.connector: Se utiliza para conectar la aplicación con la base de datos MySQL. Permite ejecutar consultas SQL y gestionar la base de datos.
•	pandas: Se utiliza para exportar los datos de productos a un archivo Excel, facilitando la gestión e informes.
________________________________________
2. Clase Principal: ElectronicStoreApp
La clase principal ElectronicStoreApp contiene la lógica central de la aplicación. Gestiona la conexión a la base de datos, la interfaz de usuario, y las operaciones relacionadas con la tienda electrónica.
Constructor de la Clase
python
Copiar código
class ElectronicStoreApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.connection = None
        self.show_login()
•	El constructor inicializa la página de la aplicación (self.page) y establece una conexión a la base de datos (self.connection), además de mostrar la pantalla de inicio de sesión mediante self.show_login().
________________________________________
3. Método: connect_to_db
python
Copiar código
def connect_to_db(self):
    """Conecta a la base de datos MySQL."""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",  # Cambia según tu configuración
            password="",  # Cambia según tu configuración
            database="tienda_electronica"
        )
        if connection.is_connected():
            print("Conexión exitosa a MySQL.")
            return connection
    except Error as e:
        print(f"Error al conectar con MySQL: {e}")
        return None
•	Función: Este método establece una conexión a la base de datos MySQL.
•	Parámetros: No tiene parámetros de entrada.
•	Retorno: Devuelve un objeto de conexión si la conexión a la base de datos es exitosa. En caso de error, imprime el error y devuelve None.
________________________________________
4. Método: show_login
python
Copiar código
def show_login(self):
    """Muestra la pantalla de inicio de sesión."""
    self.page.add(
        ft.Column([
            ft.Text("Iniciar sesión"),
            ft.TextField(label="Nombre de usuario", autofocus=True),
            ft.TextField(label="Contraseña", password=True),
            ft.ElevatedButton("Iniciar sesión", on_click=self.login)
        ])
    )
•	Función: Este método genera la interfaz gráfica de la pantalla de inicio de sesión, donde el usuario puede ingresar su nombre de usuario y contraseña.
•	Parámetros: No tiene parámetros de entrada.
•	Acciones: Crea campos de texto para el nombre de usuario y contraseña, junto con un botón para iniciar sesión.
________________________________________
5. Método: login
python
Copiar código
def login(self, e):
    """Valida las credenciales del usuario."""
    username = self.username_field.value
    password = self.password_field.value
    if username == "admin" and password == "admin123":
        self.show_main_page()
    else:
        self.error_message.value = "Credenciales incorrectas."
        self.error_message.update()
•	Función: Este método se activa cuando el usuario hace clic en el botón de inicio de sesión. Verifica si las credenciales del usuario son correctas (en este caso, con valores fijos de "admin" y "admin123").
•	Parámetros: e es el evento generado por el clic del botón.
•	Acciones: Si las credenciales son correctas, se llama al método show_main_page() para mostrar la pantalla principal. Si las credenciales son incorrectas, se muestra un mensaje de error.
________________________________________
6. Método: show_main_page
python
Copiar código
def show_main_page(self):
    """Muestra la pantalla principal de la aplicación."""
    self.page.add(
        ft.Column([
            ft.Text("Bienvenido a la Tienda Electrónica"),
            ft.ElevatedButton("Gestionar Productos", on_click=self.show_manage_products),
            ft.ElevatedButton("Gestionar Usuarios", on_click=self.show_manage_users),
            ft.ElevatedButton("Exportar a Excel", on_click=self.export_products_to_excel)
        ])
    )
•	Función: Este método genera la interfaz gráfica de la pantalla principal después de que el usuario ha iniciado sesión correctamente. Incluye botones para gestionar productos, gestionar usuarios y exportar los productos a Excel.
•	Parámetros: No tiene parámetros de entrada.
•	Acciones: Añade botones para las funcionalidades principales y asocia eventos a cada botón.
________________________________________
7. Método: show_manage_products
python
Copiar código
def show_manage_products(self, e):
    """Muestra la pantalla de gestión de productos."""
    self.page.add(
        ft.Column([
            ft.Text("Gestión de Productos"),
            ft.TextField(label="Nombre del Producto"),
            ft.TextField(label="Precio"),
            ft.Dropdown(label="Categoría", options=["Computadora", "Celular", "Consola", "Accesorio"]),
            ft.ElevatedButton("Agregar Producto", on_click=self.add_product),
            ft.ElevatedButton("Volver", on_click=self.show_main_page)
        ])
    )
•	Función: Este método genera la interfaz gráfica para gestionar los productos (agregar productos, editar, etc.).
•	Parámetros: e es el evento generado por el clic del botón.
•	Acciones: Se agregan campos para ingresar el nombre del producto, precio y categoría. También se añaden botones para agregar el producto y para volver a la pantalla principal.
________________________________________
8. Método: add_product
python
Copiar código
def add_product(self, e):
    """Agrega un producto a la base de datos."""
    categoria = category_dropdown.value
    nombre = product_name.value
    precio = product_price.value

    if not categoria or not nombre or not precio.isdigit():
        self.error_message.value = "Por favor, completa todos los campos correctamente."
        self.error_message.update()
        return

    try:
        cursor = self.connection.cursor()
        cursor.execute(
            "INSERT INTO productos (categoria, nombre, precio) VALUES (%s, %s, %s)",
            (categoria, nombre, float(precio))
        )
        self.connection.commit()
        self.success_message.value = f"Producto '{nombre}' agregado correctamente."
        self.success_message.update()
    except Error as e:
        self.error_message.value = f"Error al agregar producto: {e}"
        self.error_message.update()
•	Función: Este método se encarga de agregar un nuevo producto a la base de datos.
•	Parámetros: e es el evento generado por el clic del botón.
•	Acciones: Valida que todos los campos estén completos y que el precio sea un número. Luego, inserta el producto en la base de datos mediante una consulta SQL.
________________________________________
9. Método: export_products_to_excel
python
Copiar código
def export_products_to_excel(self):
    """Exporta los productos a un archivo Excel."""
    try:
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM productos")
        rows = cursor.fetchall()

        if rows:
            df = pd.DataFrame(rows)
            df.to_excel("productos_tienda.xlsx", index=False)
            self.success_message.value = "Productos exportados a 'productos_tienda.xlsx'."
            self.success_message.update()
        else:
            self.error_message.value = "No hay productos para exportar."
            self.error_message.update()
    except Error as e:
        self.error_message.value = f"Error al exportar productos: {e}"
        self.error_message.update()
•	Función: Este método exporta todos los productos de la base de datos a un archivo Excel.
•	Parámetros: No tiene parámetros de entrada.
•	Acciones: Obtiene todos los productos desde la base de datos y los exporta a un archivo .xlsx utilizando Pandas.



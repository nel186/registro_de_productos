import flet as ft
import mysql.connector
import pandas as pd
from mysql.connector import Error


class ElectronicStoreApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "Tienda Electrónica Avanzada con MySQL"
        self.page.window_width = 800
        self.page.window_height = 600

        # Conexión a la base de datos
        self.connection = self.connect_to_db()
        
        self.page.bgcolor = ft.colors.GREY

        # Mensajes globales
        self.error_message = ft.Text("", color=ft.colors.RED)
        self.success_message = ft.Text("", color=ft.colors.GREEN)
        

        # Inicia con la pantalla de inicio de sesión
        self.show_login()

    def connect_to_db(self):
        """Conecta a la base de datos MySQL."""
        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="tienda_electronica"
            )
            if connection.is_connected():
                print("Conexión exitosa a MySQL.")
                return connection
        except Error as e:
            print(f"Error al conectar con MySQL: {e}")
            return None

    def show_login(self):
        """Pantalla de inicio de sesión."""
        self.page.controls.clear()

        username_input = ft.TextField(label="Usuario", width=300)
        password_input = ft.TextField(label="Contraseña", width=300, password=True)

        def verify_login(e):
            username = username_input.value
            password = password_input.value

            if self.validate_user(username, password):
                self.show_home()
            else:
                self.error_message.value = "Usuario o contraseña incorrectos."
                self.error_message.update()

        login_button = ft.ElevatedButton("Iniciar Sesión", on_click=verify_login)
        login_controls = ft.Column(
            controls=[
                ft.Text("Inicio de Sesión", size=30, weight=ft.FontWeight.BOLD),
                username_input,
                password_input,
                login_button,
                self.error_message
            ],
            alignment=ft.MainAxisAlignment.CENTER
        )

        self.page.add(
            ft.Row(
                controls=[login_controls],
                alignment=ft.MainAxisAlignment.CENTER
            )
        )
        self.page.update()

    def validate_user(self, username, password):
        """Valida las credenciales de un usuario."""
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM usuarios WHERE username=%s AND password=%s", (username, password))
            user = cursor.fetchone()
            return user is not None
        except Error as e:
            print(f"Error al validar usuario: {e}")
            return False

    def show_home(self):
        """Pantalla principal con opciones."""
        self.page.controls.clear()

        def go_to_products(e):
            self.show_products()

        def go_to_users(e):
            self.show_users()

        def export_to_excel(e):
            self.export_products_to_excel()

        def logout(e):
            self.show_login()

        home_controls = ft.Column(
            controls=[
                ft.Text("Bienvenido a la Tienda Electrónica", size=28, weight=ft.FontWeight.BOLD),
                ft.Text("Elige una opción:", size=20),
                ft.Row([
                    ft.ElevatedButton("Productos", on_click=go_to_products),
                    ft.ElevatedButton("Usuarios", on_click=go_to_users),
                    ft.ElevatedButton("Exportar Productos a Excel", on_click=export_to_excel)
                ], alignment=ft.MainAxisAlignment.CENTER),
                ft.ElevatedButton("Cerrar Sesión", on_click=logout)
            ],
            alignment=ft.MainAxisAlignment.CENTER
        )

        self.page.add(
            ft.Row(
                controls=[home_controls],
                alignment=ft.MainAxisAlignment.CENTER
            )
        )
        self.page.update()

    def show_products(self):
        """Pantalla de productos."""
        self.page.controls.clear()

        def go_back(e):
            self.show_home()

        def logout(e):
            self.show_login()

        def load_products():
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM productos")
            return cursor.fetchall()

        def delete_product(product_id):
            cursor = self.connection.cursor()
            cursor.execute("DELETE FROM productos WHERE id=%s", (product_id,))
            self.connection.commit()
            self.show_products()

        def edit_product(product):
            self.show_edit_product(product)

        def add_new_product(e):
            self.show_add_product()

        products = load_products()
        product_list = ft.Column(
            controls=[
                ft.Row([
                    ft.Text(f"{product['nombre']} - ${product['precio']} - {product['categoria']}"),
                    ft.ElevatedButton("Editar", on_click=lambda e, p=product: edit_product(p)),
                    ft.ElevatedButton("Eliminar", on_click=lambda e, pid=product['id']: delete_product(pid))
                ])
                for product in products
            ],
            alignment=ft.MainAxisAlignment.CENTER
        )

        self.page.add(
            ft.Row(
                controls=[product_list],
                alignment=ft.MainAxisAlignment.CENTER
            ),
            ft.ElevatedButton("Agregar Producto", on_click=add_new_product),
            ft.Row([
                ft.ElevatedButton("Volver", on_click=go_back),
                ft.ElevatedButton("Cerrar Sesión", on_click=logout)
            ], alignment=ft.MainAxisAlignment.CENTER)
        )
        self.page.update()

    def show_add_product(self):
        """Pantalla para agregar productos."""
        self.page.controls.clear()

        category_dropdown = ft.Dropdown(
            label="Categoría",
            options=[
                ft.dropdown.Option("Computadoras"),
                ft.dropdown.Option("Celulares"),
                ft.dropdown.Option("Consolas (PS4, PS5)")
            ],
            width=300
        )
        product_name = ft.TextField(label="Nombre del Producto", width=300)
        product_price = ft.TextField(label="Precio (USD)", width=300)

        def save_product(e):
            categoria = category_dropdown.value
            nombre = product_name.value
            precio = product_price.value

            if not categoria or not nombre or not precio.isdigit():
                self.error_message.value = "Por favor, completa todos los campos correctamente."
                self.error_message.update()
                return

            cursor = self.connection.cursor()
            cursor.execute(
                "INSERT INTO productos (categoria, nombre, precio) VALUES (%s, %s, %s)",
                (categoria, nombre, float(precio))
            )
            self.connection.commit()
            self.success_message.value = f"Producto '{nombre}' agregado correctamente."
            self.success_message.update()
            self.show_products()

        def go_back(e):
            self.show_products()

        add_product_controls = ft.Column(
            controls=[
                ft.Text("Agregar Producto", size=24, weight=ft.FontWeight.BOLD),
                category_dropdown,
                product_name,
                product_price,
                ft.ElevatedButton("Guardar Producto", on_click=save_product),
                ft.ElevatedButton("Cancelar", on_click=go_back)
            ],
            alignment=ft.MainAxisAlignment.CENTER
        )

        self.page.add(
            ft.Row(
                controls=[add_product_controls],
                alignment=ft.MainAxisAlignment.CENTER
            )
        )
        self.page.update()

    def show_edit_product(self, product):
        """Pantalla para editar un producto."""
        self.page.controls.clear()

        category_dropdown = ft.Dropdown(
            label="Categoría",
            value=product['categoria'],
            options=[
                ft.dropdown.Option("Computadoras"),
                ft.dropdown.Option("Celulares"),
                ft.dropdown.Option("Consolas (PS4, PS5)")
            ],
            width=300
        )
        product_name = ft.TextField(label="Nombre del Producto", value=product['nombre'], width=300)
        product_price = ft.TextField(label="Precio (USD)", value=str(product['precio']), width=300)

        def save_edited_product(e):
            categoria = category_dropdown.value
            nombre = product_name.value
            precio = product_price.value

            if not categoria or not nombre or not precio.isdigit():
                self.error_message.value = "Por favor, completa todos los campos correctamente."
                self.error_message.update()
                return

            cursor = self.connection.cursor()
            cursor.execute(
                "UPDATE productos SET categoria=%s, nombre=%s, precio=%s WHERE id=%s",
                (categoria, nombre, float(precio), product['id'])
            )
            self.connection.commit()
            self.success_message.value = f"Producto '{nombre}' actualizado correctamente."
            self.success_message.update()
            self.show_products()

        def go_back(e):
            self.show_products()

        edit_product_controls = ft.Column(
            controls=[
                ft.Text("Editar Producto", size=24, weight=ft.FontWeight.BOLD),
                category_dropdown,
                product_name,
                product_price,
                ft.ElevatedButton("Guardar Cambios", on_click=save_edited_product),
                ft.ElevatedButton("Cancelar", on_click=go_back)
            ],
            alignment=ft.MainAxisAlignment.CENTER
        )

        self.page.add(
            ft.Row(
                controls=[edit_product_controls],
                alignment=ft.MainAxisAlignment.CENTER
            )
        )
        self.page.update()

    def show_users(self):
        """Pantalla de usuarios."""
        self.page.controls.clear()

        def go_back(e):
            self.show_home()

        def logout(e):
            self.show_login()

        def load_users():
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM usuarios")
            return cursor.fetchall()

        def delete_user(user_id):
            cursor = self.connection.cursor()
            cursor.execute("DELETE FROM usuarios WHERE id=%s", (user_id,))
            self.connection.commit()
            self.show_users()

        def add_new_user(e):
            self.show_add_user()

        users = load_users()
        user_list = ft.Column(
            controls=[
                ft.Row([
                    ft.Text(f"{user['username']} - {user['edad']}"),
                    ft.ElevatedButton("Eliminar", on_click=lambda e, uid=user['id']: delete_user(uid))
                ])
                for user in users
            ],
            alignment=ft.MainAxisAlignment.CENTER
        )

        self.page.add(
            ft.Row(
                controls=[user_list],
                alignment=ft.MainAxisAlignment.CENTER
            ),
            ft.ElevatedButton("Agregar Usuario", on_click=add_new_user),
            ft.Row([
                ft.ElevatedButton("Volver", on_click=go_back),
                ft.ElevatedButton("Cerrar Sesión", on_click=logout)
            ], alignment=ft.MainAxisAlignment.CENTER)
        )
        self.page.update()

    def show_add_user(self):
        """Pantalla para agregar usuarios."""
        self.page.controls.clear()

        username_input = ft.TextField(label="Nombre de Usuario", width=300)
        edad_input = ft.TextField(label="Edad", width=300)
        password_input = ft.TextField(label="Contraseña", width=300, password=True)

        def save_user(e):
            username = username_input.value
            edad = edad_input.value
            password = password_input.value

            if not username or not edad or not password:
                self.error_message.value = "Por favor, completa todos los campos."
                self.error_message.update()
                return

            cursor = self.connection.cursor()
            cursor.execute(
                "INSERT INTO usuarios (username, edad, password) VALUES (%s, %s, %s)",
                (username, int(edad), password)
            )
            self.connection.commit()
            self.success_message.value = f"Usuario '{username}' agregado correctamente."
            self.success_message.update()
            self.show_users()

        def go_back(e):
            self.show_users()

        add_user_controls = ft.Column(
            controls=[
                ft.Text("Agregar Usuario", size=24, weight=ft.FontWeight.BOLD),
                username_input,
                edad_input,
                password_input,
                ft.ElevatedButton("Guardar Usuario", on_click=save_user),
                ft.ElevatedButton("Cancelar", on_click=go_back)
            ],
            alignment=ft.MainAxisAlignment.CENTER
        )

        self.page.add(
            ft.Row(
                controls=[add_user_controls],
                alignment=ft.MainAxisAlignment.CENTER
            )
        )
        self.page.update()

    def export_products_to_excel(self):
        """Exporta los productos a un archivo Excel."""
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM productos")
            data = cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]

            df = pd.DataFrame(data, columns=column_names)
            df.to_excel("productos.xlsx", index=False)
            self.success_message.value = "Archivo 'productos.xlsx' generado correctamente."
            self.success_message.update()
        except Error as e:
            self.error_message.value = f"Error al exportar a Excel: {e}"
            self.error_message.update()


def main(page: ft.Page):
    app = ElectronicStoreApp(page)


ft.app(target=main)

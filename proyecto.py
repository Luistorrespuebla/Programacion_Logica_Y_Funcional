from conexion import ConexionDB
from login import Login
import json
from datetime import datetime

class sistemaTienda:
    def __init__(self):
        self.__conexion_db = ConexionDB()

    def __respaldo_json(self):
        cursor = self.__conexion_db.conectar()
        if cursor:
            try:
                cursor.execute("SELECT * FROM t_productos")
                productos = cursor.fetchall()
                lista = []
                for p in productos:
                    lista.append({"id": p[0], "producto": p[1], "precio": p[2], "cantidad": p[3]})

                archivo = f"respaldo_productos_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
                with open(archivo, "w", encoding="utf-8") as f:
                    json.dump(lista, f, indent=4, ensure_ascii=False)

                print(f" Respaldo creado: {archivo}")
            except Exception as e:
                print(f"❌ Error al respaldar: {e}")
            finally:
                self.__conexion_db.desconectar(cursor)

    def __restaurar_respaldo(self):
        confirmacion = input(" Esta acción eliminará todos los productos actuales. Deseas continuar? (s/n): ").lower()
        if confirmacion != "s":
            print("❌ Operación cancelada.")
            return

        ruta = input(" Ingresa el nombre del archivo de respaldo (ej. respaldo_productos_20250522_152045.txt): ")
        try:
            with open(ruta, "r", encoding="utf-8") as f:
                productos = json.load(f)
        except Exception as e:
            print(f"❌ Error al leer el archivo: {e}")
            return

        cursor = self.__conexion_db.conectar()
        if cursor:
            try:
                cursor.execute("DELETE FROM t_productos")
                self.__conexion_db.get_conexion().commit()

                for prod in productos:
                    cursor.execute(
                        "INSERT INTO t_productos (producto, precio, cantidad) VALUES (%s, %s, %s)",
                        (prod["producto"], prod["precio"], prod["cantidad"])
                    )
                self.__conexion_db.get_conexion().commit()
                print(" Respaldo restaurado correctamente.")
            except Exception as e:
                print(f"❌ Error al restaurar respaldo: {e}")
            finally:
                self.__conexion_db.desconectar(cursor)

    def __mostrar_productos(self):
        cursor = self.__conexion_db.conectar()
        if cursor:
            try:
                cursor.execute("SELECT * FROM t_productos")
                productos = cursor.fetchall()
                print("\n Lista de productos:")
                for p in productos:
                    print(f"ID: {p[0]}, Producto: {p[1]}, Precio: {p[2]}, Cantidad: {p[3]}")
            except Exception as e:
                print(f"❌ Error al mostrar productos: {e}")
            finally:
                self.__conexion_db.desconectar(cursor)

    def __agregar_producto(self):
        nombre = input("Nombre del producto: ")
        precio = float(input("Precio: "))
        cantidad = int(input("Cantidad: "))
        cursor = self.__conexion_db.conectar()
        if cursor:
            try:
                cursor.execute("INSERT INTO t_productos(producto, precio, cantidad) VALUES (%s, %s, %s)",
                               (nombre, precio, cantidad))
                self.__conexion_db.get_conexion().commit()
                print(" Producto agregado.")
            except Exception as e:
                print(f"❌ Error al agregar producto: {e}")
            finally:
                self.__conexion_db.desconectar(cursor)

    def __editar_producto(self):
        id_producto = int(input("ID del producto a editar: "))
        nombre = input("Preciona un enter si no deseas realizar ninguna modificación: ")
        precio = input("Preciona un enter si no deseas realizar ninguna modificación: ")
        cantidad = input("Preciona un enter si no deseas realizar ninguna modificación: ")

        updates = []
        valores = []

        if nombre:
            updates.append("producto = %s")
            valores.append(nombre)
        if precio:
            updates.append("precio = %s")
            valores.append(float(precio))
        if cantidad:
            updates.append("cantidad = %s")
            valores.append(int(cantidad))

        if not updates:
            print("⚠️ No hay cambios.")
            return

        valores.append(id_producto)
        cursor = self.__conexion_db.conectar()
        if cursor:
            try:
                sql = f"UPDATE t_productos SET {', '.join(updates)} WHERE id_producto = %s"
                cursor.execute(sql, valores)
                self.__conexion_db.get_conexion().commit()
                print(" Producto actualizado.")
            except Exception as e:
                print(f"❌ Error al actualizar producto: {e}")
            finally:
                self.__conexion_db.desconectar(cursor)

    def __eliminar_producto(self):
        id_producto = int(input("ID del producto a eliminar: "))
        cursor = self.__conexion_db.conectar()
        if cursor:
            try:
                cursor.execute("DELETE FROM t_productos WHERE id_producto = %s", (id_producto,))
                self.__conexion_db.get_conexion().commit()
                print("❌ Producto eliminado.")
            except Exception as e:
                print(f"❌ Error al eliminar producto: {e}")
            finally:
                self.__conexion_db.desconectar(cursor)

    def menu(self, rol):
        while True:
            print("\n====== Menú de opciones para la t_productos ======")
            print("1. Mostrar productos")
            if rol == "administrador":
                print("2. Agregar producto")
                print("3. Editar producto")
                print("4. Eliminar producto")
                print("5. Crear respaldo")
                print("6. Restaurar respaldo")
            print("0. Cerrar sesión")
            op = input("Opción: ")

            if op == "1":
                self.__mostrar_productos()
            elif op == "2" and rol == "administrador":
                self.__agregar_producto()
            elif op == "3" and rol == "administrador":
                self.__editar_producto()
            elif op == "4" and rol == "administrador":
                self.__eliminar_producto()
            elif op == "5" and rol == "administrador":
                self.__respaldo_json()
            elif op == "6" and rol == "administrador":
                self.__restaurar_respaldo()
            elif op == "0":
                print(" Sesión cerrada.")
                break
            else:
                print("❌ Opción inválida.")

def main():
    login = Login()
    gestor = sistemaTienda()

    while True:
        print("\n====== Menu de login ======")
        print("1. Iniciar sesión")
        print("2. Registrar usuario")
        print("3. Finalizar sesión")
        opcion = input("Ingresa una opción: ")

        if opcion == "1":
            email = input("Correo electrónico: ")
            password = input("Contraseña: ")
            if login.login(email, password):
                gestor.menu(login.rol)
        elif opcion == "2":
            nombre = input("Nombre: ")
            rol = input("Rol (administrador/cliente): ").lower()
            email = input("Email: ")
            password = input("Contraseña: ")
            login.registrar(nombre, rol, email, password)
        elif opcion == "3":
            print(" Adiós.")
            break
        else:
            print("❌ Opción no válida.")

if __name__ == "__main__":
    main()

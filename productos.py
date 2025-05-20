import mysql.connector as db

class controladorDB:
    def __init__(self, config):
        self.config = config
        self.conexion = None

    def conectar(self):
        try:
            self.conexion = db.connect(**self.config)
            return self.conexion.cursor()
        except Exception as error:
            print(f"Error al conectar a la base de datos: {error}")
            return None

    def desconectar(self, cursor=None):
        if cursor:
            cursor.close()
        if self.conexion and self.conexion.is_connected():
            self.conexion.close()
            print("Conexión finalizada")

    def mostrar_productos(self):
        cursor = self.conectar()
        if cursor:
            try:
                cursor.execute("SELECT * FROM t_productos")
                productos = cursor.fetchall()
                if productos:
                    print("Lista de productos:")
                    for producto in productos:
                        print(f"ID: {producto[0]}, Nombre: {producto[1]}, Precio: {producto[2]}, Cantidad: {producto[3]}")
                else:
                    print("No hay productos en la base de datos.")
            except Exception as error:
                if self.conexion:
                    self.conexion.rollback()
                print(f"Error al mostrar productos: {error}")
            finally:
                self.desconectar(cursor)

    def agregar_producto(self, producto, precio, cantidad):
        cursor = self.conectar()
        if cursor:
            try:
                sql = "INSERT INTO t_productos(producto, precio, cantidad) VALUES (%s, %s, %s)"
                valores = (producto, precio, cantidad)
                cursor.execute(sql, valores)
                self.conexion.commit()
                print(f"Producto {producto} agregado correctamente.")
            except Exception as error:
                if self.conexion:
                    self.conexion.rollback()
                print(f"Error al agregar producto: {error}")
            finally:
                self.desconectar(cursor)

    def actualizar_producto(self, id_producto, producto=None, precio=None, cantidad=None):
        cursor = self.conectar()
        if cursor:
            try:
                updates = []
                valores = []
                if producto:
                    updates.append("producto = %s")
                    valores.append(producto)
                if precio:
                    updates.append("precio = %s")
                    valores.append(precio)
                if cantidad:
                    updates.append("cantidad = %s")
                    valores.append(cantidad)

                if not updates:
                    print("No hay datos para actualizar.")
                    self.desconectar(cursor)
                    return

                sql = f"UPDATE t_productos SET {', '.join(updates)} WHERE id_producto = %s"
                valores.append(id_producto)
                cursor.execute(sql, valores)
                self.conexion.commit()
                if cursor.rowcount > 0:
                    print(f"Producto con ID {id_producto} actualizado correctamente.")
                else:
                    print(f"No se encontró producto con ID {id_producto}.")
            except Exception as error:
                if self.conexion:
                    self.conexion.rollback()
                print(f"Error al actualizar producto: {error}")
            finally:
                self.desconectar(cursor)

    def eliminar_producto(self, id_producto):
        cursor = self.conectar()
        if cursor:
            try:
                sql = "DELETE FROM t_productos WHERE id_producto = %s"
                cursor.execute(sql, (id_producto,))
                self.conexion.commit()
                if cursor.rowcount > 0:
                    print(f"Producto con ID {id_producto} eliminado correctamente.")
                else:
                    print(f"No se encontró producto con ID {id_producto}.")
            except Exception as error:
                if self.conexion:
                    self.conexion.rollback()
                print(f"Error al eliminar producto: {error}")
            finally:
                self.desconectar(cursor)

config = {
    "host": "localhost",
    "user": "root",
    "port": "3306",
    "password": "",
    "database": "tienda",
    "raise_on_warnings": True
}

aplicacionFunc = controladorDB(config)

def main():
    print(" Mostrar todos los productos ")
    aplicacionFunc.mostrar_productos()

    print("\n Agregar un nuevo producto ")
    aplicacionFunc.agregar_producto("wiskas", 700, 500)
    aplicacionFunc.mostrar_productos()

    print("\n Actualizar un producto ")
    aplicacionFunc.actualizar_producto(11, producto="Laurita")
    aplicacionFunc.mostrar_productos()

    print("\n Eliminar un producto ")
    aplicacionFunc.eliminar_producto(11)
    aplicacionFunc.mostrar_productos()


if __name__ == "__main__":
    main()
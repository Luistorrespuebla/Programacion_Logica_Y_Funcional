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

    def mostrar_usuarios(self):
        cursor = self.conectar()
        if cursor:
            try:
                cursor.execute("SELECT * FROM t_usuarios")
                usuarios = cursor.fetchall()
                if usuarios:
                    print("Lista de usuarios:")
                    for usuario in usuarios:
                        print(f"ID: {usuario[0]}, Nombre: {usuario[1]}, Apellido: {usuario[2]}, Email: {usuario[3]}, Pass: {usuario[4]}")
                else:
                    print("No hay usuarios en la base de datos.")
            except Exception as error:
                if self.conexion:
                    self.conexion.rollback()
                print(f"Error al mostrar usuarios: {error}")
            finally:
                self.desconectar(cursor)

    def agregar_usuario(self, nombre, apellido, email, password):
        cursor = self.conectar()
        if cursor:
            try:
                sql = "INSERT INTO t_usuarios(nombre, apellido, email, pass) VALUES (%s, %s, %s, %s)"
                valores = (nombre, apellido, email, password)
                cursor.execute(sql, valores)
                self.conexion.commit()
                print(f"Usuario {nombre} {apellido} agregado correctamente.")
            except Exception as error:
                if self.conexion:
                    self.conexion.rollback()
                print(f"Error al agregar usuario: {error}")
            finally:
                self.desconectar(cursor)

    def actualizar_usuario(self, id_usuario, nombre=None, apellido=None, email=None, password=None):
        cursor = self.conectar()
        if cursor:
            try:
                updates = []
                valores = []
                if nombre:
                    updates.append("nombre = %s")
                    valores.append(nombre)
                if apellido:
                    updates.append("apellido = %s")
                    valores.append(apellido)
                if email:
                    updates.append("email = %s")
                    valores.append(email)
                if password:
                    updates.append("pass = %s")
                    valores.append(password)

                if not updates:
                    print("No hay datos para actualizar.")
                    self.desconectar(cursor)
                    return

                sql = f"UPDATE t_usuarios SET {', '.join(updates)} WHERE id_usuario = %s"
                valores.append(id_usuario)
                cursor.execute(sql, valores)
                self.conexion.commit()
                if cursor.rowcount > 0:
                    print(f"Usuario con ID {id_usuario} actualizado correctamente.")
                else:
                    print(f"No se encontró usuario con ID {id_usuario}.")
            except Exception as error:
                if self.conexion:
                    self.conexion.rollback()
                print(f"Error al actualizar usuario: {error}")
            finally:
                self.desconectar(cursor)

    def eliminar_usuario(self, id_usuario):
        cursor = self.conectar()
        if cursor:
            try:
                sql = "DELETE FROM t_usuarios WHERE id_usuario = %s"
                cursor.execute(sql, (id_usuario,))
                self.conexion.commit()
                if cursor.rowcount > 0:
                    print(f"Usuario con ID {id_usuario} eliminado correctamente.")
                else:
                    print(f"No se encontró usuario con ID {id_usuario}.")
            except Exception as error:
                if self.conexion:
                    self.conexion.rollback()
                print(f"Error al eliminar usuario: {error}")
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
    print(" Mostrar todos los usuarios ")
    aplicacionFunc.mostrar_usuarios()

    print("\n Agregar un nuevo usuario ")
    aplicacionFunc.agregar_usuario("Elena2", "Pérez", "elena@example.com", "secreto456")

    print("\n Actualizar un usuario ")
    aplicacionFunc.actualizar_usuario(32, nombre="Luis Angel")

    print("\n Eliminar un usuario ")
    aplicacionFunc.eliminar_usuario(34)


if __name__ == "__main__":
    main()
from conexion import ConexionDB

class Login:
    def __init__(self):
        self.__conexion_db = ConexionDB()
        self.usuario = None
        self.rol = None

    def __validar_credenciales(self, email, password):
        cursor = self.__conexion_db.conectar()
        if cursor:
            try:
                cursor.execute("SELECT id_usuario, nombre, rol FROM t_usuarios WHERE email = %s AND pass = %s", (email, password))
                return cursor.fetchone()
            except Exception as e:
                print(f"❌ Error al iniciar sesión: {e}")
            finally:
                self.__conexion_db.desconectar(cursor)
        return None

    def login(self, email, password):
        datos = self.__validar_credenciales(email, password)
        if datos:
            self.usuario = datos[1]
            self.rol = datos[2]
            print(f"\n✅ Bienvenido (rol: {self.rol}) {self.usuario} \n")
            return True
        else:
            print("❌ Credenciales incorrectas.")
            return False

    def registrar(self, nombre, rol, email, password):
        cursor = self.__conexion_db.conectar()
        if cursor:
            try:
                cursor.execute("INSERT INTO t_usuarios (nombre, rol, email, pass) VALUES (%s, %s, %s, %s)",
                               (nombre, rol.lower(), email, password))
                self.__conexion_db.get_conexion().commit()
                print("✅ Usuario registrado exitosamente.")
            except Exception as e:
                print(f"❌ Error al registrar: {e}")
            finally:
                self.__conexion_db.desconectar(cursor)

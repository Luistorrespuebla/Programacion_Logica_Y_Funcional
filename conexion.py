import mysql.connector as db

class ConexionDB:
    def __init__(self):
        self.__config = {
            "host": "localhost",
            "user": "root",
            "port": "3306",
            "password": "",
            "database": "tienda",
            "raise_on_warnings": True
        }
        self.__conexion = None

    def conectar(self):
        try:
            self.__conexion = db.connect(**self.__config)
            return self.__conexion.cursor()
        except Exception as e:
            print(f"❌ Error de conexión: {e}")
            return None

    def desconectar(self, cursor=None):
        if cursor:
            cursor.close()
        if self.__conexion and self.__conexion.is_connected():
            self.__conexion.close()
            print("🔌 Conexión cerrada correctamente.")

    def get_conexion(self):
        return self.__conexion

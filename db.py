import os
from dotenv import load_dotenv
import psycopg2
from psycopg2 import pool, extras

# Cargar variables de entorno desde .env
load_dotenv()

class Database:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        
        self.config = {
            "host": os.getenv("DB_HOST"),
            "database": os.getenv("DB_NAME"),
            "user": os.getenv("DB_USER"),
            "password": os.getenv("DB_PASSWORD"),
            "port": os.getenv("DB_PORT", "5432"),
            "sslmode": os.getenv("DB_SSLMODE", "require")
        }
        
        self.connection_pool = None
        self._initialized = True
    
    def check_connection(self):
        """
        Verifica conexión a la base de datos.
        Retorna: (bool, str) - (éxito, mensaje)
        """
        conn = None
        try:
            conn = psycopg2.connect(**self.config)
            cursor = conn.cursor()
            cursor.execute("SELECT 1;")
            cursor.close()
            conn.close()
            return True, "Conexion establecida correctamente"
            
        except psycopg2.OperationalError as e:
            error_msg = f"Error de conexion a la base de datos: {e}"
            return False, error_msg
        except Exception as e:
            error_msg = f"Error inesperado: {e}"
            return False, error_msg
    
    # === MÉTODOS CRUD PARA MARCA ===
    def get_all_marcas(self):
        """Obtener todas las marcas ordenadas por nombre"""
        query = "SELECT id_marca, nombre_marca FROM marca ORDER BY nombre_marca"
        return self.execute_query(query, fetch=True)
    
    def get_marca_by_id(self, id_marca):
        """Obtener una marca por ID"""
        query = "SELECT id_marca, nombre_marca FROM marca WHERE id_marca = %s"
        result = self.execute_query(query, (id_marca,), fetch=True)
        return result[0] if result else None
    
    def create_marca(self, nombre_marca):
        """Crear nueva marca"""
        query = "INSERT INTO marca (nombre_marca) VALUES (%s) RETURNING id_marca"
        result = self.execute_query(query, (nombre_marca,), fetch=True)
        return result[0]['id_marca'] if result else None
    
    def update_marca(self, id_marca, nombre_marca):
        """Actualizar marca existente"""
        query = "UPDATE marca SET nombre_marca = %s WHERE id_marca = %s"
        affected = self.execute_query(query, (nombre_marca, id_marca))
        return affected > 0
    
    def delete_marca(self, id_marca):
        """Eliminar marca si no tiene productos asociados"""
        # Verificar si la marca está siendo usada
        check_query = """
        SELECT 
            (SELECT COUNT(*) FROM ProductsTienda WHERE id_marca = %s) as count_tienda,
            (SELECT COUNT(*) FROM ProductsRaPe WHERE id_marca = %s) as count_rape
        """
        result = self.execute_query(check_query, (id_marca, id_marca), fetch=True)
        
        if result:
            count_tienda = result[0]['count_tienda']
            count_rape = result[0]['count_rape']
            
            if count_tienda > 0 or count_rape > 0:
                total = count_tienda + count_rape
                return False, f"No se puede eliminar: La marca tiene {total} producto(s) asociado(s)"
        
        # Eliminar si no tiene productos
        delete_query = "DELETE FROM marca WHERE id_marca = %s"
        affected = self.execute_query(delete_query, (id_marca,))
        if affected:
            return True, "Marca eliminada exitosamente"
        return False, "Error eliminando marca"
    # FIN MÉTODOS CRUD MARCA
    
    def create_pool(self, min_conn=1, max_conn=5):
        """Crear pool de conexiones para mejor rendimiento"""
        try:
            self.connection_pool = psycopg2.pool.SimpleConnectionPool(
                min_conn, max_conn, **self.config
            )
            print("Pool de conexiones creado exitosamente")
            return True
        except Exception as e:
            print(f"Error creando pool de conexiones: {e}")
            return False
    
    def get_connection(self):
        """Obtener una conexión del pool"""
        if self.connection_pool:
            try:
                return self.connection_pool.getconn()
            except Exception as e:
                print(f"Error obteniendo conexion: {e}")
                return None
        return None
    
    def return_connection(self, conn):
        """Devolver conexión al pool"""
        if self.connection_pool and conn:
            try:
                self.connection_pool.putconn(conn)
            except Exception as e:
                print(f"Error devolviendo conexion: {e}")
    
    def execute_query(self, query, params=None, fetch=False):
        """Ejecutar consulta SQL"""
        conn = None
        cursor = None
        try:
            conn = self.get_connection() or psycopg2.connect(**self.config)
            cursor = conn.cursor(cursor_factory=extras.DictCursor)
            
            cursor.execute(query, params or ())
            
            if fetch:
                result = cursor.fetchall()
                cursor.close()
                if conn and self.connection_pool:
                    self.return_connection(conn)
                else:
                    conn.close()
                return result
            else:
                conn.commit()
                affected_rows = cursor.rowcount
                cursor.close()
                if conn and self.connection_pool:
                    self.return_connection(conn)
                else:
                    conn.close()
                return affected_rows
                
        except Exception as e:
            if conn:
                conn.rollback()
            print(f"Error ejecutando consulta: {e}")
            if cursor:
                cursor.close()
            if conn and self.connection_pool:
                self.return_connection(conn)
            elif conn:
                conn.close()
            return None
    
    def close_all_connections(self):
        """Cerrar todas las conexiones del pool"""
        if self.connection_pool:
            self.connection_pool.closeall()
            print("Todas las conexiones del pool cerradas")
"""
db.py - Conexión segura a PostgreSQL Neon
Maneja conexiones compartidas para ambos sistemas
"""

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
                print(f"Error obteniendo conexión: {e}")
                return None
        return None
    
    def return_connection(self, conn):
        """Devolver conexión al pool"""
        if self.connection_pool and conn:
            try:
                self.connection_pool.putconn(conn)
            except Exception as e:
                print(f"Error devolviendo conexión: {e}")
    
    def test_connection(self):
        """Probar conexión a la base de datos"""
        conn = None
        try:
            conn = psycopg2.connect(**self.config)
            cursor = conn.cursor()
            
            # Consulta información básica de la BD
            cursor.execute("SELECT version();")
            db_version = cursor.fetchone()
            
            cursor.execute("SELECT current_database();")
            db_name = cursor.fetchone()
            
            cursor.execute("SELECT current_user;")
            db_user = cursor.fetchone()
            
            cursor.close()
            conn.close()
            
            print("=" * 50)
            print("CONEXION EXITOSA A POSTGRESQL NEON")
            print("=" * 50)
            print(f"Base de datos: {db_name[0]}")
            print(f"Usuario: {db_user[0]}")
            print(f"Version PostgreSQL: {db_version[0]}")
            print("=" * 50)
            return True
            
        except Exception as e:
            print("=" * 50)
            print("ERROR EN LA CONEXION A LA BASE DE DATOS")
            print("=" * 50)
            print(f"Error: {e}")
            print("Verifica:")
            print("1. El archivo .env con las credenciales correctas")
            print("2. La conexion a internet")
            print("3. Las credenciales en PostgreSQL Neon")
            print("=" * 50)
            return False
    
    def execute_query(self, query, params=None, fetch=False):
        """Ejecutar consulta SQL (para pruebas)"""
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

# Instancia global para uso compartido
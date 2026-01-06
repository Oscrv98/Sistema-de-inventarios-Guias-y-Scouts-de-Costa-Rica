"""
test_connection.py - Script para probar la conexión a la BD
"""

# Importar la clase Database, no una instancia
from db import Database

def main():
    print("Probando conexion a PostgreSQL Neon...")
    print()
    
    # Crear instancia de Database
    db = Database()
    
    # Probar conexión básica
    if db.test_connection():
        print("Prueba de conexion: EXITOSA")
        
        # Opcional: Probar una consulta simple
        print()
        print("Probando consulta a tablas existentes...")
        
        # Listar tablas en la base de datos
        query = """
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public'
        ORDER BY table_name;
        """
        
        tables = db.execute_query(query, fetch=True)
        if tables:
            print("Tablas encontradas en la base de datos:")
            for table in tables:
                print(f"  - {table['table_name']}")
        else:
            print("No se encontraron tablas o error en la consulta")
        
        # Crear pool de conexiones para uso futuro
        db.create_pool()
        
    else:
        print("Prueba de conexion: FALLIDA")
        print("Revisa las credenciales en el archivo .env")

if __name__ == "__main__":
    main()
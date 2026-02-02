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
            "sslmode": os.getenv("DB_SSLMODE", "require"),
            "connect_timeout": 5
        }
        
        self.connection_pool = None
        self._initialized = True
    
    # ============================================
    # MÉTODOS DE CONEXIÓN Y CONFIGURACIÓN
    # ============================================
    
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
    
    # ============================================
    # MÉTODOS DE VALIDACIÓN DE UNICIDAD
    # ============================================
    
    def check_duplicate_marca(self, nombre_marca, exclude_id=None):
        """Verifica si ya existe una marca con el mismo nombre"""
        try:
            if exclude_id:
                query = "SELECT COUNT(*) FROM marca WHERE LOWER(nombre_marca) = LOWER(%s) AND id_marca != %s"
                params = (nombre_marca, exclude_id)
            else:
                query = "SELECT COUNT(*) FROM marca WHERE LOWER(nombre_marca) = LOWER(%s)"
                params = (nombre_marca,)
            
            result = self.execute_query(query, params, fetch=True)
            return result[0]['count'] > 0 if result else False
        except Exception as e:
            print(f"Error verificando duplicado de marca: {e}")
            return False
    
    def check_duplicate_categoria(self, nombre_categoria, exclude_id=None):
        """Verifica si ya existe una categoría con el mismo nombre"""
        try:
            if exclude_id:
                query = "SELECT COUNT(*) FROM categoria WHERE LOWER(nombre_categoria) = LOWER(%s) AND id_categoria != %s"
                params = (nombre_categoria, exclude_id)
            else:
                query = "SELECT COUNT(*) FROM categoria WHERE LOWER(nombre_categoria) = LOWER(%s)"
                params = (nombre_categoria,)
            
            result = self.execute_query(query, params, fetch=True)
            return result[0]['count'] > 0 if result else False
        except Exception as e:
            print(f"Error verificando duplicado de categoría: {e}")
            return False
    
    def check_duplicate_edificio(self, nombre_edificio, exclude_id=None):
        """Verifica si ya existe un edificio con el mismo nombre"""
        try:
            if exclude_id:
                query = "SELECT COUNT(*) FROM edificio WHERE LOWER(nombre_edificio) = LOWER(%s) AND id_edificio != %s"
                params = (nombre_edificio, exclude_id)
            else:
                query = "SELECT COUNT(*) FROM edificio WHERE LOWER(nombre_edificio) = LOWER(%s)"
                params = (nombre_edificio,)
            
            result = self.execute_query(query, params, fetch=True)
            return result[0]['count'] > 0 if result else False
        except Exception as e:
            print(f"Error verificando duplicado de edificio: {e}")
            return False
    
    def check_duplicate_producto_tienda(self, nombre_producto, exclude_id=None):
        """Verifica si ya existe un producto TIENDA con el mismo nombre"""
        try:
            if exclude_id:
                query = "SELECT COUNT(*) FROM ProductsTienda WHERE LOWER(nombre_producto_tienda) = LOWER(%s) AND id_productostienda != %s"
                params = (nombre_producto, exclude_id)
            else:
                query = "SELECT COUNT(*) FROM ProductsTienda WHERE LOWER(nombre_producto_tienda) = LOWER(%s)"
                params = (nombre_producto,)
            
            result = self.execute_query(query, params, fetch=True)
            return result[0]['count'] > 0 if result else False
        except Exception as e:
            print(f"Error verificando duplicado de producto tienda: {e}")
            return False
    
    def check_duplicate_producto_rape(self, nombre_producto, exclude_id=None):
        """Verifica si ya existe un producto RA-PE con el mismo nombre"""
        try:
            if exclude_id:
                query = "SELECT COUNT(*) FROM ProductsRaPe WHERE LOWER(nombre_producto_rape) = LOWER(%s) AND id_productosrape != %s"
                params = (nombre_producto, exclude_id)
            else:
                query = "SELECT COUNT(*) FROM ProductsRaPe WHERE LOWER(nombre_producto_rape) = LOWER(%s)"
                params = (nombre_producto,)
            
            result = self.execute_query(query, params, fetch=True)
            return result[0]['count'] > 0 if result else False
        except Exception as e:
            print(f"Error verificando duplicado de producto RA-PE: {e}")
            return False
    
    # ============================================
    # MÉTODOS CRUD PARA MARCA (CON VALIDACIÓN)
    # ============================================
    
    def get_all_marcas(self):
        """Obtener todas las marcas ordenadas por nombre"""
        query = "SELECT id_marca, nombre_marca FROM marca ORDER BY id_marca, nombre_marca"
        return self.execute_query(query, fetch=True)
    
    def get_marca_by_id(self, id_marca):
        """Obtener una marca por ID"""
        query = "SELECT id_marca, nombre_marca FROM marca WHERE id_marca = %s"
        result = self.execute_query(query, (id_marca,), fetch=True)
        return result[0] if result else None
    
    def create_marca(self, nombre_marca):
        """Crear nueva marca con validación de unicidad"""
        # Validar que no exista
        if self.check_duplicate_marca(nombre_marca):
            return None, f"Ya existe una marca con el nombre '{nombre_marca}'"
        
        query = "INSERT INTO marca (nombre_marca) VALUES (%s) RETURNING id_marca"
        result = self.execute_query(query, (nombre_marca,), fetch=True)
        return (result[0]['id_marca'], "Marca creada exitosamente") if result else (None, "Error creando marca")
    
    def update_marca(self, id_marca, nombre_marca):
        """Actualizar marca existente con validación de unicidad"""
        # Validar que no exista otro con el mismo nombre
        if self.check_duplicate_marca(nombre_marca, id_marca):
            return False, f"Ya existe otra marca con el nombre '{nombre_marca}'"
        
        query = "UPDATE marca SET nombre_marca = %s WHERE id_marca = %s"
        affected = self.execute_query(query, (nombre_marca, id_marca))
        return (affected > 0, "Marca actualizada exitosamente") if affected > 0 else (False, "Error actualizando marca")
    
    def delete_marca(self, id_marca):
        """Eliminar marca si no tiene productos asociados"""
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
        
        delete_query = "DELETE FROM marca WHERE id_marca = %s"
        affected = self.execute_query(delete_query, (id_marca,))
        if affected:
            return True, "Marca eliminada exitosamente"
        return False, "Error eliminando marca"
    
    # ============================================
    # MÉTODOS CRUD PARA CATEGORÍA (CON VALIDACIÓN)
    # ============================================
    
    def get_all_categorias(self):
        """Obtener todas las categorías ordenadas por nombre"""
        query = "SELECT id_categoria, nombre_categoria FROM categoria ORDER BY id_categoria, nombre_categoria"
        return self.execute_query(query, fetch=True)
    
    def get_categoria_by_id(self, id_categoria):
        """Obtener una categoría por ID"""
        query = "SELECT id_categoria, nombre_categoria FROM categoria WHERE id_categoria = %s"
        result = self.execute_query(query, (id_categoria,), fetch=True)
        return result[0] if result else None
    
    def create_categoria(self, nombre_categoria):
        """Crear nueva categoría con validación de unicidad"""
        # Validar que no exista
        if self.check_duplicate_categoria(nombre_categoria):
            return None, f"Ya existe una categoría con el nombre '{nombre_categoria}'"
        
        query = "INSERT INTO categoria (nombre_categoria) VALUES (%s) RETURNING id_categoria"
        result = self.execute_query(query, (nombre_categoria,), fetch=True)
        if result and len(result) > 0:
            return result[0]['id_categoria'], "Categoría creada exitosamente"
        return None, "Error creando categoría"
    
    def update_categoria(self, id_categoria, nombre_categoria):
        """Actualizar categoría existente con validación de unicidad"""
        # Validar que no exista otro con el mismo nombre
        if self.check_duplicate_categoria(nombre_categoria, id_categoria):
            return False, f"Ya existe otra categoría con el nombre '{nombre_categoria}'"
        
        query = "UPDATE categoria SET nombre_categoria = %s WHERE id_categoria = %s"
        affected = self.execute_query(query, (nombre_categoria, id_categoria))
        return (affected > 0, "Categoría actualizada exitosamente") if affected > 0 else (False, "Error actualizando categoría")
    
    def delete_categoria(self, id_categoria):
        """Eliminar categoría si no tiene productos asociados"""
        check_query = """
        SELECT 
            (SELECT COUNT(*) FROM ProductsTienda WHERE id_categoria = %s) as count_tienda,
            (SELECT COUNT(*) FROM ProductsRaPe WHERE id_categoria = %s) as count_rape
        """
        result = self.execute_query(check_query, (id_categoria, id_categoria), fetch=True)
        
        if result:
            count_tienda = result[0]['count_tienda']
            count_rape = result[0]['count_rape']
            
            if count_tienda > 0 or count_rape > 0:
                total = count_tienda + count_rape
                return False, f"No se puede eliminar: La categoría tiene {total} producto(s) asociado(s)"
        
        delete_query = "DELETE FROM categoria WHERE id_categoria = %s"
        affected = self.execute_query(delete_query, (id_categoria,))
        if affected:
            return True, "Categoría eliminada exitosamente"
        return False, "Error eliminando categoría"
    
    # ============================================
    # MÉTODOS CRUD PARA EDIFICIO (CON VALIDACIÓN)
    # ============================================
    
    def get_all_edificios(self):
        """Obtener todos los edificios usando vista optimizada"""
        query = "SELECT * FROM vista_edificios_completa"
        return self.execute_query(query, fetch=True)

    def get_edificio_by_id(self, id_edificio):
        """Obtener un edificio por ID usando vista optimizada"""
        query = "SELECT * FROM vista_edificios_completa WHERE id_edificio = %s"
        result = self.execute_query(query, (id_edificio,), fetch=True)
        return result[0] if result else None

    def get_all_inventarios(self):
        """Obtener todos los inventarios disponibles"""
        query = "SELECT id_inventario, nombre_inventario FROM inventarios WHERE activo = TRUE ORDER BY nombre_inventario"
        return self.execute_query(query, fetch=True)

    def create_edificio(self, nombre_edificio, direccion, tipo, id_inventario):
        """Crear nuevo edificio con validación de unicidad"""
        # Validar que no exista
        if self.check_duplicate_edificio(nombre_edificio):
            return None, f"Ya existe un edificio con el nombre '{nombre_edificio}'"
        
        query = """
        INSERT INTO edificio (nombre_edificio, direccion, tipo, id_inventario) 
        VALUES (%s, %s, %s, %s) RETURNING id_edificio
        """
        result = self.execute_query(query, (nombre_edificio, direccion, tipo, id_inventario), fetch=True)
        if result and len(result) > 0:
            return result[0]['id_edificio'], "Edificio creado exitosamente"
        return None, "Error creando edificio"

    def update_edificio(self, id_edificio, nombre_edificio, direccion, tipo, id_inventario):
        """Actualizar edificio existente con validación de unicidad"""
        # Validar que no exista otro con el mismo nombre
        if self.check_duplicate_edificio(nombre_edificio, id_edificio):
            return False, f"Ya existe otro edificio con el nombre '{nombre_edificio}'"
        
        query = """
        UPDATE edificio 
        SET nombre_edificio = %s, direccion = %s, tipo = %s, id_inventario = %s 
        WHERE id_edificio = %s
        """
        affected = self.execute_query(query, (nombre_edificio, direccion, tipo, id_inventario, id_edificio))
        return (affected > 0, "Edificio actualizado exitosamente") if affected > 0 else (False, "Error actualizando edificio")

    def delete_edificio(self, id_edificio):
        """Eliminar edificio si no tiene inventario asociado"""
        check_query = """
        SELECT 
            (SELECT COUNT(*) FROM InvTienda WHERE id_edificio = %s) as count_tienda,
            (SELECT COUNT(*) FROM InvRaPe WHERE id_edificio = %s) as count_rape
        """
        result = self.execute_query(check_query, (id_edificio, id_edificio), fetch=True)
        
        if result:
            count_tienda = result[0]['count_tienda']
            count_rape = result[0]['count_rape']
            
            if count_tienda > 0 or count_rape > 0:
                total = count_tienda + count_rape
                return False, f"No se puede eliminar: El edificio tiene {total} item(s) de inventario asociado(s)"
        
        delete_query = "DELETE FROM edificio WHERE id_edificio = %s"
        affected = self.execute_query(delete_query, (id_edificio,))
        if affected:
            return True, "Edificio eliminado exitosamente"
        return False, "Error eliminando edificio"
    
    # ============================================
    # MÉTODOS PARA PRODUCTOS TIENDA
    # ============================================

    def get_edificios_tienda(self):
        """Obtener solo los edificios del sistema TIENDA"""
        query = """
        SELECT e.id_edificio, e.nombre_edificio 
        FROM edificio e
        JOIN inventarios i ON e.id_inventario = i.id_inventario
        WHERE i.nombre_inventario = 'TIENDA' AND i.activo = TRUE
        ORDER BY e.nombre_edificio
        """
        return self.execute_query(query, fetch=True)

    def get_productos_tienda_completo(self):
        """Obtener productos TIENDA completos usando vista optimizada"""
        query = """
        SELECT * FROM vista_productos_tienda_completa 
        ORDER BY id_productostienda
        """
        return self.execute_query(query, fetch=True)

    def get_inventario_por_producto(self, id_producto):
        """Obtener todo el inventario de un producto específico (TIENDA)"""
        query = """
        SELECT 
            it.id_invtienda,
            it.etiqueta,
            it.cantidad,
            it.estante,
            it.lugar,
            e.id_edificio,
            e.nombre_edificio
        FROM InvTienda it
        JOIN edificio e ON it.id_edificio = e.id_edificio
        WHERE it.id_productostienda = %s
        ORDER BY e.nombre_edificio
        """
        return self.execute_query(query, (id_producto,), fetch=True)

    # ============================================
    # CRUD PARA PRODUCTS TIENDA (CON VALIDACIÓN)
    # ============================================

    def create_producto_tienda(self, nombre, id_marca, id_categoria, precio_venta, 
                            precio_compra=None, color=None, talla=None, alarma_cap=5):
        """Crear nuevo producto en TIENDA con validación de unicidad"""
        # Validar que no exista
        if self.check_duplicate_producto_tienda(nombre):
            return None, f"Ya existe un producto TIENDA con el nombre '{nombre}'"
        
        query = """
        INSERT INTO ProductsTienda 
        (nombre_producto_tienda, id_marca, id_categoria, precio_venta, precio_compra, color, talla, alarma_cap) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s) 
        RETURNING id_productostienda
        """
        result = self.execute_query(query, (nombre, id_marca, id_categoria, precio_venta, 
                                        precio_compra, color, talla, alarma_cap), fetch=True)
        if result and len(result) > 0:
            return result[0]['id_productostienda'], "Producto creado exitosamente"
        return None, "Error creando producto"

    def update_producto_tienda(self, id_producto, nombre, id_marca, id_categoria, precio_venta,
                            precio_compra=None, color=None, talla=None, alarma_cap=None):
        """Actualizar producto TIENDA existente con validación de unicidad"""
        # Validar que no exista otro con el mismo nombre
        if self.check_duplicate_producto_tienda(nombre, id_producto):
            return False, f"Ya existe otro producto TIENDA con el nombre '{nombre}'"
        
        query = """
        UPDATE ProductsTienda 
        SET nombre_producto_tienda = %s, 
            id_marca = %s, 
            id_categoria = %s, 
            precio_venta = %s, 
            precio_compra = %s, 
            color = %s, 
            talla = %s, 
            alarma_cap = %s
        WHERE id_productostienda = %s
        """
        affected = self.execute_query(query, (nombre, id_marca, id_categoria, precio_venta,
                                            precio_compra, color, talla, alarma_cap, id_producto))
        return (affected > 0, "Producto actualizado exitosamente") if affected > 0 else (False, "Error actualizando producto")

    def delete_producto_tienda(self, id_producto):
        """Eliminar producto TIENDA y su inventario asociado"""
        try:
            delete_inv_query = "DELETE FROM InvTienda WHERE id_productostienda = %s"
            self.execute_query(delete_inv_query, (id_producto,), fetch=False)
            
            delete_producto_query = "DELETE FROM ProductsTienda WHERE id_productostienda = %s"
            affected = self.execute_query(delete_producto_query, (id_producto,), fetch=False)
            
            if affected:
                return True, "Producto y su inventario eliminados exitosamente"
            return False, "Error eliminando producto"
        except Exception as e:
            return False, f"Error al eliminar producto: {e}"

    # ============================================
    # CRUD PARA INVENTARIO TIENDA
    # ============================================

    def create_inventario_tienda(self, id_producto, id_edificio, cantidad=0, etiqueta=None, 
                                estante=None, lugar=None):
        """Crear registro de inventario para un producto en un edificio"""
        query = """
        INSERT INTO InvTienda 
        (id_productostienda, id_edificio, cantidad, etiqueta, estante, lugar) 
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        affected = self.execute_query(query, (id_producto, id_edificio, cantidad, 
                                            etiqueta, estante, lugar), fetch=False)
        return affected > 0

    def update_inventario_tienda(self, id_invtienda, cantidad=None, etiqueta=None, 
                                estante=None, lugar=None):
        """Actualizar registro de inventario TIENDA"""
        updates = []
        params = []
        
        if cantidad is not None:
            updates.append("cantidad = %s")
            params.append(cantidad)
        if etiqueta is not None:
            updates.append("etiqueta = %s")
            params.append(etiqueta)
        if estante is not None:
            updates.append("estante = %s")
            params.append(estante)
        if lugar is not None:
            updates.append("lugar = %s")
            params.append(lugar)
        
        if not updates:
            return False
        
        query = f"UPDATE InvTienda SET {', '.join(updates)} WHERE id_invtienda = %s"
        params.append(id_invtienda)
        
        affected = self.execute_query(query, tuple(params), fetch=False)
        return affected > 0

    def create_inventario_para_edificios_tienda(self, id_producto):
        """Crear registros de inventario para todos los edificios TIENDA"""
        edificios = self.get_edificios_tienda()
        
        if not edificios:
            return False
        
        success_count = 0
        for edificio in edificios:
            success = self.create_inventario_tienda(
                id_producto=id_producto,
                id_edificio=edificio['id_edificio'],
                cantidad=0,
                etiqueta=None,
                estante=None,
                lugar=None
            )
            if success:
                success_count += 1
        
        return success_count == len(edificios)

    # ============================================
    # MÉTODOS PARA PRODUCTOS RA-PE 
    # ============================================

    def get_productos_rape_completo(self):
        """Obtener productos RA-PE completos usando vista optimizada"""
        query = "SELECT * FROM vista_productos_rape_completa ORDER BY id_productosrape"
        return self.execute_query(query, fetch=True)

    def create_producto_rape(self, nombre, id_marca, id_categoria, alarma_cap=5):
        """Crear nuevo producto en RA-PE con validación de unicidad"""
        # Validar que no exista
        if self.check_duplicate_producto_rape(nombre):
            return None, f"Ya existe un material RA-PE con el nombre '{nombre}'"
        
        query = """
        INSERT INTO ProductsRaPe 
        (nombre_producto_rape, id_marca, id_categoria, alarma_cap) 
        VALUES (%s, %s, %s, %s) 
        RETURNING id_productosrape
        """
        result = self.execute_query(query, (nombre, id_marca, id_categoria, alarma_cap), fetch=True)
        return (result[0]['id_productosrape'], "Material creado exitosamente") if result else (None, "Error creando material")

    def update_producto_rape(self, id_producto, nombre, id_marca, id_categoria, alarma_cap=None):
        """Actualizar producto RA-PE existente con validación de unicidad"""
        # Validar que no exista otro con el mismo nombre
        if self.check_duplicate_producto_rape(nombre, id_producto):
            return False, f"Ya existe otro material RA-PE con el nombre '{nombre}'"
        
        query = """
        UPDATE ProductsRaPe 
        SET nombre_producto_rape = %s, 
            id_marca = %s, 
            id_categoria = %s, 
            alarma_cap = %s
        WHERE id_productosrape = %s
        """
        affected = self.execute_query(query, (nombre, id_marca, id_categoria, alarma_cap, id_producto))
        return (affected > 0, "Material actualizado exitosamente") if affected > 0 else (False, "Error actualizando material")

    def delete_producto_rape(self, id_producto):
        """Eliminar producto RA-PE y su inventario asociado"""
        try:
            delete_inv_query = "DELETE FROM InvRaPe WHERE id_productosrape = %s"
            self.execute_query(delete_inv_query, (id_producto,), fetch=False)
            
            delete_producto_query = "DELETE FROM ProductsRaPe WHERE id_productosrape = %s"
            affected = self.execute_query(delete_producto_query, (id_producto,), fetch=False)
            
            if affected:
                return True, "Material y su inventario eliminados exitosamente"
            return False, "Error eliminando material"
        except Exception as e:
            return False, f"Error al eliminar material: {e}"

    def get_inventario_por_producto_rape(self, id_producto):
        """Obtener todo el inventario de un producto RA-PE específico (ACTUALIZADO)"""
        query = """
        SELECT 
            ir.id_invrape,
            ir.etiqueta,
            ir.cantidad,
            ir.estante,
            ir.lugar,
            e.id_edificio,
            e.nombre_edificio
        FROM InvRaPe ir
        JOIN edificio e ON ir.id_edificio = e.id_edificio
        WHERE ir.id_productosrape = %s
        ORDER BY e.nombre_edificio
        """
        return self.execute_query(query, (id_producto,), fetch=True)

    def get_edificios_rape(self):
        """Obtener solo los edificios del sistema RA-PE"""
        query = """
        SELECT e.id_edificio, e.nombre_edificio 
        FROM edificio e
        JOIN inventarios i ON e.id_inventario = i.id_inventario
        WHERE i.nombre_inventario = 'RA-PE' AND i.activo = TRUE
        ORDER BY e.nombre_edificio
        """
        return self.execute_query(query, fetch=True)

    def create_inventario_para_edificios_rape(self, id_producto):
        """Crear registros de inventario para todos los edificios RA-PE (ACTUALIZADO)"""
        edificios = self.get_edificios_rape()
        
        if not edificios:
            return False
        
        success_count = 0
        for edificio in edificios:
            query = """
            INSERT INTO InvRaPe 
            (id_productosrape, id_edificio, cantidad, etiqueta, estante, lugar) 
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            affected = self.execute_query(query, (
                id_producto, edificio['id_edificio'], 0, None, None, None
            ), fetch=False)
            
            if affected:
                success_count += 1
        
        return success_count == len(edificios)
    
    def update_inventario_rape(self, id_invrape, cantidad=None, etiqueta=None, 
                          estante=None, lugar=None):
        """Actualizar registro de inventario RA-PE (ACTUALIZADO)"""
        updates = []
        params = []
        
        if cantidad is not None:
            updates.append("cantidad = %s")
            params.append(cantidad)
        if etiqueta is not None:
            updates.append("etiqueta = %s")
            params.append(etiqueta)
        if estante is not None:
            updates.append("estante = %s")
            params.append(estante)
        if lugar is not None:
            updates.append("lugar = %s")
            params.append(lugar)
        
        if not updates:
            return False
        
        query = f"UPDATE InvRaPe SET {', '.join(updates)} WHERE id_invrape = %s"
        params.append(id_invrape)
        
        affected = self.execute_query(query, tuple(params), fetch=False)
        return affected > 0
    
    # ============================================
    # MÉTODOS AUXILIARES GENERALES
    # ============================================

    def get_all_marcas(self):
        """Obtener todas las marcas para comboboxes"""
        query = "SELECT id_marca, nombre_marca FROM marca ORDER BY nombre_marca"
        return self.execute_query(query, fetch=True)

    def get_all_categorias(self):
        """Obtener todas las categorías para comboboxes"""
        query = "SELECT id_categoria, nombre_categoria FROM categoria ORDER BY nombre_categoria"
        return self.execute_query(query, fetch=True)
        
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
    
    def get_alarmas_tienda(self):
        """Obtener productos TIENDA con alarmas (agotados o a reponer)"""
        query = "SELECT * FROM vista_alarmas_tienda ORDER BY estado, nombre_producto"
        return self.execute_query(query, fetch=True)

    def get_alarmas_rape(self):
        """Obtener materiales RA-PE con alarmas (agotados o a reponer)"""
        query = "SELECT * FROM vista_alarmas_rape ORDER BY estado, nombre_producto"
        return self.execute_query(query, fetch=True)

    def get_alarmas_tienda(self):
        """Obtener productos TIENDA con alarmas (agotados o a reponer)"""
        query = """
        SELECT 
            va.id_productostienda,
            va.nombre_producto,
            va.alarma_cap,
            va.cantidad_total,
            va.estado,
            va.num_ubicaciones,
            pt.nombre_producto_tienda,
            m.nombre_marca,
            c.nombre_categoria,
            pt.precio_venta
        FROM vista_alarmas_tienda va
        JOIN ProductsTienda pt ON va.id_productostienda = pt.id_productostienda
        LEFT JOIN marca m ON pt.id_marca = m.id_marca
        LEFT JOIN categoria c ON pt.id_categoria = c.id_categoria
        ORDER BY va.estado DESC, va.cantidad_total ASC
        """
        return self.execute_query(query, fetch=True)
    
    def get_export_data_tienda(self):
        """Obtiene todos los datos necesarios para exportar TIENDA a Excel"""
        try:
            query_resumen = """
            SELECT 
                nombre_producto_tienda as "Producto",
                nombre_marca as "Marca",
                nombre_categoria as "Categoría",
                precio_venta as "Precio Venta",
                precio_compra as "Precio Compra",
                color as "Color",
                talla as "Talla",
                alarma_cap as "Nivel Alarma",
                stock_total as "Stock Total",
                num_ubicaciones as "Ubicaciones",
                lista_edificios as "Edificios"
            FROM vista_productos_tienda_completa 
            ORDER BY nombre_producto_tienda
            """     
            resumen_data = self.execute_query(query_resumen, fetch=True)
            query_detalle = """
            SELECT 
                p.nombre_producto_tienda as "Producto",
                e.nombre_edificio as "Edificio",
                i.cantidad as "Cantidad",
                i.estante as "Estante",
                i.lugar as "Lugar",
                i.etiqueta as "Etiqueta",
                COALESCE(m.nombre_marca, 'Sin marca') as "Marca",
                COALESCE(c.nombre_categoria, 'Sin categoría') as "Categoría"
            FROM ProductsTienda p
            LEFT JOIN InvTienda i ON p.id_productostienda = i.id_productostienda
            LEFT JOIN edificio e ON i.id_edificio = e.id_edificio
            LEFT JOIN marca m ON p.id_marca = m.id_marca
            LEFT JOIN categoria c ON p.id_categoria = c.id_categoria
            WHERE e.id_inventario = 1 OR e.id_inventario IS NULL  -- Solo edificios TIENDA
            ORDER BY p.nombre_producto_tienda, e.nombre_edificio
            """
            
            detalle_data = self.execute_query(query_detalle, fetch=True)
            
            return {
                'resumen': resumen_data if resumen_data else [],
                'detalle': detalle_data if detalle_data else []
            }
            
        except Exception as e:
            print(f"Error obteniendo datos para exportación TIENDA: {e}")
            return {'resumen': [], 'detalle': []}
        
    def get_export_data_rape(self):
        """Obtiene todos los datos necesarios para exportar RA-PE a Excel"""
        try:
            query_resumen = """
            SELECT 
                nombre_producto_rape as "Material",
                nombre_marca as "Marca",
                nombre_categoria as "Categoría",
                alarma_cap as "Nivel Alarma",
                stock_total as "Stock Total",
                num_ubicaciones as "Ubicaciones",
                lista_edificios as "Edificios"
            FROM vista_productos_rape_completa 
            ORDER BY nombre_producto_rape
            """
            
            resumen_data = self.execute_query(query_resumen, fetch=True)
            
            query_detalle = """
            SELECT 
                p.nombre_producto_rape as "Material",
                e.nombre_edificio as "Edificio",
                i.cantidad as "Cantidad",
                i.estante as "Estante",
                i.lugar as "Lugar",
                i.etiqueta as "Etiqueta",
                COALESCE(m.nombre_marca, 'Sin marca') as "Marca",
                COALESCE(c.nombre_categoria, 'Sin categoría') as "Categoría"
            FROM ProductsRaPe p
            LEFT JOIN InvRaPe i ON p.id_productosrape = i.id_productosrape
            LEFT JOIN edificio e ON i.id_edificio = e.id_edificio
            LEFT JOIN marca m ON p.id_marca = m.id_marca
            LEFT JOIN categoria c ON p.id_categoria = c.id_categoria
            WHERE e.id_inventario = 2 OR e.id_inventario IS NULL  -- Solo edificios RA-PE
            ORDER BY p.nombre_producto_rape, e.nombre_edificio
            """
            
            detalle_data = self.execute_query(query_detalle, fetch=True)
            
            return {
                'resumen': resumen_data if resumen_data else [],
                'detalle': detalle_data if detalle_data else []
            }
            
        except Exception as e:
            print(f"Error obteniendo datos para exportación RA-PE: {e}")
            return {'resumen': [], 'detalle': []}
    
    def buscar_productos_tienda(self, texto):
        """Búsqueda optimizada de productos TIENDA"""
        query = """
        SELECT * FROM vista_productos_tienda_completa 
        WHERE LOWER(nombre_producto_tienda) LIKE %s 
        OR LOWER(nombre_marca) LIKE %s 
        OR LOWER(nombre_categoria) LIKE %s
        ORDER BY nombre_producto_tienda
        """
        texto_busqueda = f"%{texto.lower()}%"
        return self.execute_query(query, (texto_busqueda, texto_busqueda, texto_busqueda), fetch=True)

    def buscar_productos_rape(self, texto):
        """Búsqueda optimizada de materiales RA-PE"""
        query = """
        SELECT * FROM vista_productos_rape_completa 
        WHERE LOWER(nombre_producto_rape) LIKE %s 
        OR LOWER(nombre_marca) LIKE %s 
        OR LOWER(nombre_categoria) LIKE %s
        ORDER BY nombre_producto_rape
        """
        texto_busqueda = f"%{texto.lower()}%"
        return self.execute_query(query, (texto_busqueda, texto_busqueda, texto_busqueda), fetch=True)

    def verify_login(self, usuario, password):
        """Verificar credenciales de usuario"""
        try:
            query = """
            SELECT usuario, rol FROM usuarios 
            WHERE usuario = %s AND password = %s
            """
            result = self.execute_query(query, (usuario, password), fetch=True)
            return result[0] if result else None
        except Exception as e:
            print(f"Error verificando login: {e}")
            return None
    
    # MÉTODO PRINCIPAL PARA EJECUTAR CONSULTAS
    # ============================================
    
    def execute_query(self, query, params=None, fetch=False):
        """Ejecutar consulta SQL - método centralizado"""
        conn = None
        cursor = None
        try:
            conn = self.get_connection() or psycopg2.connect(**self.config)
            cursor = conn.cursor(cursor_factory=extras.DictCursor)
            
            cursor.execute(query, params or ())
            
            query_lower = query.strip().lower()
            is_select = query_lower.startswith('select') or query_lower.startswith('with')
            
            if not is_select:
                conn.commit()
            
            if fetch:
                result = cursor.fetchall()
                cursor.close()
                if conn and self.connection_pool:
                    self.return_connection(conn)
                else:
                    conn.close()
                return result
            else:
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
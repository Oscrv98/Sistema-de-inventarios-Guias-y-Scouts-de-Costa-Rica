import tkinter as tk
from tkinter import ttk, messagebox
import styles

class VentanaProductosTienda:
    def __init__(self, root, system_name):
        self.root = root
        self.system_name = system_name
        self.productos_data = []  # Almacenar datos completos para filtrado
        
        # Configurar ventana
        self.window = tk.Toplevel(root)
        self.window.title(f"Productos TIENDA - {system_name}")
        
        # Tamaño grande desde el inicio
        self.window.geometry("1500x900")
        self.window.minsize(1450, 850)
        
        # Centrar ventana usando nuestra función
        self.centerWindow(1500, 900)
        
        self.window.configure(bg=styles.COLOR_FONDO_OSCURO)
        self.window.transient(root)
        self.window.grab_set()
        
        # Frame principal
        self.main_frame = tk.Frame(self.window, bg=styles.COLOR_FONDO_OSCURO, padx=20, pady=20)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título con color del sistema
        color_sistema = styles.COLOR_TIENDA
        title_frame = tk.Frame(self.main_frame, bg=color_sistema)
        title_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.lbl_titulo = tk.Label(title_frame, 
                                  text="GESTIÓN DE PRODUCTOS TIENDA",
                                  font=(styles.FUENTE_PRINCIPAL, 18, "bold"),
                                  bg=color_sistema, 
                                  fg=styles.COLOR_BLANCO,
                                  padx=20, pady=10)
        self.lbl_titulo.pack()
        
        # ============================================
        # BARRA SUPERIOR DE CONTROLES
        # ============================================
        top_frame = tk.Frame(self.main_frame, bg=styles.COLOR_FONDO_OSCURO)
        top_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Botones a la izquierda
        btn_frame_left = tk.Frame(top_frame, bg=styles.COLOR_FONDO_OSCURO)
        btn_frame_left.pack(side=tk.LEFT)
        
        self.btn_agregar = tk.Button(btn_frame_left, 
                                    text="Agregar",
                                    font=(styles.FUENTE_PRINCIPAL, 11, "bold"),
                                    bg=styles.COLOR_EXITO,
                                    fg=styles.COLOR_BLANCO,
                                    width=12,
                                    height=1,
                                    cursor="hand2",
                                    command=self.agregar_producto)
        self.btn_agregar.pack(side=tk.LEFT, padx=(0, 10))
        
        self.btn_editar = tk.Button(btn_frame_left,
                                   text="Editar",
                                   font=(styles.FUENTE_PRINCIPAL, 11, "bold"),
                                   bg=styles.COLOR_ADVERTENCIA,
                                   fg=styles.COLOR_BLANCO,
                                   width=12,
                                   height=1,
                                   state=tk.DISABLED,
                                   cursor="hand2",
                                   command=self.editar_producto)
        self.btn_editar.pack(side=tk.LEFT, padx=(0, 10))
        
        self.btn_detalles = tk.Button(btn_frame_left,
                                     text="Detalles",
                                     font=(styles.FUENTE_PRINCIPAL, 11, "bold"),
                                     bg=styles.COLOR_INFO,
                                     fg=styles.COLOR_BLANCO,
                                     width=12,
                                     height=1,
                                     state=tk.DISABLED,
                                     cursor="hand2",
                                     command=self.ver_detalles)
        self.btn_detalles.pack(side=tk.LEFT)
        
        # Barra de búsqueda a la derecha
        search_frame = tk.Frame(top_frame, bg=styles.COLOR_FONDO_OSCURO)
        search_frame.pack(side=tk.RIGHT)
        
        self.lbl_buscar = tk.Label(search_frame,
                                  text="Buscar:",
                                  font=(styles.FUENTE_PRINCIPAL, 11,"bold"),
                                  bg=styles.COLOR_FONDO_OSCURO,
                                  fg=styles.COLOR_BLANCO)
        self.lbl_buscar.pack(side=tk.LEFT, padx=(0, 8))
        
        self.entry_buscar = tk.Entry(search_frame,
                                    font=(styles.FUENTE_PRINCIPAL, 11),
                                    width=35,
                                    relief=tk.SOLID,
                                    borderwidth=1)
        self.entry_buscar.pack(side=tk.LEFT, padx=(0, 10))
        self.entry_buscar.insert(0, "Buscar por nombre, marca o categoría...")
        self.entry_buscar.config(fg="grey")
        
        # Eventos para el placeholder
        self.entry_buscar.bind("<FocusIn>", self.on_entry_focus_in)
        self.entry_buscar.bind("<FocusOut>", self.on_entry_focus_out)
        self.entry_buscar.bind("<KeyRelease>", self.filtrar_tabla)
        
        # ============================================
        # TABLA DE PRODUCTOS - VERSIÓN SIMPLE QUE FUNCIONA
        # ============================================
        table_frame = tk.Frame(self.main_frame, bg=styles.COLOR_FONDO)
        table_frame.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(table_frame, orient="vertical")
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        h_scrollbar = ttk.Scrollbar(table_frame, orient="horizontal")
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Treeview - ENFOQUE DIRECTO
        # Primero, intentemos ver qué tema está usando el sistema
        style = ttk.Style()
        print(f"Temas disponibles: {style.theme_names()}")
        print(f"Tema actual: {style.theme_use()}")
        
        # Configurar el Treeview de manera FORZADA
        # Intentar diferentes configuraciones hasta que funcione
        
        # PRIMER INTENTO: Configurar estilo básico
        style.configure("Treeview",
                       font=(styles.FUENTE_PRINCIPAL, styles.TAMANO_NORMAL),
                       rowheight=25,
                       background="white",
                       fieldbackground="white",
                       foreground=styles.COLOR_TEXTO_OSCURO)
        
        # SEGUNDO INTENTO: Configurar headings específicamente
        # Esto es lo que debería funcionar según la documentación
        style.configure("Treeview.Heading",
                       font=(styles.FUENTE_PRINCIPAL, styles.TAMANO_NORMAL, styles.PESO_NEGRITA),
                       background=styles.COLOR_TREEVIEW_HEADING,
                       foreground=styles.COLOR_BLANCO,
                       relief="flat",
                       padding=(5, 5))
        
        # TERCER INTENTO: Si lo anterior no funciona, usar map
       
        
        # Crear Treeview normal
        self.tree = ttk.Treeview(table_frame,
                                columns=("ID", "Nombre", "Marca", "Categoría", 
                                        "Precio Venta", "Precio Compra", 
                                        "Color", "Talla", "Stock", "Alarma"),
                                yscrollcommand=v_scrollbar.set,
                                xscrollcommand=h_scrollbar.set,
                                selectmode="browse",
                                height=22)
        
        v_scrollbar.config(command=self.tree.yview)
        h_scrollbar.config(command=self.tree.xview)
        
        # Configurar columnas
        column_widths = {
            "ID": 60,
            "Nombre": 250,
            "Marca": 140,
            "Categoría": 140,
            "Precio Venta": 120,
            "Precio Compra": 120,
            "Color": 100,
            "Talla": 80,
            "Stock": 90,
            "Alarma": 90
        }
        
        for col in self.tree["columns"]:
            self.tree.column(col, width=column_widths[col], anchor="center")
            self.tree.heading(col, text=col, anchor="center")
        
        self.tree.column("#0", width=0, stretch=tk.NO)
        
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # Evento de selección
        self.tree.bind("<<TreeviewSelect>>", self.on_item_selected)
        
        # ============================================
        # SOLUCIÓN DE EMERGENCIA: Si los colores no funcionan
        # Crear una función para forzar colores después de mostrar
        # ============================================
        self.window.after(100, self.forzar_colores_heading)
        
        # ============================================
        # BARRA INFERIOR DE CONTROLES
        # ============================================
        bottom_frame = tk.Frame(self.main_frame, bg=styles.COLOR_FONDO_OSCURO)
        bottom_frame.pack(fill=tk.X, pady=(20, 0))
        
        self.btn_eliminar = tk.Button(bottom_frame,
                                     text="Eliminar",
                                     font=(styles.FUENTE_PRINCIPAL, 11, "bold"),
                                     bg=styles.COLOR_PELIGRO,
                                     fg=styles.COLOR_BLANCO,
                                     width=12,
                                     height=1,
                                     state=tk.DISABLED,
                                     cursor="hand2",
                                     command=self.eliminar_producto)
        self.btn_eliminar.pack(side=tk.LEFT)
        
        self.btn_cerrar = tk.Button(bottom_frame,
                                   text="Cerrar",
                                   font=(styles.FUENTE_PRINCIPAL, 11, "bold"),
                                   bg=styles.COLOR_TEXTO_MEDIO,
                                   fg=styles.COLOR_BLANCO,
                                   width=12,
                                   height=1,
                                   cursor="hand2",
                                   command=self.window.destroy)
        self.btn_cerrar.pack(side=tk.RIGHT)
        
        # Cargar datos
        self.cargar_productos()
    
    def forzar_colores_heading(self):
        """Intenta forzar los colores de los headings después de que se muestra la ventana"""
        try:
            # Intentar acceder directamente a los elementos de heading
            # Esto depende del tema específico que esté usando ttk
            
            # OPCIÓN 1: Intentar modificar el estilo nuevamente después de creado
            style = ttk.Style()
            
            # Para el tema 'default' o 'clam'
            try:
                # Intentar configurar para tema 'clam' (suele funcionar mejor)
                style.theme_use('clam')
                
                # Reconfigurar con tema 'clam'
                style.configure("Treeview.Heading",
                               background=styles.COLOR_TREEVIEW_HEADING,
                               foreground=styles.COLOR_BLANCO,
                               font=(styles.FUENTE_PRINCIPAL, styles.TAMANO_NORMAL, styles.PESO_NEGRITA))
                
                print("Tema cambiado a 'clam' y colores reconfigurados")
                
            except:
                print("No se pudo cambiar a tema 'clam'")
            
            # OPCIÓN 2: Modificar directamente los widgets de heading
            # Esto es un hack, pero a veces funciona
            try:
                # Buscar todos los widgets de heading en el treeview
                for widget in self.tree.winfo_children():
                    if 'heading' in str(widget):
                        widget.configure(bg=styles.COLOR_TREEVIEW_HEADING,
                                        fg=styles.COLOR_BLANCO)
            except:
                pass
                
        except Exception as e:
            print(f"Error forzando colores: {e}")
    
    def centerWindow(self, width, height):
        """Centra la ventana en la pantalla"""
        screenWidth = self.window.winfo_screenwidth()
        screenHeight = self.window.winfo_screenheight()
        x = (screenWidth // 2) - (width // 2)
        y = (screenHeight // 2) - (height // 2)
        self.window.geometry(f"{width}x{height}+{x}+{y}")
    
    # ============================================
    # MÉTODOS PARA BÚSQUEDA
    # ============================================
    
    def on_entry_focus_in(self, event):
        """Maneja el foco en el campo de búsqueda"""
        if self.entry_buscar.get() == "Buscar por nombre, marca o categoría...":
            self.entry_buscar.delete(0, tk.END)
            self.entry_buscar.config(fg="black")
    
    def on_entry_focus_out(self, event):
        """Maneja la pérdida de foco en el campo de búsqueda"""
        if not self.entry_buscar.get():
            self.entry_buscar.insert(0, "Buscar por nombre, marca o categoría...")
            self.entry_buscar.config(fg="grey")
    
    def filtrar_tabla(self, event=None):
        """Filtra la tabla en base al texto de búsqueda"""
        texto_busqueda = self.entry_buscar.get().strip().lower()
        
        if texto_busqueda == "buscar por nombre, marca o categoría...":
            texto_busqueda = ""
        
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        if texto_busqueda:
            productos_filtrados = []
            for producto in self.productos_data:
                if (texto_busqueda in producto['nombre_producto_tienda'].lower() or
                    texto_busqueda in producto.get('nombre_marca', '').lower() or
                    texto_busqueda in producto.get('nombre_categoria', '').lower()):
                    productos_filtrados.append(producto)
            
            self.mostrar_productos_en_tabla(productos_filtrados)
        else:
            self.mostrar_productos_en_tabla(self.productos_data)
    
    # ============================================
    # MÉTODOS PARA CARGA DE DATOS
    # ============================================
    
    def cargar_productos(self):
        """Carga productos desde la base de datos"""
        try:
            from db import Database
            db = Database()
            self.productos_data = db.get_productos_tienda_completo()
            self.mostrar_productos_en_tabla(self.productos_data)
        except Exception as e:
            print(f"Error cargando productos: {e}")
            messagebox.showerror("Error", f"No se pudieron cargar los productos: {e}")
    
    def mostrar_productos_en_tabla(self, productos):
        """Muestra productos en la tabla Treeview"""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        for i, producto in enumerate(productos):
            # Formatear precios
            precio_venta = ""
            precio_compra = ""
            
            if producto.get('precio_venta'):
                try:
                    precio_venta = f"₡{float(producto['precio_venta']):,.2f}"
                except:
                    precio_venta = str(producto.get('precio_venta', ''))
            
            if producto.get('precio_compra'):
                try:
                    precio_compra = f"₡{float(producto['precio_compra']):,.2f}"
                except:
                    precio_compra = str(producto.get('precio_compra', ''))
            
            tags = []
            
            if i % 2 == 0:
                tags.append('evenrow')
            else:
                tags.append('oddrow')
            
            try:
                stock = float(producto.get('stock_total', 0))
                alarma = float(producto.get('alarma_cap', 0))
                if stock < alarma:
                    tags.append('alarma')
            except:
                pass
            
            self.tree.insert("", "end", 
                           values=(
                               producto['id_productostienda'],
                               producto['nombre_producto_tienda'],
                               producto.get('nombre_marca', ''),
                               producto.get('nombre_categoria', ''),
                               precio_venta,
                               precio_compra,
                               producto.get('color', ''),
                               producto.get('talla', ''),
                               producto.get('stock_total', 0),
                               producto.get('alarma_cap', 0)
                           ),
                           tags=tuple(tags))
        
        # Configurar tags para filas alternas
        self.tree.tag_configure('evenrow', background='#FFFFFF')
        self.tree.tag_configure('oddrow', background='#F5F5F5')
        self.tree.tag_configure('alarma', background='#FFF3CD')
    
    # ============================================
    # MÉTODOS PARA SELECCIÓN
    # ============================================
    
    def on_item_selected(self, event):
        """Habilita botones cuando se selecciona un item"""
        seleccionado = self.tree.selection()
        if seleccionado:
            self.btn_editar.config(state=tk.NORMAL)
            self.btn_detalles.config(state=tk.NORMAL)
            self.btn_eliminar.config(state=tk.NORMAL)
        else:
            self.btn_editar.config(state=tk.DISABLED)
            self.btn_detalles.config(state=tk.DISABLED)
            self.btn_eliminar.config(state=tk.DISABLED)
    
    # ... (los métodos CRUD se mantienen igual) ...

    def agregar_producto(self):
        """Abre ventana para agregar producto"""
        try:
            from ventanaDetalleProductoTienda import VentanaDetalleProductoTienda
            ventana = VentanaDetalleProductoTienda(self.window, self.system_name)
            self.window.wait_window(ventana.window)
            self.cargar_productos()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo abrir agregar producto: {e}")
    
    def editar_producto(self):
        """Abre ventana para editar producto seleccionado"""
        seleccionado = self.tree.selection()
        if seleccionado:
            id_producto = self.tree.item(seleccionado[0])['values'][0]
            try:
                from ventanaDetalleProductoTienda import VentanaDetalleProductoTienda
                ventana = VentanaDetalleProductoTienda(self.window, self.system_name, id_producto)
                self.window.wait_window(ventana.window)
                self.cargar_productos()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo editar producto: {e}")
    
    def ver_detalles(self):
        """Abre ventana para ver detalles del producto"""
        seleccionado = self.tree.selection()
        if seleccionado:
            id_producto = self.tree.item(seleccionado[0])['values'][0]
            nombre_producto = self.tree.item(seleccionado[0])['values'][1]  # Obtener nombre también
            
            try:
                from ventanaDistribucionInventario import VentanaDistribucionInventario
                
                # LLAMAR EXACTAMENTE IGUAL QUE EN RA-PE
                ventana = VentanaDistribucionInventario(
                    self.window,                # parent
                    id_producto,                # id_producto
                    nombre_producto,            # nombre_producto
                    sistema="tienda",           # ¡IMPORTANTE: sistema="tienda"!
                    callback_obj=self,          # callback object
                    modo="detalles"            # mode
                )
                
            except Exception as e:
                print(f"Error abriendo detalles: {e}")
                messagebox.showerror("Error", f"No se pudo ver detalles: {e}")
    
    def eliminar_producto(self):
        """Elimina el producto seleccionado"""
        seleccionado = self.tree.selection()
        if seleccionado:
            id_producto = self.tree.item(seleccionado[0])['values'][0]
            nombre_producto = self.tree.item(seleccionado[0])['values'][1]
            
            respuesta = messagebox.askyesno(
                "Confirmar Eliminación",
                f"¿Está seguro de eliminar el producto:\n{nombre_producto}?\n\n"
                "Esta acción eliminará también todo su inventario asociado."
            )
            
            if respuesta:
                try:
                    from db import Database
                    db = Database()
                    success, mensaje = db.delete_producto_tienda(id_producto)
                    
                    if success:
                        messagebox.showinfo("Éxito", mensaje)
                        self.cargar_productos()
                    else:
                        messagebox.showerror("Error", mensaje)
                except Exception as e:
                    messagebox.showerror("Error", f"No se pudo eliminar producto: {e}")
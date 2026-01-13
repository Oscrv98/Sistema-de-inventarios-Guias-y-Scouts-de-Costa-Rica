"""
Ventana CRUD para gestión de Productos TIENDA
"""

import tkinter as tk
from tkinter import ttk, messagebox
import styles
from db import Database

class VentanaProductosTienda:
    def __init__(self, parent, systemName):
        self.parent = parent
        self.systemName = systemName
        self.db = Database()
        
        # Crear ventana emergente
        self.window = tk.Toplevel(parent)
        self.window.title(f"Gestión de Productos TIENDA - {systemName}")
        self.window.geometry("1200x700")
        self.window.minsize(1200, 700)
        self.window.maxsize(1200, 700)
        self.window.configure(bg=styles.COLOR_FONDO)
        self.window.transient(parent)
        self.window.grab_set()
        
        # Centrar ventana
        self.centerWindow(1200, 700)
        
        # Crear interfaz
        self.createWidgets()
        self.loadProductos()
    
    def centerWindow(self, width, height):
        """Centra la ventana en la pantalla"""
        screenWidth = self.window.winfo_screenwidth()
        screenHeight = self.window.winfo_screenheight()
        x = (screenWidth // 2) - (width // 2)
        y = (screenHeight // 2) - (height // 2)
        self.window.geometry(f"{width}x{height}+{x}+{y}")
    
    def createWidgets(self):
        """Crea todos los widgets de la ventana principal"""
        # Frame principal
        mainFrame = tk.Frame(self.window, bg=styles.COLOR_FONDO, padx=20, pady=20)
        mainFrame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        title = tk.Label(mainFrame, 
                        text="GESTIÓN DE PRODUCTOS TIENDA", 
                        font=(styles.FUENTE_PRINCIPAL, styles.TAMANO_TITULO, styles.PESO_NEGRITA),
                        bg=styles.COLOR_FONDO, 
                        fg=styles.COLOR_TEXTO_OSCURO)
        title.pack(pady=(0, 20))
        
        # Frame para botones de acción principales
        buttonFrame = tk.Frame(mainFrame, bg=styles.COLOR_FONDO)
        buttonFrame.pack(fill=tk.X, pady=(0, 15))
        
        # Botón Agregar Producto
        self.btnAgregar = tk.Button(buttonFrame, 
                                    text="Agregar Nuevo Producto", 
                                    font=(styles.FUENTE_PRINCIPAL, styles.TAMANO_NORMAL),
                                    bg=styles.COLOR_EXITO, 
                                    fg=styles.COLOR_BLANCO,
                                    width=20,
                                    command=self.abrirAgregarProducto)
        self.btnAgregar.pack(side=tk.LEFT, padx=(0, 10))
        
        # Botón Editar
        self.btnEditar = tk.Button(buttonFrame, 
                                   text="Editar Producto", 
                                   font=(styles.FUENTE_PRINCIPAL, styles.TAMANO_NORMAL),
                                   bg=styles.COLOR_INFO, 
                                   fg=styles.COLOR_BLANCO,
                                   width=20,
                                   state=tk.DISABLED,
                                   command=self.abrirEditarProducto)
        self.btnEditar.pack(side=tk.LEFT, padx=(0, 10))
        
        # Botón Detalles/Inventario
        self.btnDetalles = tk.Button(buttonFrame, 
                                     text="Ver Detalles/Inventario", 
                                     font=(styles.FUENTE_PRINCIPAL, styles.TAMANO_NORMAL),
                                     bg=styles.COLOR_BOTON_5, 
                                     fg=styles.COLOR_BLANCO,
                                     width=20,
                                     state=tk.DISABLED,
                                     command=self.abrirDetallesInventario)
        self.btnDetalles.pack(side=tk.LEFT, padx=(0, 10))
        
        # Botón Cerrar
        btnCerrar = tk.Button(buttonFrame, 
                              text="Cerrar", 
                              font=(styles.FUENTE_PRINCIPAL, styles.TAMANO_NORMAL),
                              bg=styles.COLOR_TEXTO_MEDIO, 
                              fg=styles.COLOR_BLANCO,
                              width=15,
                              command=self.window.destroy)
        btnCerrar.pack(side=tk.RIGHT)
        
        # Separador
        separator = tk.Frame(mainFrame, height=2, bg=styles.COLOR_BORDE)
        separator.pack(fill=tk.X, pady=(0, 10))
        
        # Frame para la tabla (Treeview)
        tableFrame = tk.Frame(mainFrame, bg=styles.COLOR_FONDO)
        tableFrame.pack(fill=tk.BOTH, expand=True)
        
        # Crear Treeview con columnas para productos
        columns = ("ID", "Nombre", "Marca", "Categoría", "Precio Venta", 
                  "Precio Compra", "Color", "Talla", "Stock", "Alarma")
        self.tree = ttk.Treeview(tableFrame, columns=columns, show="headings", height=15)
        
        # Configurar columnas
        column_configs = [
            ("ID", "ID", 60, "center"),
            ("Nombre", "Nombre Producto", 200, "center"),
            ("Marca", "Marca", 100, "center"),
            ("Categoría", "Categoría", 120, "center"),
            ("Precio Venta", "Precio Venta", 100, "center"),
            ("Precio Compra", "Precio Compra", 100, "center"),
            ("Color", "Color", 80, "center"),
            ("Talla", "Talla", 70, "center"),
            ("Stock", "Stock Total", 80, "center"),
            ("Alarma", "Alarma Cap", 80, "center")
        ]
        
        for i, (col, heading, width, anchor) in enumerate(column_configs):
            self.tree.heading(col, text=heading)
            self.tree.column(col, width=width, anchor=anchor)

        # Configurar estilo para el Treeview
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configurar estilo global para Treeview
        style.configure("Treeview",
                        background=styles.COLOR_FONDO,
                        foreground=styles.COLOR_TEXTO_OSCURO,
                        fieldbackground=styles.COLOR_FONDO,
                        borderwidth=1,
                        rowheight=25)
        
        # Configurar específicamente los headings
        style.configure("Treeview.Heading", 
                        background=styles.COLOR_TREEVIEW_HEADING,
                        foreground=styles.COLOR_TEXTO_OSCURO,
                        font=(styles.FUENTE_PRINCIPAL, styles.TAMANO_NORMAL, styles.PESO_NEGRITA),
                        relief="flat",
                        padding=(5, 5))
        
        # Configurar color de selección
        style.map('Treeview',
                  background=[('selected', styles.COLOR_TREEVIEW_SELECTION)],
                  foreground=[('selected', styles.COLOR_TEXTO_OSCURO)])
        
        # Configurar colores para filas alternas
        self.tree.tag_configure('odd', background=styles.COLOR_TREEVIEW_ODD)
        self.tree.tag_configure('even', background=styles.COLOR_TREEVIEW_EVEN)
        # Configurar color para stock bajo
        self.tree.tag_configure('bajo_stock', background='#FFF3CD', foreground=styles.COLOR_TEXTO_OSCURO)

        # Scrollbar
        scrollbar = ttk.Scrollbar(tableFrame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Layout Treeview y Scrollbar
        self.tree.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")
        
        # Configurar grid para expansión
        tableFrame.grid_rowconfigure(0, weight=1)
        tableFrame.grid_columnconfigure(0, weight=1)
        
        # Frame para botones inferiores
        bottomFrame = tk.Frame(mainFrame, bg=styles.COLOR_FONDO)
        bottomFrame.pack(fill=tk.X, pady=(10, 0))
        
        # Botón Eliminar
        self.btnEliminar = tk.Button(bottomFrame, 
                                     text="Eliminar Producto Seleccionado", 
                                     font=(styles.FUENTE_PRINCIPAL, styles.TAMANO_NORMAL),
                                     bg=styles.COLOR_PELIGRO, 
                                     fg=styles.COLOR_BLANCO,
                                     width=25,
                                     state=tk.DISABLED,
                                     command=self.eliminarProducto)
        self.btnEliminar.pack(side=tk.LEFT, padx=(0, 20))
        
        # Evento de selección en Treeview
        self.tree.bind("<<TreeviewSelect>>", self.onTreeSelect)
        
        # Variables para control de selección
        self.productoSeleccionado = None
        self.productoNombre = None
    
    def loadProductos(self):
        """Carga los productos desde la base de datos usando vista optimizada"""
        # Limpiar tabla
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Obtener productos usando vista optimizada
        productos = self.db.get_productos_tienda_completo()
        
        if productos:
            # Ordenar por ID para consistencia
            productos_ordenados = sorted(productos, key=lambda x: x['id_productostienda'])
            
            for i, producto in enumerate(productos_ordenados):
                # Determinar tag para fila alternada
                tag_actual = 'even' if i % 2 == 0 else 'odd'
                
                # Verificar si stock está bajo alarma
                stock_total = producto.get('stock_total', 0)
                alarma_cap = producto.get('alarma_cap', 5)
                if stock_total < alarma_cap:
                    tag_actual = 'bajo_stock'
                
                # Insertar con tag
                self.tree.insert("", tk.END, 
                                values=(producto['id_productostienda'],
                                       producto['nombre_producto_tienda'],
                                       producto['nombre_marca'],
                                       producto['nombre_categoria'],
                                       f"₡{producto['precio_venta']:,.2f}",
                                       f"₡{producto['precio_compra']:,.2f}" if producto['precio_compra'] else "",
                                       producto['color'] or "",
                                       producto['talla'] or "",
                                       stock_total,
                                       alarma_cap),
                                tags=(tag_actual,))
    
    def onTreeSelect(self, event):
        """Maneja la selección de un producto en el Treeview"""
        selection = self.tree.selection()
        if selection:
            # Habilitar botones de edición, detalles y eliminación
            self.btnEditar.config(state=tk.NORMAL)
            self.btnDetalles.config(state=tk.NORMAL)
            self.btnEliminar.config(state=tk.NORMAL)
            
            # Guardar el producto seleccionado
            item = self.tree.item(selection[0])
            self.productoSeleccionado = item['values'][0]  # ID
            self.productoNombre = item['values'][1]  # Nombre
        else:
            self.btnEditar.config(state=tk.DISABLED)
            self.btnDetalles.config(state=tk.DISABLED)
            self.btnEliminar.config(state=tk.DISABLED)
            self.productoSeleccionado = None
            self.productoNombre = None
    
    def abrirAgregarProducto(self):
        """Abre ventana para agregar nuevo producto"""
        try:
            from ventanaDetalleProductoTienda import VentanaDetalleProductoTienda
            VentanaDetalleProductoTienda(self.window, "Agregar Producto", None, self)
        except ImportError as e:
            messagebox.showerror("Error", f"No se pudo abrir formulario de producto: {e}")
    
    def abrirEditarProducto(self):
        """Abre ventana para editar producto existente"""
        if self.productoSeleccionado:
            try:
                from ventanaDetalleProductoTienda import VentanaDetalleProductoTienda
                VentanaDetalleProductoTienda(self.window, "Editar Producto", 
                                           self.productoSeleccionado, self)
            except ImportError as e:
                messagebox.showerror("Error", f"No se pudo abrir formulario de edición: {e}")
        else:
            messagebox.showwarning("Selección requerida", 
                                 "Por favor seleccione un producto para editar")
    
    def abrirDetallesInventario(self):
        """Abre ventana para ver detalles del inventario del producto"""
        if self.productoSeleccionado:
            try:
                from ventanaDistribucionInventario import VentanaDistribucionInventario
                
                # Crear ventana de detalles pasando self como callback
                ventana_detalles = VentanaDistribucionInventario(
                    self.window, 
                    self.productoSeleccionado, 
                    self.productoNombre, 
                    self,  # Pasar self como callback para poder refrescar
                    modo="detalles"
                )
                
            except ImportError as e:
                messagebox.showerror("Error", f"No se pudo abrir detalles de inventario: {e}")
        else:
            messagebox.showwarning("Selección requerida", 
                                 "Por favor seleccione un producto para ver detalles")
    
    def eliminarProducto(self):
        """Elimina el producto seleccionado"""
        if not self.productoSeleccionado:
            return
        
        # Confirmar eliminación
        confirm = messagebox.askyesno("Confirmar eliminación", 
                                     f"¿Está seguro de eliminar el producto '{self.productoNombre}'?\n\n"
                                     "Esta acción eliminará también todo el inventario asociado.")
        if not confirm:
            return
        
        try:
            success, message = self.db.delete_producto_tienda(self.productoSeleccionado)
            if success:
                messagebox.showinfo("Éxito", message)
                self.loadProductos()  # Refrescar tabla
                self.productoSeleccionado = None
                self.productoNombre = None
                self.btnEditar.config(state=tk.DISABLED)
                self.btnDetalles.config(state=tk.DISABLED)
                self.btnEliminar.config(state=tk.DISABLED)
            else:
                messagebox.showwarning("Error al eliminar", message)
        except Exception as e:
            messagebox.showerror("Error", f"Error al eliminar producto: {e}")
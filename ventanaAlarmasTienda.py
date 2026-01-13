"""
Ventana para visualizar PRODUCTOS TIENDA con alarmas (agotados o a reponer)
Solo lectura - no permite agregar/editar/eliminar productos
"""

import tkinter as tk
from tkinter import ttk, messagebox
import styles
from db import Database

class VentanaAlarmasTienda:
    def __init__(self, parent, systemName):
        self.parent = parent
        self.systemName = systemName
        self.db = Database()
        
        # Crear ventana emergente
        self.window = tk.Toplevel(parent)
        self.window.title(f"Alarmas de Productos TIENDA - {systemName}")
        self.window.geometry("1200x800")  
        self.window.configure(bg=styles.COLOR_FONDO)
        self.window.transient(parent)
        self.window.grab_set()
        
        # Centrar ventana
        self.centerWindow(1200, 800) 
        
        # Crear interfaz
        self.createWidgets()
        self.loadAlarmas()
    
    def centerWindow(self, width, height):
        """Centra la ventana en la pantalla"""
        screenWidth = self.window.winfo_screenwidth()
        screenHeight = self.window.winfo_screenheight()
        x = (screenWidth // 2) - (width // 2)
        y = (screenHeight // 2) - (height // 2)
        self.window.geometry(f"{width}x{height}+{x}+{y}")
    
    def createWidgets(self):
        """Crea todos los widgets de la ventana"""
        # Frame principal
        mainFrame = tk.Frame(self.window, bg=styles.COLOR_FONDO, padx=20, pady=20)
        mainFrame.pack(fill=tk.BOTH, expand=True)
        
        # Título específico para TIENDA
        title = tk.Label(mainFrame, 
                        text="ALARMAS DE PRODUCTOS TIENDA - PRODUCTOS CON STOCK BAJO", 
                        font=(styles.FUENTE_PRINCIPAL, styles.TAMANO_TITULO, styles.PESO_NEGRITA),
                        bg=styles.COLOR_FONDO, 
                        fg=styles.COLOR_PELIGRO)
        title.pack(pady=(0, 15))
        
        # Leyenda de colores específica para TIENDA
        legendFrame = tk.Frame(mainFrame, bg=styles.COLOR_FONDO)
        legendFrame.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(legendFrame, 
                text="PRODUCTOS AGOTADOS", 
                font=(styles.FUENTE_PRINCIPAL, styles.TAMANO_PEQUENO, styles.PESO_NEGRITA),
                bg=styles.COLOR_AGOTADO, 
                fg=styles.COLOR_BLANCO,
                padx=10, pady=2).pack(side=tk.LEFT, padx=(0, 20))
        
        tk.Label(legendFrame, 
                text="PRODUCTOS A REPONER", 
                font=(styles.FUENTE_PRINCIPAL, styles.TAMANO_PEQUENO, styles.PESO_NEGRITA),
                bg=styles.COLOR_REPONER, 
                fg=styles.COLOR_BLANCO,
                padx=10, pady=2).pack(side=tk.LEFT)
        
        # Información adicional para TIENDA
        infoLabel = tk.Label(mainFrame,
                            text="Esta vista muestra solo productos TIENDA con stock por debajo del nivel mínimo de alarma",
                            font=(styles.FUENTE_PRINCIPAL, styles.TAMANO_PEQUENO),
                            bg=styles.COLOR_FONDO,
                            fg=styles.COLOR_TEXTO_MEDIO)
        infoLabel.pack(pady=(0, 10))
        
        # Separador
        separator = tk.Frame(mainFrame, height=2, bg=styles.COLOR_BORDE)
        separator.pack(fill=tk.X, pady=(0, 10))
        
        # Frame para la tabla (Treeview) - COLUMNAS ESPECÍFICAS PARA TIENDA
        tableFrame = tk.Frame(mainFrame, bg=styles.COLOR_FONDO)
        tableFrame.pack(fill=tk.BOTH, expand=True)
        
        # Columnas específicas para TIENDA
        columns = ("ID", "Nombre", "Marca", "Categoría", "Precio Venta", "Estado", "Stock Actual", "Alarma Mínima", "Ubicaciones")
        
        # AUMENTAR height del Treeview de 15 a 18
        self.tree = ttk.Treeview(tableFrame, columns=columns, show="headings", height=18)
        
        # Configurar columnas para TIENDA
        column_configs = [
            ("ID", "ID", 60, "center"),
            ("Nombre", "Nombre Producto", 180, "center"),
            ("Marca", "Marca", 90, "center"),
            ("Categoría", "Categoría", 110, "center"),
            ("Precio Venta", "Precio Venta", 100, "center"),
            ("Estado", "Estado", 90, "center"),
            ("Stock Actual", "Stock Actual", 100, "center"),
            ("Alarma Mínima", "Alarma Mín.", 100, "center"),
            ("Ubicaciones", "N° Ubicaciones", 100, "center")
        ]
        
        for i, (col, heading, width, anchor) in enumerate(column_configs):
            self.tree.heading(col, text=heading)
            self.tree.column(col, width=width, anchor=anchor)

        # Configurar estilo para el Treeview
        style = ttk.Style()
        style.theme_use('clam')
        
        style.configure("Treeview",
                        background=styles.COLOR_FONDO,
                        foreground=styles.COLOR_TEXTO_OSCURO,
                        fieldbackground=styles.COLOR_FONDO,
                        borderwidth=1,
                        rowheight=25)
        
        style.configure("Treeview.Heading", 
                        background=styles.COLOR_TREEVIEW_HEADING,
                        foreground=styles.COLOR_TEXTO_OSCURO,
                        font=(styles.FUENTE_PRINCIPAL, styles.TAMANO_NORMAL, styles.PESO_NEGRITA),
                        relief="flat",
                        padding=(5, 5))
        
        style.map('Treeview',
                  background=[('selected', styles.COLOR_TREEVIEW_SELECTION)],
                  foreground=[('selected', styles.COLOR_TEXTO_OSCURO)])
        
        # Configurar colores para alarmas TIENDA
        self.tree.tag_configure('agotado', background='#F8D7DA', foreground=styles.COLOR_TEXTO_OSCURO)
        self.tree.tag_configure('reponer', background='#FFF3CD', foreground=styles.COLOR_TEXTO_OSCURO)

        # Scrollbar
        scrollbar = ttk.Scrollbar(tableFrame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Layout Treeview y Scrollbar
        self.tree.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")
        
        # Configurar grid para expansión
        tableFrame.grid_rowconfigure(0, weight=1)
        tableFrame.grid_columnconfigure(0, weight=1)
        
        # AUMENTAR pady superior para botones
        bottomFrame = tk.Frame(mainFrame, bg=styles.COLOR_FONDO)
        bottomFrame.pack(fill=tk.X, pady=(20, 0))  # CAMBIADO: 10 -> 20
        
        # Botón Ver Detalles TIENDA
        self.btnDetalles = tk.Button(bottomFrame, 
                                     text="Ver Detalles del Producto", 
                                     font=(styles.FUENTE_PRINCIPAL, styles.TAMANO_NORMAL),
                                     bg=styles.COLOR_TIENDA, 
                                     fg=styles.COLOR_BLANCO,
                                     width=25,
                                     state=tk.DISABLED,
                                     command=self.abrirDetallesProducto)
        self.btnDetalles.pack(side=tk.LEFT, padx=(0, 20))
        
        # Botón Actualizar TIENDA
        btnActualizar = tk.Button(bottomFrame, 
                                 text="Actualizar Alarmas", 
                                 font=(styles.FUENTE_PRINCIPAL, styles.TAMANO_NORMAL),
                                 bg=styles.COLOR_EXITO, 
                                 fg=styles.COLOR_BLANCO,
                                 width=20,
                                 command=self.loadAlarmas)
        btnActualizar.pack(side=tk.LEFT, padx=(0, 20))
        
        # Botón Cerrar
        btnCerrar = tk.Button(bottomFrame, 
                              text="Cerrar", 
                              font=(styles.FUENTE_PRINCIPAL, styles.TAMANO_NORMAL),
                              bg=styles.COLOR_TEXTO_MEDIO, 
                              fg=styles.COLOR_BLANCO,
                              width=15,
                              command=self.window.destroy)
        btnCerrar.pack(side=tk.RIGHT)
        
        # Evento de selección
        self.tree.bind("<<TreeviewSelect>>", self.onTreeSelect)
        
        # Variables para control
        self.productoSeleccionado = None
        self.productoNombre = None
    
    def loadAlarmas(self):
        """Carga las alarmas de productos TIENDA"""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Obtener alarmas TIENDA desde vista
        alarmas = self.db.get_alarmas_tienda()
        
        if alarmas:
            # Para cada alarma, necesitamos información completa del producto
            productos_completos = self.db.get_productos_tienda_completo()
            
            for alarma in alarmas:
                # Buscar producto completo para obtener marca y categoría
                producto_completo = None
                for prod in productos_completos:
                    if prod['id_productostienda'] == alarma['id_productostienda']:
                        producto_completo = prod
                        break
                
                # Determinar tag según estado
                if alarma['estado'] == 'AGOTADO':
                    tag_actual = 'agotado'
                else:  # 'A REPONER'
                    tag_actual = 'reponer'
                
                # Formatear precio
                precio_venta_str = "N/A"
                if producto_completo and producto_completo.get('precio_venta'):
                    precio_venta_str = f"₡{producto_completo['precio_venta']:,.2f}"
                
                # Insertar en tabla
                self.tree.insert("", tk.END, 
                                values=(alarma['id_productostienda'],
                                       alarma['nombre_producto'],
                                       producto_completo['nombre_marca'] if producto_completo else "N/A",
                                       producto_completo['nombre_categoria'] if producto_completo else "N/A",
                                       precio_venta_str,
                                       alarma['estado'],
                                       alarma['cantidad_total'],
                                       alarma['alarma_cap'],
                                       alarma['num_ubicaciones']),
                                tags=(tag_actual,))
    
    def onTreeSelect(self, event):
        """Maneja la selección de un producto TIENDA"""
        selection = self.tree.selection()
        if selection:
            self.btnDetalles.config(state=tk.NORMAL)
            item = self.tree.item(selection[0])
            self.productoSeleccionado = item['values'][0]
            self.productoNombre = item['values'][1]
        else:
            self.btnDetalles.config(state=tk.DISABLED)
            self.productoSeleccionado = None
            self.productoNombre = None
    
    def abrirDetallesProducto(self):
        """Abre ventana para ver detalles del producto TIENDA seleccionado"""
        if not self.productoSeleccionado:
            return
        
        try:
            from ventanaDistribucionInventario import VentanaDistribucionInventario
            
            ventana_detalles = VentanaDistribucionInventario(
                self.window, 
                self.productoSeleccionado, 
                self.productoNombre, 
                sistema="tienda",
                callback_obj=self,  # IMPORTANTE: Pasar self como callback
                modo="detalles"
            )
            
        except ImportError as e:
            messagebox.showerror("Error", f"No se pudo abrir detalles del producto: {e}")
    
    def actualizarTabla(self):
        """Método para que otras ventanas puedan actualizar esta tabla"""
        self.loadAlarmas()
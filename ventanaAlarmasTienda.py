"""
Ventana para visualizar PRODUCTOS TIENDA con alarmas (agotados o a reponer)
"""

import tkinter as tk
from tkinter import ttk, messagebox
import styles
from db import Database

class VentanaAlarmasTienda:
    # ===== INICIALIZACIÓN =====
    def __init__(self, parent, systemName):
        self.parent = parent
        self.systemName = systemName
        self.db = Database()
        
        self.window = tk.Toplevel(parent)
        self.window.title(f"Alarmas de Productos TIENDA - {systemName}")
        self.window.geometry("1300x900")  
        self.window.configure(bg=styles.COLOR_FONDO_OSCURO)
        self.window.transient(parent)
        self.window.grab_set()
        
        self.centerWindow(1300, 900)
        self.createWidgets()
        self.loadAlarmas()
    
    # ===== MÉTODOS DE CONFIGURACIÓN DE VENTANA =====
    def centerWindow(self, width, height):
        screenWidth = self.window.winfo_screenwidth()
        screenHeight = self.window.winfo_screenheight()
        x = (screenWidth // 2) - (width // 2)
        y = (screenHeight // 2) - (height // 2)
        self.window.geometry(f"{width}x{height}+{x}+{y}")
    
    # ===== CREACIÓN DE INTERFAZ =====
    def createWidgets(self):
        mainFrame = tk.Frame(self.window, bg=styles.COLOR_FONDO_OSCURO, padx=20, pady=20)
        mainFrame.pack(fill=tk.BOTH, expand=True)
        
        title = tk.Label(mainFrame, 
                        text="ALARMAS DE PRODUCTOS TIENDA - PRODUCTOS CON STOCK BAJO", 
                        font=(styles.FUENTE_PRINCIPAL, styles.TAMANO_TITULO, styles.PESO_NEGRITA),
                        bg=styles.COLOR_FONDO_OSCURO, 
                        fg=styles.COLOR_PELIGRO)
        title.pack(pady=(0, 15))
        
        legendFrame = tk.Frame(mainFrame, bg=styles.COLOR_FONDO_OSCURO)
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
        
        infoLabel = tk.Label(mainFrame,
                            text="Esta vista muestra solo productos TIENDA con stock por debajo del nivel mínimo de alarma",
                            font=(styles.FUENTE_PRINCIPAL, styles.TAMANO_PEQUENO),
                            bg=styles.COLOR_FONDO_OSCURO,
                            fg=styles.COLOR_BLANCO)
        infoLabel.pack(pady=(0, 10))
        
        separator = tk.Frame(mainFrame, height=2, bg=styles.COLOR_BORDE)
        separator.pack(fill=tk.X, pady=(0, 10))
        
        tableFrame = tk.Frame(mainFrame, bg=styles.COLOR_FONDO)
        tableFrame.pack(fill=tk.BOTH, expand=True)
        
        columns = ("ID", "Nombre", "Marca", "Categoría", "Precio Venta", "Estado", "Stock Actual", "Alarma Mínima", "Ubicaciones")
        self.tree = ttk.Treeview(tableFrame, columns=columns, show="headings", height=18)
        
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
                        foreground=styles.COLOR_BLANCO,
                        font=(styles.FUENTE_PRINCIPAL, styles.TAMANO_NORMAL, styles.PESO_NEGRITA),
                        relief="flat",
                        padding=(5, 5))
        
        style.map('Treeview',
                  background=[('selected', styles.COLOR_TREEVIEW_SELECTION)],
                  foreground=[('selected', styles.COLOR_TEXTO_OSCURO)])
        
        self.tree.tag_configure('agotado', background='#F8D7DA', foreground=styles.COLOR_TEXTO_OSCURO)
        self.tree.tag_configure('reponer', background='#FFF3CD', foreground=styles.COLOR_TEXTO_OSCURO)

        scrollbar = ttk.Scrollbar(tableFrame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")
        
        tableFrame.grid_rowconfigure(0, weight=1)
        tableFrame.grid_columnconfigure(0, weight=1)
        
        bottomFrame = tk.Frame(mainFrame, bg=styles.COLOR_FONDO_OSCURO)
        bottomFrame.pack(fill=tk.X, pady=(20, 0))
        
        self.btnDetalles = tk.Button(bottomFrame, 
                                     text="Ver Detalles del Producto", 
                                     font=(styles.FUENTE_PRINCIPAL, styles.TAMANO_NORMAL),
                                     bg=styles.COLOR_TIENDA, 
                                     fg=styles.COLOR_BLANCO,
                                     width=25,
                                     state=tk.DISABLED,
                                     command=self.abrirDetallesProducto)
        self.btnDetalles.pack(side=tk.LEFT, padx=(0, 20))
        
        btnActualizar = tk.Button(bottomFrame, 
                                 text="Actualizar Alarmas", 
                                 font=(styles.FUENTE_PRINCIPAL, styles.TAMANO_NORMAL),
                                 bg=styles.COLOR_EXITO, 
                                 fg=styles.COLOR_BLANCO,
                                 width=20,
                                 command=self.loadAlarmas)
        btnActualizar.pack(side=tk.LEFT, padx=(0, 20))
        
        btnCerrar = tk.Button(bottomFrame, 
                              text="Cerrar", 
                              font=(styles.FUENTE_PRINCIPAL, styles.TAMANO_NORMAL),
                              bg=styles.COLOR_TEXTO_MEDIO, 
                              fg=styles.COLOR_BLANCO,
                              width=15,
                              command=self.window.destroy)
        btnCerrar.pack(side=tk.RIGHT)
        
        self.tree.bind("<<TreeviewSelect>>", self.onTreeSelect)
        
        self.productoSeleccionado = None
        self.productoNombre = None
    
    # ===== CARGA DE ALARMAS =====
    def loadAlarmas(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        alarmas = self.db.get_alarmas_tienda()
        
        if alarmas:
            productos_completos = self.db.get_productos_tienda_completo()
            
            for alarma in alarmas:
                producto_completo = None
                for prod in productos_completos:
                    if prod['id_productostienda'] == alarma['id_productostienda']:
                        producto_completo = prod
                        break
                
                tag_actual = 'agotado' if alarma['estado'] == 'AGOTADO' else 'reponer'
                
                precio_venta_str = "N/A"
                if producto_completo and producto_completo.get('precio_venta'):
                    precio_venta_str = f"₡{producto_completo['precio_venta']:,.2f}"
                
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
    
    # ===== EVENTOS =====
    def onTreeSelect(self, event):
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
    
    # ===== MÉTODOS AUXILIARES =====
    def abrirDetallesProducto(self):
        if not self.productoSeleccionado:
            return
        
        try:
            from ventanaDistribucionInventario import VentanaDistribucionInventario
            
            ventana_detalles = VentanaDistribucionInventario(
                self.window, 
                self.productoSeleccionado, 
                self.productoNombre, 
                sistema="tienda",
                callback_obj=self,
                modo="detalles"
            )
            
        except ImportError as e:
            messagebox.showerror("Error", f"No se pudo abrir detalles del producto: {e}")
    
    def actualizarTabla(self):
        self.loadAlarmas()
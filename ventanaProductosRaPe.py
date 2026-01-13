"""
Ventana CRUD para gestión de Materiales RA-PE
"""

import tkinter as tk
from tkinter import ttk, messagebox
import styles
from db import Database

class VentanaProductosRaPe:
    def __init__(self, parent, systemName):
        self.parent = parent
        self.systemName = systemName
        self.db = Database()
        
        # Crear ventana emergente
        self.window = tk.Toplevel(parent)
        self.window.title(f"Gestión de Materiales RA-PE - {systemName}")
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
        
        # Título con leyenda
        titleFrame = tk.Frame(mainFrame, bg=styles.COLOR_FONDO)
        titleFrame.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(titleFrame, 
                text="GESTIÓN DE MATERIALES RA-PE", 
                font=(styles.FUENTE_PRINCIPAL, styles.TAMANO_TITULO, styles.PESO_NEGRITA),
                bg=styles.COLOR_FONDO, 
                fg=styles.COLOR_TEXTO_OSCURO).pack()
        
        tk.Label(titleFrame, 
                text="⚠ Los materiales en AMARILLO tienen stock por debajo del nivel mínimo", 
                font=(styles.FUENTE_PRINCIPAL, styles.TAMANO_PEQUENO),
                bg=styles.COLOR_FONDO, 
                fg=styles.COLOR_ADVERTENCIA).pack(pady=(5, 0))
        
        # Frame para botones de acción principales
        buttonFrame = tk.Frame(mainFrame, bg=styles.COLOR_FONDO)
        buttonFrame.pack(fill=tk.X, pady=(0, 15))
        
        # Botón Agregar Material
        self.btnAgregar = tk.Button(buttonFrame, 
                                    text="Agregar Nuevo Material", 
                                    font=(styles.FUENTE_PRINCIPAL, styles.TAMANO_NORMAL),
                                    bg=styles.COLOR_EXITO, 
                                    fg=styles.COLOR_BLANCO,
                                    width=20,
                                    command=self.abrirAgregarMaterial)
        self.btnAgregar.pack(side=tk.LEFT, padx=(0, 10))
        
        # Botón Editar
        self.btnEditar = tk.Button(buttonFrame, 
                                   text="Editar Material", 
                                   font=(styles.FUENTE_PRINCIPAL, styles.TAMANO_NORMAL),
                                   bg=styles.COLOR_INFO, 
                                   fg=styles.COLOR_BLANCO,
                                   width=20,
                                   state=tk.DISABLED,
                                   command=self.abrirEditarMaterial)
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
        
        # Crear Treeview con columnas para materiales RA-PE
        columns = ("ID", "Nombre", "Marca", "Categoría", "Stock", "Alarma")
        self.tree = ttk.Treeview(tableFrame, columns=columns, show="headings", height=15)
        
        # Configurar columnas
        column_configs = [
            ("ID", "ID", 60, "center"),
            ("Nombre", "Nombre Material", 200, "center"),
            ("Marca", "Marca", 100, "center"),
            ("Categoría", "Categoría", 120, "center"),
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
                                     text="Eliminar Material Seleccionado", 
                                     font=(styles.FUENTE_PRINCIPAL, styles.TAMANO_NORMAL),
                                     bg=styles.COLOR_PELIGRO, 
                                     fg=styles.COLOR_BLANCO,
                                     width=25,
                                     state=tk.DISABLED,
                                     command=self.eliminarMaterial)
        self.btnEliminar.pack(side=tk.LEFT, padx=(0, 20))
        
        # Evento de selección en Treeview
        self.tree.bind("<<TreeviewSelect>>", self.onTreeSelect)
        
        # Variables para control de selección
        self.materialSeleccionado = None
        self.materialNombre = None
    
    def loadProductos(self):
        """Carga los materiales RA-PE desde la base de datos"""
        # Limpiar tabla
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Obtener materiales usando vista optimizada
        materiales = self.db.get_productos_rape_completo()
        
        if materiales:
            # Ordenar por ID para consistencia
            materiales_ordenados = sorted(materiales, key=lambda x: x['id_productosrape'])
            
            for i, material in enumerate(materiales_ordenados):
                # Determinar tag para fila alternada
                tag_actual = 'even' if i % 2 == 0 else 'odd'
                
                # Verificar si stock está bajo alarma
                stock_total = material.get('stock_total', 0)
                alarma_cap = material.get('alarma_cap', 5)
                if stock_total < alarma_cap:
                    tag_actual = 'bajo_stock'
                
                # Insertar con tag
                self.tree.insert("", tk.END, 
                                values=(material['id_productosrape'],
                                       material['nombre_producto_rape'],
                                       material['nombre_marca'],
                                       material['nombre_categoria'],
                                       stock_total,
                                       alarma_cap),
                                tags=(tag_actual,))
    
    def onTreeSelect(self, event):
        """Maneja la selección de un material en el Treeview"""
        selection = self.tree.selection()
        if selection:
            # Habilitar botones de edición, detalles y eliminación
            self.btnEditar.config(state=tk.NORMAL)
            self.btnDetalles.config(state=tk.NORMAL)
            self.btnEliminar.config(state=tk.NORMAL)
            
            # Guardar el material seleccionado
            item = self.tree.item(selection[0])
            self.materialSeleccionado = item['values'][0]  # ID
            self.materialNombre = item['values'][1]  # Nombre
        else:
            self.btnEditar.config(state=tk.DISABLED)
            self.btnDetalles.config(state=tk.DISABLED)
            self.btnEliminar.config(state=tk.DISABLED)
            self.materialSeleccionado = None
            self.materialNombre = None
    
    def abrirAgregarMaterial(self):
        """Abre ventana para agregar nuevo material"""
        try:
            from ventanaDetalleMaterialRaPe import VentanaDetalleMaterialRaPe
            VentanaDetalleMaterialRaPe(self.window, "Agregar Material RA-PE", None, self)
        except ImportError as e:
            messagebox.showerror("Error", f"No se pudo abrir formulario de material: {e}")
    
    def abrirEditarMaterial(self):
        """Abre ventana para editar material existente"""
        if self.materialSeleccionado:
            try:
                from ventanaDetalleMaterialRaPe import VentanaDetalleMaterialRaPe
                VentanaDetalleMaterialRaPe(self.window, "Editar Material RA-PE", 
                                         self.materialSeleccionado, self)
            except ImportError as e:
                messagebox.showerror("Error", f"No se pudo abrir formulario de edición: {e}")
        else:
            messagebox.showwarning("Selección requerida", 
                                 "Por favor seleccione un material para editar")
    
    def abrirDetallesInventario(self):
        """Abre ventana para ver detalles del inventario del material"""
        if self.materialSeleccionado:
            try:
                from ventanaDistribucionInventario import VentanaDistribucionInventario
                
                # Crear ventana de detalles pasando self como callback
                ventana_detalles = VentanaDistribucionInventario(
                    self.window, 
                    self.materialSeleccionado, 
                    self.materialNombre, 
                    sistema="rape",  # Especificar sistema RA-PE
                    callback_obj=self,
                    modo="detalles"
                )
                
            except ImportError as e:
                messagebox.showerror("Error", f"No se pudo abrir detalles de inventario: {e}")
        else:
            messagebox.showwarning("Selección requerida", 
                                 "Por favor seleccione un material para ver detalles")
    
    def eliminarMaterial(self):
        """Elimina el material seleccionado"""
        if not self.materialSeleccionado:
            return
        
        # Confirmar eliminación
        confirm = messagebox.askyesno("Confirmar eliminación", 
                                     f"¿Está seguro de eliminar el material '{self.materialNombre}'?\n\n"
                                     "Esta acción eliminará también todo el inventario asociado.")
        if not confirm:
            return
        
        try:
            success, message = self.db.delete_producto_rape(self.materialSeleccionado)
            if success:
                messagebox.showinfo("Éxito", message)
                self.loadProductos()  # Refrescar tabla
                self.materialSeleccionado = None
                self.materialNombre = None
                self.btnEditar.config(state=tk.DISABLED)
                self.btnDetalles.config(state=tk.DISABLED)
                self.btnEliminar.config(state=tk.DISABLED)
            else:
                messagebox.showwarning("Error al eliminar", message)
        except Exception as e:
            messagebox.showerror("Error", f"Error al eliminar material: {e}")
"""
Ventana para visualizar MATERIALES RA-PE con alarmas (agotados o a reponer)
"""

import tkinter as tk
from tkinter import ttk, messagebox
import styles
from db import Database

class VentanaAlarmasRaPe:
    # ===== INICIALIZACIÓN =====
    def __init__(self, parent, systemName):
        self.parent = parent
        self.systemName = systemName
        self.db = Database()
        
        self.window = tk.Toplevel(parent)
        self.window.title(f"Alarmas de Materiales RA-PE - {systemName}")
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
                        text="ALARMAS DE MATERIALES RA-PE - MATERIALES CON STOCK BAJO", 
                        font=(styles.FUENTE_PRINCIPAL, styles.TAMANO_TITULO, styles.PESO_NEGRITA),
                        bg=styles.COLOR_FONDO_OSCURO, 
                        fg=styles.COLOR_PELIGRO)
        title.pack(pady=(0, 15))
        
        legendFrame = tk.Frame(mainFrame, bg=styles.COLOR_FONDO_OSCURO)
        legendFrame.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(legendFrame, 
                text="MATERIALES AGOTADOS", 
                font=(styles.FUENTE_PRINCIPAL, styles.TAMANO_PEQUENO, styles.PESO_NEGRITA),
                bg=styles.COLOR_AGOTADO, 
                fg=styles.COLOR_BLANCO,
                padx=10, pady=2).pack(side=tk.LEFT, padx=(0, 20))
        
        tk.Label(legendFrame, 
                text="MATERIALES A REPONER", 
                font=(styles.FUENTE_PRINCIPAL, styles.TAMANO_PEQUENO, styles.PESO_NEGRITA),
                bg=styles.COLOR_REPONER, 
                fg=styles.COLOR_BLANCO,
                padx=10, pady=2).pack(side=tk.LEFT)
        
        infoLabel = tk.Label(mainFrame,
                            text="Esta vista muestra solo materiales RA-PE con stock por debajo del nivel mínimo de alarma",
                            font=(styles.FUENTE_PRINCIPAL, styles.TAMANO_PEQUENO),
                            bg=styles.COLOR_FONDO_OSCURO,
                            fg=styles.COLOR_BLANCO)
        infoLabel.pack(pady=(0, 10))
        
        separator = tk.Frame(mainFrame, height=2, bg=styles.COLOR_BORDE)
        separator.pack(fill=tk.X, pady=(0, 10))
        
        tableFrame = tk.Frame(mainFrame, bg=styles.COLOR_FONDO_OSCURO)
        tableFrame.pack(fill=tk.BOTH, expand=True)
        
        columns = ("ID", "Nombre", "Marca", "Categoría", "Estado", "Stock Actual", "Alarma Mínima", "Ubicaciones")
        self.tree = ttk.Treeview(tableFrame, columns=columns, show="headings", height=18)
        
        column_configs = [
            ("ID", "ID", 60, "center"),
            ("Nombre", "Nombre Material", 180, "center"),
            ("Marca", "Marca", 90, "center"),
            ("Categoría", "Categoría", 110, "center"),
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
                                     text="Ver Detalles del Material", 
                                     font=(styles.FUENTE_PRINCIPAL, styles.TAMANO_NORMAL),
                                     bg=styles.COLOR_RAPE, 
                                     fg=styles.COLOR_BLANCO,
                                     width=25,
                                     state=tk.DISABLED,
                                     command=self.abrirDetallesMaterial)
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
        
        self.materialSeleccionado = None
        self.materialNombre = None
    
    # ===== CARGA DE ALARMAS =====
    def loadAlarmas(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        alarmas = self.db.get_alarmas_rape()
        
        if alarmas:
            materiales_completos = self.db.get_productos_rape_completo()
            
            for alarma in alarmas:
                material_completo = None
                for mat in materiales_completos:
                    if mat['id_productosrape'] == alarma['id_productosrape']:
                        material_completo = mat
                        break
                
                tag_actual = 'agotado' if alarma['estado'] == 'AGOTADO' else 'reponer'
                
                self.tree.insert("", tk.END, 
                                values=(alarma['id_productosrape'],
                                       alarma['nombre_producto'],
                                       material_completo['nombre_marca'] if material_completo else "N/A",
                                       material_completo['nombre_categoria'] if material_completo else "N/A",
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
            self.materialSeleccionado = item['values'][0]
            self.materialNombre = item['values'][1]
        else:
            self.btnDetalles.config(state=tk.DISABLED)
            self.materialSeleccionado = None
            self.materialNombre = None
    
    # ===== MÉTODOS AUXILIARES =====
    def abrirDetallesMaterial(self):
        if not self.materialSeleccionado:
            return
        
        try:
            from ventanaDistribucionInventario import VentanaDistribucionInventario
            
            ventana_detalles = VentanaDistribucionInventario(
                self.window, 
                self.materialSeleccionado, 
                self.materialNombre, 
                sistema="rape",
                callback_obj=self,
                modo="detalles"
            )
            
        except ImportError as e:
            messagebox.showerror("Error", f"No se pudo abrir detalles del material: {e}")
    
    def actualizarTabla(self):
        self.loadAlarmas()
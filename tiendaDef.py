import tkinter as tk
from tkinter import messagebox
from baseSystem import BaseSystem
import styles

class TiendaSystem(BaseSystem):
    def __init__(self, root, return_callback, db_status="Conectado"):
        super().__init__(root, return_callback, "TIENDA", db_status)
        
        # Configurar botón específico de TIENDA
        self.btn_productos.config(text="PRODUCTOS TIENDA", command=self.open_productos_tienda)
        self.btn_excel.config(text="EXPORTAR EXCEL", command=self.exportar_excel_tienda)
        
        # Crear panel de alarmas específico para TIENDA
        self.create_alarm_panel_tienda()
    
    def create_alarm_panel_tienda(self):
        """Crea panel de alarmas específico para TIENDA"""
        alarm_frame = tk.Frame(self.main_frame, 
                              bg=styles.COLOR_ALARMA_FONDO, 
                              relief=tk.RIDGE, 
                              bd=styles.BORDE_GROSOR)
        alarm_frame.pack(anchor=tk.NE, pady=(0, styles.PADDING_Y))
        
        # Título específico para TIENDA
        alarm_title = tk.Label(alarm_frame, 
                              text="ALERTAS DE PRODUCTOS", 
                              font=(styles.FUENTE_PRINCIPAL, styles.TAMANO_ENCABEZADO, styles.PESO_NEGRITA),
                              bg=styles.COLOR_ALARMA_FONDO, 
                              fg=styles.COLOR_ALARMA_TEXTO)
        alarm_title.grid(row=0, column=0, columnspan=3, 
                        padx=styles.PADDING_X, pady=5, sticky="w")
        
        # Contadores específicos para TIENDA
        self.lbl_agotados = tk.Label(alarm_frame, 
                                    text="Productos agotados: 0",
                                    font=(styles.FUENTE_PRINCIPAL, styles.TAMANO_PEQUENO, styles.PESO_NORMAL),
                                    bg=styles.COLOR_ALARMA_FONDO, 
                                    fg=styles.COLOR_AGOTADO)
        self.lbl_agotados.grid(row=1, column=0, 
                              padx=styles.PADDING_X, pady=2, sticky="w")
        
        self.lbl_reponer = tk.Label(alarm_frame,
                                   text="Productos a reponer: 0", 
                                   font=(styles.FUENTE_PRINCIPAL, styles.TAMANO_PEQUENO, styles.PESO_NORMAL),
                                   bg=styles.COLOR_ALARMA_FONDO, 
                                   fg=styles.COLOR_REPONER)
        self.lbl_reponer.grid(row=2, column=0, 
                             padx=styles.PADDING_X, pady=2, sticky="w")
        
        # Botón para ver detalles (placeholder)
        btn_ver = tk.Button(alarm_frame, 
                           text="Ver Productos", 
                           font=(styles.FUENTE_PRINCIPAL, styles.TAMANO_MUY_PEQUENO, styles.PESO_NEGRITA),
                           bg=styles.COLOR_ALARMA_TEXTO, 
                           fg=styles.COLOR_BLANCO,
                           width=12,
                           cursor=styles.CURSOR_BOTON,
                           command=self.show_alarm_details_tienda)
        btn_ver.grid(row=1, column=1, rowspan=2, 
                    padx=5, pady=2)
        
        # Botón para actualizar (placeholder)
        btn_update = tk.Button(alarm_frame, 
                              text="Actualizar", 
                              font=(styles.FUENTE_PRINCIPAL, styles.TAMANO_MUY_PEQUENO),
                              bg=styles.COLOR_ALARMA_FONDO, 
                              fg=styles.COLOR_ALARMA_TEXTO,
                              width=8,
                              relief="flat",
                              cursor=styles.CURSOR_BOTON,
                              command=self.update_alarms_tienda)
        btn_update.grid(row=1, column=2, rowspan=2, 
                       padx=(0, styles.PADDING_X), pady=2)
    
    # ============================================
    # FUNCIONES ESPECÍFICAS DE TIENDA (PLACEHOLDERS)
    # ============================================
    
    def open_productos_tienda(self):
        """Placeholder para gestión de productos TIENDA"""
        print("[TIENDA] Abriendo gestión de productos...")
        messagebox.showinfo("Productos Tienda", 
                          "Gestión de productos TIENDA\n(En desarrollo)")
    
    def exportar_excel_tienda(self):
        """Placeholder para exportar a Excel TIENDA"""
        print("[TIENDA] Exportando a Excel...")
        messagebox.showinfo("Exportar Excel", 
                          "Exportando datos TIENDA a Excel\n(En desarrollo)")
    
    def show_alarm_details_tienda(self):
        """Placeholder para ver detalles de alarmas TIENDA"""
        print("[TIENDA] Mostrando detalles de alarmas...")
        messagebox.showinfo("Alarmas Tienda", 
                          "Mostrando productos con alertas TIENDA\n(En desarrollo)")
    
    def update_alarms_tienda(self):
        """Placeholder para actualizar alarmas TIENDA"""
        print("[TIENDA] Actualizando alarmas...")
        messagebox.showinfo("Actualizar Alarmas", 
                          "Actualizando alarmas TIENDA\n(En desarrollo)")
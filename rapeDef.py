import tkinter as tk
from tkinter import messagebox
from baseSystem import BaseSystem
import styles

class RAPESystem(BaseSystem):
    def __init__(self, root, return_callback):
        super().__init__(root, return_callback, "RA-PE")
        
        # Configurar botón específico de RA-PE
        self.btn_productos.config(text="MATERIALES RA-PE", command=self.open_materiales_rape)
        self.btn_excel.config(text="EXPORTAR EXCEL", command=self.exportar_excel_rape)
        
        # Crear panel de alarmas específico para RA-PE
        self.create_alarm_panel_rape()
    
    def create_alarm_panel_rape(self):
        """Crea panel de alarmas específico para RA-PE"""
        alarm_frame = tk.Frame(self.main_frame, 
                              bg=styles.COLOR_ALARMA_FONDO, 
                              relief=tk.RIDGE, 
                              bd=styles.BORDE_GROSOR)
        alarm_frame.pack(anchor=tk.NE, pady=(0, styles.PADDING_Y))
        
        # Título específico para RA-PE
        alarm_title = tk.Label(alarm_frame, 
                              text="ALERTAS DE MATERIALES", 
                              font=(styles.FUENTE_PRINCIPAL, styles.TAMANO_ENCABEZADO, styles.PESO_NEGRITA),
                              bg=styles.COLOR_ALARMA_FONDO, 
                              fg=styles.COLOR_ALARMA_TEXTO)
        alarm_title.grid(row=0, column=0, columnspan=3, 
                        padx=styles.PADDING_X, pady=5, sticky="w")
        
        # Contadores específicos para RA-PE
        self.lbl_agotados = tk.Label(alarm_frame, 
                                    text="Materiales agotados: 0",
                                    font=(styles.FUENTE_PRINCIPAL, styles.TAMANO_PEQUENO, styles.PESO_NORMAL),
                                    bg=styles.COLOR_ALARMA_FONDO, 
                                    fg=styles.COLOR_AGOTADO)
        self.lbl_agotados.grid(row=1, column=0, 
                              padx=styles.PADDING_X, pady=2, sticky="w")
        
        self.lbl_reponer = tk.Label(alarm_frame,
                                   text="Materiales a reponer: 0", 
                                   font=(styles.FUENTE_PRINCIPAL, styles.TAMANO_PEQUENO, styles.PESO_NORMAL),
                                   bg=styles.COLOR_ALARMA_FONDO, 
                                   fg=styles.COLOR_REPONER)
        self.lbl_reponer.grid(row=2, column=0, 
                             padx=styles.PADDING_X, pady=2, sticky="w")
        
        # Botón para ver detalles (placeholder)
        btn_ver = tk.Button(alarm_frame, 
                           text="Ver Materiales", 
                           font=(styles.FUENTE_PRINCIPAL, styles.TAMANO_MUY_PEQUENO, styles.PESO_NEGRITA),
                           bg=styles.COLOR_ALARMA_TEXTO, 
                           fg=styles.COLOR_BLANCO,
                           width=12,
                           cursor=styles.CURSOR_BOTON,
                           command=self.show_alarm_details_rape)
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
                              command=self.update_alarms_rape)
        btn_update.grid(row=1, column=2, rowspan=2, 
                       padx=(0, styles.PADDING_X), pady=2)
    
    # ============================================
    # FUNCIONES ESPECÍFICAS DE RA-PE (PLACEHOLDERS)
    # ============================================
    
    def open_materiales_rape(self):
        """Placeholder para gestión de materiales RA-PE"""
        print("[RA-PE] Abriendo gestión de materiales...")
        messagebox.showinfo("Materiales RA-PE", 
                          "Gestión de materiales RA-PE\n(En desarrollo)")
    
    def exportar_excel_rape(self):
        """Placeholder para exportar a Excel RA-PE"""
        print("[RA-PE] Exportando a Excel...")
        messagebox.showinfo("Exportar Excel", 
                          "Exportando datos RA-PE a Excel\n(En desarrollo)")
    
    def show_alarm_details_rape(self):
        """Placeholder para ver detalles de alarmas RA-PE"""
        print("[RA-PE] Mostrando detalles de alarmas...")
        messagebox.showinfo("Alarmas RA-PE", 
                          "Mostrando materiales con alertas RA-PE\n(En desarrollo)")
    
    def update_alarms_rape(self):
        """Placeholder para actualizar alarmas RA-PE"""
        print("[RA-PE] Actualizando alarmas...")
        messagebox.showinfo("Actualizar Alarmas", 
                          "Actualizando alarmas RA-PE\n(En desarrollo)")
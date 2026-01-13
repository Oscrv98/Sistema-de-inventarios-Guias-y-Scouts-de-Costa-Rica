import tkinter as tk
from tkinter import messagebox
from baseSystem import BaseSystem
import styles

class RAPESystem(BaseSystem):
    def __init__(self, root, return_callback, db_status="Conectado"):
        super().__init__(root, return_callback, "RA-PE", db_status)
        
        # Configurar botón específico de RA-PE
        self.btn_productos.config(text="MATERIALES RA-PE", command=self.open_materiales_rape)
        self.btn_excel.config(text="EXPORTAR EXCEL", command=self.exportar_excel_rape)
        
        # Crear panel de alarmas específico para RA-PE
        self.create_alarm_panel_rape()
        
        # Actualizar alarmas UNA SOLA VEZ al abrir el menú
        self.update_alarms_rape()
    
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
        
        # Contadores específicos para RA-PE (valores iniciales)
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
        
        # Botón para ver detalles de alarmas RA-PE
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
        
        # Botón para actualizar alarmas (refresh manual)
        btn_update = tk.Button(alarm_frame, 
                              text="Actualizar", 
                              font=(styles.FUENTE_PRINCIPAL, styles.TAMANO_MUY_PEQUENO),
                              bg=styles.COLOR_ALARMA_FONDO, 
                              fg=styles.COLOR_ALARMA_TEXTO,
                              width=8,
                              relief="flat",
                              cursor=styles.CURSOR_BOTON,
                              command=self.update_alarms_rape)  # Conectado a la función
        btn_update.grid(row=1, column=2, rowspan=2, 
                       padx=(0, styles.PADDING_X), pady=2)
    
    def update_alarms_rape(self):
        """Actualiza las alarmas de materiales RA-PE con datos reales de la BD"""
        try:
            # Importar Database aquí para evitar importaciones circulares
            from db import Database
            
            db = Database()
            alarmas = db.get_alarmas_rape()
            
            # Inicializar contadores
            agotados = 0
            reponer = 0
            
            # Contar alarmas por estado
            if alarmas:
                for a in alarmas:
                    if a['estado'] == 'AGOTADO':
                        agotados += 1
                    elif a['estado'] == 'A REPONER':
                        reponer += 1
            
            # Actualizar las etiquetas en pantalla
            self.lbl_agotados.config(text=f"Materiales agotados: {agotados}")
            self.lbl_reponer.config(text=f"Materiales a reponer: {reponer}")
            
            # Cambiar colores según prioridad
            if agotados > 0:
                self.lbl_agotados.config(fg=styles.COLOR_PELIGRO)  # Rojo para agotados
            else:
                # Volver al color original si no hay agotados
                self.lbl_agotados.config(fg=styles.COLOR_AGOTADO)
            
            if reponer > 0:
                self.lbl_reponer.config(fg=styles.COLOR_ADVERTENCIA)  # Amarillo/Naranja para reponer
            else:
                # Volver al color original si no hay por reponer
                self.lbl_reponer.config(fg=styles.COLOR_REPONER)
            
            # Debug en consola
            print(f"[RA-PE] Alarmas actualizadas: {agotados} agotados, {reponer} a reponer")
            if alarmas:
                for a in alarmas:
                    print(f"  - {a['nombre_producto']}: {a['estado']} (Stock: {a['cantidad_total']}, Alarma: {a['alarma_cap']})")
            
        except Exception as e:
            print(f"Error actualizando alarmas RA-PE: {e}")
            # Mostrar error en la interfaz
            self.lbl_agotados.config(text="Error cargando alarmas", fg=styles.COLOR_PELIGRO)
            self.lbl_reponer.config(text="Click en Actualizar", fg=styles.COLOR_ADVERTENCIA)
    
    # ============================================
    # FUNCIONES ESPECÍFICAS DE RA-PE
    # ============================================

    def open_materiales_rape(self):
        """Abre la ventana de gestión de materiales RA-PE"""
        try:
            from ventanaProductosRaPe import VentanaProductosRaPe
            VentanaProductosRaPe(self.root, self.system_name)
        except ImportError as e:
            messagebox.showerror("Error", f"No se pudo abrir gestión de materiales: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"Error al abrir materiales RA-PE: {e}")
    
    def exportar_excel_rape(self):
        """Placeholder para exportar a Excel RA-PE"""
        print("[RA-PE] Exportando a Excel...")
        messagebox.showinfo("Exportar Excel", 
                          "Exportando datos RA-PE a Excel\n(En desarrollo)")
    
    def show_alarm_details_rape(self):
        """Abre ventana para ver detalles de alarmas RA-PE"""
        try:
            # Intentar importar ventana específica de alarmas
            from ventanaAlarmaRape import VentanaAlarmasRaPe
            VentanaAlarmasRaPe(self.root, self.system_name)
        except ImportError as e:
            print(f"ventanaAlarmasRaPe no encontrada: {e}")
            # Si no existe, abrir la ventana principal de materiales
            self.open_materiales_rape()
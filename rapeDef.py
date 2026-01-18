import tkinter as tk
from tkinter import messagebox
from baseSystem import BaseSystem
import styles
from datetime import datetime
import os

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
                              command=self.update_alarms_rape)
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
                self.lbl_agotados.config(fg=styles.COLOR_PELIGRO)
            else:
                self.lbl_agotados.config(fg=styles.COLOR_AGOTADO)
            
            if reponer > 0:
                self.lbl_reponer.config(fg=styles.COLOR_ADVERTENCIA)
            else:
                self.lbl_reponer.config(fg=styles.COLOR_REPONER)
            
            # Debug en consola
            print(f"[RA-PE] Alarmas actualizadas: {agotados} agotados, {reponer} a reponer")
            if alarmas:
                for a in alarmas:
                    print(f"  - {a['nombre_producto']}: {a['estado']} (Stock: {a['cantidad_total']}, Alarma: {a['alarma_cap']})")
            
        except Exception as e:
            print(f"Error actualizando alarmas RA-PE: {e}")
            self.lbl_agotados.config(text="Error cargando alarmas", fg=styles.COLOR_PELIGRO)
            self.lbl_reponer.config(text="Click en Actualizar", fg=styles.COLOR_ADVERTENCIA)
    
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
        """Exporta datos de RA-PE a Excel con formato profesional"""
        try:
            # Importar openpyxl DENTRO de la función
            import openpyxl
            from openpyxl.styles import Font, Alignment, PatternFill
            
            from db import Database
            
            # Obtener datos
            db = Database()
            data = db.get_export_data_rape()  # ¡Necesitamos crear esta función!
            
            if not data['resumen'] and not data['detalle']:
                messagebox.showwarning("Sin datos", "No hay datos para exportar en RA-PE")
                return
            
            # Crear workbook
            wb = openpyxl.Workbook()
            
            # ============================================
            # HOJA 1: RESUMEN DE MATERIALES
            # ============================================
            ws1 = wb.active
            ws1.title = "Resumen Materiales"
            
            # Título
            fecha_actual = datetime.now().strftime("%d/%m/%Y %H:%M")
            ws1.merge_cells('A1:G1')
            title_cell = ws1['A1']
            title_cell.value = f"INVENTARIO RA-PE - Exportado el {fecha_actual}"
            title_cell.font = Font(size=14, bold=True, color="FFFFFF")
            title_cell.alignment = Alignment(horizontal='center', vertical='center')
            title_cell.fill = PatternFill(start_color="8064A2", end_color="8064A2", fill_type="solid")
            
            # Encabezados
            if data['resumen']:
                headers = list(data['resumen'][0].keys())
                for col_num, header in enumerate(headers, 1):
                    cell = ws1.cell(row=3, column=col_num, value=header)
                    cell.font = Font(bold=True, color="FFFFFF")
                    cell.alignment = Alignment(horizontal='center')
                    cell.fill = PatternFill(start_color="9BBB59", end_color="9BBB59", fill_type="solid")
                
                # Datos
                for row_num, row_data in enumerate(data['resumen'], 4):
                    for col_num, key in enumerate(headers, 1):
                        value = row_data[key]
                        
                        # Formato para números enteros
                        if key in ["Stock Total", "Nivel Alarma", "Ubicaciones"] and value is not None:
                            try:
                                cell = ws1.cell(row=row_num, column=col_num, value=int(value))
                                cell.number_format = '#,##0'
                            except:
                                cell = ws1.cell(row=row_num, column=col_num, value=value)
                        else:
                            cell = ws1.cell(row=row_num, column=col_num, value=value)
                        
                        # Resaltar stock bajo
                        if key == "Stock Total" and value is not None:
                            try:
                                stock = int(value)
                                alarma_col = headers.index("Nivel Alarma") + 1
                                alarma_val = ws1.cell(row=row_num, column=alarma_col).value
                                if alarma_val and stock < int(alarma_val):
                                    cell.fill = PatternFill(start_color="FFC7CE", end_color="FFC7CE", fill_type="solid")
                            except:
                                pass
                
                # ANCHOS FIJOS PROFESIONALES
                column_widths = {
                    'A': 35,  # Material
                    'B': 20,  # Marca
                    'C': 20,  # Categoría
                    'D': 15,  # Nivel Alarma
                    'E': 15,  # Stock Total
                    'F': 15,  # Ubicaciones
                    'G': 30,  # Edificios
                }
                
                for col_letter, width in column_widths.items():
                    ws1.column_dimensions[col_letter].width = width
            
            # ============================================
            # HOJA 2: DETALLE DE INVENTARIO
            # ============================================
            if data['detalle']:
                ws2 = wb.create_sheet(title="Inventario Detallado")
                
                # Título
                ws2.merge_cells('A1:H1')
                title_cell = ws2['A1']
                title_cell.value = f"DETALLE DE INVENTARIO POR EDIFICIO - {fecha_actual}"
                title_cell.font = Font(size=14, bold=True, color="FFFFFF")
                title_cell.alignment = Alignment(horizontal='center', vertical='center')
                title_cell.fill = PatternFill(start_color="366092", end_color="366092", fill_type="solid")
                
                # Encabezados
                headers = list(data['detalle'][0].keys())
                for col_num, header in enumerate(headers, 1):
                    cell = ws2.cell(row=3, column=col_num, value=header)
                    cell.font = Font(bold=True, color="FFFFFF")
                    cell.alignment = Alignment(horizontal='center')
                    cell.fill = PatternFill(start_color="4F81BD", end_color="4F81BD", fill_type="solid")
                
                # Datos
                for row_num, row_data in enumerate(data['detalle'], 4):
                    for col_num, key in enumerate(headers, 1):
                        value = row_data[key]
                        
                        # Formato para cantidades
                        if key == "Cantidad" and value is not None:
                            try:
                                cell = ws2.cell(row=row_num, column=col_num, value=int(value))
                                cell.number_format = '#,##0'
                                # Resaltar si es 0
                                if value == 0:
                                    cell.fill = PatternFill(start_color="FFC7CE", end_color="FFC7CE", fill_type="solid")
                            except:
                                cell = ws2.cell(row=row_num, column=col_num, value=value)
                        else:
                            cell = ws2.cell(row=row_num, column=col_num, value=value)
                
                # ANCHOS FIJOS PARA HOJA 2
                column_widths2 = {
                    'A': 35,  # Material
                    'B': 20,  # Edificio
                    'C': 12,  # Cantidad
                    'D': 10,  # Estante
                    'E': 15,  # Lugar
                    'F': 20,  # Etiqueta
                    'G': 20,  # Marca
                    'H': 20,  # Categoría
                }
                
                for col_letter, width in column_widths2.items():
                    ws2.column_dimensions[col_letter].width = width
            
            # ============================================
            # GUARDAR ARCHIVO
            # ============================================
            # Crear carpeta si no existe
            export_dir = "exportaciones"
            if not os.path.exists(export_dir):
                os.makedirs(export_dir)
            
            # Nombre con fecha
            fecha_nombre = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{export_dir}/Inventario_RA-PE_{fecha_nombre}.xlsx"
            
            # Guardar
            wb.save(filename)
            
            # Mostrar mensaje de éxito
            messagebox.showinfo(
                "Exportación Exitosa", 
                f"Archivo exportado correctamente:\n{filename}\n\n"
                f"Total materiales: {len(data['resumen'])}\n"
                f"Registros de inventario: {len(data['detalle'])}"
            )
            
            print(f"[RA-PE] Excel exportado: {filename}")
            
        except Exception as e:
            print(f"Error exportando Excel RA-PE: {e}")
            messagebox.showerror(
                "Error de Exportación", 
                f"No se pudo exportar el archivo:\n{str(e)}"
            )
    
    def show_alarm_details_rape(self):
        """Abre ventana para ver detalles de alarmas RA-PE"""
        try:
            from ventanaAlarmaRape import VentanaAlarmasRaPe
            VentanaAlarmasRaPe(self.root, self.system_name)
        except ImportError as e:
            print(f"ventanaAlarmasRaPe no encontrada: {e}")
            self.open_materiales_rape()
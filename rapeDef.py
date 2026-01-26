import tkinter as tk
from tkinter import messagebox
from baseSystem import BaseSystem
import styles
from datetime import datetime
import os

class RAPESystem(BaseSystem):
    def __init__(self, root, return_callback, db_status="Conectado"):
        # Configurar botón personalizado para el encabezado
        custom_button = {
            'text': "EXPORTAR EXCEL",
            'command': self.exportar_excel_rape
        }
        
        super().__init__(root, return_callback, "RA-PE", db_status, custom_button)
        
        # Actualizar alarmas
        self.update_alarms()
    
    def open_productos(self):
        """Abre la ventana de gestión de materiales RA-PE"""
        try:
            from ventanaProductosRaPe import VentanaProductosRaPe
            VentanaProductosRaPe(self.root, self.system_name)
        except ImportError as e:
            messagebox.showerror("Error", f"No se pudo abrir gestión de materiales: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"Error al abrir materiales RA-PE: {e}")
    
    def get_alarmas(self):
        """Obtiene las alarmas específicas de RA-PE desde la base de datos"""
        try:
            from db import Database
            db = Database()
            return db.get_alarmas_rape()
        except Exception as e:
            print(f"Error obteniendo alarmas RA-PE: {e}")
            return None
    
    def show_alarm_details(self):
        """Abre ventana para ver detalles de alarmas RA-PE"""
        try:
            from ventanaAlarmaRape import VentanaAlarmasRaPe
            VentanaAlarmasRaPe(self.root, self.system_name)
        except ImportError as e:
            print(f"ventanaAlarmasRaPe no encontrada: {e}")
            self.open_productos()
    
    def exportar_excel_rape(self):
        """Exporta datos de RA-PE a Excel con formato profesional"""
        try:
            import openpyxl
            from openpyxl.styles import Font, Alignment, PatternFill
            from db import Database
            
            # Obtener datos
            db = Database()
            data = db.get_export_data_rape()
            
            if not data['resumen'] and not data['detalle']:
                messagebox.showwarning("Sin datos", "No hay datos para exportar en RA-PE")
                return
            
            # Crear workbook
            wb = openpyxl.Workbook()
            
            # HOJA 1: RESUMEN DE MATERIALES
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
                        
                        if key in ["Stock Total", "Nivel Alarma", "Ubicaciones"] and value is not None:
                            try:
                                cell = ws1.cell(row=row_num, column=col_num, value=int(value))
                                cell.number_format = '#,##0'
                            except:
                                cell = ws1.cell(row=row_num, column=col_num, value=value)
                        else:
                            cell = ws1.cell(row=row_num, column=col_num, value=value)
                        
                        if key == "Stock Total" and value is not None:
                            try:
                                stock = int(value)
                                alarma_col = headers.index("Nivel Alarma") + 1
                                alarma_val = ws1.cell(row=row_num, column=alarma_col).value
                                if alarma_val and stock < int(alarma_val):
                                    cell.fill = PatternFill(start_color="FFC7CE", end_color="FFC7CE", fill_type="solid")
                            except:
                                pass
                
                column_widths = {
                    'A': 35, 'B': 20, 'C': 20, 'D': 15,
                    'E': 15, 'F': 15, 'G': 30,
                }
                
                for col_letter, width in column_widths.items():
                    ws1.column_dimensions[col_letter].width = width
            
            # HOJA 2: DETALLE DE INVENTARIO
            if data['detalle']:
                ws2 = wb.create_sheet(title="Inventario Detallado")
                
                ws2.merge_cells('A1:H1')
                title_cell = ws2['A1']
                title_cell.value = f"DETALLE DE INVENTARIO POR EDIFICIO - {fecha_actual}"
                title_cell.font = Font(size=14, bold=True, color="FFFFFF")
                title_cell.alignment = Alignment(horizontal='center', vertical='center')
                title_cell.fill = PatternFill(start_color="366092", end_color="366092", fill_type="solid")
                
                headers = list(data['detalle'][0].keys())
                for col_num, header in enumerate(headers, 1):
                    cell = ws2.cell(row=3, column=col_num, value=header)
                    cell.font = Font(bold=True, color="FFFFFF")
                    cell.alignment = Alignment(horizontal='center')
                    cell.fill = PatternFill(start_color="4F81BD", end_color="4F81BD", fill_type="solid")
                
                for row_num, row_data in enumerate(data['detalle'], 4):
                    for col_num, key in enumerate(headers, 1):
                        value = row_data[key]
                        
                        if key == "Cantidad" and value is not None:
                            try:
                                cell = ws2.cell(row=row_num, column=col_num, value=int(value))
                                cell.number_format = '#,##0'
                                if value == 0:
                                    cell.fill = PatternFill(start_color="FFC7CE", end_color="FFC7CE", fill_type="solid")
                            except:
                                cell = ws2.cell(row=row_num, column=col_num, value=value)
                        else:
                            cell = ws2.cell(row=row_num, column=col_num, value=value)
                
                column_widths2 = {
                    'A': 35, 'B': 20, 'C': 12, 'D': 10,
                    'E': 15, 'F': 20, 'G': 20, 'H': 20,
                }
                
                for col_letter, width in column_widths2.items():
                    ws2.column_dimensions[col_letter].width = width
            
            # GUARDAR ARCHIVO
            export_dir = "exportaciones"
            if not os.path.exists(export_dir):
                os.makedirs(export_dir)
            
            fecha_nombre = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{export_dir}/Inventario_RA-PE_{fecha_nombre}.xlsx"
            
            wb.save(filename)
            
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
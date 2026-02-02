"""
Ventana para agregar/editar Materiales RA-PE 
"""

import tkinter as tk
from tkinter import ttk, messagebox
import styles
from db import Database

class VentanaDetalleMaterialRaPe:
    # ===== INICIALIZACIÓN =====
    def __init__(self, parent, titulo, material_id=None, callback_obj=None):
        self.parent = parent
        self.titulo = titulo
        self.material_id = material_id
        self.callback_obj = callback_obj
        self.db = Database()
        
        self.window = tk.Toplevel(parent)
        self.window.title(titulo)
        self.window.geometry("600x650")  
        self.window.configure(bg=styles.COLOR_FONDO)
        self.window.transient(parent)
        self.window.grab_set()
        
        self.centerWindow(600, 650)
        self.createWidgets()
        self.loadDatos()
    
    # ===== MÉTODOS DE CONFIGURACIÓN DE VENTANA =====
    def centerWindow(self, width, height):
        screenWidth = self.window.winfo_screenwidth()
        screenHeight = self.window.winfo_screenheight()
        x = (screenWidth // 2) - (width // 2)
        y = (screenHeight // 2) - (height // 2)
        self.window.geometry(f"{width}x{height}+{x}+{y}")
    
    # ===== CREACIÓN DE INTERFAZ =====
    def createWidgets(self):
        mainFrame = tk.Frame(self.window, bg=styles.COLOR_FONDO, padx=30, pady=30)
        mainFrame.pack(fill=tk.BOTH, expand=True)
        
        title = tk.Label(mainFrame, 
                        text=self.titulo, 
                        font=(styles.FUENTE_PRINCIPAL, styles.TAMANO_SUBTITULO, styles.PESO_NEGRITA),
                        bg=styles.COLOR_FONDO, 
                        fg=styles.COLOR_TEXTO_OSCURO)
        title.pack(pady=(0, 25))
        
        formFrame = tk.Frame(mainFrame, bg=styles.COLOR_FONDO)
        formFrame.pack(fill=tk.X)
        
        tk.Label(formFrame, 
                text="Nombre del Material:*", 
                font=(styles.FUENTE_PRINCIPAL, styles.TAMANO_NORMAL),
                bg=styles.COLOR_FONDO, 
                fg=styles.COLOR_TEXTO_OSCURO).grid(row=0, column=0, padx=(0, 10), pady=15, sticky="w")
        
        self.nombreVar = tk.StringVar()
        self.nombreEntry = tk.Entry(formFrame, 
                                    textvariable=self.nombreVar,
                                    font=(styles.FUENTE_PRINCIPAL, styles.TAMANO_NORMAL),
                                    width=30)
        self.nombreEntry.grid(row=0, column=1, pady=15, sticky="w")
        
        tk.Label(formFrame, 
                text="Marca:*", 
                font=(styles.FUENTE_PRINCIPAL, styles.TAMANO_NORMAL),
                bg=styles.COLOR_FONDO, 
                fg=styles.COLOR_TEXTO_OSCURO).grid(row=1, column=0, padx=(0, 10), pady=15, sticky="w")
        
        self.marcaVar = tk.IntVar()
        self.marcaCombobox = ttk.Combobox(formFrame, 
                                         font=(styles.FUENTE_PRINCIPAL, styles.TAMANO_NORMAL),
                                         width=28,
                                         state="readonly")
        self.marcaCombobox.grid(row=1, column=1, pady=15, sticky="w")
        
        tk.Label(formFrame, 
                text="Categoría:*", 
                font=(styles.FUENTE_PRINCIPAL, styles.TAMANO_NORMAL),
                bg=styles.COLOR_FONDO, 
                fg=styles.COLOR_TEXTO_OSCURO).grid(row=2, column=0, padx=(0, 10), pady=15, sticky="w")
        
        self.categoriaVar = tk.IntVar()
        self.categoriaCombobox = ttk.Combobox(formFrame, 
                                             font=(styles.FUENTE_PRINCIPAL, styles.TAMANO_NORMAL),
                                             width=28,
                                             state="readonly")
        self.categoriaCombobox.grid(row=2, column=1, pady=15, sticky="w")
        
        tk.Label(formFrame, 
                text="Alarma Cap (mínimo stock):", 
                font=(styles.FUENTE_PRINCIPAL, styles.TAMANO_NORMAL),
                bg=styles.COLOR_FONDO, 
                fg=styles.COLOR_TEXTO_OSCURO).grid(row=3, column=0, padx=(0, 10), pady=15, sticky="w")
        
        self.alarmaVar = tk.IntVar(value=5)
        self.alarmaSpinbox = tk.Spinbox(formFrame, 
                                        from_=0, to=999, 
                                        textvariable=self.alarmaVar,
                                        font=(styles.FUENTE_PRINCIPAL, styles.TAMANO_NORMAL),
                                        width=10)
        self.alarmaSpinbox.grid(row=3, column=1, pady=15, sticky="w")
        
        infoLabel = tk.Label(formFrame, 
                            text="* Campos requeridos", 
                            font=(styles.FUENTE_PRINCIPAL, styles.TAMANO_PEQUENO),
                            bg=styles.COLOR_FONDO, 
                            fg=styles.COLOR_TEXTO_CLARO)
        infoLabel.grid(row=4, column=0, columnspan=2, pady=(20, 5), sticky="w")
        
        buttonFrame = tk.Frame(mainFrame, bg=styles.COLOR_FONDO)
        buttonFrame.pack(fill=tk.X, pady=(20, 0))
        
        btnText = "Siguiente →" if not self.material_id else "Guardar Cambios"
        self.btnGuardar = tk.Button(buttonFrame, 
                                   text=btnText, 
                                   font=(styles.FUENTE_PRINCIPAL, styles.TAMANO_NORMAL),
                                   bg=styles.COLOR_EXITO, 
                                   fg=styles.COLOR_BLANCO,
                                   width=20,
                                   command=self.guardarMaterial)
        self.btnGuardar.pack(side=tk.LEFT, padx=(0, 10))
        
        btnCancelar = tk.Button(buttonFrame, 
                               text="Cancelar", 
                               font=(styles.FUENTE_PRINCIPAL, styles.TAMANO_NORMAL),
                               bg=styles.COLOR_ADVERTENCIA, 
                               fg=styles.COLOR_BLANCO,
                               width=20,
                               command=self.cancelar)
        btnCancelar.pack(side=tk.LEFT)
    
    # ===== CARGA DE DATOS =====
    def loadDatos(self):
        marcas = self.db.get_all_marcas()
        if marcas:
            marca_dict = {}
            nombres_marcas = []
            for marca in marcas:
                nombres_marcas.append(marca['nombre_marca'])
                marca_dict[marca['nombre_marca']] = marca['id_marca']
            
            self.marcaCombobox['values'] = nombres_marcas
            self.marca_dict = marca_dict
        
        categorias = self.db.get_all_categorias()
        if categorias:
            categoria_dict = {}
            nombres_categorias = []
            for categoria in categorias:
                nombres_categorias.append(categoria['nombre_categoria'])
                categoria_dict[categoria['nombre_categoria']] = categoria['id_categoria']
            
            self.categoriaCombobox['values'] = nombres_categorias
            self.categoria_dict = categoria_dict
        
        if self.material_id:
            materiales = self.db.get_productos_rape_completo()
            material = next((m for m in materiales if m['id_productosrape'] == self.material_id), None)
            
            if material:
                self.nombreVar.set(material['nombre_producto_rape'])
                self.marcaCombobox.set(material['nombre_marca'])
                self.categoriaCombobox.set(material['nombre_categoria'])
                self.alarmaVar.set(material['alarma_cap'])
    
    # ===== OPERACIONES DE MATERIAL =====
    def guardarMaterial(self):
        nombre = self.nombreVar.get().strip()
        if not nombre:
            messagebox.showwarning("Campo requerido", "Por favor ingrese el nombre del material")
            self.nombreEntry.focus()
            return
        
        marca_nombre = self.marcaCombobox.get()
        if not marca_nombre:
            messagebox.showwarning("Campo requerido", "Por favor seleccione una marca")
            self.marcaCombobox.focus()
            return
        
        categoria_nombre = self.categoriaCombobox.get()
        if not categoria_nombre:
            messagebox.showwarning("Campo requerido", "Por favor seleccione una categoría")
            self.categoriaCombobox.focus()
            return
        
        id_marca = self.marca_dict.get(marca_nombre)
        id_categoria = self.categoria_dict.get(categoria_nombre)
        alarma_cap = self.alarmaVar.get()
        
        try:
            if self.material_id:
                resultado = self.db.update_producto_rape(
                    self.material_id, nombre, id_marca, id_categoria, alarma_cap
                )
                
                if resultado[0]:
                    success, mensaje = resultado
                    messagebox.showinfo("Éxito", mensaje)
                    
                    if self.callback_obj and hasattr(self.callback_obj, 'loadProductos'):
                        self.callback_obj.loadProductos()
                    
                    self.actualizarAlarmasSiEstanAbiertas()
                    self.window.destroy()
                else:
                    success, mensaje_error = resultado
                    messagebox.showerror("Error", mensaje_error)
            else:
                resultado = self.db.create_producto_rape(
                    nombre, id_marca, id_categoria, alarma_cap
                )
                
                if resultado[0]:
                    material_id, mensaje = resultado
                    success = self.db.create_inventario_para_edificios_rape(material_id)
                    
                    if success:
                        self.abrirDistribucionInventario(material_id, nombre)
                        self.window.destroy()
                    else:
                        messagebox.showwarning("Advertencia", 
                                             "Material creado pero hubo problemas al crear el inventario")
                        
                        if self.callback_obj and hasattr(self.callback_obj, 'loadProductos'):
                            self.callback_obj.loadProductos()
                        
                        self.actualizarAlarmasSiEstanAbiertas()
                        self.window.destroy()
                else:
                    material_id, mensaje_error = resultado
                    messagebox.showerror("Error", mensaje_error)
                    
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar material: {e}")
    
    # ===== MÉTODOS AUXILIARES =====
    def actualizarAlarmasSiEstanAbiertas(self):
        try:
            root_window = self.window.winfo_toplevel()
            
            for child in root_window.winfo_children():
                if isinstance(child, tk.Toplevel):
                    try:
                        title = child.title().lower()
                        if 'alarma' in title or 'alerta' in title:
                            if hasattr(child, 'actualizarTabla'):
                                child.actualizarTabla()
                                return True
                    except:
                        continue
        except Exception as e:
            print(f"[ERROR] Error buscando alarmas RA-PE: {e}")
        
        return False
    
    def abrirDistribucionInventario(self, material_id, material_nombre):
        try:
            from ventanaDistribucionInventario import VentanaDistribucionInventario
            
            ventana_dist = VentanaDistribucionInventario(
                self.parent, 
                material_id, 
                material_nombre, 
                sistema="rape",
                callback_obj=self.callback_obj,
                modo="agregar"
            )
            
        except ImportError as e:
            messagebox.showerror("Error", f"No se pudo abrir distribución de inventario: {e}")
    
    def cancelar(self):
        self.window.destroy()
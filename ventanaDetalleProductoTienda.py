"""
Ventana para agregar/editar Productos TIENDA (Paso 1)
"""

import tkinter as tk
from tkinter import ttk, messagebox
import styles
from db import Database

class VentanaDetalleProductoTienda:
    """Ventana emergente para agregar/editar productos TIENDA"""
    
    def __init__(self, parent, titulo, producto_id=None, callback_obj=None):
        self.parent = parent
        self.titulo = titulo
        self.producto_id = producto_id
        self.callback_obj = callback_obj
        self.db = Database()
        
        # Crear ventana emergente
        self.window = tk.Toplevel(parent)
        self.window.title(titulo)
        self.window.geometry("600x550")
        self.window.configure(bg=styles.COLOR_FONDO)
        self.window.transient(parent)
        self.window.grab_set()
        
        # Centrar ventana
        self.centerWindow(600, 550)
        
        # Crear interfaz
        self.createWidgets()
        self.loadDatos()
    
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
        mainFrame = tk.Frame(self.window, bg=styles.COLOR_FONDO, padx=30, pady=30)
        mainFrame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        title = tk.Label(mainFrame, 
                        text=self.titulo, 
                        font=(styles.FUENTE_PRINCIPAL, styles.TAMANO_SUBTITULO, styles.PESO_NEGRITA),
                        bg=styles.COLOR_FONDO, 
                        fg=styles.COLOR_TEXTO_OSCURO)
        title.pack(pady=(0, 25))
        
        # Frame para formulario
        formFrame = tk.Frame(mainFrame, bg=styles.COLOR_FONDO)
        formFrame.pack(fill=tk.X)
        
        # Campo: Nombre del Producto
        tk.Label(formFrame, 
                text="Nombre del Producto:*", 
                font=(styles.FUENTE_PRINCIPAL, styles.TAMANO_NORMAL),
                bg=styles.COLOR_FONDO, 
                fg=styles.COLOR_TEXTO_OSCURO).grid(row=0, column=0, padx=(0, 10), pady=10, sticky="w")
        
        self.nombreVar = tk.StringVar()
        self.nombreEntry = tk.Entry(formFrame, 
                                    textvariable=self.nombreVar,
                                    font=(styles.FUENTE_PRINCIPAL, styles.TAMANO_NORMAL),
                                    width=30)
        self.nombreEntry.grid(row=0, column=1, pady=10, sticky="w")
        
        # Campo: Marca (Combobox)
        tk.Label(formFrame, 
                text="Marca:*", 
                font=(styles.FUENTE_PRINCIPAL, styles.TAMANO_NORMAL),
                bg=styles.COLOR_FONDO, 
                fg=styles.COLOR_TEXTO_OSCURO).grid(row=1, column=0, padx=(0, 10), pady=10, sticky="w")
        
        self.marcaVar = tk.IntVar()
        self.marcaCombobox = ttk.Combobox(formFrame, 
                                         font=(styles.FUENTE_PRINCIPAL, styles.TAMANO_NORMAL),
                                         width=28,
                                         state="readonly")
        self.marcaCombobox.grid(row=1, column=1, pady=10, sticky="w")
        
        # Campo: Categoría (Combobox)
        tk.Label(formFrame, 
                text="Categoría:*", 
                font=(styles.FUENTE_PRINCIPAL, styles.TAMANO_NORMAL),
                bg=styles.COLOR_FONDO, 
                fg=styles.COLOR_TEXTO_OSCURO).grid(row=2, column=0, padx=(0, 10), pady=10, sticky="w")
        
        self.categoriaVar = tk.IntVar()
        self.categoriaCombobox = ttk.Combobox(formFrame, 
                                             font=(styles.FUENTE_PRINCIPAL, styles.TAMANO_NORMAL),
                                             width=28,
                                             state="readonly")
        self.categoriaCombobox.grid(row=2, column=1, pady=10, sticky="w")
        
        # Campo: Precio Venta
        tk.Label(formFrame, 
                text="Precio de Venta:*", 
                font=(styles.FUENTE_PRINCIPAL, styles.TAMANO_NORMAL),
                bg=styles.COLOR_FONDO, 
                fg=styles.COLOR_TEXTO_OSCURO).grid(row=3, column=0, padx=(0, 10), pady=10, sticky="w")
        
        self.precioVentaVar = tk.StringVar()
        self.precioVentaEntry = tk.Entry(formFrame, 
                                         textvariable=self.precioVentaVar,
                                         font=(styles.FUENTE_PRINCIPAL, styles.TAMANO_NORMAL),
                                         width=30)
        self.precioVentaEntry.grid(row=3, column=1, pady=10, sticky="w")
        
        # Campo: Precio Compra (opcional)
        tk.Label(formFrame, 
                text="Precio de Compra:", 
                font=(styles.FUENTE_PRINCIPAL, styles.TAMANO_NORMAL),
                bg=styles.COLOR_FONDO, 
                fg=styles.COLOR_TEXTO_OSCURO).grid(row=4, column=0, padx=(0, 10), pady=10, sticky="w")
        
        self.precioCompraVar = tk.StringVar()
        self.precioCompraEntry = tk.Entry(formFrame, 
                                          textvariable=self.precioCompraVar,
                                          font=(styles.FUENTE_PRINCIPAL, styles.TAMANO_NORMAL),
                                          width=30)
        self.precioCompraEntry.grid(row=4, column=1, pady=10, sticky="w")
        
        # Campo: Color (opcional)
        tk.Label(formFrame, 
                text="Color:", 
                font=(styles.FUENTE_PRINCIPAL, styles.TAMANO_NORMAL),
                bg=styles.COLOR_FONDO, 
                fg=styles.COLOR_TEXTO_OSCURO).grid(row=5, column=0, padx=(0, 10), pady=10, sticky="w")
        
        self.colorVar = tk.StringVar()
        self.colorEntry = tk.Entry(formFrame, 
                                   textvariable=self.colorVar,
                                   font=(styles.FUENTE_PRINCIPAL, styles.TAMANO_NORMAL),
                                   width=30)
        self.colorEntry.grid(row=5, column=1, pady=10, sticky="w")
        
        # Campo: Talla (Combobox con opciones específicas)
        tk.Label(formFrame, 
                text="Talla:", 
                font=(styles.FUENTE_PRINCIPAL, styles.TAMANO_NORMAL),
                bg=styles.COLOR_FONDO, 
                fg=styles.COLOR_TEXTO_OSCURO).grid(row=6, column=0, padx=(0, 10), pady=10, sticky="w")
        
        self.tallaVar = tk.StringVar()
        self.tallaCombobox = ttk.Combobox(formFrame, 
                                         textvariable=self.tallaVar,
                                         font=(styles.FUENTE_PRINCIPAL, styles.TAMANO_NORMAL),
                                         width=28,
                                         state="readonly")
        self.tallaCombobox['values'] = ('XXS', 'XS', 'S', 'M', 'L', 'XL', 'XXL', 'XXXL', '----')
        self.tallaCombobox.grid(row=6, column=1, pady=10, sticky="w")
        
        # Campo: Alarma Cap
        tk.Label(formFrame, 
                text="Alarma Cap (mínimo stock):", 
                font=(styles.FUENTE_PRINCIPAL, styles.TAMANO_NORMAL),
                bg=styles.COLOR_FONDO, 
                fg=styles.COLOR_TEXTO_OSCURO).grid(row=7, column=0, padx=(0, 10), pady=10, sticky="w")
        
        self.alarmaVar = tk.IntVar(value=5)
        self.alarmaSpinbox = tk.Spinbox(formFrame, 
                                        from_=0, to=999, 
                                        textvariable=self.alarmaVar,
                                        font=(styles.FUENTE_PRINCIPAL, styles.TAMANO_NORMAL),
                                        width=10)
        self.alarmaSpinbox.grid(row=7, column=1, pady=10, sticky="w")
        
        # Información sobre campos requeridos
        infoLabel = tk.Label(formFrame, 
                            text="* Campos requeridos", 
                            font=(styles.FUENTE_PRINCIPAL, styles.TAMANO_PEQUENO),
                            bg=styles.COLOR_FONDO, 
                            fg=styles.COLOR_TEXTO_CLARO)
        infoLabel.grid(row=8, column=0, columnspan=2, pady=(15, 5), sticky="w")
        
        # Frame para botones
        buttonFrame = tk.Frame(mainFrame, bg=styles.COLOR_FONDO)
        buttonFrame.pack(fill=tk.X, pady=(20, 0))
        
        # Botón Guardar/Siguiente
        btnText = "Siguiente →" if not self.producto_id else "Guardar Cambios"
        self.btnGuardar = tk.Button(buttonFrame, 
                                   text=btnText, 
                                   font=(styles.FUENTE_PRINCIPAL, styles.TAMANO_NORMAL),
                                   bg=styles.COLOR_EXITO, 
                                   fg=styles.COLOR_BLANCO,
                                   width=20,
                                   command=self.guardarProducto)
        self.btnGuardar.pack(side=tk.LEFT, padx=(0, 10))
        
        # Botón Cancelar
        btnCancelar = tk.Button(buttonFrame, 
                               text="Cancelar", 
                               font=(styles.FUENTE_PRINCIPAL, styles.TAMANO_NORMAL),
                               bg=styles.COLOR_ADVERTENCIA, 
                               fg=styles.COLOR_BLANCO,
                               width=20,
                               command=self.cancelar)
        btnCancelar.pack(side=tk.LEFT)
    
    def loadDatos(self):
        """Carga datos en el formulario"""
        # Cargar marcas en el combobox
        marcas = self.db.get_all_marcas()
        if marcas:
            marca_dict = {}
            nombres_marcas = []
            for marca in marcas:
                nombres_marcas.append(marca['nombre_marca'])
                marca_dict[marca['nombre_marca']] = marca['id_marca']
            
            self.marcaCombobox['values'] = nombres_marcas
            self.marca_dict = marca_dict
        
        # Cargar categorías en el combobox
        categorias = self.db.get_all_categorias()
        if categorias:
            categoria_dict = {}
            nombres_categorias = []
            for categoria in categorias:
                nombres_categorias.append(categoria['nombre_categoria'])
                categoria_dict[categoria['nombre_categoria']] = categoria['id_categoria']
            
            self.categoriaCombobox['values'] = nombres_categorias
            self.categoria_dict = categoria_dict
        
        # Si es edición, cargar datos del producto
        if self.producto_id:
            # Obtener producto desde vista optimizada
            productos = self.db.get_productos_tienda_completo()
            producto = next((p for p in productos if p['id_productostienda'] == self.producto_id), None)
            
            if producto:
                self.nombreVar.set(producto['nombre_producto_tienda'])
                self.marcaCombobox.set(producto['nombre_marca'])
                self.categoriaCombobox.set(producto['nombre_categoria'])
                self.precioVentaVar.set(str(producto['precio_venta']))
                if producto['precio_compra']:
                    self.precioCompraVar.set(str(producto['precio_compra']))
                if producto['color']:
                    self.colorVar.set(producto['color'])
                if producto['talla']:
                    self.tallaVar.set(producto['talla'])
                self.alarmaVar.set(producto['alarma_cap'])
    
    def validarNumero(self, valor, campo):
        """Valida que un valor sea un número válido"""
        if valor.strip() == "":
            return None  # Vacío es permitido para campos opcionales
        
        try:
            num = float(valor)
            if num < 0:
                messagebox.showwarning("Valor inválido", f"{campo} no puede ser negativo")
                return None
            return num
        except ValueError:
            messagebox.showwarning("Valor inválido", f"{campo} debe ser un número")
            return None
    
    def actualizarAlarmasSiEstanAbiertas(self):
        """Intenta actualizar ventanas de alarmas si están abiertas"""
        try:
            # Buscar ventana raíz de la aplicación
            root_window = self.window.winfo_toplevel()
            
            # Buscar entre todas las ventanas hijas del root
            for child in root_window.winfo_children():
                if isinstance(child, tk.Toplevel):
                    try:
                        title = child.title().lower()
                        if 'alarma' in title or 'alerta' in title:
                            if hasattr(child, 'actualizarTabla'):
                                child.actualizarTabla()
                                print(f"[INFO] Tabla de alarmas actualizada desde detalle producto")
                                return True
                    except:
                        continue
        except Exception as e:
            print(f"[ERROR] Error buscando alarmas: {e}")
        
        return False
    
    def guardarProducto(self):
        """Guarda o actualiza el producto - VERSIÓN CORREGIDA"""
        # Validar campos requeridos
        nombre = self.nombreVar.get().strip()
        if not nombre:
            messagebox.showwarning("Campo requerido", "Por favor ingrese el nombre del producto")
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
        
        # Validar precios
        precio_venta = self.validarNumero(self.precioVentaVar.get(), "Precio de venta")
        if precio_venta is None:
            self.precioVentaEntry.focus()
            return
        
        precio_compra = self.validarNumero(self.precioCompraVar.get(), "Precio de compra")
        # precio_compra puede ser None (opcional)
        
        # Obtener IDs
        id_marca = self.marca_dict.get(marca_nombre)
        id_categoria = self.categoria_dict.get(categoria_nombre)
        
        # Obtener otros campos
        color = self.colorVar.get().strip() or None
        talla = self.tallaVar.get() or None
        alarma_cap = self.alarmaVar.get()
        
        try:
            if self.producto_id:
                # Actualizar producto existente
                success = self.db.update_producto_tienda(
                    self.producto_id, nombre, id_marca, id_categoria, 
                    precio_venta, precio_compra, color, talla, alarma_cap
                )
                if success:
                    messagebox.showinfo("Éxito", f"Producto '{nombre}' actualizado exitosamente")
                    
                    # Actualizar tabla principal
                    if self.callback_obj and hasattr(self.callback_obj, 'loadProductos'):
                        self.callback_obj.loadProductos()
                    
                    # Intentar actualizar alarmas si están abiertas
                    self.actualizarAlarmasSiEstanAbiertas()
                    
                    self.window.destroy()
                else:
                    messagebox.showerror("Error", "No se pudo actualizar el producto")
            else:
                # Crear nuevo producto
                producto_id = self.db.create_producto_tienda(
                    nombre, id_marca, id_categoria, precio_venta, 
                    precio_compra, color, talla, alarma_cap
                )
                if producto_id:
                    # Crear inventario para todos los edificios TIENDA
                    success = self.db.create_inventario_para_edificios_tienda(producto_id)
                    
                    if success:
                        # NO cerrar esta ventana todavía
                        # La ventana de distribución manejará el refresco
                        self.abrirDistribucionInventario(producto_id, nombre)
                        self.window.destroy()
                    else:
                        messagebox.showwarning("Advertencia", 
                                             "Producto creado pero hubo problemas al crear el inventario")
                        
                        # Refrescar tabla aunque haya problemas
                        if self.callback_obj:
                            self.callback_obj.loadProductos()

                        # Intentar actualizar alarmas si están abiertas
                        self.actualizarAlarmasSiEstanAbiertas()
                        
                        self.window.destroy()
                else:
                    messagebox.showerror("Error", "No se pudo crear el producto")
                    
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar producto: {e}")
    
    def abrirDistribucionInventario(self, producto_id, producto_nombre):
        """Abre ventana para distribución de inventario (Paso 2)"""
        try:
            from ventanaDistribucionInventario import VentanaDistribucionInventario
            
            # Crear ventana de distribución pasando el callback principal
            ventana_dist = VentanaDistribucionInventario(
                self.parent, 
                producto_id, 
                producto_nombre, 
                sistema="tienda",  # <-- Especificar sistema
                callback_obj=self.callback_obj,
                modo="agregar"
            )
            
            # Configurar para que cuando se cierre la distribución, también se cierre esta ventana
            def on_dist_close():
                self.window.destroy()
            
            ventana_dist.window.protocol("WM_DELETE_WINDOW", on_dist_close)
            
        except ImportError as e:
            messagebox.showerror("Error", f"No se pudo abrir distribución de inventario: {e}")
    
    def cancelar(self):
        """Cierra la ventana sin guardar cambios"""
        self.window.destroy()
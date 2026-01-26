"""
Ventana para distribución y edición de inventario por edificio
GENERICO para TIENDA y RA-PE
"""

import tkinter as tk
from tkinter import ttk, messagebox
import styles
from db import Database

class VentanaDistribucionInventario:
    def __init__(self, parent, producto_id, producto_nombre, sistema="tienda", 
                 callback_obj=None, modo="detalles"):
        """
        Inicializa ventana de distribución de inventario
        
        Args:
            parent: Ventana padre
            producto_id: ID del producto/material
            producto_nombre: Nombre del producto/material  
            sistema: "tienda" o "rape" (determina tablas DB)
            callback_obj: Objeto para callback
            modo: "detalles" o "agregar" o "editar"
        """
        self.parent = parent
        self.producto_id = producto_id
        self.producto_nombre = producto_nombre
        self.sistema = sistema.lower()  # "tienda" o "rape"
        self.callback_obj = callback_obj
        self.modo = modo.lower()
        
        # Determinar si es producto nuevo
        self.es_nuevo_producto = (modo.lower() == "agregar")
        self.db = Database()
        
        # Crear ventana emergente
        self.window = tk.Toplevel(parent)
        title_suffix = "TIENDA" if sistema == "tienda" else "RA-PE"
        self.window.title(f"Distribución de Inventario {title_suffix} - {producto_nombre}")
        self.window.geometry("900x600")
        self.window.minsize(900, 600) 
        self.window.configure(bg=styles.COLOR_FONDO)
        self.window.transient(parent)
        self.window.grab_set()
        
        # Centrar ventana
        self.centerWindow(900, 600)
        
        # Configurar evento de cierre
        self.window.protocol("WM_DELETE_WINDOW", self.on_window_close)
        
        # Crear interfaz
        self.createWidgets()
        self.loadInventario()
    
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
        mainFrame = tk.Frame(self.window, bg=styles.COLOR_FONDO, padx=20, pady=20)
        mainFrame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        sistema_text = "TIENDA" if self.sistema == "tienda" else "RA-PE"
        title_text = f"Distribución en Edificios - {sistema_text}"
        if self.es_nuevo_producto:
            title_text = f"Distribuir en Edificios - {sistema_text}"
        
        title = tk.Label(mainFrame, 
                        text=title_text, 
                        font=(styles.FUENTE_PRINCIPAL, styles.TAMANO_SUBTITULO, styles.PESO_NEGRITA),
                        bg=styles.COLOR_FONDO, 
                        fg=styles.COLOR_TEXTO_OSCURO)
        title.pack(pady=(0, 10))
        
        # Subtítulo con nombre del producto
        tipo_producto = "Producto" if self.sistema == "tienda" else "Material"
        subtitle = tk.Label(mainFrame, 
                          text=f"{tipo_producto}: {self.producto_nombre}", 
                          font=(styles.FUENTE_PRINCIPAL, styles.TAMANO_NORMAL),
                          bg=styles.COLOR_FONDO, 
                          fg=styles.COLOR_TEXTO_MEDIO)
        subtitle.pack(pady=(0, 20))
        
        # Instrucción
        if self.es_nuevo_producto:
            instruction = tk.Label(mainFrame, 
                                 text="Configure el inventario para cada edificio. Luego guarde los cambios.", 
                                 font=(styles.FUENTE_PRINCIPAL, styles.TAMANO_PEQUENO, styles.PESO_NORMAL),
                                 bg=styles.COLOR_FONDO, 
                                 fg=styles.COLOR_TEXTO_CLARO)
            instruction.pack(pady=(0, 10))
        else:
            instruction = tk.Label(mainFrame, 
                                 text="Edite la información de inventario para cada edificio.", 
                                 font=(styles.FUENTE_PRINCIPAL, styles.TAMANO_PEQUENO, styles.PESO_NORMAL),
                                 bg=styles.COLOR_FONDO, 
                                 fg=styles.COLOR_TEXTO_CLARO)
            instruction.pack(pady=(0, 10))
        
        # Frame para la tabla (Treeview)
        tableFrame = tk.Frame(mainFrame, bg=styles.COLOR_FONDO)
        tableFrame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        # Crear Treeview
        columns = ("ID_Inv", "Edificio", "Cantidad", "Etiqueta", "Estante", "Lugar")
        self.tree = ttk.Treeview(tableFrame, columns=columns, show="headings", height=8)
        
        # Configurar columnas
        column_configs = [
            ("ID_Inv", "ID Inv", 80, "center"),
            ("Edificio", "Edificio", 200, "center"),
            ("Cantidad", "Cantidad", 100, "center"),
            ("Etiqueta", "Etiqueta", 150, "center"),
            ("Estante", "Estante", 100, "center"),
            ("Lugar", "Lugar", 150, "center")
        ]
        
        for col, heading, width, anchor in column_configs:
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
                        foreground=styles.COLOR_BLANCO,
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

        # Scrollbar
        scrollbar = ttk.Scrollbar(tableFrame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Layout Treeview y Scrollbar
        self.tree.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")
        
        # Configurar grid para expansión
        tableFrame.grid_rowconfigure(0, weight=1)
        tableFrame.grid_columnconfigure(0, weight=1)
        
        # Frame para botones
        buttonFrame = tk.Frame(mainFrame, bg=styles.COLOR_FONDO)
        buttonFrame.pack(fill=tk.X, pady=(0, 10))
        
        # Botón Editar Seleccionado
        self.btnEditar = tk.Button(buttonFrame, 
                                   text="Editar Registro Seleccionado", 
                                   font=(styles.FUENTE_PRINCIPAL, styles.TAMANO_NORMAL),
                                   bg=styles.COLOR_INFO, 
                                   fg=styles.COLOR_BLANCO,
                                   width=25,
                                   state=tk.DISABLED,
                                   command=self.editarRegistro)
        self.btnEditar.pack(side=tk.LEFT, padx=(0, 10))
        
        # Frame para botones finales
        finalButtonFrame = tk.Frame(mainFrame, bg=styles.COLOR_FONDO)
        finalButtonFrame.pack(fill=tk.X)
        
        # Botón Guardar (solo visible para nuevo producto)
        if self.es_nuevo_producto:
            self.btnGuardar = tk.Button(finalButtonFrame, 
                                       text="Guardar y Finalizar", 
                                       font=(styles.FUENTE_PRINCIPAL, styles.TAMANO_NORMAL, styles.PESO_NEGRITA),
                                       bg=styles.COLOR_EXITO, 
                                       fg=styles.COLOR_BLANCO,
                                       width=20,
                                       command=self.finalizarAgregado)
            self.btnGuardar.pack(side=tk.LEFT, padx=(0, 10))
        
        # Botón Cerrar
        btnText = "Cerrar" if not self.es_nuevo_producto else "Cancelar"
        btnCommand = self.window.destroy if not self.es_nuevo_producto else self.cancelarAgregado
        
        btnCerrar = tk.Button(finalButtonFrame, 
                             text=btnText, 
                             font=(styles.FUENTE_PRINCIPAL, styles.TAMANO_NORMAL),
                             bg=styles.COLOR_ADVERTENCIA if self.es_nuevo_producto else styles.COLOR_TEXTO_MEDIO, 
                             fg=styles.COLOR_BLANCO,
                             width=15,
                             command=btnCommand)
        btnCerrar.pack(side=tk.RIGHT)
        
        # Evento de selección en Treeview
        self.tree.bind("<<TreeviewSelect>>", self.onTreeSelect)
        
        # Variables para control
        self.registroSeleccionado = None
    
    def loadInventario(self):
        """Carga el inventario según el sistema (TIENDA o RA-PE)"""
        # Limpiar tabla
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Obtener inventario según sistema
        if self.sistema == "tienda":
            inventario = self.db.get_inventario_por_producto(self.producto_id)
        else:  # rape
            inventario = self.db.get_inventario_por_producto_rape(self.producto_id)
        
        if inventario:
            for i, registro in enumerate(inventario):
                # Determinar tag para fila alternada
                if i % 2 == 0:
                    tag_actual = 'even'
                else:
                    tag_actual = 'odd'
                
                # Insertar con tag
                self.tree.insert("", tk.END, 
                                values=(registro['id_invtienda'] if self.sistema == 'tienda' else registro['id_invrape'],
                                       registro['nombre_edificio'],
                                       registro['cantidad'],
                                       registro['etiqueta'] or "",
                                       registro['estante'] or "",
                                       registro['lugar'] or ""),
                                tags=(tag_actual,))
        
        # Si es producto nuevo y no hay registros, crearlos
        elif self.es_nuevo_producto:
            if self.crearRegistrosIniciales():
                self.loadInventario()  # Recargar tabla
    
    def crearRegistrosIniciales(self):
        """Crea registros iniciales de inventario para un nuevo producto"""
        try:
            if self.sistema == "tienda":
                success = self.db.create_inventario_para_edificios_tienda(self.producto_id)
            else:  # rape
                success = self.db.create_inventario_para_edificios_rape(self.producto_id)
            
            if success:
                return True
            else:
                sistema_text = "TIENDA" if self.sistema == "tienda" else "RA-PE"
                messagebox.showerror("Error", f"No se pudieron crear los registros de inventario iniciales para {sistema_text}")
                return False
        except Exception as e:
            messagebox.showerror("Error", f"Error creando registros iniciales: {e}")
            return False
    
    def onTreeSelect(self, event):
        """Maneja la selección de un registro en el Treeview"""
        selection = self.tree.selection()
        if selection:
            # Habilitar botón de edición
            self.btnEditar.config(state=tk.NORMAL)
            
            # Guardar el registro seleccionado
            item = self.tree.item(selection[0])
            self.registroSeleccionado = item['values'][0]
        else:
            self.btnEditar.config(state=tk.DISABLED)
            self.registroSeleccionado = None
    
    def editarRegistro(self):
        """Abre ventana para editar el registro seleccionado"""
        if not self.registroSeleccionado:
            return
        
        # Obtener datos del registro seleccionado
        selection = self.tree.selection()
        if not selection:
            return
        
        item = self.tree.item(selection[0])
        registro_data = {
            'id_inv': item['values'][0],
            'nombre_edificio': item['values'][1],
            'cantidad_actual': item['values'][2],
            'etiqueta_actual': item['values'][3],
            'estante_actual': item['values'][4],
            'lugar_actual': item['values'][5],
            'sistema': self.sistema  # Agregar sistema para saber qué tabla usar
        }
        
        # Abrir ventana de edición
        VentanaEditarRegistroInventario(self.window, registro_data, self)
        
    def actualizarRegistroEnTabla(self, id_inv, nuevos_valores):
        """Actualiza un registro en la tabla después de editarlo"""
        for child in self.tree.get_children():
            item = self.tree.item(child)
            if item['values'][0] == id_inv:
                # Actualizar valores
                self.tree.item(child, values=(
                    id_inv,
                    item['values'][1],  # Edificio (no cambia)
                    nuevos_valores['cantidad'],
                    nuevos_valores['etiqueta'],
                    nuevos_valores['estante'],
                    nuevos_valores['lugar']
                ))
                break
    
    def finalizarAgregado(self):
        """Finaliza el proceso de agregado de producto"""
        # Refrescar tabla principal si hay callback
        if self.callback_obj and hasattr(self.callback_obj, 'loadProductos'):
            self.callback_obj.loadProductos()
        
        sistema_text = "TIENDA" if self.sistema == "tienda" else "RA-PE"
        tipo_text = "Producto" if self.sistema == "tienda" else "Material"
        
        messagebox.showinfo("Éxito", 
                          f"{tipo_text} '{self.producto_nombre}' agregado exitosamente con su inventario distribuido en {sistema_text}.")
        self.window.destroy()
    
    def cancelarAgregado(self):
        """Cancela el proceso de agregado de producto"""
        sistema_text = "TIENDA" if self.sistema == "tienda" else "RA-PE"
        confirm = messagebox.askyesno("Cancelar", 
                                     f"¿Está seguro de cancelar la distribución en {sistema_text}?\n\n"
                                     f"El {self.sistema} se creará pero sin inventario distribuido.")
        if confirm:
            self.window.destroy()
    
    def on_window_close(self):
        """Se ejecuta cuando se cierra la ventana (X)"""
        # Si estamos en modo "detalles", refrescar la tabla principal
        if self.modo == "detalles" and self.callback_obj:
            if hasattr(self.callback_obj, 'loadProductos'):
                self.callback_obj.loadProductos()
        
        self.window.destroy()


class VentanaEditarRegistroInventario:
    """Ventana emergente para editar un registro de inventario específico"""
    
    def __init__(self, parent, registro_data, callback_obj):
        self.parent = parent
        self.registro_data = registro_data
        self.callback_obj = callback_obj
        self.sistema = registro_data.get('sistema', 'tienda')
        self.db = Database()
        
        # Crear ventana emergente
        self.window = tk.Toplevel(parent)
        self.window.title(f"Editar Registro de Inventario")
        self.window.geometry("500x700")
        self.window.configure(bg=styles.COLOR_FONDO)
        self.window.transient(parent)
        self.window.grab_set()
        
        # Centrar ventana
        self.centerWindow(500, 700)
        
        # Crear interfaz
        self.createWidgets()
    
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
        sistema_text = "TIENDA" if self.sistema == "tienda" else "RA-PE"
        title = tk.Label(mainFrame, 
                        text=f"EDITAR REGISTRO - {sistema_text}", 
                        font=(styles.FUENTE_PRINCIPAL, styles.TAMANO_SUBTITULO, styles.PESO_NEGRITA),
                        bg=styles.COLOR_FONDO, 
                        fg=styles.COLOR_TEXTO_OSCURO)
        title.pack(pady=(0, 20))
        
        # Información del edificio (solo lectura)
        edificioFrame = tk.Frame(mainFrame, bg=styles.COLOR_FONDO)
        edificioFrame.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(edificioFrame, 
                text="Edificio:", 
                font=(styles.FUENTE_PRINCIPAL, styles.TAMANO_NORMAL, styles.PESO_NEGRITA),
                bg=styles.COLOR_FONDO, 
                fg=styles.COLOR_TEXTO_OSCURO).pack(side=tk.LEFT)
        
        tk.Label(edificioFrame, 
                text=self.registro_data['nombre_edificio'], 
                font=(styles.FUENTE_PRINCIPAL, styles.TAMANO_NORMAL),
                bg=styles.COLOR_FONDO, 
                fg=styles.COLOR_TEXTO_MEDIO).pack(side=tk.LEFT, padx=(10, 0))
        
        # Separador
        separator = tk.Frame(mainFrame, height=2, bg=styles.COLOR_BORDE)
        separator.pack(fill=tk.X, pady=(0, 20))
        
        # Frame para formulario
        formFrame = tk.Frame(mainFrame, bg=styles.COLOR_FONDO)
        formFrame.pack(fill=tk.X)
        
        # Campo: Cantidad
        tk.Label(formFrame, 
                text="Cantidad:", 
                font=(styles.FUENTE_PRINCIPAL, styles.TAMANO_NORMAL),
                bg=styles.COLOR_FONDO, 
                fg=styles.COLOR_TEXTO_OSCURO).grid(row=0, column=0, padx=(0, 10), pady=10, sticky="w")
        
        self.cantidadVar = tk.StringVar(value=str(self.registro_data['cantidad_actual']))
        self.cantidadEntry = tk.Entry(formFrame, 
                                      textvariable=self.cantidadVar,
                                      font=(styles.FUENTE_PRINCIPAL, styles.TAMANO_NORMAL),
                                      width=15)
        self.cantidadEntry.grid(row=0, column=1, pady=10, sticky="w")
        
        # Campo: Etiqueta
        tk.Label(formFrame, 
                text="Etiqueta:", 
                font=(styles.FUENTE_PRINCIPAL, styles.TAMANO_NORMAL),
                bg=styles.COLOR_FONDO, 
                fg=styles.COLOR_TEXTO_OSCURO).grid(row=1, column=0, padx=(0, 10), pady=10, sticky="w")
        
        self.etiquetaVar = tk.StringVar(value=self.registro_data['etiqueta_actual'] or "")
        self.etiquetaEntry = tk.Entry(formFrame, 
                                      textvariable=self.etiquetaVar,
                                      font=(styles.FUENTE_PRINCIPAL, styles.TAMANO_NORMAL),
                                      width=20)
        self.etiquetaEntry.grid(row=1, column=1, pady=10, sticky="w")
        
        # Campo: Estante
        tk.Label(formFrame, 
                text="Estante:", 
                font=(styles.FUENTE_PRINCIPAL, styles.TAMANO_NORMAL),
                bg=styles.COLOR_FONDO, 
                fg=styles.COLOR_TEXTO_OSCURO).grid(row=2, column=0, padx=(0, 10), pady=10, sticky="w")
        
        self.estanteVar = tk.StringVar(value=self.registro_data['estante_actual'] or "")
        self.estanteEntry = tk.Entry(formFrame, 
                                     textvariable=self.estanteVar,
                                     font=(styles.FUENTE_PRINCIPAL, styles.TAMANO_NORMAL),
                                     width=20)
        self.estanteEntry.grid(row=2, column=1, pady=10, sticky="w")
        
        # Campo: Lugar
        tk.Label(formFrame, 
                text="Lugar:", 
                font=(styles.FUENTE_PRINCIPAL, styles.TAMANO_NORMAL),
                bg=styles.COLOR_FONDO, 
                fg=styles.COLOR_TEXTO_OSCURO).grid(row=3, column=0, padx=(0, 10), pady=10, sticky="w")
        
        self.lugarVar = tk.StringVar(value=self.registro_data['lugar_actual'] or "")
        self.lugarEntry = tk.Entry(formFrame, 
                                   textvariable=self.lugarVar,
                                   font=(styles.FUENTE_PRINCIPAL, styles.TAMANO_NORMAL),
                                   width=20)
        self.lugarEntry.grid(row=3, column=1, pady=10, sticky="w")
        
        # Frame para botones
        buttonFrame = tk.Frame(mainFrame, bg=styles.COLOR_FONDO)
        buttonFrame.pack(fill=tk.X, pady=(30, 0))
        
        # Botón Guardar
        btnGuardar = tk.Button(buttonFrame, 
                              text="Guardar Cambios", 
                              font=(styles.FUENTE_PRINCIPAL, styles.TAMANO_NORMAL),
                              bg=styles.COLOR_EXITO, 
                              fg=styles.COLOR_BLANCO,
                              width=15,
                              command=self.guardarCambios)
        btnGuardar.pack(side=tk.LEFT, padx=(0, 10))
        
        # Botón Cancelar
        btnCancelar = tk.Button(buttonFrame, 
                               text="Cancelar", 
                               font=(styles.FUENTE_PRINCIPAL, styles.TAMANO_NORMAL),
                               bg=styles.COLOR_ADVERTENCIA, 
                               fg=styles.COLOR_BLANCO,
                               width=15,
                               command=self.window.destroy)
        btnCancelar.pack(side=tk.LEFT)
    
    def buscarYActualizarAlarmas(self):
        """Busca ventana de alarmas y la actualiza - VERSIÓN MEJORADA"""
        try:
            # Si el callback_obj es una ventana de alarmas, actualizarla directamente
            if hasattr(self.callback_obj, 'callback_obj'):
                alarm_window = self.callback_obj.callback_obj
                if alarm_window and hasattr(alarm_window, 'actualizarTabla'):
                    alarm_window.actualizarTabla()
                    print(f"[INFO] Tabla de alarmas actualizada directamente desde inventario")
                    return True
            
            # Buscar ventana de alarmas en la jerarquía de ventanas
            # Buscar en el parent principal (ventana raíz de la aplicación)
            root_window = self.window.winfo_toplevel()
            
            # Buscar entre todas las ventanas hijas del root
            for child in root_window.winfo_children():
                if isinstance(child, tk.Toplevel):
                    try:
                        title = child.title().lower()
                        if 'alarma' in title or 'alerta' in title:
                            if hasattr(child, 'actualizarTabla'):
                                child.actualizarTabla()
                                print(f"[INFO] Ventana de alarmas encontrada y actualizada")
                                return True
                    except:
                        continue
                        
        except Exception as e:
            print(f"[ERROR] Error buscando alarmas: {e}")
        
        print("[INFO] No se encontró ventana de alarmas para actualizar")
        return False

    def guardarCambios(self):
        """Guarda los cambios del registro de inventario"""
        # Validar cantidad
        try:
            cantidad = int(self.cantidadVar.get().strip())
            if cantidad < 0:
                raise ValueError("La cantidad no puede ser negativa")
        except ValueError:
            messagebox.showwarning("Valor inválido", "Por favor ingrese una cantidad válida (número entero no negativo)")
            self.cantidadEntry.focus()
            return
        
        # Preparar datos
        etiqueta = self.etiquetaVar.get().strip()
        estante = self.estanteVar.get().strip()
        lugar = self.lugarVar.get().strip()
        
        # Convertir a None si están vacíos
        etiqueta = etiqueta if etiqueta else None
        estante = estante if estante else None
        lugar = lugar if lugar else None
        
        try:
            # Actualizar en base de datos según sistema
            if self.sistema == "tienda":
                success = self.db.update_inventario_tienda(
                    id_invtienda=self.registro_data['id_inv'],
                    cantidad=cantidad,
                    etiqueta=etiqueta,
                    estante=estante,
                    lugar=lugar
                )
            else:  # rape
                success = self.db.update_inventario_rape(
                    id_invrape=self.registro_data['id_inv'],
                    cantidad=cantidad,
                    etiqueta=etiqueta,
                    estante=estante,
                    lugar=lugar
                )
            
            if success:
                messagebox.showinfo("Éxito", "Registro actualizado exitosamente")
                
                # Notificar a la ventana padre para actualizar la tabla
                nuevos_valores = {
                    'cantidad': cantidad,
                    'etiqueta': etiqueta or "",
                    'estante': estante or "",
                    'lugar': lugar or ""
                }
                self.callback_obj.actualizarRegistroEnTabla(
                    self.registro_data['id_inv'], 
                    nuevos_valores
                )
                
                # Actualizar ventana de alarmas si está abierta
                self.buscarYActualizarAlarmas()
                
                # Actualizar tabla principal si hay callback principal
                if hasattr(self.callback_obj, 'callback_obj'):
                    main_callback = self.callback_obj.callback_obj
                    if main_callback and hasattr(main_callback, 'loadProductos'):
                        main_callback.loadProductos()
                
                self.window.destroy()
            else:
                messagebox.showerror("Error", "No se pudo actualizar el registro")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al actualizar registro: {e}")
"""
Ventana CRUD para gestión de Edificios
"""

import tkinter as tk
from tkinter import ttk, messagebox
import styles
from db import Database

class VentanaEdificio:
    def __init__(self, parent, systemName):
        self.parent = parent
        self.systemName = systemName
        self.db = Database()
        
        # Crear ventana emergente
        self.window = tk.Toplevel(parent)
        self.window.title(f"Gestión de Edificios - {systemName}")
        self.window.geometry("1000x700")
        self.window.minsize(1000, 700) 
        self.window.maxsize(1000, 700)  
        self.window.configure(bg=styles.COLOR_FONDO)
        self.window.transient(parent)
        self.window.grab_set()
        
        # Centrar ventana
        self.centerWindow(600, 400)
        
        # Crear interfaz principal
        self.createWidgets()
        self.loadEdificios()
    
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
        
        # Título
        title = tk.Label(mainFrame, 
                        text="GESTIÓN DE EDIFICIOS", 
                        font=(styles.FUENTE_PRINCIPAL, styles.TAMANO_TITULO, styles.PESO_NEGRITA),
                        bg=styles.COLOR_FONDO, 
                        fg=styles.COLOR_TEXTO_OSCURO)
        title.pack(pady=(0, 20))
        
        # Frame para botones de acción principales
        buttonFrame = tk.Frame(mainFrame, bg=styles.COLOR_FONDO)
        buttonFrame.pack(fill=tk.X, pady=(0, 15))
        
        # Botón Agregar Edificio
        self.btnAgregar = tk.Button(buttonFrame, 
                                    text="Agregar Nuevo Edificio", 
                                    font=(styles.FUENTE_PRINCIPAL, styles.TAMANO_NORMAL),
                                    bg=styles.COLOR_EXITO, 
                                    fg=styles.COLOR_BLANCO,
                                    width=20,
                                    command=self.abrirAgregarEdificio)
        self.btnAgregar.pack(side=tk.LEFT, padx=(0, 10))
        
        # Botón Editar
        self.btnEditar = tk.Button(buttonFrame, 
                                   text="Editar Edificio", 
                                   font=(styles.FUENTE_PRINCIPAL, styles.TAMANO_NORMAL),
                                   bg=styles.COLOR_INFO, 
                                   fg=styles.COLOR_BLANCO,
                                   width=20,
                                   state=tk.DISABLED,
                                   command=self.abrirEditarEdificio)
        self.btnEditar.pack(side=tk.LEFT, padx=(0, 10))
        
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
        
        # Crear Treeview con más columnas
        columns = ("ID", "Nombre", "Dirección", "Tipo", "Inventario")
        self.tree = ttk.Treeview(tableFrame, columns=columns, show="headings", height=15)
        
        # Configurar columnas
        column_widths = [80, 200, 250, 150, 200]
        column_names = ["ID", "Nombre del Edificio", "Dirección", "Tipo", "Sistema Inventario"]
        
        for i, (col, name, width) in enumerate(zip(columns, column_names, column_widths)):
            self.tree.heading(col, text=name)
            self.tree.column(col, width=width, anchor="center")

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
                                     text="Eliminar Edificio Seleccionado", 
                                     font=(styles.FUENTE_PRINCIPAL, styles.TAMANO_NORMAL),
                                     bg=styles.COLOR_PELIGRO, 
                                     fg=styles.COLOR_BLANCO,
                                     width=25,
                                     state=tk.DISABLED,
                                     command=self.eliminarEdificio)
        self.btnEliminar.pack(side=tk.LEFT, padx=(0, 20))
        
        # Evento de selección en Treeview
        self.tree.bind("<<TreeviewSelect>>", self.onTreeSelect)
        
        # Variables para control de edición
        self.edificioSeleccionado = None
    
    def loadEdificios(self):
        """Carga los edificios desde la base de datos usando vista optimizada"""
        # Limpiar tabla
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Obtener edificios usando vista optimizada
        edificios = self.db.get_all_edificios()
        
        if edificios:
            for i, edificio in enumerate(edificios):
                # Determinar tag para fila alternada
                if i % 2 == 0:
                    tag_actual = 'even'
                else:
                    tag_actual = 'odd'
                
                # Insertar con tag
                self.tree.insert("", tk.END, 
                                values=(edificio['id_edificio'], 
                                    edificio['nombre_edificio'],
                                    edificio['direccion'],
                                    edificio['tipo'],
                                    edificio['nombre_inventario']),
                                tags=(tag_actual,))
    
    def onTreeSelect(self, event):
        """Maneja la selección de un edificio en el Treeview"""
        selection = self.tree.selection()
        if selection:
            # Habilitar botones de edición y eliminación
            self.btnEditar.config(state=tk.NORMAL)
            self.btnEliminar.config(state=tk.NORMAL)
            
            # Guardar el edificio seleccionado
            item = self.tree.item(selection[0])
            self.edificioSeleccionado = item['values'][0]
        else:
            self.btnEditar.config(state=tk.DISABLED)
            self.btnEliminar.config(state=tk.DISABLED)
            self.edificioSeleccionado = None
    
    def abrirAgregarEdificio(self):
        """Abre ventana para agregar nuevo edificio"""
        VentanaDetalleEdificio(self.window, "Agregar Edificio", None, self)
    
    def abrirEditarEdificio(self):
        """Abre ventana para editar edificio existente"""
        if self.edificioSeleccionado:
            VentanaDetalleEdificio(self.window, "Editar Edificio", self.edificioSeleccionado, self)
        else:
            messagebox.showwarning("Selección requerida", "Por favor seleccione un edificio para editar")
    
    def eliminarEdificio(self):
        """Elimina el edificio seleccionado"""
        if not self.edificioSeleccionado:
            return
        
        # Obtener nombre del edificio
        selection = self.tree.selection()
        if not selection:
            return
        
        item = self.tree.item(selection[0])
        edificioNombre = item['values'][1]
        
        # Confirmar eliminación
        confirm = messagebox.askyesno("Confirmar eliminación", 
                                     f"¿Está seguro de eliminar el edificio '{edificioNombre}'?\n\nEsta acción no se puede deshacer.")
        if not confirm:
            return
        
        try:
            success, message = self.db.delete_edificio(self.edificioSeleccionado)
            if success:
                messagebox.showinfo("Éxito", message)
                self.loadEdificios()
                self.edificioSeleccionado = None
                self.btnEditar.config(state=tk.DISABLED)
                self.btnEliminar.config(state=tk.DISABLED)
            else:
                messagebox.showwarning("No se puede eliminar", message)
        except Exception as e:
            messagebox.showerror("Error", f"Error al eliminar edificio: {e}")


class VentanaDetalleEdificio:
    """Ventana emergente para agregar/editar edificios"""
    
    def __init__(self, parent, titulo, edificio_id=None, callback_obj=None):
        self.parent = parent
        self.titulo = titulo
        self.edificio_id = edificio_id
        self.callback_obj = callback_obj
        self.db = Database()
        
        # Crear ventana emergente
        self.window = tk.Toplevel(parent)
        self.window.title(titulo)
        self.window.geometry("500x400")
        self.window.configure(bg=styles.COLOR_FONDO)
        self.window.transient(parent)
        self.window.grab_set()
        
        # Centrar ventana
        self.centerWindow(500, 400)
        
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
        
        # Campo: Nombre del Edificio
        tk.Label(formFrame, 
                text="Nombre del Edificio:", 
                font=(styles.FUENTE_PRINCIPAL, styles.TAMANO_NORMAL),
                bg=styles.COLOR_FONDO, 
                fg=styles.COLOR_TEXTO_OSCURO).grid(row=0, column=0, padx=(0, 10), pady=10, sticky="w")
        
        self.nombreVar = tk.StringVar()
        self.nombreEntry = tk.Entry(formFrame, 
                                    textvariable=self.nombreVar,
                                    font=(styles.FUENTE_PRINCIPAL, styles.TAMANO_NORMAL),
                                    width=30)
        self.nombreEntry.grid(row=0, column=1, pady=10, sticky="w")
        
        # Campo: Dirección
        tk.Label(formFrame, 
                text="Dirección:", 
                font=(styles.FUENTE_PRINCIPAL, styles.TAMANO_NORMAL),
                bg=styles.COLOR_FONDO, 
                fg=styles.COLOR_TEXTO_OSCURO).grid(row=1, column=0, padx=(0, 10), pady=10, sticky="w")
        
        self.direccionVar = tk.StringVar()
        self.direccionEntry = tk.Entry(formFrame, 
                                       textvariable=self.direccionVar,
                                       font=(styles.FUENTE_PRINCIPAL, styles.TAMANO_NORMAL),
                                       width=30)
        self.direccionEntry.grid(row=1, column=1, pady=10, sticky="w")
        
        # Campo: Tipo (Combobox)
        tk.Label(formFrame, 
                text="Tipo:", 
                font=(styles.FUENTE_PRINCIPAL, styles.TAMANO_NORMAL),
                bg=styles.COLOR_FONDO, 
                fg=styles.COLOR_TEXTO_OSCURO).grid(row=2, column=0, padx=(0, 10), pady=10, sticky="w")
        
        self.tipoVar = tk.StringVar()
        self.tipoCombobox = ttk.Combobox(formFrame, 
                                        textvariable=self.tipoVar,
                                        font=(styles.FUENTE_PRINCIPAL, styles.TAMANO_NORMAL),
                                        width=28,
                                        state="readonly")
        self.tipoCombobox['values'] = ('Bodega', 'Armarios', 'Almacen')
        self.tipoCombobox.grid(row=2, column=1, pady=10, sticky="w")
        
        # Campo: Inventario (Combobox)
        tk.Label(formFrame, 
                text="Sistema Inventario:", 
                font=(styles.FUENTE_PRINCIPAL, styles.TAMANO_NORMAL),
                bg=styles.COLOR_FONDO, 
                fg=styles.COLOR_TEXTO_OSCURO).grid(row=3, column=0, padx=(0, 10), pady=10, sticky="w")
        
        self.inventarioVar = tk.IntVar()
        self.inventarioCombobox = ttk.Combobox(formFrame, 
                                              font=(styles.FUENTE_PRINCIPAL, styles.TAMANO_NORMAL),
                                              width=28,
                                              state="readonly")
        self.inventarioCombobox.grid(row=3, column=1, pady=10, sticky="w")
        
        # Frame para botones
        buttonFrame = tk.Frame(mainFrame, bg=styles.COLOR_FONDO)
        buttonFrame.pack(fill=tk.X, pady=(30, 0))
        
        # Botón Guardar
        btnGuardar = tk.Button(buttonFrame, 
                              text="Guardar", 
                              font=(styles.FUENTE_PRINCIPAL, styles.TAMANO_NORMAL),
                              bg=styles.COLOR_EXITO, 
                              fg=styles.COLOR_BLANCO,
                              width=15,
                              command=self.guardarEdificio)
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
    
    def loadDatos(self):
        """Carga datos en el formulario"""
        # Cargar inventarios en el combobox
        inventarios = self.db.get_all_inventarios()
        if inventarios:
            inventario_dict = {}
            nombres_inventarios = []
            for inv in inventarios:
                nombres_inventarios.append(inv['nombre_inventario'])
                inventario_dict[inv['nombre_inventario']] = inv['id_inventario']
            
            self.inventarioCombobox['values'] = nombres_inventarios
            self.inventario_dict = inventario_dict
        
        # Si es edición, cargar datos del edificio
        if self.edificio_id:
            edificio = self.db.get_edificio_by_id(self.edificio_id)
            if edificio:
                self.nombreVar.set(edificio['nombre_edificio'])
                self.direccionVar.set(edificio['direccion'])
                self.tipoVar.set(edificio['tipo'])
                
                # Seleccionar el inventario correspondiente
                if 'nombre_inventario' in edificio and edificio['nombre_inventario']:
                    self.inventarioCombobox.set(edificio['nombre_inventario'])
    
    def guardarEdificio(self):
        """Guarda o actualiza el edificio"""
        # Validar campos
        nombre = self.nombreVar.get().strip()
        direccion = self.direccionVar.get().strip()
        tipo = self.tipoVar.get()
        inventario_nombre = self.inventarioCombobox.get()
        
        if not nombre:
            messagebox.showwarning("Campo requerido", "Por favor ingrese el nombre del edificio")
            self.nombreEntry.focus()
            return
        
        if not direccion:
            messagebox.showwarning("Campo requerido", "Por favor ingrese la dirección del edificio")
            self.direccionEntry.focus()
            return
        
        if not tipo:
            messagebox.showwarning("Campo requerido", "Por favor seleccione el tipo de edificio")
            self.tipoCombobox.focus()
            return
        
        if not inventario_nombre:
            messagebox.showwarning("Campo requerido", "Por favor seleccione el sistema de inventario")
            self.inventarioCombobox.focus()
            return
        
        # Obtener ID del inventario
        id_inventario = self.inventario_dict.get(inventario_nombre)
        if not id_inventario:
            messagebox.showerror("Error", "Sistema de inventario no válido")
            return
        
        try:
            if self.edificio_id:
                # Actualizar edificio existente
                success = self.db.update_edificio(self.edificio_id, nombre, direccion, tipo, id_inventario)
                if success:
                    messagebox.showinfo("Éxito", f"Edificio '{nombre}' actualizado exitosamente")
                    self.window.destroy()
                    if self.callback_obj:
                        self.callback_obj.loadEdificios()
                else:
                    messagebox.showerror("Error", "No se pudo actualizar el edificio")
            else:
                # Crear nuevo edificio
                edificioId = self.db.create_edificio(nombre, direccion, tipo, id_inventario)
                if edificioId:
                    messagebox.showinfo("Éxito", f"Edificio '{nombre}' creado exitosamente")
                    self.window.destroy()
                    if self.callback_obj:
                        self.callback_obj.loadEdificios()
                else:
                    messagebox.showerror("Error", "No se pudo crear el edificio")
                    
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar edificio: {e}")
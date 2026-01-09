"""
Ventana CRUD para gestión de Marcas
"""

import tkinter as tk
from tkinter import ttk, messagebox
import styles
from db import Database

class VentanaMarca:
    def __init__(self, parent, systemName):
        self.parent = parent
        self.systemName = systemName
        self.db = Database()
        
        # Crear ventana emergente
        self.window = tk.Toplevel(parent)
        self.window.title(f"Gestión de Marcas - {systemName}")
        self.window.geometry("1000x700")
        self.window.minsize(1000, 700) 
        self.window.maxsize(1000, 700)  
        self.window.configure(bg=styles.COLOR_FONDO)
        self.window.transient(parent)
        self.window.grab_set()
        
        # Centrar ventana
        self.centerWindow(600, 400)
        
        # Crear interfaz
        self.createWidgets()
        self.loadMarcas()
    
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
        title = tk.Label(mainFrame, 
                        text="GESTIÓN DE MARCAS", 
                        font=(styles.FUENTE_PRINCIPAL, styles.TAMANO_TITULO, styles.PESO_NEGRITA),
                        bg=styles.COLOR_FONDO, 
                        fg=styles.COLOR_TEXTO_OSCURO)
        title.pack(pady=(0, 20))
        
        # Frame para controles (agregar/editar)
        controlFrame = tk.Frame(mainFrame, bg=styles.COLOR_FONDO)
        controlFrame.pack(fill=tk.X, pady=(0, 15))
        
        # Label y Entry para nombre de marca
        tk.Label(controlFrame, 
                text="Nombre de la marca:", 
                font=(styles.FUENTE_PRINCIPAL, styles.TAMANO_NORMAL),
                bg=styles.COLOR_FONDO, 
                fg=styles.COLOR_TEXTO_OSCURO).grid(row=0, column=0, padx=(0, 10), sticky="w")
        
        self.nombreVar = tk.StringVar()
        self.nombreEntry = tk.Entry(controlFrame, 
                                    textvariable=self.nombreVar,
                                    font=(styles.FUENTE_PRINCIPAL, styles.TAMANO_NORMAL),
                                    width=30)
        self.nombreEntry.grid(row=0, column=1, padx=(0, 15))
        
        # Frame para botones de acción
        buttonFrame = tk.Frame(controlFrame, bg=styles.COLOR_FONDO)
        buttonFrame.grid(row=0, column=2, sticky="w")
        
        # Botones Agregar/Editar/Cancelar
        self.btnAgregar = tk.Button(buttonFrame, 
                                    text="Agregar", 
                                    font=(styles.FUENTE_PRINCIPAL, styles.TAMANO_NORMAL),
                                    bg=styles.COLOR_EXITO, 
                                    fg=styles.COLOR_BLANCO,
                                    width=10,
                                    command=self.agregarMarca)
        self.btnAgregar.pack(side=tk.LEFT, padx=5)
        
        self.btnEditar = tk.Button(buttonFrame, 
                                   text="Editar", 
                                   font=(styles.FUENTE_PRINCIPAL, styles.TAMANO_NORMAL),
                                   bg=styles.COLOR_INFO, 
                                   fg=styles.COLOR_BLANCO,
                                   width=10,
                                   state=tk.DISABLED,
                                   command=self.editarMarca)
        self.btnEditar.pack(side=tk.LEFT, padx=5)
        
        self.btnCancelar = tk.Button(buttonFrame, 
                                     text="Cancelar", 
                                     font=(styles.FUENTE_PRINCIPAL, styles.TAMANO_NORMAL),
                                     bg=styles.COLOR_ADVERTENCIA, 
                                     fg=styles.COLOR_BLANCO,
                                     width=10,
                                     state=tk.DISABLED,
                                     command=self.cancelarEdicion)
        self.btnCancelar.pack(side=tk.LEFT, padx=5)
        
        # Separador
        separator = tk.Frame(mainFrame, height=2, bg=styles.COLOR_BORDE)
        separator.pack(fill=tk.X, pady=(0, 10))
        
        # Frame para la tabla (Treeview)
        tableFrame = tk.Frame(mainFrame, bg=styles.COLOR_FONDO)
        tableFrame.pack(fill=tk.BOTH, expand=True)
        
        # Crear Treeview
        columns = ("ID", "Nombre")
        self.tree = ttk.Treeview(tableFrame, columns=columns, show="headings", height=15)
        
        # Configurar columnas
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nombre", text="Nombre de la Marca")
        self.tree.column("ID", width=100, anchor="center")
        self.tree.column("Nombre", width=700, anchor="center")

        # Configurar estilo para el Treeview
        style = ttk.Style()
        
        # Configurar estilo global para Treeview
        style.configure("Treeview",
                        background=styles.COLOR_FONDO,
                        foreground=styles.COLOR_TEXTO_OSCURO,
                        fieldbackground=styles.COLOR_FONDO)
        
        # Configurar específicamente los headings
        style.configure("Treeview.Heading", 
                        background=styles.COLOR_TREEVIEW_HEADING,
                        foreground=styles.COLOR_TEXTO_OSCURO,
                        font=(styles.FUENTE_PRINCIPAL, styles.TAMANO_NORMAL, styles.PESO_NEGRITA))
        
        # Aplicar el estilo al Treeview
        self.tree.configure(style="Treeview")

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
                                     text="Eliminar Marca Seleccionada", 
                                     font=(styles.FUENTE_PRINCIPAL, styles.TAMANO_NORMAL),
                                     bg=styles.COLOR_PELIGRO, 
                                     fg=styles.COLOR_BLANCO,
                                     width=25,
                                     state=tk.DISABLED,
                                     command=self.eliminarMarca)
        self.btnEliminar.pack(side=tk.LEFT, padx=(0, 20))
        
        # Botón Cerrar
        btnCerrar = tk.Button(bottomFrame, 
                              text="Cerrar", 
                              font=(styles.FUENTE_PRINCIPAL, styles.TAMANO_NORMAL),
                              bg=styles.COLOR_TEXTO_MEDIO, 
                              fg=styles.COLOR_BLANCO,
                              width=15,
                              command=self.window.destroy)
        btnCerrar.pack(side=tk.RIGHT)
        
        # Evento de selección en Treeview
        self.tree.bind("<<TreeviewSelect>>", self.onTreeSelect)
        
        # Variables para control de edición
        self.editingId = None
    
    def loadMarcas(self):
        """Carga las marcas desde la base de datos"""
        # Limpiar tabla
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Obtener marcas
        marcas = self.db.get_all_marcas()
        
        if marcas:
            for i, marca in enumerate(marcas):
                # Determinar tag para fila alternada
                if i % 2 == 0:
                    tag_actual = 'even'
                else:
                    tag_actual = 'odd'
                
                # Insertar con tag
                self.tree.insert("", tk.END, 
                                values=(marca['id_marca'], marca['nombre_marca']),
                                tags=(tag_actual,))
    
    def onTreeSelect(self, event):
        """Maneja la selección de una marca en el Treeview"""
        selection = self.tree.selection()
        if selection:
            # Habilitar botones de edición y eliminación
            self.btnEditar.config(state=tk.NORMAL)
            self.btnEliminar.config(state=tk.NORMAL)
            
            # Si no estamos en modo edición, cargar la marca seleccionada en el entry
            if not self.editingId:
                item = self.tree.item(selection[0])
                self.nombreVar.set(item['values'][1])
        else:
            self.btnEditar.config(state=tk.DISABLED)
            self.btnEliminar.config(state=tk.DISABLED)
    
    def agregarMarca(self):
        """Agrega una nueva marca"""
        nombre = self.nombreVar.get().strip()
        
        if not nombre:
            messagebox.showwarning("Campo requerido", "Por favor ingrese un nombre para la marca")
            return
        
        try:
            marcaId = self.db.create_marca(nombre)
            if marcaId:
                messagebox.showinfo("Éxito", f"Marca '{nombre}' creada exitosamente")
                self.nombreVar.set("")
                self.loadMarcas()
            else:
                messagebox.showerror("Error", "No se pudo crear la marca")
        except Exception as e:
            messagebox.showerror("Error", f"Error al crear marca: {e}")
    
    def editarMarca(self):
        """Inicia modo edición para la marca seleccionada"""
        selection = self.tree.selection()
        if not selection:
            return
        
        item = self.tree.item(selection[0])
        self.editingId = item['values'][0]
        
        # Cambiar estado de botones
        self.btnAgregar.config(state=tk.DISABLED)
        self.btnEditar.config(text="Guardar", command=self.guardarEdicion)
        self.btnCancelar.config(state=tk.NORMAL)
        self.btnEliminar.config(state=tk.DISABLED)
        
        # Cargar datos en entry
        self.nombreVar.set(item['values'][1])
        self.nombreEntry.focus()
    
    def guardarEdicion(self):
        """Guarda los cambios de la marca editada"""
        if not self.editingId:
            return
        
        nombre = self.nombreVar.get().strip()
        
        if not nombre:
            messagebox.showwarning("Campo requerido", "Por favor ingrese un nombre para la marca")
            return
        
        try:
            success = self.db.update_marca(self.editingId, nombre)
            if success:
                messagebox.showinfo("Éxito", f"Marca actualizada exitosamente")
                self.cancelarEdicion()
                self.loadMarcas()
            else:
                messagebox.showerror("Error", "No se pudo actualizar la marca")
        except Exception as e:
            messagebox.showerror("Error", f"Error al actualizar marca: {e}")
    
    def cancelarEdicion(self):
        """Cancela el modo edición"""
        self.editingId = None
        self.nombreVar.set("")
        
        # Restaurar estado de botones
        self.btnAgregar.config(state=tk.NORMAL)
        self.btnEditar.config(text="Editar", command=self.editarMarca)
        self.btnCancelar.config(state=tk.DISABLED)
        self.btnEliminar.config(state=tk.NORMAL)
        
        # Limpiar selección
        self.tree.selection_remove(self.tree.selection())
    
    def eliminarMarca(self):
        """Elimina la marca seleccionada"""
        selection = self.tree.selection()
        if not selection:
            return
        
        item = self.tree.item(selection[0])
        marcaId = item['values'][0]
        marcaNombre = item['values'][1]
        
        # Confirmar eliminación
        confirm = messagebox.askyesno("Confirmar eliminación", 
                                     f"¿Está seguro de eliminar la marca '{marcaNombre}'?")
        if not confirm:
            return
        
        try:
            success, message = self.db.delete_marca(marcaId)
            if success:
                messagebox.showinfo("Éxito", message)
                self.loadMarcas()
                self.nombreVar.set("")
            else:
                messagebox.showwarning("No se puede eliminar", message)
        except Exception as e:
            messagebox.showerror("Error", f"Error al eliminar marca: {e}")
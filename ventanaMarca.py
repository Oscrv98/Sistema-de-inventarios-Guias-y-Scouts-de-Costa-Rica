"""
Ventana CRUD para gestión de Marcas
"""

import tkinter as tk
from tkinter import ttk, messagebox
import styles
from db import Database

class VentanaMarca:
    # ===== INICIALIZACIÓN =====
    def __init__(self, parent, systemName):
        self.parent = parent
        self.systemName = systemName
        self.db = Database()
        
        self.window = tk.Toplevel(parent)
        self.window.title(f"Gestión de Marcas - {systemName}")
        self.window.geometry("1000x700")
        self.window.minsize(1000, 700) 
        self.window.maxsize(1000, 700)  
        self.window.configure(bg=styles.COLOR_FONDO_OSCURO)
        self.window.transient(parent)
        self.window.grab_set()
        
        self.centerWindow(600, 400)
        self.createWidgets()
        self.loadMarcas()
    
    # ===== MÉTODOS DE CONFIGURACIÓN DE VENTANA =====
    def centerWindow(self, width, height):
        screenWidth = self.window.winfo_screenwidth()
        screenHeight = self.window.winfo_screenheight()
        x = (screenWidth // 2) - (width // 2)
        y = (screenHeight // 2) - (height // 2)
        self.window.geometry(f"{width}x{height}+{x}+{y}")
    
    # ===== CREACIÓN DE INTERFAZ =====
    def createWidgets(self):
        mainFrame = tk.Frame(self.window, bg=styles.COLOR_FONDO_OSCURO, padx=20, pady=20)
        mainFrame.pack(fill=tk.BOTH, expand=True)
        
        title = tk.Label(mainFrame, 
                        text="GESTIÓN DE MARCAS", 
                        font=(styles.FUENTE_PRINCIPAL, styles.TAMANO_TITULO, styles.PESO_NEGRITA),
                        bg=styles.COLOR_FONDO_OSCURO, 
                        fg=styles.COLOR_BLANCO)
        title.pack(pady=(0, 20))
        
        controlFrame = tk.Frame(mainFrame, bg=styles.COLOR_FONDO_OSCURO)
        controlFrame.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(controlFrame, 
                text="Nombre de la marca:", 
                font=(styles.FUENTE_PRINCIPAL, styles.TAMANO_NORMAL),
                bg=styles.COLOR_FONDO_OSCURO, 
                fg=styles.COLOR_BLANCO).grid(row=0, column=0, padx=(0, 10), sticky="w")
        
        self.nombreVar = tk.StringVar()
        self.nombreEntry = tk.Entry(controlFrame, 
                                    textvariable=self.nombreVar,
                                    font=(styles.FUENTE_PRINCIPAL, styles.TAMANO_NORMAL),
                                    width=30)
        self.nombreEntry.grid(row=0, column=1, padx=(0, 15))
        
        buttonFrame = tk.Frame(controlFrame, bg=styles.COLOR_FONDO_OSCURO)
        buttonFrame.grid(row=0, column=2, sticky="w")
        
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
        
        separator = tk.Frame(mainFrame, height=2, bg=styles.COLOR_BORDE)
        separator.pack(fill=tk.X, pady=(0, 10))
        
        tableFrame = tk.Frame(mainFrame, bg=styles.COLOR_FONDO)
        tableFrame.pack(fill=tk.BOTH, expand=True)
        
        columns = ("ID", "Nombre")
        self.tree = ttk.Treeview(tableFrame, columns=columns, show="headings", height=15)
        
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nombre", text="Nombre de la Marca")
        self.tree.column("ID", width=100, anchor="center")
        self.tree.column("Nombre", width=700, anchor="center")

        style = ttk.Style()
        style.theme_use('clam')
        
        style.configure("Treeview",
                        background=styles.COLOR_FONDO,
                        foreground=styles.COLOR_TEXTO_OSCURO,
                        fieldbackground=styles.COLOR_FONDO,
                        borderwidth=1,
                        rowheight=25)
        
        style.configure("Treeview.Heading", 
                        background=styles.COLOR_TREEVIEW_HEADING,
                        foreground=styles.COLOR_BLANCO,
                        font=(styles.FUENTE_PRINCIPAL, styles.TAMANO_NORMAL, styles.PESO_NEGRITA),
                        relief="flat",
                        padding=(5, 5))
        
        style.map('Treeview',
                  background=[('selected', styles.COLOR_TREEVIEW_SELECTION)],
                  foreground=[('selected', styles.COLOR_TEXTO_OSCURO)])
        
        self.tree.tag_configure('odd', background=styles.COLOR_TREEVIEW_ODD)
        self.tree.tag_configure('even', background=styles.COLOR_TREEVIEW_EVEN)

        scrollbar = ttk.Scrollbar(tableFrame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")
        
        tableFrame.grid_rowconfigure(0, weight=1)
        tableFrame.grid_columnconfigure(0, weight=1)
        
        bottomFrame = tk.Frame(mainFrame, bg=styles.COLOR_FONDO_OSCURO)
        bottomFrame.pack(fill=tk.X, pady=(10, 0))
        
        self.btnEliminar = tk.Button(bottomFrame, 
                                     text="Eliminar Marca Seleccionada", 
                                     font=(styles.FUENTE_PRINCIPAL, styles.TAMANO_NORMAL),
                                     bg=styles.COLOR_PELIGRO, 
                                     fg=styles.COLOR_BLANCO,
                                     width=25,
                                     state=tk.DISABLED,
                                     command=self.eliminarMarca)
        self.btnEliminar.pack(side=tk.LEFT, padx=(0, 20))
        
        btnCerrar = tk.Button(bottomFrame, 
                              text="Cerrar", 
                              font=(styles.FUENTE_PRINCIPAL, styles.TAMANO_NORMAL),
                              bg=styles.COLOR_TEXTO_MEDIO, 
                              fg=styles.COLOR_BLANCO,
                              width=15,
                              command=self.window.destroy)
        btnCerrar.pack(side=tk.RIGHT)
        
        self.tree.bind("<<TreeviewSelect>>", self.onTreeSelect)
        self.editingId = None
    
    # ===== CARGA DE DATOS =====
    def loadMarcas(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        marcas = self.db.get_all_marcas()
        
        if marcas:
            for i, marca in enumerate(marcas):
                tag_actual = 'even' if i % 2 == 0 else 'odd'
                self.tree.insert("", tk.END, 
                                values=(marca['id_marca'], marca['nombre_marca']),
                                tags=(tag_actual,))
    
    # ===== EVENTOS =====
    def onTreeSelect(self, event):
        selection = self.tree.selection()
        if selection:
            self.btnEditar.config(state=tk.NORMAL)
            self.btnEliminar.config(state=tk.NORMAL)
            
            if not self.editingId:
                item = self.tree.item(selection[0])
                self.nombreVar.set(item['values'][1])
        else:
            self.btnEditar.config(state=tk.DISABLED)
            self.btnEliminar.config(state=tk.DISABLED)
    
    # ===== OPERACIONES CRUD =====
    def agregarMarca(self):
        nombre = self.nombreVar.get().strip()
        
        if not nombre:
            messagebox.showwarning("Campo requerido", "Por favor ingrese un nombre para la marca")
            return
        
        try:
            resultado = self.db.create_marca(nombre)
            
            if resultado[0]:
                marcaId, mensaje = resultado
                messagebox.showinfo("Éxito", mensaje)
                self.nombreVar.set("")
                self.loadMarcas()
            else:
                marcaId, mensaje_error = resultado
                messagebox.showerror("Error", mensaje_error)
        except Exception as e:
            messagebox.showerror("Error", f"Error al crear marca: {e}")
    
    def editarMarca(self):
        selection = self.tree.selection()
        if not selection:
            return
        
        item = self.tree.item(selection[0])
        self.editingId = item['values'][0]
        
        self.btnAgregar.config(state=tk.DISABLED)
        self.btnEditar.config(text="Guardar", command=self.guardarEdicion)
        self.btnCancelar.config(state=tk.NORMAL)
        self.btnEliminar.config(state=tk.DISABLED)
        
        self.nombreVar.set(item['values'][1])
        self.nombreEntry.focus()
    
    def guardarEdicion(self):
        if not self.editingId:
            return
        
        nombre = self.nombreVar.get().strip()
        
        if not nombre:
            messagebox.showwarning("Campo requerido", "Por favor ingrese un nombre para la marca")
            return
        
        try:
            resultado = self.db.update_marca(self.editingId, nombre)
            
            if resultado[0]:
                success, mensaje = resultado
                messagebox.showinfo("Éxito", mensaje)
                self.cancelarEdicion()
                self.loadMarcas()
            else:
                success, mensaje_error = resultado
                messagebox.showerror("Error", mensaje_error)
        except Exception as e:
            messagebox.showerror("Error", f"Error al actualizar marca: {e}")
    
    def cancelarEdicion(self):
        self.editingId = None
        self.nombreVar.set("")
        
        self.btnAgregar.config(state=tk.NORMAL)
        self.btnEditar.config(text="Editar", command=self.editarMarca)
        self.btnCancelar.config(state=tk.DISABLED)
        self.btnEliminar.config(state=tk.NORMAL)
        
        self.tree.selection_remove(self.tree.selection())
    
    def eliminarMarca(self):
        selection = self.tree.selection()
        if not selection:
            return
        
        item = self.tree.item(selection[0])
        marcaId = item['values'][0]
        marcaNombre = item['values'][1]
        
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
import tkinter as tk
import styles

class BaseSystem:
    def __init__(self, root, return_callback, system_name):
        self.root = root
        self.return_callback = return_callback
        self.system_name = system_name
        
        # Obtener color según sistema
        self.system_color = styles.COLOR_TIENDA if system_name.upper() == "TIENDA" else styles.COLOR_RAPE
        
        # Configurar ventana
        self.root.title(f"Sistema {system_name}")
        self.root.geometry(f"{styles.ANCHO_VENTANA_SISTEMA}x{styles.ALTO_VENTANA_SISTEMA}")
        self.root.configure(bg=styles.COLOR_FONDO)
        
        # Frame principal
        self.main_frame = tk.Frame(self.root, 
                                  bg=styles.COLOR_FONDO, 
                                  padx=styles.PADDING_X, 
                                  pady=styles.PADDING_Y)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Crear componentes básicos
        self.create_header()
        self.create_menu_container()
    
    def create_header(self):
        """Crea el encabezado común"""
        header_frame = tk.Frame(self.main_frame, 
                               bg=self.system_color, 
                               height=80)
        header_frame.pack(fill=tk.X, pady=(0, styles.PADDING_Y))
        header_frame.pack_propagate(False)
        
        # Título
        title = tk.Label(header_frame, 
                        text=f"SISTEMA {self.system_name}", 
                        font=(styles.FUENTE_PRINCIPAL, styles.TAMANO_TITULO, styles.PESO_NEGRITA), 
                        bg=self.system_color, 
                        fg=styles.COLOR_BLANCO)
        title.pack(side=tk.LEFT, 
                  padx=styles.PADDING_X, 
                  pady=styles.PADDING_Y)
        
        # Botón volver
        btn_back = tk.Button(header_frame, 
                            text="Volver al Menú", 
                            font=(styles.FUENTE_PRINCIPAL, styles.TAMANO_NORMAL, styles.PESO_NEGRITA),
                            bg=styles.COLOR_BLANCO, 
                            fg=self.system_color,
                            relief=styles.BORDE_RELIEF,
                            bd=styles.BORDE_GROSOR,
                            cursor=styles.CURSOR_BOTON,
                            command=self.return_to_main)
        btn_back.pack(side=tk.RIGHT, 
                     padx=styles.PADDING_X, 
                     pady=styles.PADDING_Y)
    
    def create_menu_container(self):
        """Crea el contenedor para el menú"""
        self.menu_frame = tk.LabelFrame(self.main_frame, 
                                       text="MENU PRINCIPAL",
                                       font=(styles.FUENTE_PRINCIPAL, styles.TAMANO_ENCABEZADO, styles.PESO_NEGRITA),
                                       bg=styles.COLOR_FONDO, 
                                       fg=self.system_color,
                                       relief=tk.RAISED, 
                                       bd=styles.BORDE_GROSOR)
        self.menu_frame.pack(fill=tk.BOTH, expand=True, pady=(0, styles.PADDING_Y))
        
        # Frame interno para botones
        self.inner_frame = tk.Frame(self.menu_frame, 
                                   bg=styles.COLOR_FONDO, 
                                   padx=styles.PADDING_X, 
                                   pady=styles.PADDING_Y)
        self.inner_frame.pack(fill=tk.BOTH, expand=True)
        
        # Ahora creamos los 5 botones del menú
        self.create_menu_buttons()
    
    def create_menu_buttons(self):
        """Crea los 5 botones del menú"""
        # Botón 1: Productos/Materiales (ESPECÍFICO - se implementa en clases hijas)
        self.btn_productos = tk.Button(self.inner_frame, 
                                      text="PRODUCTOS",  # Cambiará según sistema
                                      font=(styles.FUENTE_PRINCIPAL, styles.TAMANO_NORMAL, styles.PESO_NEGRITA),
                                      bg=styles.COLOR_BOTON_1, 
                                      fg=styles.COLOR_BLANCO,
                                      width=styles.ANCHO_BOTON_MENU, 
                                      height=styles.ALTO_BOTON_MENU,
                                      relief=styles.BORDE_RELIEF, 
                                      bd=styles.BORDE_GROSOR,
                                      cursor=styles.CURSOR_BOTON)
        self.btn_productos.grid(row=0, column=0, padx=15, pady=15, sticky="nsew")
        
        # Botón 2: Marcas (COMPARTIDO)
        self.btn_marcas = tk.Button(self.inner_frame, 
                                   text="MARCAS", 
                                   font=(styles.FUENTE_PRINCIPAL, styles.TAMANO_NORMAL, styles.PESO_NEGRITA),
                                   bg=styles.COLOR_BOTON_2, 
                                   fg=styles.COLOR_BLANCO,
                                   width=styles.ANCHO_BOTON_MENU, 
                                   height=styles.ALTO_BOTON_MENU,
                                   relief=styles.BORDE_RELIEF, 
                                   bd=styles.BORDE_GROSOR,
                                   cursor=styles.CURSOR_BOTON)
        self.btn_marcas.grid(row=0, column=1, padx=15, pady=15, sticky="nsew")
        
        # Botón 3: Categorías (COMPARTIDO)
        self.btn_categorias = tk.Button(self.inner_frame, 
                                       text="CATEGORIAS", 
                                       font=(styles.FUENTE_PRINCIPAL, styles.TAMANO_NORMAL, styles.PESO_NEGRITA),
                                       bg=styles.COLOR_BOTON_3, 
                                       fg=styles.COLOR_BLANCO,
                                       width=styles.ANCHO_BOTON_MENU, 
                                       height=styles.ALTO_BOTON_MENU,
                                       relief=styles.BORDE_RELIEF, 
                                       bd=styles.BORDE_GROSOR,
                                       cursor=styles.CURSOR_BOTON)
        self.btn_categorias.grid(row=0, column=2, padx=15, pady=15, sticky="nsew")
        
        # Botón 4: Edificios (COMPARTIDO)
        self.btn_edificios = tk.Button(self.inner_frame, 
                                      text="EDIFICIOS", 
                                      font=(styles.FUENTE_PRINCIPAL, styles.TAMANO_NORMAL, styles.PESO_NEGRITA),
                                      bg=styles.COLOR_BOTON_4, 
                                      fg=styles.COLOR_BLANCO,
                                      width=styles.ANCHO_BOTON_MENU, 
                                      height=styles.ALTO_BOTON_MENU,
                                      relief=styles.BORDE_RELIEF, 
                                      bd=styles.BORDE_GROSOR,
                                      cursor=styles.CURSOR_BOTON)
        self.btn_edificios.grid(row=0, column=3, padx=15, pady=15, sticky="nsew")
        
        # Botón 5: Exportar Excel (ESPECÍFICO - se implementa en clases hijas)
        self.btn_excel = tk.Button(self.inner_frame, 
                                  text="EXPORTAR EXCEL", 
                                  font=(styles.FUENTE_PRINCIPAL, styles.TAMANO_NORMAL, styles.PESO_NEGRITA),
                                  bg=styles.COLOR_BOTON_5, 
                                  fg=styles.COLOR_BLANCO,
                                  width=styles.ANCHO_BOTON_MENU, 
                                  height=styles.ALTO_BOTON_MENU,
                                  relief=styles.BORDE_RELIEF, 
                                  bd=styles.BORDE_GROSOR,
                                  cursor=styles.CURSOR_BOTON)
        self.btn_excel.grid(row=1, column=0, padx=15, pady=15, sticky="nsew")
        
        # Configurar grid para que se expanda
        for i in range(4):
            self.inner_frame.grid_columnconfigure(i, weight=1)
        for i in range(2):
            self.inner_frame.grid_rowconfigure(i, weight=1)
        
        # Por ahora, los comandos serán placeholders
        # Luego en las clases hijas se sobreescribirán
        self.btn_marcas.config(command=self.placeholder_func)
        self.btn_categorias.config(command=self.placeholder_func)
        self.btn_edificios.config(command=self.placeholder_func)
        self.btn_productos.config(command=self.placeholder_func)
        self.btn_excel.config(command=self.placeholder_func)
    
    def placeholder_func(self):
        """Función placeholder que luego será reemplazada"""
        print(f"[{self.system_name}] Función no implementada aún")
    
    def return_to_main(self):
        """Regresa al menú principal"""
        self.main_frame.destroy()
        self.return_callback()
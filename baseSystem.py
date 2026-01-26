import tkinter as tk
from tkinter import messagebox  
import styles

class BaseSystem:
    def __init__(self, root, return_callback, system_name, db_status="Conectado", custom_header_button=None):
        self.root = root
        self.return_callback = return_callback
        self.system_name = system_name
        self.db_status = db_status
        
        # Obtener color según sistema
        self.system_color = styles.COLOR_TIENDA if system_name.upper() == "TIENDA" else styles.COLOR_RAPE
        
        # Configurar ventana con fondo MORADO OSCURO
        self.root.title(f"Sistema {system_name}")
        self.root.geometry(f"{styles.ANCHO_VENTANA_SISTEMA}x{styles.ALTO_VENTANA_SISTEMA}")
        self.root.configure(bg=styles.COLOR_FONDO_OSCURO)
        
        # Frame principal SIN PADDING y con fondo MORADO OSCURO
        self.main_frame = tk.Frame(self.root, 
                                  bg=styles.COLOR_FONDO_OSCURO,
                                  padx=0,
                                  pady=0)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Crear componentes básicos
        if custom_header_button:
            self.create_header(custom_header_button['text'], custom_header_button['command'])
        else:
            self.create_header()
        
        self.create_menu_container()
        self.create_alarm_panel()
        self.create_status_bar()
    
    def create_status_bar(self):
        """Crea barra de estado en la parte inferior"""
        status_frame = tk.Frame(self.main_frame, 
                            bg=styles.COLOR_FONDO_OSCURO,
                            height=35)
        status_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=0)
        status_frame.pack_propagate(False)
        
        # Determinar color según estado
        if "Conectado" in self.db_status:
            status_color = styles.COLOR_EXITO
            status_text = "✓ " + self.db_status
        elif "Conectando" in self.db_status:
            status_color = styles.COLOR_ADVERTENCIA
            status_text = self.db_status
        else:
            status_color = styles.COLOR_PELIGRO
            status_text = "✗ " + self.db_status
        
        # Indicador de conexión BD
        self.connection_status = tk.Label(status_frame, 
                                        text=status_text, 
                                        font=(styles.FUENTE_PRINCIPAL, styles.TAMANO_MUY_PEQUENO, styles.PESO_NORMAL),
                                        bg=styles.COLOR_FONDO_OSCURO, 
                                        fg=status_color)
        self.connection_status.pack(side=tk.LEFT, padx=(10, 0), pady=8)
        
        # Separador
        separator = tk.Frame(status_frame, 
                            bg=styles.COLOR_TEXTO_CLARO, 
                            width=1,
                            height=20)
        separator.pack(side=tk.LEFT, padx=10, pady=8)
        
        # Nombre del sistema
        system_label = tk.Label(status_frame, 
                            text=f"Sistema: {self.system_name}", 
                            font=(styles.FUENTE_PRINCIPAL, styles.TAMANO_MUY_PEQUENO, styles.PESO_NORMAL),
                            bg=styles.COLOR_FONDO_OSCURO, 
                            fg=styles.COLOR_TEXTO_CLARO)
        system_label.pack(side=tk.RIGHT, padx=(0, 10), pady=8)
    
    def create_header(self, right_button_text=None, right_button_command=None):
        """Crea el encabezado común CON BOTÓN DE EXPORTAR COMPACTO CON EMOJI MÁS GRANDE"""
        header_frame = tk.Frame(self.main_frame,
                            bg=self.system_color,
                            height=70)
        header_frame.pack(fill=tk.X, padx=10, pady=0)
        header_frame.pack_propagate(False)
        
        # TÍTULO DEL SISTEMA
        title = tk.Label(header_frame,
                        text=f"SISTEMA {self.system_name}",
                        font=(styles.FUENTE_PRINCIPAL, styles.TAMANO_TITULO, styles.PESO_NEGRITA),
                        bg=self.system_color,
                        fg=styles.COLOR_BLANCO)
        title.pack(side=tk.LEFT, padx=20, pady=15)
        
        # Botón derecho: EXPORTAR EXCEL compacto con emoji más grande
        if right_button_text:
            # Crear un Frame que actúe como botón (para poder tener diferentes fuentes)
            btn_frame = tk.Frame(header_frame,
                            bg=styles.COLOR_BLANCO,
                            relief=tk.FLAT,
                            bd=0)
            btn_frame.pack(side=tk.RIGHT, padx=20, pady=15)
            
            # Configurar cursor de mano
            btn_frame.config(cursor="hand2")
            
            # Emoji con fuente GRANDE
            emoji_label = tk.Label(btn_frame,
                                text="📥",
                                font=("Segoe UI Emoji", 18),  # Más grande
                                bg=styles.COLOR_BLANCO,
                                fg=self.system_color)
            emoji_label.pack(side=tk.LEFT, padx=(10, 5))
            
            # Texto con fuente normal
            text_label = tk.Label(btn_frame,
                                text=right_button_text,
                                font=(styles.FUENTE_PRINCIPAL, styles.TAMANO_NORMAL, styles.PESO_NEGRITA),
                                bg=styles.COLOR_BLANCO,
                                fg=self.system_color)
            text_label.pack(side=tk.LEFT, padx=(0, 10))
            
            # Hacer que todo el frame sea clickeable
            def on_click(e=None):
                right_button_command()
            
            btn_frame.bind("<Button-1>", on_click)
            emoji_label.bind("<Button-1>", on_click)
            text_label.bind("<Button-1>", on_click)
            
            # Efecto hover (cambia color al pasar el mouse)
            def on_enter(e):
                btn_frame.config(bg=styles.COLOR_FONDO_GRIS)
                emoji_label.config(bg=styles.COLOR_FONDO_GRIS)
                text_label.config(bg=styles.COLOR_FONDO_GRIS)
            
            def on_leave(e):
                btn_frame.config(bg=styles.COLOR_BLANCO)
                emoji_label.config(bg=styles.COLOR_BLANCO)
                text_label.config(bg=styles.COLOR_BLANCO)
            
            btn_frame.bind("<Enter>", on_enter)
            btn_frame.bind("<Leave>", on_leave)
            emoji_label.bind("<Enter>", on_enter)
            emoji_label.bind("<Leave>", on_leave)
            text_label.bind("<Enter>", on_enter)
            text_label.bind("<Leave>", on_leave)

    def create_menu_container(self):
        """Crea el contenedor para el menú con distribución 2x2 MEJORADA"""
        # Frame del menú con fondo BLANCO
        self.menu_frame = tk.Frame(self.main_frame, bg=styles.COLOR_FONDO)
        self.menu_frame.pack(fill=tk.BOTH, expand=True, pady=0, padx=25)
        
        # Frame interno
        self.inner_frame = tk.Frame(self.menu_frame,
                                bg=styles.COLOR_FONDO,
                                padx=25,
                                pady=20)
        self.inner_frame.pack(fill=tk.BOTH, expand=True)
        
        # TÍTULO CON BORDE INFERIOR MEJORADO
        title_container = tk.Frame(self.inner_frame, bg=styles.COLOR_FONDO)
        title_container.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 20))
        
        menu_title = tk.Label(title_container,
                             text="MENÚ PRINCIPAL",
                             font=(styles.FUENTE_PRINCIPAL, styles.TAMANO_ENCABEZADO, styles.PESO_NEGRITA),
                             bg=styles.COLOR_FONDO,
                             fg=self.system_color,
                             anchor="w")
        menu_title.pack(side=tk.TOP, fill=tk.X)
        
        # Línea decorativa doble
        line_frame = tk.Frame(title_container, bg=styles.COLOR_FONDO, height=3)
        line_frame.pack(side=tk.TOP, fill=tk.X, pady=(5, 0))
        
        # Línea principal (color del sistema)
        main_line = tk.Frame(line_frame, bg=self.system_color, height=3)
        main_line.pack(side=tk.TOP, fill=tk.X)
        
        # Línea de acento (morado)
        accent_line = tk.Frame(line_frame, bg=styles.COLOR_BOTON_1, height=3)
        accent_line.place(x=0, y=0, width=120, height=3)
        
        # Crear botones del menú
        self.create_menu_buttons()
    
    def create_menu_buttons(self):
        """Crea los botones del menú en distribución 2x2 con emojis centrados"""
        # Configurar grid para 2x2
        for i in range(2):
            self.inner_frame.grid_columnconfigure(i, weight=1)
            self.inner_frame.grid_rowconfigure(i+1, weight=1)
        
        # Determinar texto y EMOJI según sistema
        if self.system_name == "RA-PE":
            productos_text = "MATERIALES RA-PE"
            producto_emoji = "📦"  # Caja para RA-PE
        else:
            productos_text = "PRODUCTOS TIENDA"
            producto_emoji = "🛍️"  # Bolsa de compras para Tienda
        
        # FUNCIÓN PARA CREAR BOTONES CON CONTENIDO CENTRADO
        def create_button_with_large_emoji(parent, emoji, text, bg_color, command):
            """Crea un botón con emoji grande y texto normal - TODO CENTRADO"""
            # Usamos un Frame como contenedor
            btn_frame = tk.Frame(parent, bg=bg_color)
            
            # AJUSTAR TAMAÑO DE FUENTE SEGÚN EMOJI
            emoji_size = 24  # Tamaño base
            
            if emoji == "🛒":
                emoji_size = 28
            elif emoji == "🛍️":
                emoji_size = 26
            elif emoji in ["🔧", "🏢", "🏷️", "🗂️"]:
                emoji_size = 24
            
            # CONTENEDOR PRINCIPAL para centrar vertical y horizontalmente
            center_container = tk.Frame(btn_frame, bg=bg_color)
            center_container.place(relx=0.5, rely=0.5, anchor=tk.CENTER)  # ¡Centrado perfecto!
            
            # Emoji con fuente ajustada - CENTRADO
            emoji_label = tk.Label(center_container,
                                text=emoji,
                                font=("Segoe UI Emoji", emoji_size),
                                bg=bg_color,
                                fg=styles.COLOR_BLANCO)
            emoji_label.pack(pady=(0, 2))  # Solo padding abajo de 2px
            
            # Texto con fuente normal - CENTRADO
            text_label = tk.Label(center_container,
                                text=text,
                                font=(styles.FUENTE_PRINCIPAL, styles.TAMANO_NORMAL, styles.PESO_NEGRITA),
                                bg=bg_color,
                                fg=styles.COLOR_BLANCO)
            text_label.pack()  # Sin padding extra
            
            # Hacer frame clickeable
            def on_click(e=None):
                command()
            
            btn_frame.bind("<Button-1>", on_click)
            center_container.bind("<Button-1>", on_click)
            emoji_label.bind("<Button-1>", on_click)
            text_label.bind("<Button-1>", on_click)
            
            # Cambiar cursor al pasar sobre el frame
            btn_frame.bind("<Enter>", lambda e: btn_frame.config(cursor="hand2"))
            btn_frame.bind("<Leave>", lambda e: btn_frame.config(cursor=""))
            
            return btn_frame
        
        # Crear botones con contenido centrado
        btn1 = create_button_with_large_emoji(
            self.inner_frame, 
            producto_emoji, 
            productos_text,
            styles.COLOR_FONDO_OSCURO,
            self.open_productos
        )
        btn1.grid(row=1, column=0, padx=(0, 7), pady=(0, 7), sticky="nsew")
        
        btn2 = create_button_with_large_emoji(
            self.inner_frame,
            "🏢",
            "EDIFICIOS",
            self.system_color,
            self.openEdificiosWindow
        )
        btn2.grid(row=1, column=1, padx=(7, 0), pady=(0, 7), sticky="nsew")
        
        btn3 = create_button_with_large_emoji(
            self.inner_frame,
            "🏷️",
            "MARCAS",
            styles.COLOR_FONDO_OSCURO,
            self.openMarcasWindow
        )
        btn3.grid(row=2, column=0, padx=(0, 7), pady=(7, 0), sticky="nsew")
        
        btn4 = create_button_with_large_emoji(
            self.inner_frame,
            "🗂️",
            "CATEGORIAS",
            self.system_color,
            self.openCategoriasWindow
        )
        btn4.grid(row=2, column=1, padx=(7, 0), pady=(7, 0), sticky="nsew")
        
        # Configurar altura mínima
        self.inner_frame.grid_rowconfigure(1, minsize=110)
        self.inner_frame.grid_rowconfigure(2, minsize=110)


    def create_alarm_panel(self):
        """Crea panel de alarmas MEJORADO (común para ambos sistemas)"""
        # Frame para sección de alarmas
        alarm_section = tk.Frame(self.main_frame, bg=styles.COLOR_FONDO)
        alarm_section.pack(fill=tk.X, pady=(0, 0), padx=25)
        
        # TÍTULO CON BORDE MEJORADO
        title_container = tk.Frame(alarm_section, bg=styles.COLOR_FONDO)
        title_container.pack(fill=tk.X, padx=25, pady=(0, 15))
        
        alert_title_text = "ALERTAS DE MATERIALES" if self.system_name == "RA-PE" else "ALERTAS DE PRODUCTOS"
        alarm_title = tk.Label(title_container,
                              text=alert_title_text,
                              font=(styles.FUENTE_PRINCIPAL, styles.TAMANO_ENCABEZADO, styles.PESO_NEGRITA),
                              bg=styles.COLOR_FONDO,
                              fg=self.system_color,
                              anchor="w")
        alarm_title.pack(side=tk.TOP, fill=tk.X)
        
        # Línea decorativa doble
        line_frame = tk.Frame(title_container, bg=styles.COLOR_FONDO, height=3)
        line_frame.pack(side=tk.TOP, fill=tk.X, pady=(5, 0))
        
        main_line = tk.Frame(line_frame, bg=self.system_color, height=3)
        main_line.pack(side=tk.TOP, fill=tk.X)
        
        accent_line = tk.Frame(line_frame, bg=styles.COLOR_BOTON_1, height=3)
        accent_line.place(x=0, y=0, width=120, height=3)
        
        # CONTENEDOR DE ALARMAS CON FONDO
        alarm_container = tk.Frame(alarm_section,
                                  bg=styles.COLOR_ALARMA_FONDO,
                                  relief=tk.FLAT,
                                  bd=0)
        alarm_container.pack(fill=tk.X,padx=25, pady=(0, 15))
        
        # Borde lateral izquierdo (color del sistema)
        left_border = tk.Frame(alarm_container, bg=self.system_color, width=5)
        left_border.pack(side=tk.LEFT, fill=tk.Y)
        
        # Contenido interno
        inner_content = tk.Frame(alarm_container, bg=styles.COLOR_ALARMA_FONDO)
        inner_content.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Grid: Información a la izquierda, botones a la derecha
        inner_content.grid_columnconfigure(0, weight=2)
        inner_content.grid_columnconfigure(1, weight=1)
        
        # COLUMNA IZQUIERDA: Información de alarmas
        info_frame = tk.Frame(inner_content, bg=styles.COLOR_ALARMA_FONDO)
        info_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 20))
        
        # Card 1: Items agotados
        card1 = tk.Frame(info_frame, bg=styles.COLOR_ALARMA_CARD, relief=tk.FLAT)
        card1.pack(fill=tk.X, pady=(0, 12))
        
        card1_inner = tk.Frame(card1, bg=styles.COLOR_ALARMA_CARD)
        card1_inner.pack(fill=tk.X, padx=15, pady=10)
        
        # Badge circular
        self.badge_agotados = tk.Label(card1_inner,
                                      text="0",
                                      font=(styles.FUENTE_PRINCIPAL, styles.TAMANO_NORMAL, styles.PESO_NEGRITA),
                                      bg=styles.COLOR_AGOTADO,
                                      fg=styles.COLOR_BLANCO,
                                      width=3,
                                      height=1)
        self.badge_agotados.pack(side=tk.LEFT, padx=(0, 12))
        
        label_text_agotados = "Materiales agotados" if self.system_name == "RA-PE" else "Productos agotados"
        self.lbl_agotados = tk.Label(card1_inner,
                                    text=label_text_agotados,
                                    font=(styles.FUENTE_PRINCIPAL, styles.TAMANO_PEQUENO),
                                    bg=styles.COLOR_ALARMA_CARD,
                                    fg=styles.COLOR_TEXTO_OSCURO,
                                    anchor="w")
        self.lbl_agotados.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Card 2: Items a reponer
        card2 = tk.Frame(info_frame, bg=styles.COLOR_ALARMA_CARD, relief=tk.FLAT)
        card2.pack(fill=tk.X)
        
        card2_inner = tk.Frame(card2, bg=styles.COLOR_ALARMA_CARD)
        card2_inner.pack(fill=tk.X, padx=15, pady=10)
        
        self.badge_reponer = tk.Label(card2_inner,
                                     text="0",
                                     font=(styles.FUENTE_PRINCIPAL, styles.TAMANO_NORMAL, styles.PESO_NEGRITA),
                                     bg=styles.COLOR_ADVERTENCIA,
                                     fg=styles.COLOR_BLANCO,
                                     width=3,
                                     height=1)
        self.badge_reponer.pack(side=tk.LEFT, padx=(0, 12))
        
        label_text_reponer = "Materiales a reponer" if self.system_name == "RA-PE" else "Productos a reponer"
        self.lbl_reponer = tk.Label(card2_inner,
                                   text=label_text_reponer,
                                   font=(styles.FUENTE_PRINCIPAL, styles.TAMANO_PEQUENO),
                                   bg=styles.COLOR_ALARMA_CARD,
                                   fg=styles.COLOR_TEXTO_OSCURO,
                                   anchor="w")
        self.lbl_reponer.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # COLUMNA DERECHA: Botones de acción
        actions_frame = tk.Frame(inner_content, bg=styles.COLOR_ALARMA_FONDO)
        actions_frame.grid(row=0, column=1, sticky="nsew")
        
        btn_ver = tk.Button(actions_frame,
                           text="Ver alarmas",
                           font=(styles.FUENTE_PRINCIPAL, styles.TAMANO_PEQUENO, styles.PESO_NEGRITA),
                           bg=self.system_color,
                           fg=styles.COLOR_BLANCO,
                           relief=tk.FLAT,
                           bd=0,
                           cursor=styles.CURSOR_BOTON,
                           command=self.show_alarm_details,
                           activebackground=self.system_color,
                           activeforeground=styles.COLOR_BLANCO)
        btn_ver.pack(fill=tk.X, pady=(0, 10), ipady=8)
        
        btn_update = tk.Button(actions_frame,
                              text="Actualizar",
                              font=(styles.FUENTE_PRINCIPAL, styles.TAMANO_PEQUENO, styles.PESO_NEGRITA),
                              bg=styles.COLOR_BOTON_GRIS,
                              fg=styles.COLOR_BLANCO,
                              relief=tk.FLAT,
                              bd=0,
                              highlightbackground=self.system_color,  
                              highlightcolor=self.system_color,       
                              highlightthickness=1,         
                              cursor=styles.CURSOR_BOTON,
                              command=self.update_alarms,
                              activebackground=styles.COLOR_BOTON_GRIS,
                              activeforeground=styles.COLOR_BLANCO)
        btn_update.pack(fill=tk.X, ipady=8)
        
        # BOTÓN VOLVER (separado)
        # BOTÓN VOLVER MEJORADO (borde del sistema, fondo morado oscuro)
        btn_volver = tk.Button(alarm_section,
                            text="Volver al Menú",
                            font=(styles.FUENTE_PRINCIPAL, styles.TAMANO_PEQUENO, styles.PESO_NEGRITA),
                            bg=self.system_color,  
                            fg=styles.COLOR_BLANCO,         
                            relief=tk.SOLID,
                            bd=0,
                            highlightbackground=self.system_color,  
                            highlightcolor=self.system_color,       
                            highlightthickness=1,                  
                            cursor=styles.CURSOR_BOTON,
                            command=self.return_to_main,
                            activebackground=self.system_color,    
                            activeforeground=styles.COLOR_BLANCO)   
        btn_volver.pack(anchor=tk.E, padx=0, pady=(0, 0), ipadx=15, ipady=6)
    
    def update_alarms(self):
        """Actualiza las alarmas (DEBE SER SOBRESCRITO por subclases)"""
        try:
            alarmas = self.get_alarmas()
            
            if alarmas is None:
                self.badge_agotados.config(text="!")
                self.badge_reponer.config(text="!")
                return
            
            agotados = 0
            reponer = 0
            
            for a in alarmas:
                if a['estado'] == 'AGOTADO':
                    agotados += 1
                elif a['estado'] == 'A REPONER':
                    reponer += 1
            
            # Actualizar badges
            self.badge_agotados.config(text=str(agotados))
            self.badge_reponer.config(text=str(reponer))
            
            print(f"[{self.system_name}] Alarmas actualizadas: {agotados} agotados, {reponer} a reponer")
            
        except Exception as e:
            print(f"Error actualizando alarmas {self.system_name}: {e}")
            self.badge_agotados.config(text="!")
            self.badge_reponer.config(text="!")
    
    # MÉTODOS QUE DEBEN SER SOBRESCRITOS POR SUBCLASES
    def get_alarmas(self):
        """Obtiene alarmas desde la BD - DEBE SER SOBRESCRITO"""
        return None
    
    def show_alarm_details(self):
        """Muestra detalles de alarmas - DEBE SER SOBRESCRITO"""
        print(f"[{self.system_name}] show_alarm_details no implementado")
    
    def open_productos(self):
        """Abre ventana de productos - DEBE SER SOBRESCRITO"""
        print(f"[{self.system_name}] open_productos no implementado")
    
    # MÉTODOS COMUNES
    def openMarcasWindow(self):
        """Abre la ventana de gestión de marcas"""
        try:
            from ventanaMarca import VentanaMarca
            VentanaMarca(self.root, self.system_name)
        except ImportError as e:
            print(f"Error al importar ventanaMarca: {e}")
            messagebox.showerror("Error", f"No se pudo abrir gestión de marcas: {e}")
    
    def openCategoriasWindow(self):
        """Abre la ventana de gestión de categorías"""
        try:
            from ventanaCategoria import VentanaCategoria
            VentanaCategoria(self.root, self.system_name)
        except ImportError as e:
            print(f"Error al importar ventanaCategoria: {e}")
            messagebox.showerror("Error", f"No se pudo abrir gestión de categorías: {e}")
            
    def openEdificiosWindow(self):
        """Abre la ventana de gestión de edificios"""
        try:
            from ventanaEdificio import VentanaEdificio
            VentanaEdificio(self.root, self.system_name)
        except ImportError as e:
            print(f"Error al importar ventanaEdificio: {e}")
            messagebox.showerror("Error", f"No se pudo abrir gestión de edificios: {e}")

    def placeholder_func(self):
        """Función placeholder que luego será reemplazada"""
        print(f"[{self.system_name}] Función no implementada aún")
    
    def return_to_main(self):
        """Regresa al menú principal"""
        self.main_frame.destroy()
        self.return_callback()
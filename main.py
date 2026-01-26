import tkinter as tk
from tkinter import messagebox
import styles
from tiendaDef import TiendaSystem
from rapeDef import RAPESystem
from db import Database
from PIL import Image, ImageTk  # Necesitarás: pip install pillow

class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Inventario")
        
        # Verificar conexión primero
        self.db_status = self.check_database_connection()
        
        # Si no hay conexión, db_status será False y no continuamos
        if self.db_status is False:
            return
        
        # Configurar ventana principal con dimensiones del sistema
        self.root.geometry(f"{styles.ANCHO_VENTANA_SISTEMA}x{styles.ALTO_VENTANA_SISTEMA}")
        self.root.configure(bg=styles.COLOR_FONDO_OSCURO)  # Mismo fondo que sistemas internos
        
        # Centrar ventana
        self.center_window(styles.ANCHO_VENTANA_SISTEMA, styles.ALTO_VENTANA_SISTEMA)
        
        # Cargar logo
        self.logo_image = self.load_logo()
        
        # Mostrar pantalla de selección con nuevo diseño
        self.show_system_selection()
    
    def load_logo(self):
        """Carga y escala el logo institucional"""
        try:
            # Intentar cargar el logo desde la carpeta actual
            logo_path = "Sistema-de-inventarios-Guias-y-Scouts-de-Costa-Rica\EMBLEMA-HORIZONTAL-3.png"
            
            # Abrir imagen con PIL
            pil_image = Image.open(logo_path)
            
            # Escalar a tamaño apropiado para encabezado (alto máximo 60px)
            base_height = 115
            w_percent = (base_height / float(pil_image.size[1]))
            w_size = int(float(pil_image.size[0]) * float(w_percent))
            
            # Redimensionar manteniendo aspect ratio
            pil_image = pil_image.resize((w_size, base_height), Image.Resampling.LANCZOS)
            
            # Convertir a formato Tkinter
            return ImageTk.PhotoImage(pil_image)
            
        except FileNotFoundError:
            print(f"Advertencia: No se encontró el logo en {logo_path}")
            return None
        except Exception as e:
            print(f"Error cargando logo: {e}")
            return None
    
    def check_database_connection(self):
        """Verifica conexión y retorna mensaje de estado o False si hay error crítico"""
        try:
            print("Verificando conexion a la base de datos...")
            db = Database()
            success, message = db.check_connection()
            
            if success:
                print("Conexion establecida correctamente")
                return "Conectado a BD"
            else:
                # Mostrar ventana de error
                self.show_connection_error(message)
                return False
                
        except Exception as e:
            error_msg = f"Error verificando conexion: {e}"
            self.show_connection_error(error_msg)
            return False
    
    def show_connection_error(self, error_message):
        """Muestra ventana de error de conexión - MANTENIDO"""
        error_window = tk.Tk()
        error_window.title("Error de Conexion")
        error_window.geometry("500x250")
        error_window.configure(bg=styles.COLOR_FONDO)
        
        # Centrar ventana de error
        screen_width = error_window.winfo_screenwidth()
        screen_height = error_window.winfo_screenheight()
        x = (screen_width // 2) - (500 // 2)
        y = (screen_height // 2) - (250 // 2)
        error_window.geometry(f"500x250+{x}+{y}")
        
        # Contenido del mensaje de error
        tk.Label(error_window, 
                text="ERROR DE CONEXION", 
                font=(styles.FUENTE_PRINCIPAL, 16, styles.PESO_NEGRITA),
                bg=styles.COLOR_FONDO, 
                fg=styles.COLOR_PELIGRO).pack(pady=20)
        
        tk.Label(error_window, 
                text="No se pudo conectar a la base de datos", 
                font=(styles.FUENTE_PRINCIPAL, 12),
                bg=styles.COLOR_FONDO, 
                fg=styles.COLOR_TEXTO_OSCURO).pack(pady=5)
        
        # Mensaje detallado
        error_frame = tk.Frame(error_window, bg=styles.COLOR_ALARMA_FONDO, bd=1, relief=tk.SUNKEN)
        error_frame.pack(padx=30, pady=10, fill=tk.BOTH, expand=True)
        
        tk.Label(error_frame, 
                text=error_message, 
                font=(styles.FUENTE_MONO, 9),
                bg=styles.COLOR_ALARMA_FONDO, 
                fg=styles.COLOR_ALARMA_TEXTO,
                wraplength=400,
                justify=tk.LEFT).pack(padx=10, pady=10)
        
        # Botón para salir
        tk.Button(error_window, 
                 text="Salir", 
                 font=(styles.FUENTE_PRINCIPAL, 10),
                 bg=styles.COLOR_PELIGRO, 
                 fg=styles.COLOR_BLANCO,
                 command=lambda: [error_window.destroy(), self.root.quit()],
                 width=15).pack(pady=20)
        
        # Cerrar ventana principal
        self.root.withdraw()
        error_window.mainloop()
    
    def center_window(self, width, height):
        """Centra la ventana en la pantalla"""
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        
        self.root.geometry(f"{width}x{height}+{x}+{y}")
    
    def show_system_selection(self):
        """Muestra pantalla de selección de sistema con diseño moderno"""
        self.clear_window()
        
        # Frame principal con fondo MORADO OSCURO (igual que sistemas internos)
        self.main_frame = tk.Frame(self.root, 
                                  bg=styles.COLOR_FONDO_OSCURO,
                                  padx=0,
                                  pady=0)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 1. ENCABEZADO CON LOGO (NUEVO DISEÑO)
        self.create_header()
        
        # 2. CONTENIDO PRINCIPAL (contenedor blanco)
        content_frame = tk.Frame(self.main_frame, bg=styles.COLOR_FONDO)
        content_frame.pack(fill=tk.BOTH, expand=True, pady=0, padx=25)
        
        inner_content = tk.Frame(content_frame,
                               bg=styles.COLOR_FONDO,
                               padx=40,
                               pady=40)
        inner_content.pack(fill=tk.BOTH, expand=True)
        
        # 3. TÍTULO CON BORDE INFERIOR (estilo igual a sistemas internos)
        title_container = tk.Frame(inner_content, bg=styles.COLOR_FONDO)
        title_container.pack(fill=tk.X, pady=(0, 40))  # Más espacio debajo
        
        main_title = tk.Label(title_container,
                             text="SELECCIÓN DEL SISTEMA",
                             font=(styles.FUENTE_PRINCIPAL, styles.TAMANO_ENCABEZADO, styles.PESO_NEGRITA),
                             bg=styles.COLOR_FONDO,
                             fg=styles.COLOR_FONDO_OSCURO,  # Morado igual que fondo
                             anchor="w")
        main_title.pack(side=tk.TOP, fill=tk.X)
        
        # Línea decorativa doble (estilo sistemas internos)
        line_frame = tk.Frame(title_container, bg=styles.COLOR_FONDO, height=3)
        line_frame.pack(side=tk.TOP, fill=tk.X, pady=(8, 0))
        
        main_line = tk.Frame(line_frame, bg=styles.COLOR_FONDO_OSCURO, height=3)
        main_line.pack(side=tk.TOP, fill=tk.X)
        
        accent_line = tk.Frame(line_frame, bg=styles.COLOR_BOTON_1, height=3)
        accent_line.place(x=0, y=0, width=120, height=3)
        
        # 4. BOTONES DE SISTEMAS (DISEÑO ESPECIAL)
        buttons_container = tk.Frame(inner_content, bg=styles.COLOR_FONDO)
        buttons_container.pack(fill=tk.BOTH, expand=True)
        
        # Configurar grid para dos columnas
        buttons_container.grid_columnconfigure(0, weight=1)
        buttons_container.grid_columnconfigure(1, weight=1)
        buttons_container.grid_rowconfigure(0, weight=1)
        
        # BOTÓN TIENDA (diseño especial)
        tienda_frame = tk.Frame(buttons_container, 
                               bg=styles.COLOR_TIENDA,
                               relief=tk.FLAT)
        tienda_frame.grid(row=0, column=0, padx=(0, 15), sticky="nsew")
        
        tienda_content = tk.Frame(tienda_frame, bg=styles.COLOR_TIENDA)
        tienda_content.pack(fill=tk.BOTH, expand=True, padx=30, pady=40)
        
        # Icono/imagen para TIENDA (usando texto como placeholder)
        tk.Label(tienda_content,
                text="🛒",  # Puedes cambiar por un icono real si lo tienes
                font=("Arial", 48),
                bg=styles.COLOR_TIENDA,
                fg=styles.COLOR_BLANCO).pack(pady=(0, 20))
        
        tk.Label(tienda_content,
                text="SISTEMA TIENDA",
                font=(styles.FUENTE_PRINCIPAL, styles.TAMANO_ENCABEZADO, styles.PESO_NEGRITA),
                bg=styles.COLOR_TIENDA,
                fg=styles.COLOR_BLANCO).pack(pady=(0, 10))
        
        tk.Label(tienda_content,
                text="Gestión de productos\npara venta al público",
                font=(styles.FUENTE_PRINCIPAL, styles.TAMANO_PEQUENO),
                bg=styles.COLOR_TIENDA,
                fg=styles.COLOR_BLANCO,
                justify=tk.CENTER).pack(pady=(0, 25))
        
        btn_tienda = tk.Button(tienda_content,
                              text="INGRESAR",
                              font=(styles.FUENTE_PRINCIPAL, styles.TAMANO_NORMAL, styles.PESO_NEGRITA),
                              bg=styles.COLOR_BLANCO,
                              fg=styles.COLOR_TIENDA,
                              relief=tk.FLAT,
                              bd=0,
                              cursor=styles.CURSOR_BOTON,
                              command=self.open_tienda_login,
                              activebackground=styles.COLOR_BLANCO,
                              activeforeground=styles.COLOR_TIENDA,
                              padx=30,
                              pady=12)
        btn_tienda.pack()
        
        # Hacer todo el frame clickeable
        tienda_frame.bind("<Button-1>", lambda e: self.open_tienda_login())
        for widget in tienda_frame.winfo_children():
            widget.bind("<Button-1>", lambda e: self.open_tienda_login())
        
        # BOTÓN RA-PE (diseño especial)
        rape_frame = tk.Frame(buttons_container,
                             bg=styles.COLOR_RAPE,
                             relief=tk.FLAT)
        rape_frame.grid(row=0, column=1, padx=(15, 0), sticky="nsew")
        
        rape_content = tk.Frame(rape_frame, bg=styles.COLOR_RAPE)
        rape_content.pack(fill=tk.BOTH, expand=True, padx=30, pady=40)
        
        # Icono/imagen para RA-PE
        tk.Label(rape_content,
                text="🔧",  # Puedes cambiar por un icono real si lo tienes
                font=("Arial", 48),
                bg=styles.COLOR_RAPE,
                fg=styles.COLOR_BLANCO).pack(pady=(0, 20))
        
        tk.Label(rape_content,
                text="SISTEMA RA-PE",
                font=(styles.FUENTE_PRINCIPAL, styles.TAMANO_ENCABEZADO, styles.PESO_NEGRITA),
                bg=styles.COLOR_RAPE,
                fg=styles.COLOR_BLANCO).pack(pady=(0, 10))
        
        tk.Label(rape_content,
                text="Gestión de materiales\nde reparación y proyectos",
                font=(styles.FUENTE_PRINCIPAL, styles.TAMANO_PEQUENO),
                bg=styles.COLOR_RAPE,
                fg=styles.COLOR_BLANCO,
                justify=tk.CENTER).pack(pady=(0, 25))
        
        btn_rape = tk.Button(rape_content,
                            text="INGRESAR",
                            font=(styles.FUENTE_PRINCIPAL, styles.TAMANO_NORMAL, styles.PESO_NEGRITA),
                            bg=styles.COLOR_BLANCO,
                            fg=styles.COLOR_RAPE,
                            relief=tk.FLAT,
                            bd=0,
                            cursor=styles.CURSOR_BOTON,
                            command=self.open_rape_login,
                            activebackground=styles.COLOR_BLANCO,
                            activeforeground=styles.COLOR_RAPE,
                            padx=30,
                            pady=12)
        btn_rape.pack()
        
        # Hacer todo el frame clickeable
        rape_frame.bind("<Button-1>", lambda e: self.open_rape_login())
        for widget in rape_frame.winfo_children():
            widget.bind("<Button-1>", lambda e: self.open_rape_login())
        
        # 5. BOTÓN SALIR ABAJO A LA DERECHA (FUERA DE LA BARRA DE ESTADO)
        bottom_container = tk.Frame(self.main_frame, bg=styles.COLOR_FONDO_OSCURO)
        bottom_container.pack(fill=tk.X, padx=25, pady=(0, 15))
        
        btn_exit = tk.Button(bottom_container,
                            text="Salir del Sistema",
                            font=(styles.FUENTE_PRINCIPAL, styles.TAMANO_PEQUENO, styles.PESO_NEGRITA),
                            bg=styles.COLOR_PELIGRO,
                            fg=styles.COLOR_BLANCO,
                            relief=tk.FLAT,
                            bd=0,
                            cursor=styles.CURSOR_BOTON,
                            command=self.root.quit,
                            padx=25,
                            pady=10)
        btn_exit.pack(side=tk.RIGHT)
        
        # 6. BARRA DE ESTADO INFERIOR (SIMPLIFICADA)
        self.create_status_bar(self.main_frame)
    
    def create_header(self):
        """Crea encabezado con logo institucional y título del sistema"""
        header_frame = tk.Frame(self.main_frame,
                              bg=styles.COLOR_FONDO_OSCURO,
                              height=135)
        header_frame.pack(fill=tk.X, pady=0)
        header_frame.pack_propagate(False)
        
        # Contenedor para alinear logo y texto a la izquierda
        left_container = tk.Frame(header_frame, bg=styles.COLOR_FONDO_OSCURO)
        left_container.pack(side=tk.LEFT, padx=25, pady=10, fill=tk.Y)
        
        # Mostrar logo si se cargó correctamente
        if self.logo_image:
            logo_label = tk.Label(left_container,
                                 image=self.logo_image,
                                 bg=styles.COLOR_FONDO_OSCURO)
            logo_label.pack(side=tk.LEFT, padx=(0, 15))
            
            # Texto institucional (opcional - si el logo ya lo incluye, puedes omitir esto)
            # Si el logo solo tiene imágenes y no texto, puedes añadir:
            """
            tk.Label(left_container,
                    text="Guias y Scouts de Costa Rica\ninstitución benemérita",
                    font=(styles.FUENTE_PRINCIPAL, 9, styles.PESO_NORMAL),
                    bg=styles.COLOR_FONDO_OSCURO,
                    fg=styles.COLOR_BLANCO,
                    justify=tk.LEFT).pack(side=tk.LEFT)
            """
        
        else:
            # Fallback: Mostrar texto si no hay logo
            tk.Label(left_container,
                    text="Guias y Scouts de Costa Rica\ninstitución benemérita",
                    font=(styles.FUENTE_PRINCIPAL, 10, styles.PESO_NORMAL),
                    bg=styles.COLOR_FONDO_OSCURO,
                    fg=styles.COLOR_BLANCO,
                    justify=tk.LEFT).pack(side=tk.LEFT)
        
        # Título del sistema a la derecha
        title_container = tk.Frame(header_frame, bg=styles.COLOR_FONDO_OSCURO)
        title_container.pack(side=tk.RIGHT, padx=25, pady=20)
        
        system_title = tk.Label(title_container,
                               text="SISTEMA DE INVENTARIO",
                               font=(styles.FUENTE_PRINCIPAL, styles.TAMANO_TITULO, styles.PESO_NEGRITA),
                               bg=styles.COLOR_FONDO_OSCURO,
                               fg=styles.COLOR_BLANCO)
        system_title.pack()
    
    def create_status_bar(self, parent_frame):
        """Crea barra de estado simplificada"""
        status_frame = tk.Frame(parent_frame, 
                              bg=styles.COLOR_FONDO_OSCURO,
                              height=30)
        status_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=(0, 5))
        status_frame.pack_propagate(False)
        
        # Estado de conexión (solo icono y texto breve)
        if "Conectado" in self.db_status:
            status_color = styles.COLOR_EXITO
            status_text = "✓ Conectado"
        else:
            status_color = styles.COLOR_PELIGRO
            status_text = "✗ Desconectado"
        
        status_label = tk.Label(status_frame,
                               text=status_text,
                               font=(styles.FUENTE_PRINCIPAL, styles.TAMANO_MUY_PEQUENO, styles.PESO_NORMAL),
                               bg=styles.COLOR_FONDO_OSCURO,
                               fg=status_color)
        status_label.pack(side=tk.LEFT, padx=(10, 0), pady=5)
        
        # Separador
        separator = tk.Frame(status_frame,
                            bg=styles.COLOR_TEXTO_CLARO,
                            width=1,
                            height=15)
        separator.pack(side=tk.LEFT, padx=10, pady=5)
        
        # Información del sistema
        info_label = tk.Label(status_frame,
                             text="v1.0 | © 2026",
                             font=(styles.FUENTE_PRINCIPAL, styles.TAMANO_MUY_PEQUENO, styles.PESO_NORMAL),
                             bg=styles.COLOR_FONDO_OSCURO,
                             fg=styles.COLOR_TEXTO_CLARO)
        info_label.pack(side=tk.RIGHT, padx=(0, 10), pady=5)
    
    def open_tienda_login(self):
        """Muestra ventana de login para TIENDA"""
        self.show_login_window("TIENDA", self.open_tienda_system)
    
    def open_rape_login(self):
        """Muestra ventana de login para RA-PE"""
        self.show_login_window("RAPE", self.open_rape_system)
    
    def show_login_window(self, sistema, success_callback):
        """Muestra ventana emergente de login"""
        login_window = tk.Toplevel(self.root)
        login_window.title(f"Acceso Sistema {sistema}")
        login_window.geometry("400x300")
        login_window.configure(bg=styles.COLOR_FONDO)
        login_window.resizable(False, False)
        
        # Centrar ventana
        login_window.transient(self.root)
        login_window.grab_set()
        
        screen_width = login_window.winfo_screenwidth()
        screen_height = login_window.winfo_screenheight()
        x = (screen_width // 2) - (400 // 2)
        y = (screen_height // 2) - (300 // 2)
        login_window.geometry(f"400x300+{x}+{y}")
        
        # Frame principal
        main_frame = tk.Frame(login_window, bg=styles.COLOR_FONDO, padx=30, pady=30)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        color_sistema = styles.COLOR_TIENDA if sistema == "TIENDA" else styles.COLOR_RAPE
        tk.Label(main_frame,
                text=f"ACCESO SISTEMA",
                font=(styles.FUENTE_PRINCIPAL, 18, styles.PESO_NEGRITA),
                bg=styles.COLOR_FONDO,
                fg=color_sistema).pack(pady=(0, 5))
        
        tk.Label(main_frame,
                text=sistema,
                font=(styles.FUENTE_PRINCIPAL, 22, styles.PESO_NEGRITA),
                bg=styles.COLOR_FONDO,
                fg=color_sistema).pack(pady=(0, 25))
        
        # Información de usuario
        tk.Label(main_frame,
                text=f"Usuario: {sistema}",
                font=(styles.FUENTE_PRINCIPAL, 12, styles.PESO_NEGRITA),
                bg=styles.COLOR_FONDO,
                fg=styles.COLOR_TEXTO_OSCURO).pack(pady=(0, 5))
        
        tk.Label(main_frame,
                text="Ingrese la contraseña:",
                font=(styles.FUENTE_PRINCIPAL, 11),
                bg=styles.COLOR_FONDO,
                fg=styles.COLOR_TEXTO_MEDIO).pack(pady=(15, 5))
        
        # Campo de contraseña
        password_var = tk.StringVar()
        password_entry = tk.Entry(main_frame,
                                 textvariable=password_var,
                                 font=(styles.FUENTE_PRINCIPAL, 12),
                                 show="*",
                                 width=25,
                                 relief=tk.SOLID,
                                 bd=1)
        password_entry.pack(pady=5, ipady=8)
        password_entry.focus_set()
        
        # Función para verificar login
        def verify_login():
            password = password_var.get().strip()
            
            if not password:
                messagebox.showwarning("Contraseña requerida", "Por favor ingrese la contraseña")
                return
            
            try:
                db = Database()
                usuario_info = db.verify_login(sistema, password)
                
                if usuario_info:
                    print(f"Login exitoso para usuario: {sistema}")
                    login_window.destroy()
                    success_callback()
                else:
                    messagebox.showerror("Acceso denegado", "Contraseña incorrecta")
                    password_var.set("")
                    password_entry.focus_set()
                    
            except Exception as e:
                messagebox.showerror("Error", f"Error verificando credenciales: {e}")
        
        # Botón de acceso
        btn_access = tk.Button(main_frame,
                              text="Acceder",
                              font=(styles.FUENTE_PRINCIPAL, 11, styles.PESO_NEGRITA),
                              bg=color_sistema,
                              fg=styles.COLOR_BLANCO,
                              width=15,
                              relief=tk.FLAT,
                              bd=0,
                              cursor=styles.CURSOR_BOTON,
                              command=verify_login,
                              padx=20,
                              pady=10)
        btn_access.pack(pady=20)
        
        # Botón cancelar
        btn_cancel = tk.Button(main_frame,
                              text="Cancelar",
                              font=(styles.FUENTE_PRINCIPAL, 10),
                              bg=styles.COLOR_TEXTO_CLARO,
                              fg=styles.COLOR_BLANCO,
                              width=10,
                              relief=tk.FLAT,
                              bd=0,
                              cursor=styles.CURSOR_BOTON,
                              command=login_window.destroy,
                              padx=15,
                              pady=8)
        btn_cancel.pack()
        
        # Permitir Enter para enviar
        login_window.bind('<Return>', lambda e: verify_login())
        
        # Esperar a que se cierre la ventana
        self.root.wait_window(login_window)
    
    def open_tienda_system(self):
        """Abre el sistema de Tienda después de login exitoso"""
        print("Acceso concedido - Abriendo Sistema Tienda...")
        self.clear_window()
        TiendaSystem(self.root, self.show_system_selection, self.db_status)
    
    def open_rape_system(self):
        """Abre el sistema de RA-PE después de login exitoso"""
        print("Acceso concedido - Abriendo Sistema RA-PE...")
        self.clear_window()
        RAPESystem(self.root, self.show_system_selection, self.db_status)
    
    def clear_window(self):
        """Limpia todos los widgets de la ventana"""
        for widget in self.root.winfo_children():
            widget.destroy()

def main():
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
import tkinter as tk
from tkinter import messagebox
import styles
from tiendaDef import TiendaSystem
from rapeDef import RAPESystem
from db import Database

class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Inventario")
        
        # Verificar conexión primero
        self.db_status = self.check_database_connection()
        
        # Si no hay conexión, db_status será False y no continuamos
        if self.db_status is False:
            return
        
        # Configurar ventana principal
        self.root.geometry(f"{styles.ANCHO_VENTANA_PRINCIPAL}x{styles.ALTO_VENTANA_PRINCIPAL}")
        self.root.configure(bg=styles.COLOR_FONDO)
        
        # Centrar ventana
        self.center_window(styles.ANCHO_VENTANA_PRINCIPAL, styles.ALTO_VENTANA_PRINCIPAL)
        
        # Mostrar pantalla de selección
        self.show_system_selection()
    
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
        """Muestra ventana de error de conexión"""
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
        """Muestra pantalla para seleccionar sistema con barra de estado"""
        self.clear_window()
        
        # Frame principal
        main_frame = tk.Frame(self.root, 
                             bg=styles.COLOR_FONDO, 
                             padx=styles.PADDING_X, 
                             pady=styles.PADDING_Y)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título principal
        title = tk.Label(main_frame, 
                        text="SISTEMA DE INVENTARIO", 
                        font=(styles.FUENTE_PRINCIPAL, styles.TAMANO_TITULO, styles.PESO_NEGRITA), 
                        bg=styles.COLOR_FONDO, 
                        fg=styles.COLOR_TEXTO_OSCURO)
        title.pack(pady=(0, 10))
        
        # Subtítulo
        subtitle = tk.Label(main_frame, 
                           text="Gestion de Inventarios",
                           font=(styles.FUENTE_PRINCIPAL, styles.TAMANO_SUBTITULO, styles.PESO_NORMAL), 
                           bg=styles.COLOR_FONDO, 
                           fg=styles.COLOR_TEXTO_MEDIO)
        subtitle.pack(pady=(0, 30))
        
        # Separador
        separator = tk.Frame(main_frame, 
                            height=2, 
                            bg=styles.COLOR_BORDE)
        separator.pack(fill=tk.X, pady=styles.PADDING_Y)
        
        # Instrucción
        instruction = tk.Label(main_frame, 
                              text="Seleccione el sistema a gestionar:",
                              font=(styles.FUENTE_PRINCIPAL, styles.TAMANO_NORMAL, styles.PESO_NEGRITA), 
                              bg=styles.COLOR_FONDO, 
                              fg=styles.COLOR_TEXTO_OSCURO)
        instruction.pack(pady=styles.PADDING_Y)
        
        # Frame para botones de sistemas
        systems_frame = tk.Frame(main_frame, 
                                bg=styles.COLOR_FONDO)
        systems_frame.pack(pady=20)
        
        # Botón Tienda
        btn_tienda = tk.Button(systems_frame, 
                              text="SISTEMA TIENDA", 
                              font=(styles.FUENTE_PRINCIPAL, styles.TAMANO_ENCABEZADO, styles.PESO_NEGRITA),
                              bg=styles.COLOR_TIENDA, 
                              fg=styles.COLOR_BLANCO,
                              width=styles.ANCHO_BOTON_SISTEMA, 
                              height=styles.ALTO_BOTON_SISTEMA,
                              relief=styles.BORDE_RELIEF, 
                              bd=styles.BORDE_GROSOR,
                              cursor=styles.CURSOR_BOTON,
                              command=self.open_tienda_system)
        btn_tienda.grid(row=0, column=0, 
                       padx=styles.PADDING_X, pady=10, sticky="nsew")
        
        # Botón RA-PE
        btn_rape = tk.Button(systems_frame, 
                            text="SISTEMA RA-PE", 
                            font=(styles.FUENTE_PRINCIPAL, styles.TAMANO_ENCABEZADO, styles.PESO_NEGRITA),
                            bg=styles.COLOR_RAPE, 
                            fg=styles.COLOR_BLANCO,
                            width=styles.ANCHO_BOTON_SISTEMA, 
                            height=styles.ALTO_BOTON_SISTEMA,
                            relief=styles.BORDE_RELIEF, 
                            bd=styles.BORDE_GROSOR,
                            cursor=styles.CURSOR_BOTON,
                            command=self.open_rape_system)
        btn_rape.grid(row=0, column=1, 
                     padx=styles.PADDING_X, pady=10, sticky="nsew")
        
        # Separador inferior
        separator2 = tk.Frame(main_frame, 
                             height=2, 
                             bg=styles.COLOR_BORDE)
        separator2.pack(fill=tk.X, pady=20)
        
        # Frame para botón de salir
        control_frame = tk.Frame(main_frame, 
                                bg=styles.COLOR_FONDO)
        control_frame.pack()
        
        # Botón Salir
        btn_exit = tk.Button(control_frame, 
                            text="Salir", 
                            font=(styles.FUENTE_PRINCIPAL, styles.TAMANO_NORMAL, styles.PESO_NORMAL),
                            bg=styles.COLOR_PELIGRO, 
                            fg=styles.COLOR_BLANCO,
                            width=10, 
                            height=1,
                            relief=styles.BORDE_RELIEF,
                            bd=styles.BORDE_GROSOR,
                            cursor=styles.CURSOR_BOTON,
                            command=self.root.quit)
        btn_exit.pack(pady=5)
        
        # Barra de estado en menú principal también
        self.create_status_bar(main_frame)
    
    def create_status_bar(self, parent_frame):
        """Crea barra de estado en el menú principal"""
        status_frame = tk.Frame(parent_frame, 
                               bg=styles.COLOR_FONDO_OSCURO, 
                               height=25)
        status_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=(10, 0))
        status_frame.pack_propagate(False)
        
        # Estado de conexión
        status_label = tk.Label(status_frame, 
                               text="✓ " + self.db_status if self.db_status else "✗ Sin conexión",
                               font=(styles.FUENTE_PRINCIPAL, styles.TAMANO_MUY_PEQUENO, styles.PESO_NORMAL),
                               bg=styles.COLOR_FONDO_OSCURO, 
                               fg=styles.COLOR_EXITO if self.db_status else styles.COLOR_PELIGRO)
        status_label.pack(side=tk.LEFT, padx=(10, 0))
        
        # Separador
        separator = tk.Frame(status_frame, 
                            bg=styles.COLOR_TEXTO_CLARO, 
                            width=1, 
                            height=15)
        separator.pack(side=tk.LEFT, padx=10)
        
        # Versión/Info
        info_label = tk.Label(status_frame, 
                             text="Sistema de Inventario v1.0", 
                             font=(styles.FUENTE_PRINCIPAL, styles.TAMANO_MUY_PEQUENO, styles.PESO_NORMAL),
                             bg=styles.COLOR_FONDO_OSCURO, 
                             fg=styles.COLOR_TEXTO_CLARO)
        info_label.pack(side=tk.RIGHT, padx=(0, 10))
    
    def open_tienda_system(self):
        """Abre el sistema de Tienda pasando el estado de conexión"""
        print("Abriendo Sistema Tienda...")
        self.clear_window()
        TiendaSystem(self.root, self.show_system_selection, self.db_status)
    
    def open_rape_system(self):
        """Abre el sistema de RA-PE pasando el estado de conexión"""
        print("Abriendo Sistema RA-PE...")
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
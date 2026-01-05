import tkinter as tk
import styles
from tiendaDef import TiendaSystem
from rapeDef import RAPESystem

class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Inventario")
        self.root.geometry(f"{styles.ANCHO_VENTANA_PRINCIPAL}x{styles.ALTO_VENTANA_PRINCIPAL}")
        self.root.configure(bg=styles.COLOR_FONDO)
        
        # Centrar ventana
        self.center_window(styles.ANCHO_VENTANA_PRINCIPAL, styles.ALTO_VENTANA_PRINCIPAL)
        
        # Pantalla de selección de sistema
        self.show_system_selection()
    
    def center_window(self, width, height):
        """Centra la ventana en la pantalla"""
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        
        self.root.geometry(f"{width}x{height}+{x}+{y}")
    
    def show_system_selection(self):
        """Muestra pantalla para seleccionar sistema"""
        self.clear_window()
        
        # Frame principal con padding
        main_frame = tk.Frame(self.root, 
                             bg=styles.COLOR_FONDO, 
                             padx=styles.PADDING_X, 
                             pady=styles.PADDING_Y)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título principal (usando styles)
        title = tk.Label(main_frame, 
                        text="SISTEMA DE INVENTARIO", 
                        font=(styles.FUENTE_PRINCIPAL, styles.TAMANO_TITULO, styles.PESO_NEGRITA), 
                        bg=styles.COLOR_FONDO, 
                        fg=styles.COLOR_TEXTO_OSCURO)
        title.pack(pady=(0, 10))
        
        # Subtítulo (usando styles)
        subtitle = tk.Label(main_frame, 
                           text="Gestion de Inventarios",
                           font=(styles.FUENTE_PRINCIPAL, styles.TAMANO_SUBTITULO, styles.PESO_NORMAL), 
                           bg=styles.COLOR_FONDO, 
                           fg=styles.COLOR_TEXTO_MEDIO)
        subtitle.pack(pady=(0, 30))
        
        # Separador (usando styles)
        separator = tk.Frame(main_frame, 
                            height=2, 
                            bg=styles.COLOR_BORDE)
        separator.pack(fill=tk.X, pady=styles.PADDING_Y)
        
        # Instrucción (usando styles)
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
        
        # Botón Tienda (usando styles)
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
        
        # Botón RA-PE (usando styles)
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
        
        # Solo botón Salir (usando styles)
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
        
        # Footer simplificado
        footer = tk.Label(main_frame, 
                         text="Sistema de Inventario", 
                         font=(styles.FUENTE_PRINCIPAL, styles.TAMANO_MUY_PEQUENO, styles.PESO_NORMAL), 
                         bg=styles.COLOR_FONDO, 
                         fg=styles.COLOR_TEXTO_CLARO)
        footer.pack(side=tk.BOTTOM, pady=10)
    
    def open_tienda_system(self):
        """Abre el sistema de Tienda"""
        print("Abriendo Sistema Tienda...")
        # Limpia la ventana actual y carga TiendaSystem
        self.clear_window()
        TiendaSystem(self.root, self.show_system_selection)
    
    def open_rape_system(self):
        """Abre el sistema de RA-PE"""
        print("Abriendo Sistema RA-PE...")
        # Limpia la ventana actual y carga RAPESystem
        self.clear_window()
        RAPESystem(self.root, self.show_system_selection)
    
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
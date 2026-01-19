"""
Archivo de estilos - SOLO variables
Centraliza colores, fuentes y tamaños
"""

# ============================================
# PALETA DE COLORES
# ============================================

# Colores principales por sistema (Actualizados según paleta Scouts)
COLOR_TIENDA = "#021DA3"      # Azul (HEX: 021DA3) - Color distintivo
COLOR_RAPE = "#04bc99"        # Verde turquesa (HEX: 04bc99) - Color distintivo

# Colores de estado
COLOR_PELIGRO = "#e74c3c"     # Rojo (mantenido)
COLOR_ADVERTENCIA = "#f39c12" # Naranja (mantenido)
COLOR_EXITO = "#2ecc71"       # Verde éxito (mantenido)
COLOR_INFO = "#3498db"        # Azul info (mantenido)

# Colores neutrales
COLOR_FONDO = "#ffffff"       # Blanco (como solicitado)
COLOR_FONDO_OSCURO = "#2c1261" # Morado primario (HEX: 2c1261)
COLOR_TEXTO_OSCURO = "#2c3e50"
COLOR_TEXTO_MEDIO = "#7f8c8d"
COLOR_TEXTO_CLARO = "#95a5a6"
COLOR_BORDE = "#bdc3c7"
COLOR_BLANCO = "#ffffff"

# Colores para alarmas
COLOR_ALARMA_FONDO = "#f8d7da"
COLOR_ALARMA_TEXTO = "#721c24"
COLOR_AGOTADO = "#dc3545"
COLOR_REPONER = "#fd7e14"

# Colores para botones del menú (8 colores diferentes)
# Actualizados con colores de la paleta Scouts
COLOR_BOTON_1 = "#2c1261"      # Morado primario
COLOR_BOTON_2 = "#ed1a39"      # Rojo primario
COLOR_BOTON_3 = "#021DA3"      # Azul (TIENDA)
COLOR_BOTON_4 = "#04bc99"      # Verde turquesa (RAPE)
COLOR_BOTON_5 = "#ffa400"      # Naranja (secundario)
COLOR_BOTON_6 = "#e8197b"      # Rosa (secundario)
COLOR_BOTON_7 = "#00365f"      # Azul noche (secundario)
COLOR_BOTON_8 = "#633510"      # Marrón (secundario)

# ============================================
# FUENTES (Actualizadas según guía Scouts)
# ============================================

# Según PDF: Para títulos -> Arial Bold, Avenir Black/Heavy
FUENTE_PRINCIPAL = "Arial"      # Para títulos (equivalente Avenir Black/Heavy)

# Según PDF: Para subtítulos -> Arial Bold Italic, Avenir Medium
FUENTE_SECUNDARIA = "Arial"     # Para subtítulos (equivalente Avenir Medium)

# Según PDF: Para cuerpo -> Arial Regular, Avenir Book/Light
FUENTE_MONO = "Consolas"        # Mantenido para código/monospace

# ============================================
# TAMAÑOS DE FUENTE
# ============================================

TAMANO_TITULO = 20
TAMANO_SUBTITULO = 16
TAMANO_ENCABEZADO = 14
TAMANO_NORMAL = 11
TAMANO_PEQUENO = 9
TAMANO_MUY_PEQUENO = 8

# ============================================
# PESOS DE FUENTE (Actualizados según guía)
# ============================================

PESO_NORMAL = "normal"
PESO_NEGRITA = "bold"

# ============================================
# OTROS ESTILOS
# ============================================

# Bordes
BORDE_GROSOR = 2
BORDE_RELIEF = "raised"

# Cursor
CURSOR_NORMAL = "arrow"
CURSOR_BOTON = "hand2"

# Padding estándar
PADDING_X = 20
PADDING_Y = 10

# Tamaños de ventana
ANCHO_VENTANA_PRINCIPAL = 600
ALTO_VENTANA_PRINCIPAL = 500
ANCHO_VENTANA_SISTEMA = 900
ALTO_VENTANA_SISTEMA = 650

# Tamaños de botones
ANCHO_BOTON_SISTEMA = 15
ALTO_BOTON_SISTEMA = 3
ANCHO_BOTON_MENU = 15
ALTO_BOTON_MENU = 4

# ============================================
# ESTILOS PARA TREEVIEW
# ============================================

# Colores para Treeview
COLOR_TREEVIEW_HEADING = "#2c1261"  # Morado primario para encabezados
COLOR_TREEVIEW_ODD = "#f9f9f9"      # Fondo filas impares  
COLOR_TREEVIEW_EVEN = "#A7A4A4"     # Fondo filas pares
COLOR_TREEVIEW_SELECTION = "#d4e6f1"  # Color al seleccionar fila
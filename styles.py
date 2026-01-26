"""
Archivo de estilos - SOLO variables
Centraliza colores, fuentes y tamaños
"""

# ============================================
# PALETA DE COLORES
# ============================================

# Colores principales por sistema (Actualizados según paleta Scouts)
COLOR_TIENDA = "#00365f"      # Azul (HEX: 021DA3) - Color distintivo
COLOR_RAPE = "#04bc99"        # Verde turquesa (HEX: 04bc99) - Color distintivo

# Colores de estado
COLOR_PELIGRO = "#ed1a39"     # Rojo (mantenido)
COLOR_ADVERTENCIA = "#ffa400" # Naranja (mantenido)
COLOR_EXITO = "#2ecc71"       # Verde éxito (mantenido)
COLOR_INFO = "#3498db"        # Azul info (mantenido)

# Colores neutrales
COLOR_FONDO = "#ffffff"       # Blanco puro
COLOR_FONDO_OSCURO = "#2c1261" # Morado primario (HEX: 2c1261)
COLOR_FONDO_GRIS = "#f8f9fa"  # Gris muy claro para contenedores
COLOR_TEXTO_OSCURO = "#2c3e50"
COLOR_TEXTO_MEDIO = "#7f8c8d"
COLOR_TEXTO_CLARO = "#95a5a6"
COLOR_BORDE = "#bdc3c7"
COLOR_BLANCO = "#ffffff"

# Colores para alarmas
COLOR_ALARMA_FONDO = "#f8f9fa"  # Fondo gris claro
COLOR_ALARMA_CARD = "#ffffff"   # Cards blancas
COLOR_AGOTADO = "#ed1a39"
COLOR_REPONER = "#ffa400"

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
COLOR_BOTON_GRIS = "#6c757d"   # Gris para botones secundarios

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

TAMANO_TITULO = 24
TAMANO_SUBTITULO = 16
TAMANO_ENCABEZADO = 16
TAMANO_NORMAL = 14
TAMANO_PEQUENO = 12
TAMANO_MUY_PEQUENO = 11

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
BORDE_GROSOR_GRUESO = 3
BORDE_GROSOR_FINO = 1
BORDE_RELIEF = "flat"  # Cambiado de "raised" a "flat" para diseño más moderno
BORDE_RADIUS = 6  # Para esquinas redondeadas (simulado con relief)

# Cursor
CURSOR_NORMAL = "arrow"
CURSOR_BOTON = "hand2"

# Padding estándar
PADDING_X = 20
PADDING_Y = 10
PADDING_HEADER = 10
PADDING_MENU = 25
PADDING_INTERNO = 25
PADDING_STATUS = 10

# Tamaños de ventana
ANCHO_VENTANA_PRINCIPAL = 600
ALTO_VENTANA_PRINCIPAL = 500
ANCHO_VENTANA_SISTEMA = 900
ALTO_VENTANA_SISTEMA = 750

# Tamaños de botones del menú principal (ACTUALIZADOS)
ANCHO_BOTON_MENU = 25  # Más ancho
ALTO_BOTON_MENU = 3    # Más alto
PADDING_BOTON_Y = 20   # Padding vertical interno
ANCHO_BOTON_SISTEMA = 15
ALTO_BOTON_SISTEMA = 3


# Gap entre elementos
GAP_MENU = 15          # Gap entre botones del menú
GAP_SECCIONES = 30     # Gap entre secciones principales

# ============================================
# ESTILOS PARA TREEVIEW
# ============================================

# Colores para Treeview
COLOR_TREEVIEW_HEADING = "#2c1261"  # Morado primario para encabezados
COLOR_TREEVIEW_ODD = "#f9f9f9"      # Fondo filas impares  
COLOR_TREEVIEW_EVEN = "#A7A4A4"     # Fondo filas pares
COLOR_TREEVIEW_SELECTION = "#d4e6f1"  # Color al seleccionar fila
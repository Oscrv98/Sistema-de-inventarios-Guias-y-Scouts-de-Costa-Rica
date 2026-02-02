@echo off
REM ====================================================================
REM Script de Construcción del Ejecutable - USA python -m pyinstaller
REM ====================================================================
echo.
echo ====================================================================
echo   CONSTRUCCION DEL EJECUTABLE - SISTEMA DE INVENTARIO
echo ====================================================================
echo.

REM Verificar que Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python no está instalado o no está en el PATH
    pause
    exit /b 1
)

echo [1/2] Python encontrado correctamente
echo.

REM Limpiar compilaciones anteriores
echo [2/2] Limpiando archivos antiguos...
if exist "dist" rmdir /s /q dist
if exist "build" rmdir /s /q build
if exist "__pycache__" rmdir /s /q __pycache__
echo.

REM Ejecutar PyInstaller usando python -m
echo ====================================================================
echo   EJECUTANDO PYINSTALLER...
echo ====================================================================
echo.

python -m PyInstaller --name="SistemaInventario" --onefile --windowed --add-data ".env;." --add-data "EMBLEMA-HORIZONTAL-3.png;." --hidden-import=psycopg2 --hidden-import=psycopg2.extras --hidden-import=psycopg2.pool --hidden-import=PIL --hidden-import=PIL.Image --hidden-import=PIL.ImageTk --hidden-import=PIL.ImageDraw --hidden-import=PIL.ImageFont --hidden-import=dotenv main.py

if errorlevel 1 (
    echo.
    echo ====================================================================
    echo   ERROR: Fallo al crear el ejecutable
    echo ====================================================================
    echo.
    echo Posibles soluciones:
    echo 1. Verifica que main.py exista en esta carpeta
    echo 2. Verifica que .env exista en esta carpeta
    echo 3. Si no tienes el logo, quita esa linea del comando
    echo.
    pause
    exit /b 1
)

echo.
echo ====================================================================
echo   EXITO: Ejecutable creado correctamente
echo ====================================================================
echo.
echo El archivo ejecutable se encuentra en: dist\SistemaInventario.exe
echo.
echo IMPORTANTE: Para distribuir el programa, copia:
echo   1. dist\SistemaInventario.exe
echo   2. .env (con credenciales de BD)
echo   3. EMBLEMA-HORIZONTAL-3.png (logo)
echo.
echo Los 3 archivos deben estar en la MISMA CARPETA.
echo.
pause

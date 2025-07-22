# 📄 Procesador de PDF - Extractor de Tablas

Una aplicación web robusta para extraer y visualizar tablas de archivos PDF con soporte completo para UTF-8 y exportación a Excel/CSV.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0.0-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 📋 Tabla de Contenidos

- [Características](#-características)
- [Requisitos Previos](#-requisitos-previos)
- [Instalación](#-instalación)
- [Uso](#-uso)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [API Endpoints](#-api-endpoints)
- [Solución de Problemas](#-solución-de-problemas)
- [Configuración Avanzada](#-configuración-avanzada)
- [Contribuir](#-contribuir)

## ✨ Características

### Principales
- **Extracción inteligente de tablas** desde archivos PDF
- **Soporte completo UTF-8** para caracteres especiales
- **Interfaz drag & drop** para subir archivos
- **Visualización interactiva** con DataTables
- **Exportación** a Excel (múltiples hojas) y CSV
- **Procesamiento robusto** de PDFs complejos o mal formateados

### Técnicas
- Detección automática de estructuras tabulares
- Limpieza y normalización de datos
- Manejo de PDFs de hasta 16MB
- Eliminación automática de archivos temporales
- Mensajes de error descriptivos

## 🔧 Requisitos Previos

### Software necesario
- Python 3.8 o superior
- pip (gestor de paquetes de Python)
- Navegador web moderno (Chrome, Firefox, Safari, Edge)

### Verificar instalación de Python
```bash
python --version
# o
python3 --version
```

## 📦 Instalación

### 1. Clonar o descargar el proyecto

```bash
# Opción 1: Crear carpeta y archivos manualmente
mkdir procesador-pdf
cd procesador-pdf

# Crear la estructura de carpetas
mkdir templates static
```

### 2. Crear los archivos del proyecto

Copia cada uno de los siguientes archivos en su ubicación correspondiente:
- `app.py` (raíz del proyecto)
- `requirements.txt` (raíz del proyecto)
- `templates/index.html`
- `static/style.css`
- `static/script.js`

### 3. Crear entorno virtual

#### Windows
```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
venv\Scripts\activate
```

#### macOS/Linux
```bash
# Crear entorno virtual
python3 -m venv venv

# Activar entorno virtual
source venv/bin/activate
```

### 4. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 5. Verificar instalación

```bash
pip list
```

Deberías ver las siguientes librerías instaladas:
- Flask
- flask-cors
- pdfplumber
- pandas
- openpyxl
- Werkzeug

## 🚀 Uso

### Iniciar la aplicación

```bash
python app.py
```

Verás un mensaje similar a:
```
 * Running on http://127.0.0.1:5000
 * Debug mode: on
```

### Acceder a la aplicación

1. Abre tu navegador web
2. Ve a: `http://localhost:5000`

### Cómo usar la aplicación

#### 1. Subir un PDF
- **Opción A**: Arrastra y suelta un archivo PDF en la zona designada
- **Opción B**: Haz clic en "Seleccionar archivo" y elige un PDF

#### 2. Procesamiento automático
- La aplicación extraerá automáticamente todas las tablas encontradas
- Verás la información del documento (páginas, tablas extraídas, fecha)

#### 3. Visualizar resultados
- Cada tabla se muestra de forma interactiva
- Puedes:
  - Buscar dentro de cada tabla
  - Ordenar por columnas
  - Paginar resultados
  - Ver información de página y posición

#### 4. Exportar datos
- **Excel**: Crea un archivo con cada tabla en una hoja separada
- **CSV**: Combina todas las tablas en un único archivo

### Formatos de PDF soportados

✅ **Funciona bien con:**
- PDFs con tablas bien definidas
- Documentos con bordes de tabla
- PDFs generados digitalmente
- Archivos con múltiples tablas

⚠️ **Limitaciones:**
- PDFs escaneados (requieren OCR)
- Tablas sin bordes claros
- Formatos muy complejos o irregulares

## 📁 Estructura del Proyecto

```
procesador-pdf/
│
├── app.py                 # Aplicación principal Flask
├── requirements.txt       # Dependencias Python
├── README.md             # Este archivo
│
├── templates/
│   └── index.html        # Interfaz de usuario
│
├── static/
│   ├── style.css         # Estilos CSS
│   └── script.js         # Lógica JavaScript
│
└── uploads/              # Carpeta temporal (se crea automáticamente)
```

## 🔌 API Endpoints

### POST `/upload`
Sube y procesa un archivo PDF.

**Request:**
- Method: `POST`
- Content-Type: `multipart/form-data`
- Body: `file` (archivo PDF)

**Response:**
```json
{
    "success": true,
    "metadata": {
        "total_pages": 10,
        "extracted_tables": 3,
        "extraction_date": "2024-01-15 10:30:45"
    },
    "tables": [
        {
            "page": 1,
            "table_index": 0,
            "headers": ["Columna1", "Columna2"],
            "data": [["dato1", "dato2"]],
            "rows": 5,
            "columns": 2
        }
    ]
}
```

### POST `/export/<format>`
Exporta los datos extraídos.

**Parámetros:**
- `format`: "excel" o "csv"

**Request Body:**
```json
{
    "tables": [/* array de tablas */]
}
```

## 🔍 Solución de Problemas

### Error: "No module named 'pdfplumber'"
```bash
# Asegúrate de que el entorno virtual está activado
# Windows: venv\Scripts\activate
# macOS/Linux: source venv/bin/activate

# Reinstalar dependencias
pip install -r requirements.txt
```

### Error: "El archivo es demasiado grande"
- El límite es 16MB por defecto
- Para cambiarlo, edita `app.py`:
```python
app.config['MAX_CONTENT_LENGTH'] = 32 * 1024 * 1024  # 32MB
```

### No se extraen tablas de mi PDF
Posibles causas:
1. El PDF está escaneado (imagen, no texto)
2. Las tablas no tienen bordes definidos
3. Formato de tabla muy irregular

Soluciones:
- Asegúrate de que el PDF contiene texto seleccionable
- Prueba con PDFs que tengan tablas con bordes claros

### Error de codificación UTF-8
La aplicación maneja automáticamente problemas de codificación, pero si encuentras problemas:
1. Verifica que tu sistema operativo esté configurado para UTF-8
2. Asegúrate de que el PDF no esté corrupto

## ⚙️ Configuración Avanzada

### Cambiar puerto
```python
# En app.py, última línea:
app.run(debug=True, port=8080)  # Cambia a puerto 8080
```

### Modo producción
```python
# En app.py:
app.run(debug=False, host='0.0.0.0', port=5000)
```

### Configurar CORS
```python
# En app.py, después de crear la app:
CORS(app, origins=['http://tudominio.com'])
```

### Agregar autenticación básica
```python
from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(username, password):
    return username == "admin" and password == "secreto"

@app.route('/upload', methods=['POST'])
@auth.login_required
def upload_file():
    # ... resto del código
```

## 🐛 Debug

### Activar logs detallados
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Ver estructura de PDF problemático
```python
# Agregar en extract_tables_from_pdf():
print(f"Procesando página {page_num}")
print(f"Tablas encontradas: {len(tables)}")
```

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📝 Licencia

Este proyecto está bajo la Licencia MIT. Puedes usarlo libremente en tus proyectos personales o comerciales.

## 🆘 Soporte

Si encuentras algún problema o tienes preguntas:
1. Revisa la sección de [Solución de Problemas](#-solución-de-problemas)
2. Abre un issue en el repositorio
3. Contacta al desarrollador

---

**Desarrollado con ❤️ usando Python y Flask**
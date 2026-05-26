# Numerika Métodos

## Descripción

**Numerika Métodos** es una aplicación web académica de Métodos Numéricos.
Permite calcular aproximaciones de raíces e interpolaciones desde una
interfaz sencilla en el navegador.

El proyecto está desarrollado con **Python y Flask** para el backend, y con
**HTML, CSS y JavaScript** para la interfaz. El usuario selecciona un método,
ingresa los datos solicitados y consulta el resultado junto con su tabla,
procedimiento o gráfica, según el cálculo realizado.

## Tecnologías utilizadas

- Python
- Flask
- SymPy
- HTML
- CSS
- JavaScript
- Chart.js, para la gráfica de Raíces Múltiples
- `unittest`, para pruebas automatizadas

## Métodos incluidos

### Métodos cerrados

- Bisección
- Regla Falsa

### Métodos abiertos

- Newton
- Secante
- Raíces Múltiples
- Müller

### Interpolación

- Interpolación Lineal
- Interpolación de Lagrange

## Requisitos previos

Para ejecutar la aplicación se necesita:

- **Python 3** instalado.
- **pip**, el instalador de paquetes de Python.
- **Git**, si se desea clonar el proyecto directamente desde GitHub.
- Un navegador web, como Chrome, Edge, Firefox o Safari.

**Python es obligatorio** para iniciar la aplicación. **Git es necesario
únicamente si se desea clonar el repositorio**; también es posible descargar
el proyecto como archivo ZIP.

**Node.js es opcional.** Solo se necesita si se desea ejecutar la validación
del archivo JavaScript con el comando `node --check`. No es obligatorio para
iniciar ni utilizar la aplicación.

Enlaces oficiales de descarga:

- Python: <https://www.python.org/downloads/>
- Git: <https://git-scm.com/downloads>
- Node.js: <https://nodejs.org/en/download>

## Verificar instalaciones

Antes de comenzar, abrir una terminal y verificar Python y pip:

```bash
python --version
pip --version
```

En algunos sistemas, especialmente macOS o Linux, los comandos pueden ser:

```bash
python3 --version
pip3 --version
```

Si se desea validar JavaScript con Node.js, verificar su instalación con:

```bash
node --version
```

Si se descargará el proyecto mediante Git, verificarlo con:

```bash
git --version
```

Si alguno de estos comandos no funciona, instalar la herramienta necesaria
desde los enlaces oficiales indicados en la sección anterior.

## Descargar o clonar el proyecto

### Opción A: Clonar con Git

Abrir una terminal y ejecutar:

```bash
git clone https://github.com/Bry4n07/metnum-python.git
cd metnum-python
```

### Opción B: Descargar ZIP desde GitHub

1. Abrir el repositorio: <https://github.com/Bry4n07/metnum-python>.
2. Presionar el botón **Code**.
3. Seleccionar **Download ZIP**.
4. Descomprimir el archivo descargado.
5. Abrir una terminal y entrar a la carpeta `metnum-python`.

## Instalación del proyecto

Una vez dentro de la carpeta `metnum-python`, crear un entorno virtual:

```bash
python -m venv .venv
```

Si en macOS o Linux el comando `python` no funciona, probar:

```bash
python3 -m venv .venv
```

Activar el entorno virtual en macOS o Linux:

```bash
source .venv/bin/activate
```

Activar el entorno virtual en Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Activar el entorno virtual en Windows CMD:

```cmd
.venv\Scripts\activate.bat
```

Instalar las dependencias del proyecto:

```bash
python -m pip install -r requirements.txt
```

Es preferible usar `python -m pip install` en lugar de solamente
`pip install`, porque así se asegura que se utilice el instalador del entorno
virtual activo.

El archivo `requirements.txt` instala las librerías necesarias del proyecto:

- Flask
- SymPy

Si se está usando `python3` en macOS o Linux, se puede ejecutar:

```bash
python3 -m pip install -r requirements.txt
```

## Si pip o venv no funcionan

El entorno virtual se crea con el módulo `venv` incluido en Python. No es una
dependencia del proyecto y no se instala con `pip`.

Si `pip` no aparece o no está disponible, probar:

```bash
python -m ensurepip --upgrade
```

Si el sistema utiliza `python3`, probar:

```bash
python3 -m ensurepip --upgrade
```

Si el entorno virtual no se crea:

- Verificar que Python esté instalado correctamente.
- Cerrar y volver a abrir la terminal después de instalar Python.
- En algunos sistemas Linux o Ubuntu puede ser necesario instalar el paquete
  de entornos virtuales:

```bash
sudo apt install python3-venv
```

Este último comando aplica solamente a algunos sistemas Linux o Ubuntu; no
es un paso obligatorio para todos los usuarios.

## Ejecutar el proyecto

Con el entorno virtual activo, ejecutar:

```bash
python app.py
```

También puede ejecutarse directamente con el intérprete del entorno virtual,
sin activarlo manualmente.

En macOS o Linux:

```bash
.venv/bin/python app.py
```

En Windows:

```cmd
.venv\Scripts\python app.py
```

Como alternativa secundaria, si el sistema utiliza `python3` y las
dependencias fueron instaladas correctamente en ese entorno, también puede
funcionar `python3 app.py`.

Después, abrir en el navegador una de estas direcciones:

- <http://127.0.0.1:5000>
- <http://localhost:5000>

La terminal debe permanecer abierta mientras se utiliza la aplicación,
porque allí se mantiene ejecutándose el servidor local.

Para detener el servidor, volver a la terminal y presionar:

```text
Ctrl + C
```

## Comandos rápidos

### macOS o Linux

```bash
git clone https://github.com/Bry4n07/metnum-python.git
cd metnum-python
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python app.py
```

### Windows PowerShell

```powershell
git clone https://github.com/Bry4n07/metnum-python.git
cd metnum-python
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python app.py
```

## Ejecutar pruebas

Con el entorno virtual activo, ejecutar las pruebas automatizadas con:

```bash
python -m unittest discover -s tests -q
```

Si el sistema utiliza `python3`, también puede ejecutarse:

```bash
python3 -m unittest discover -s tests -q
```

Para validar la sintaxis del archivo JavaScript principal, únicamente si
Node.js está instalado:

```bash
node --check static/js/app.js
```

## Estructura del proyecto

```text
metnum-python/
├── app.py
├── methods/
├── services/
├── templates/
├── static/
├── tests/
├── requirements.txt
└── README.md
```

- `app.py`: inicia el servidor Flask y conecta la interfaz con los cálculos.
- `methods/`: contiene la implementación de los métodos numéricos.
- `services/`: contiene herramientas de apoyo, como la evaluación segura de funciones matemáticas.
- `templates/`: contiene las páginas HTML que se muestran en el navegador.
- `static/`: contiene estilos CSS y la interacción JavaScript de la aplicación.
- `tests/`: contiene las pruebas automatizadas del proyecto.
- `requirements.txt`: contiene las dependencias de Python que deben instalarse.
- `README.md`: contiene esta guía de instalación y uso.

## Uso básico

1. Abrir la aplicación en el navegador.
2. Entrar a la calculadora.
3. Seleccionar el método que se desea utilizar.
4. Ingresar los datos solicitados por el formulario.
5. Presionar `Calcular raíz` o `Interpolar`, según corresponda.
6. Revisar el resultado y la información disponible:
   tabla de iteraciones, procedimiento matemático o gráfica.

## Notas importantes

- Los resultados se muestran con un máximo de **4 decimales** en pantalla.
- Los cálculos internos conservan mayor precisión.
- La gráfica aparece únicamente en **Raíces Múltiples**.
- Las interpolaciones muestran un procedimiento matemático, no una tabla de iteraciones.
- Raíces Múltiples detecta automáticamente valores `xi` sugeridos en el rango de `-9` a `9`.
- La tolerancia por defecto es `0.001`.
- El máximo de iteraciones por defecto es `100`.

## Problemas comunes

### El comando `python` no funciona

Probar con:

```bash
python3 --version
```

Si tampoco funciona, instalar o reinstalar Python desde el sitio oficial. En
Windows, durante la instalación es recomendable marcar la opción
**Add Python to PATH**.

### El comando `pip` no funciona

Usar pip a través de Python:

```bash
python -m pip --version
```

Si todavía no está disponible, ejecutar:

```bash
python -m ensurepip --upgrade
```

### El comando `git` no funciona

Instalar Git desde su sitio oficial:

<https://git-scm.com/downloads>

### El entorno virtual no se crea en Ubuntu o Linux

En algunos sistemas puede ser necesario instalar el paquete para entornos
virtuales:

```bash
sudo apt install python3-venv
```

### La página no abre en el navegador

Confirmar que el servidor esté ejecutándose en la terminal con
`python app.py`, y abrir:

<http://127.0.0.1:5000>

### El puerto 5000 está ocupado

Puede existir otro servidor ejecutándose. Cerrarlo con `Ctrl + C` en la
terminal correspondiente. Si fuera necesario utilizar otro puerto, este se
puede configurar en `app.py`.

## Autor o entrega

Desarrollado como proyecto académico de Métodos Numéricos.

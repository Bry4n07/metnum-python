# MetNum Python

Nueva base del proyecto de Métodos Numéricos con Flask, HTML, CSS, JavaScript
y SymPy. Actualmente implementa:

- Bisección.
- Regla Falsa.
- Newton.
- Secante.
- Müller.
- Raíces Múltiples.
- Interpolación Lineal.
- Interpolación de Lagrange.

Los dos métodos fueron portados desde:

- `app/Services/MetNum/Methods/BisectionMethod.php`
- `app/Services/MetNum/Methods/FalsePositionMethod.php`

del proyecto Laravel anterior. Se conservaron el criterio
`T = |xr_actual - xr_anterior|`, el orden de actualización del intervalo, las
columnas de `steps` y los mensajes del resultado para facilitar comparaciones.

## Ejecutar

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python app.py
```

Abrir `http://127.0.0.1:5000/` o `http://127.0.0.1:5000/calculadora`.

## API

`POST /api/calculate`

```json
{
  "method": "bisection",
  "function": "x^3 - x - 2",
  "a": 0,
  "b": 2,
  "tolerance": 0.001,
  "max_iterations": 100
}
```

Los métodos de una sola aproximación responden con `success`, `method`,
`root`, `tolerance`, `iterations`, `message` y `steps`. Raíces Múltiples
responde con `function`, `derivative`, `second_derivative`, `search_table`,
`suggested_roots`, `tables`, `final_roots` y `chart_points`, además de su
estado, tolerancia y mensaje. Cada tabla contiene su `initial_xi`, `final_xr`
y filas de iteración.

Newton calcula su derivada simbólicamente con SymPy a partir de la función
ingresada. Secante recibe dos valores iniciales, `x0` y `x1`. Müller recibe
`x0`, `x1` y `x2`, y obtiene únicamente raíces reales con su aproximación
cuadrática. Raíces Múltiples no solicita valores iniciales: recorre `[-9, 9]` con paso `1`,
detecta hasta cuatro valores sugeridos y usa `f'(x)` y `f''(x)` simbólicas
en una tabla por candidato. Su gráfica XY muestra la línea `f(x)` y puntos
en los resultados finales `(xr, f(xr))`. Cuando se detecta un intervalo con
cambio de signo, sus dos extremos se usan como `xi` independientes; no se
calcula un punto medio.

Interpolación Lineal y Lagrange reciben directamente los valores de dos
puntos y el `x` a evaluar; no solicitan una función, tolerancia ni máximo de
iteraciones. Ambas responden con `success`, `method`, `x`, `result`, `message`
y `procedure` para presentar fórmula, sustitución, desarrollo y resultado.
Se conserva una fila de `steps` como dato de compatibilidad de la API, pero
la interfaz presenta el procedimiento en bloques matemáticos, no en tabla.

## Probar

```bash
python -m unittest discover -s tests -v
```

Las pruebas de paridad fijan como referencia, para `x^3 - x - 2` en
`[0, 2]` con tolerancia `0.001`, los resultados producidos por Laravel:

| Método | Raíz | Iteraciones |
| --- | ---: | ---: |
| Bisección | `1.5205078125` | `11` |
| Regla Falsa | `1.5211202663776955` | `8` |

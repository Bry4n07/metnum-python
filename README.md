# MetNum Python - Primera fase

Nueva base del proyecto de Métodos Numéricos con Flask, HTML, CSS, JavaScript,
Chart.js y SymPy. Esta fase implementa únicamente:

- Bisección.
- Regla Falsa.

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

La respuesta siempre incluye `success`, `method`, `root`, `tolerance`,
`iterations`, `message` y `steps`. Para la interfaz también se incluyen
`chart_points`, evaluados por el backend.

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

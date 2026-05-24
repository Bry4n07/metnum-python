from __future__ import annotations

import math

from flask import Flask, jsonify, render_template, request

from methods.bisection import BisectionMethod
from methods.false_position import FalsePositionMethod
from services.math_evaluator import MathEvaluator, MathExpressionError


app = Flask(__name__)
evaluator = MathEvaluator()
METHODS = {
    "bisection": BisectionMethod,
    "false_position": FalsePositionMethod,
}


class RequestValidationError(ValueError):
    pass


def error_result(method: str, tolerance: float, message: str) -> dict:
    return {
        "success": False,
        "method": method,
        "root": None,
        "tolerance": tolerance,
        "iterations": 0,
        "message": message,
        "steps": [],
        "chart_points": [],
    }


def required_number(data: dict, key: str, label: str) -> float:
    value = data.get(key)
    if value is None or value == "":
        raise RequestValidationError(f"El campo {label} es obligatorio.")

    try:
        number = float(value)
    except (TypeError, ValueError) as exc:
        raise RequestValidationError(f"El campo {label} debe ser numerico.") from exc

    if not math.isfinite(number):
        raise RequestValidationError(f"El campo {label} debe ser finito.")

    return number


def positive_number_or_default(data: dict, key: str, default: float) -> float:
    if data.get(key) is None or data.get(key) == "":
        return default

    value = required_number(data, key, key)
    if value <= 0:
        raise RequestValidationError(f"El campo {key} debe ser mayor que cero.")
    return value


def max_iterations_or_default(data: dict) -> int:
    value = data.get("max_iterations")
    if value is None or value == "":
        return 100

    if isinstance(value, bool):
        raise RequestValidationError("El campo max_iterations debe ser un entero.")

    try:
        as_float = float(value)
        iterations = int(as_float)
    except (TypeError, ValueError, OverflowError) as exc:
        raise RequestValidationError(
            "El campo max_iterations debe ser un entero."
        ) from exc

    if as_float != iterations or iterations < 1 or iterations > 1000:
        raise RequestValidationError(
            "El campo max_iterations debe estar entre 1 y 1000."
        )
    return iterations


def chart_points(function: str, a: float, b: float) -> list[dict[str, float]]:
    lower = min(a, b)
    upper = max(a, b)
    interval = upper - lower
    padding = interval * 0.16 if interval else 1.0
    return evaluator.sample(function, lower - padding, upper + padding)


@app.get("/")
def home():
    return render_template("home.html")


@app.get("/calculadora")
def calculator():
    return render_template("calculator.html")


@app.post("/api/calculate")
def calculate():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        result = error_result("", 0.001, "La solicitud debe contener datos JSON.")
        return jsonify(result), 422

    method = data.get("method", "")
    tolerance = 0.001

    try:
        if method not in METHODS:
            raise RequestValidationError("Selecciona un metodo disponible.")

        function = data.get("function")
        if not isinstance(function, str) or not function.strip():
            raise RequestValidationError("La funcion es obligatoria.")

        a = required_number(data, "a", "a")
        b = required_number(data, "b", "b")
        tolerance = positive_number_or_default(data, "tolerance", 0.001)
        max_iterations = max_iterations_or_default(data)
    except RequestValidationError as exc:
        return jsonify(error_result(method, tolerance, str(exc))), 422

    try:
        result = METHODS[method](evaluator).solve(
            function, a, b, tolerance, max_iterations
        )
        result["chart_points"] = chart_points(function, a, b)
        return jsonify(result)
    except (MathExpressionError, ValueError, ArithmeticError) as exc:
        return jsonify(error_result(method, tolerance, str(exc))), 422


if __name__ == "__main__":
    app.run(debug=True)


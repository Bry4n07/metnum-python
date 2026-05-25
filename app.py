from __future__ import annotations

import math

from flask import Flask, jsonify, render_template, request

from methods.bisection import BisectionMethod
from methods.false_position import FalsePositionMethod
from methods.lagrange_interpolation import LagrangeInterpolationMethod
from methods.linear_interpolation import LinearInterpolationMethod
from methods.muller import MullerMethod
from methods.multiple_roots import MultipleRootsMethod
from methods.newton import NewtonMethod
from methods.secant import SecantMethod
from services.math_evaluator import MathEvaluator, MathExpressionError


app = Flask(__name__)
evaluator = MathEvaluator()
METHODS = {
    "bisection": BisectionMethod,
    "false_position": FalsePositionMethod,
    "newton": NewtonMethod,
    "secant": SecantMethod,
    "muller": MullerMethod,
    "multiple_roots": MultipleRootsMethod,
    "linear_interpolation": LinearInterpolationMethod,
    "lagrange_interpolation": LagrangeInterpolationMethod,
}
INTERPOLATION_METHODS = {"linear_interpolation", "lagrange_interpolation"}


class RequestValidationError(ValueError):
    pass


def error_result(
    method: str,
    tolerance: float,
    message: str,
    function: str = "",
    x: object = None,
) -> dict:
    if method in INTERPOLATION_METHODS:
        return {
            "success": False,
            "method": method,
            "x": x,
            "result": None,
            "message": message,
            "steps": [],
            "procedure": [],
        }

    if method == "multiple_roots":
        return {
            "success": False,
            "method": method,
            "tolerance": tolerance,
            "function": function,
            "derivative": None,
            "second_derivative": None,
            "search_table": [],
            "suggested_roots": [],
            "tables": [],
            "final_roots": [],
            "chart_points": [],
            "message": message,
        }

    return {
        "success": False,
        "method": method,
        "root": None,
        "tolerance": tolerance,
        "iterations": 0,
        "message": message,
        "steps": [],
    }


def required_number(data: dict, key: str, label: str) -> float:
    value = data.get(key)
    if value is None or value == "":
        raise RequestValidationError(f"El campo {label} es obligatorio.")

    try:
        number = float(value)
    except (TypeError, ValueError) as exc:
        raise RequestValidationError(f"El campo {label} debe ser numérico.") from exc

    if not math.isfinite(number):
        raise RequestValidationError(f"El campo {label} debe ser finito.")

    return number


def positive_number_or_default(
    data: dict, key: str, default: float, label: str | None = None
) -> float:
    if data.get(key) is None or data.get(key) == "":
        return default

    label = label or key
    value = required_number(data, key, label)
    if value <= 0:
        raise RequestValidationError(f"El campo {label} debe ser mayor que cero.")
    return value


def max_iterations_or_default(data: dict) -> int:
    value = data.get("max_iterations")
    if value is None or value == "":
        return 100

    if isinstance(value, bool):
        raise RequestValidationError(
            "El campo máximo de iteraciones debe ser un entero."
        )

    try:
        as_float = float(value)
        iterations = int(as_float)
    except (TypeError, ValueError, OverflowError) as exc:
        raise RequestValidationError(
            "El campo máximo de iteraciones debe ser un entero."
        ) from exc

    if as_float != iterations or iterations < 1 or iterations > 1000:
        raise RequestValidationError(
            "El campo máximo de iteraciones debe estar entre 1 y 1000."
        )
    return iterations


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
    function = ""

    try:
        if method not in METHODS:
            raise RequestValidationError("Selecciona un método disponible.")

        if method == "linear_interpolation":
            arguments = (
                required_number(data, "x", "x"),
                required_number(data, "x1", "x1"),
                required_number(data, "y1", "y1"),
                required_number(data, "x2", "x2"),
                required_number(data, "y2", "y2"),
            )
        elif method == "lagrange_interpolation":
            arguments = (
                required_number(data, "x", "x"),
                required_number(data, "x0", "x0"),
                required_number(data, "y0", "y0"),
                required_number(data, "x1", "x1"),
                required_number(data, "y1", "y1"),
            )
        else:
            function = data.get("function")
            if not isinstance(function, str) or not function.strip():
                raise RequestValidationError("La función es obligatoria.")

            tolerance = positive_number_or_default(
                data, "tolerance", 0.001, "tolerancia"
            )
            max_iterations = max_iterations_or_default(data)

        if method in {"bisection", "false_position"}:
            arguments = (
                required_number(data, "a", "a"),
                required_number(data, "b", "b"),
            )
        elif method == "newton":
            arguments = (required_number(data, "x0", "x0"),)
        elif method == "multiple_roots":
            arguments = ()
        elif method == "secant":
            arguments = (
                required_number(data, "x0", "x0"),
                required_number(data, "x1", "x1"),
            )
        elif method == "muller":
            arguments = (
                required_number(data, "x0", "x0"),
                required_number(data, "x1", "x1"),
                required_number(data, "x2", "x2"),
            )
    except RequestValidationError as exc:
        return jsonify(
            error_result(method, tolerance, str(exc), function, data.get("x"))
        ), 422

    try:
        if method in INTERPOLATION_METHODS:
            return jsonify(METHODS[method]().solve(*arguments))

        result = METHODS[method](evaluator).solve(
            function, *arguments, tolerance, max_iterations
        )
        return jsonify(result)
    except (MathExpressionError, ValueError, ArithmeticError) as exc:
        return jsonify(error_result(method, tolerance, str(exc), function, data.get("x"))), 422


if __name__ == "__main__":
    app.run(debug=True)

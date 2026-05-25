"""Muller method implementation restricted to real roots."""

from __future__ import annotations

import math

from services.math_evaluator import MathEvaluator


class MullerMethod:
    def __init__(self, evaluator: MathEvaluator) -> None:
        self.evaluator = evaluator

    def solve(
        self,
        function: str,
        x0: float,
        x1: float,
        x2: float,
        tolerance: float = 0.001,
        max_iterations: int = 100,
    ) -> dict:
        steps = []

        for iteration in range(1, max_iterations + 1):
            f_x0 = self.evaluator.evaluate(function, x0)
            f_x1 = self.evaluator.evaluate(function, x1)
            f_x2 = self.evaluator.evaluate(function, x2)
            h0 = x1 - x0
            h1 = x2 - x1

            if h0 == 0.0 or h1 == 0.0:
                return self._failure(
                    tolerance,
                    iteration - 1,
                    steps,
                    "No se puede continuar con Müller: los valores iniciales deben ser distintos.",
                )

            d0 = (f_x1 - f_x0) / h0
            d1 = (f_x2 - f_x1) / h1
            interval = h1 + h0

            if interval == 0.0:
                return self._failure(
                    tolerance,
                    iteration - 1,
                    steps,
                    "No se puede continuar con Müller: h1 + h0 es cero.",
                )

            a = (d1 - d0) / interval
            b = (a * h1) + d1
            c = f_x2
            discriminant = (b**2) - (4 * a * c)

            if discriminant < 0:
                return self._failure(
                    tolerance,
                    iteration - 1,
                    steps,
                    "Müller solo trabaja con raíces reales: el discriminante es negativo.",
                )

            d = math.sqrt(discriminant)
            plus_denominator = b + d
            minus_denominator = b - d
            denominator = (
                plus_denominator
                if abs(plus_denominator) > abs(minus_denominator)
                else minus_denominator
            )

            if denominator == 0.0:
                return self._failure(
                    tolerance,
                    iteration - 1,
                    steps,
                    "No se puede continuar con Müller: el denominador es cero.",
                )

            x3 = x2 + ((-2 * c) / denominator)
            err = abs(x3 - x2)
            steps.append(
                {
                    "iteration": iteration,
                    "x0": x0,
                    "x1": x1,
                    "x2": x2,
                    "f_x0": f_x0,
                    "f_x1": f_x1,
                    "f_x2": f_x2,
                    "h0": h0,
                    "h1": h1,
                    "d0": d0,
                    "d1": d1,
                    "a": a,
                    "b": b,
                    "c": c,
                    "x3": x3,
                    "err": err,
                }
            )

            if err <= tolerance:
                return {
                    "success": True,
                    "method": "muller",
                    "root": x3,
                    "tolerance": tolerance,
                    "iterations": iteration,
                    "message": "Müller convergió correctamente.",
                    "steps": steps,
                }

            x0 = x1
            x1 = x2
            x2 = x3

        return {
            "success": False,
            "method": "muller",
            "root": x2,
            "tolerance": tolerance,
            "iterations": max_iterations,
            "message": "No se alcanzó la tolerancia en el número máximo de iteraciones.",
            "steps": steps,
        }

    @staticmethod
    def _failure(
        tolerance: float, iterations: int, steps: list[dict], message: str
    ) -> dict:
        return {
            "success": False,
            "method": "muller",
            "root": None,
            "tolerance": tolerance,
            "iterations": iterations,
            "message": message,
            "steps": steps,
        }

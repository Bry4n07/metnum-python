"""Secant method implementation."""

from __future__ import annotations

from services.math_evaluator import MathEvaluator


class SecantMethod:
    def __init__(self, evaluator: MathEvaluator) -> None:
        self.evaluator = evaluator

    def solve(
        self,
        function: str,
        x0: float,
        x1: float,
        tolerance: float = 0.001,
        max_iterations: int = 100,
    ) -> dict:
        steps = []

        for iteration in range(1, max_iterations + 1):
            fx0 = self.evaluator.evaluate(function, x0)
            fx1 = self.evaluator.evaluate(function, x1)
            denominator = fx1 - fx0

            if denominator == 0.0:
                return {
                    "method": "secant",
                    "root": None,
                    "tolerance": tolerance,
                    "iterations": iteration - 1,
                    "message": "No se puede continuar con Secante: f(x1) - f(x0) es cero.",
                    "success": False,
                    "steps": steps,
                }

            x_next = x1 - (fx1 * (x1 - x0) / denominator)
            error = abs(x_next - x1)

            steps.append(
                {
                    "iteration": iteration,
                    "x0": x0,
                    "x1": x1,
                    "fx0": fx0,
                    "fx1": fx1,
                    "x_next": x_next,
                    "error": error,
                }
            )

            if error <= tolerance:
                return {
                    "method": "secant",
                    "root": x_next,
                    "tolerance": tolerance,
                    "iterations": iteration,
                    "message": "Secante convergio correctamente.",
                    "success": True,
                    "steps": steps,
                }

            x0 = x1
            x1 = x_next

        return {
            "method": "secant",
            "root": x1,
            "tolerance": tolerance,
            "iterations": max_iterations,
            "message": "No se alcanzó la tolerancia en el número máximo de iteraciones.",
            "success": False,
            "steps": steps,
        }


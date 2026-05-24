"""False position ported from the previous Laravel implementation."""

from __future__ import annotations

from services.math_evaluator import MathEvaluator


class FalsePositionMethod:
    def __init__(self, evaluator: MathEvaluator) -> None:
        self.evaluator = evaluator

    def solve(
        self,
        function: str,
        a: float,
        b: float,
        tolerance: float = 0.001,
        max_iterations: int = 100,
    ) -> dict:
        fa = self.evaluator.evaluate(function, a)
        fb = self.evaluator.evaluate(function, b)

        if fa * fb >= 0:
            return {
                "method": "false_position",
                "root": None,
                "tolerance": tolerance,
                "iterations": 0,
                "message": "No se puede aplicar Regla Falsa: no hay cambio de signo en [a, b].",
                "success": False,
                "steps": [],
            }

        steps = []
        previous_xr = None

        for iteration in range(1, max_iterations + 1):
            fa = self.evaluator.evaluate(function, a)
            fb = self.evaluator.evaluate(function, b)
            denominator = fb - fa

            if denominator == 0.0:
                raise ValueError("No se puede continuar: f(b) - f(a) es cero.")

            xr = ((a * fb) - (b * fa)) / denominator
            fxr = self.evaluator.evaluate(function, xr)
            t = None if previous_xr is None else abs(xr - previous_xr)

            steps.append(
                {
                    "iteration": iteration,
                    "a": a,
                    "b": b,
                    "xr": xr,
                    "f_a": fa,
                    "f_b": fb,
                    "f_xr": fxr,
                    "t": t,
                }
            )

            if t is not None and t <= tolerance:
                return {
                    "method": "false_position",
                    "root": xr,
                    "tolerance": tolerance,
                    "iterations": iteration,
                    "message": "Regla Falsa convergio correctamente.",
                    "success": True,
                    "steps": steps,
                }

            if fa * fxr < 0:
                b = xr
            else:
                a = xr

            previous_xr = xr

        return {
            "method": "false_position",
            "root": previous_xr,
            "tolerance": tolerance,
            "iterations": max_iterations,
            "message": "No se alcanzó la tolerancia en el número máximo de iteraciones.",
            "success": False,
            "steps": steps,
        }


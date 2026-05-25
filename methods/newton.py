"""Newton method using a symbolic first derivative from the safe evaluator."""

from __future__ import annotations

from services.math_evaluator import MathEvaluator


class NewtonMethod:
    def __init__(self, evaluator: MathEvaluator) -> None:
        self.evaluator = evaluator

    def solve(
        self,
        function: str,
        x0: float,
        tolerance: float = 0.001,
        max_iterations: int = 100,
    ) -> dict:
        steps = []
        x = x0

        for iteration in range(1, max_iterations + 1):
            fx = self.evaluator.evaluate(function, x)
            dfx = self.evaluator.evaluate_first_derivative(function, x)

            if dfx == 0.0:
                return {
                    "method": "newton",
                    "root": None,
                    "tolerance": tolerance,
                    "iterations": iteration - 1,
                    "message": "No se puede continuar con Newton: f'(x) es cero.",
                    "success": False,
                    "steps": steps,
                }

            x_next = x - (fx / dfx)
            error = abs(x_next - x)

            steps.append(
                {
                    "iteration": iteration,
                    "x": x,
                    "fx": fx,
                    "dfx": dfx,
                    "x_next": x_next,
                    "error": error,
                }
            )

            if error <= tolerance:
                return {
                    "method": "newton",
                    "root": x_next,
                    "tolerance": tolerance,
                    "iterations": iteration,
                    "message": "Newton convergio correctamente.",
                    "success": True,
                    "steps": steps,
                }

            x = x_next

        return {
            "method": "newton",
            "root": x,
            "tolerance": tolerance,
            "iterations": max_iterations,
            "message": "No se alcanzó la tolerancia en el número máximo de iteraciones.",
            "success": False,
            "steps": steps,
        }


"""Multiple roots method with automatic initial value detection."""

from __future__ import annotations

from services.math_evaluator import MathEvaluator, MathExpressionError


class MultipleRootsMethod:
    SEARCH_START = -9
    SEARCH_END = 9
    ROOT_DETECTION_TOLERANCE = 1e-10
    MAX_TABLES = 4

    def __init__(self, evaluator: MathEvaluator) -> None:
        self.evaluator = evaluator

    def solve(
        self,
        function: str,
        tolerance: float = 0.001,
        max_iterations: int = 100,
    ) -> dict:
        derivative = self._format_expression(self.evaluator.first_derivative(function))
        second_derivative = self._format_expression(
            self.evaluator.second_derivative(function)
        )
        search_table, suggested_roots = self._scan_initial_values(function)

        if not suggested_roots:
            return self._result(
                function,
                derivative,
                second_derivative,
                search_table,
                [],
                [],
                [],
                tolerance,
                False,
                (
                    "No se encontraron raíces exactas ni intervalos con cambio "
                    "de signo en el rango de búsqueda [-9, 9]."
                ),
            )

        tables = [
            self._solve_table(
                function, item["xi"], item["n"], tolerance, max_iterations
            )
            for item in suggested_roots
        ]
        final_roots = []
        for table in tables:
            if table["final_xr"] is None:
                continue
            final_roots.append(
                {
                    "table": table["table_number"],
                    "xr": table["final_xr"],
                    "y": self.evaluator.evaluate(function, table["final_xr"]),
                }
            )

        successful_roots = sum(1 for table in tables if table["success"])
        success = successful_roots > 0
        if success:
            message = (
                f"Raíces Múltiples obtuvo {successful_roots} tabla"
                f"{'s' if successful_roots != 1 else ''} convergente"
                f"{'s' if successful_roots != 1 else ''}."
            )
        else:
            message = "No se obtuvo una raíz convergente en las tablas generadas."

        chart_points = (
            self.evaluator.sample(function, self.SEARCH_START, self.SEARCH_END, 181)
            if final_roots
            else []
        )
        return self._result(
            function,
            derivative,
            second_derivative,
            search_table,
            suggested_roots,
            tables,
            final_roots,
            tolerance,
            success,
            message,
            chart_points,
        )

    def _scan_initial_values(self, function: str) -> tuple[list[dict], list[dict]]:
        rows = []
        for x in range(self.SEARCH_START, self.SEARCH_END + 1):
            try:
                fx = self.evaluator.evaluate(function, float(x))
            except MathExpressionError:
                fx = None
            rows.append(
                {
                    "x": float(x),
                    "fx": fx,
                    "sign": self._sign(fx),
                    "interval_or_exact": "",
                    "suggested_xi": None,
                    "n": None,
                }
            )

        suggestions = []
        for index, row in enumerate(rows):
            if row["fx"] is not None and abs(row["fx"]) <= self.ROOT_DETECTION_TOLERANCE:
                row["interval_or_exact"] = "Raíz exacta"
                self._add_suggestion(
                    suggestions, row, row["x"], "Raíz exacta"
                )

            if index == len(rows) - 1:
                continue
            next_row = rows[index + 1]
            if (
                row["fx"] is None
                or next_row["fx"] is None
                or abs(row["fx"]) <= self.ROOT_DETECTION_TOLERANCE
                or abs(next_row["fx"]) <= self.ROOT_DETECTION_TOLERANCE
                or row["fx"] * next_row["fx"] >= 0
            ):
                continue

            finding = f"Intervalo [{row['x']:g}, {next_row['x']:g}]"
            self._mark_interval(row, finding)
            self._mark_interval(next_row, finding)
            self._add_suggestion(suggestions, row, row["x"], finding)
            self._add_suggestion(suggestions, next_row, next_row["x"], finding)

        return rows, suggestions

    @staticmethod
    def _mark_interval(row: dict, finding: str) -> None:
        current = row["interval_or_exact"]
        if not current:
            row["interval_or_exact"] = finding
        elif finding not in current:
            row["interval_or_exact"] = f"{current}; {finding}"

    def _add_suggestion(
        self, suggestions: list[dict], row: dict, xi: float, source: str
    ) -> None:
        if len(suggestions) >= self.MAX_TABLES:
            return
        if any(
            abs(item["xi"] - xi) <= self.ROOT_DETECTION_TOLERANCE
            for item in suggestions
        ):
            return

        n = len(suggestions) + 1
        row["suggested_xi"] = xi
        row["n"] = n
        suggestions.append({"n": n, "xi": xi, "source": source})

    def _solve_table(
        self,
        function: str,
        initial_xi: float,
        table_number: int,
        tolerance: float,
        max_iterations: int,
    ) -> dict:
        iterations = []
        xi = initial_xi
        previous_xr = None

        for iteration in range(1, max_iterations + 1):
            fx = self.evaluator.evaluate(function, xi)
            dfx = self.evaluator.evaluate_first_derivative(function, xi)
            ddfx = self.evaluator.evaluate_second_derivative(function, xi)

            if abs(fx) <= self.ROOT_DETECTION_TOLERANCE:
                error = None if previous_xr is None else abs(xi - previous_xr)
                iterations.append(
                    self._iteration(
                        iteration, xi, fx, dfx, ddfx, xi, error, "Raíz exacta"
                    )
                )
                return self._table_result(
                    table_number,
                    initial_xi,
                    xi,
                    iterations,
                    True,
                    "Raíz exacta detectada.",
                )

            denominator = (dfx**2) - (fx * ddfx)
            if denominator == 0.0:
                iterations.append(
                    self._iteration(
                        iteration,
                        xi,
                        fx,
                        dfx,
                        ddfx,
                        None,
                        None,
                        "Denominador cero",
                    )
                )
                return self._table_result(
                    table_number,
                    initial_xi,
                    previous_xr,
                    iterations,
                    False,
                    "No se puede continuar: el denominador es cero.",
                )

            xr = xi - ((fx * dfx) / denominator)
            error = None if previous_xr is None else abs(xr - previous_xr)
            fxr = self.evaluator.evaluate(function, xr)

            if abs(fxr) <= self.ROOT_DETECTION_TOLERANCE:
                status = "Raíz exacta"
                success = True
                message = "Raíz exacta detectada."
            elif error is not None and error <= tolerance:
                status = "Convergió"
                success = True
                message = "Se alcanzó la tolerancia indicada."
            else:
                status = "Iterando"
                success = False
                message = ""

            iterations.append(
                self._iteration(iteration, xi, fx, dfx, ddfx, xr, error, status)
            )
            if success:
                return self._table_result(
                    table_number, initial_xi, xr, iterations, True, message
                )

            previous_xr = xr
            xi = xr

        iterations[-1]["status"] = "Máximo de iteraciones"
        return self._table_result(
            table_number,
            initial_xi,
            previous_xr,
            iterations,
            False,
            "No se alcanzó la tolerancia en el número máximo de iteraciones.",
        )

    @staticmethod
    def _sign(value: float | None) -> str:
        if value is None:
            return "No definido"
        if abs(value) <= MultipleRootsMethod.ROOT_DETECTION_TOLERANCE:
            return "0"
        return "+" if value > 0 else "-"

    @staticmethod
    def _format_expression(expression) -> str:
        return str(expression.expand()).replace("**", "^")

    @staticmethod
    def _iteration(
        iteration: int,
        xi: float,
        fx: float,
        dfx: float,
        ddfx: float,
        xr: float | None,
        error: float | None,
        status: str,
    ) -> dict:
        return {
            "iteration": iteration,
            "xi": xi,
            "fx": fx,
            "dfx": dfx,
            "ddfx": ddfx,
            "xr": xr,
            "error": error,
            "status": status,
        }

    @staticmethod
    def _table_result(
        table_number: int,
        initial_xi: float,
        final_xr: float | None,
        iterations: list[dict],
        success: bool,
        message: str,
    ) -> dict:
        return {
            "table_number": table_number,
            "initial_xi": initial_xi,
            "final_xr": final_xr,
            "iterations": iterations,
            "success": success,
            "message": message,
        }

    @staticmethod
    def _result(
        function: str,
        derivative: str,
        second_derivative: str,
        search_table: list[dict],
        suggested_roots: list[dict],
        tables: list[dict],
        final_roots: list[dict],
        tolerance: float,
        success: bool,
        message: str,
        chart_points: list[dict] | None = None,
    ) -> dict:
        return {
            "success": success,
            "method": "multiple_roots",
            "tolerance": tolerance,
            "function": function,
            "derivative": derivative,
            "second_derivative": second_derivative,
            "search_table": search_table,
            "suggested_roots": suggested_roots,
            "tables": tables,
            "final_roots": final_roots,
            "chart_points": chart_points or [],
            "message": message,
        }

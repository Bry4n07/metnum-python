"""Restricted mathematical expression evaluation powered by SymPy."""

from __future__ import annotations

from functools import lru_cache
import math
import re

import sympy as sp


class MathExpressionError(ValueError):
    """Raised when an expression cannot be safely evaluated."""


class MathEvaluator:
    """Build restricted SymPy expressions using the grammar of the Laravel app."""

    _x = sp.Symbol("x", real=True)
    _functions = {
        "sin": sp.sin,
        "cos": sp.cos,
        "tan": sp.tan,
        "sqrt": sp.sqrt,
        "abs": sp.Abs,
        "log": sp.log,
        "exp": sp.exp,
        "pow": sp.Pow,
    }
    _operators = {"+", "-", "*", "/", "^", "u+", "u-"}
    _allowed_characters = re.compile(r"^[0-9x+\-*/^().,\s_a-z]+$")

    @classmethod
    @lru_cache(maxsize=128)
    def parse(cls, expression: str) -> sp.Expr:
        if not isinstance(expression, str) or not expression.strip():
            raise MathExpressionError("La funcion no puede estar vacia.")

        normalized = expression.lower().strip()

        if not cls._allowed_characters.fullmatch(normalized):
            raise MathExpressionError("La funcion contiene caracteres no permitidos.")

        try:
            parsed = cls._build_expression(cls._to_rpn(cls._tokenize(normalized)))
        except MathExpressionError:
            raise
        except Exception as exc:
            raise MathExpressionError(
                "La funcion no se pudo evaluar. Revisa la expresion."
            ) from exc

        return parsed

    @classmethod
    def _tokenize(cls, expression: str) -> list[dict[str, object]]:
        tokens = []
        position = 0
        previous_type = None

        while position < len(expression):
            character = expression[position]

            if character.isspace():
                position += 1
                continue

            if character.isdigit() or character == ".":
                text = ""
                while position < len(expression) and (
                    expression[position].isdigit() or expression[position] == "."
                ):
                    text += expression[position]
                    position += 1

                try:
                    float(text)
                except ValueError as exc:
                    raise MathExpressionError(
                        "La funcion contiene un numero invalido."
                    ) from exc

                value = sp.Float(text) if "." in text else sp.Integer(text)
                tokens.append({"type": "number", "value": value})
                previous_type = "number"
                continue

            if character.isalpha() or character == "_":
                if previous_type in {"number", "close_parenthesis"}:
                    raise MathExpressionError(
                        "Multiplicacion implicita no permitida. Usa * (por ejemplo, 2*x)."
                    )

                word = ""
                while position < len(expression) and (
                    expression[position].isalpha() or expression[position] == "_"
                ):
                    word += expression[position]
                    position += 1

                if word == "x":
                    tokens.append({"type": "number", "value": cls._x})
                    previous_type = "number"
                    continue

                if word in cls._functions:
                    tokens.append({"type": "function", "value": word})
                    previous_type = "function"
                    continue

                raise MathExpressionError(
                    "La funcion contiene palabras o funciones no permitidas."
                )

            if character in cls._operators:
                tokens.append({"type": "operator", "value": character})
                position += 1
                previous_type = "operator"
                continue

            if character in {"(", ")"}:
                if character == "(" and previous_type in {
                    "number",
                    "close_parenthesis",
                }:
                    raise MathExpressionError(
                        "Multiplicacion implicita no permitida. Usa * (por ejemplo, 2*x)."
                    )

                tokens.append({"type": "parenthesis", "value": character})
                position += 1
                previous_type = (
                    "open_parenthesis" if character == "(" else "close_parenthesis"
                )
                continue

            if character == ",":
                tokens.append({"type": "separator", "value": character})
                position += 1
                previous_type = "separator"
                continue

            raise MathExpressionError("La funcion contiene caracteres no permitidos.")

        return tokens

    @classmethod
    def _to_rpn(cls, tokens: list[dict[str, object]]) -> list[dict[str, object]]:
        output = []
        operators = []
        previous_type = None

        for token in tokens:
            token_type = token["type"]
            if token_type == "number":
                output.append(token)
                previous_type = "number"
                continue

            if token_type == "function":
                operators.append(token)
                previous_type = "function"
                continue

            if token_type == "separator":
                while operators and operators[-1]["value"] != "(":
                    output.append(operators.pop())
                if not operators:
                    raise MathExpressionError(
                        "La funcion contiene separadores invalidos."
                    )
                previous_type = "separator"
                continue

            if token_type == "parenthesis":
                if token["value"] == "(":
                    operators.append(token)
                    previous_type = "open_parenthesis"
                    continue

                while operators and operators[-1]["value"] != "(":
                    output.append(operators.pop())
                if not operators:
                    raise MathExpressionError(
                        "La funcion contiene parentesis desbalanceados."
                    )
                operators.pop()

                if operators and operators[-1]["type"] == "function":
                    output.append(operators.pop())
                previous_type = "number"
                continue

            operator = str(token["value"])
            if operator in {"+", "-"} and (
                previous_type is None
                or previous_type
                in {"operator", "function", "separator", "open_parenthesis"}
            ):
                operator = f"u{operator}"

            while operators and operators[-1]["type"] == "operator":
                top = str(operators[-1]["value"])
                if (
                    cls._is_left_associative(operator)
                    and cls._precedence(operator) <= cls._precedence(top)
                ) or (
                    not cls._is_left_associative(operator)
                    and cls._precedence(operator) < cls._precedence(top)
                ):
                    output.append(operators.pop())
                    continue
                break

            operators.append({"type": "operator", "value": operator})
            previous_type = "operator"

        while operators:
            operator = operators.pop()
            if operator["type"] == "parenthesis":
                raise MathExpressionError(
                    "La funcion contiene parentesis desbalanceados."
                )
            output.append(operator)

        return output

    @classmethod
    def _build_expression(cls, tokens: list[dict[str, object]]) -> sp.Expr:
        stack = []

        for token in tokens:
            token_type = token["type"]
            if token_type == "number":
                stack.append(token["value"])
                continue

            if token_type == "operator":
                operator = str(token["value"])
                if operator in {"u+", "u-"}:
                    if not stack:
                        raise MathExpressionError("La funcion no se pudo evaluar.")
                    value = stack.pop()
                    stack.append(
                        value
                        if operator == "u+"
                        else sp.Mul(sp.Integer(-1), value, evaluate=False)
                    )
                    continue

                if len(stack) < 2:
                    raise MathExpressionError("La funcion no se pudo evaluar.")
                right = stack.pop()
                left = stack.pop()
                stack.append(cls._binary_expression(operator, left, right))
                continue

            if token_type == "function":
                function = str(token["value"])
                arity = 2 if function == "pow" else 1
                if len(stack) < arity:
                    raise MathExpressionError(
                        "La funcion no se pudo evaluar. Revisa sus parametros."
                    )

                if arity == 2:
                    right = stack.pop()
                    left = stack.pop()
                    stack.append(sp.Pow(left, right, evaluate=False))
                else:
                    value = stack.pop()
                    stack.append(cls._functions[function](value, evaluate=False))

        if len(stack) != 1:
            raise MathExpressionError(
                "La funcion no se pudo evaluar. Revisa la expresion."
            )

        return stack.pop()

    @staticmethod
    def _binary_expression(operator: str, left: sp.Expr, right: sp.Expr) -> sp.Expr:
        if operator == "+":
            return sp.Add(left, right, evaluate=False)
        if operator == "-":
            return sp.Add(
                left, sp.Mul(sp.Integer(-1), right, evaluate=False), evaluate=False
            )
        if operator == "*":
            return sp.Mul(left, right, evaluate=False)
        if operator == "/":
            return sp.Mul(
                left, sp.Pow(right, sp.Integer(-1), evaluate=False), evaluate=False
            )
        if operator == "^":
            return sp.Pow(left, right, evaluate=False)
        raise MathExpressionError("La funcion no se pudo evaluar.")

    @staticmethod
    def _precedence(operator: str) -> int:
        return {"u+": 4, "u-": 4, "^": 3, "*": 2, "/": 2, "+": 1, "-": 1}[
            operator
        ]

    @staticmethod
    def _is_left_associative(operator: str) -> bool:
        return operator not in {"^", "u+", "u-"}

    def evaluate(self, expression: str, x: float) -> float:
        try:
            evaluated = self.parse(expression).subs(self._x, sp.Float(x)).evalf()
            if evaluated.is_real is False:
                raise MathExpressionError("El resultado de la funcion no es real.")
            value = float(evaluated)
        except MathExpressionError:
            raise
        except Exception as exc:
            raise MathExpressionError(
                "La funcion no se pudo evaluar para el valor indicado."
            ) from exc

        if not math.isfinite(value):
            raise MathExpressionError("El resultado de la funcion no es finito.")

        return value

    @classmethod
    @lru_cache(maxsize=128)
    def first_derivative(cls, expression: str) -> sp.Expr:
        """Return the symbolic first derivative of an already restricted expression."""
        return sp.diff(cls.parse(expression), cls._x)

    def evaluate_first_derivative(self, expression: str, x: float) -> float:
        try:
            evaluated = self.first_derivative(expression).subs(
                self._x, sp.Float(x)
            ).evalf()
            if evaluated.is_real is False:
                raise MathExpressionError("El resultado de la derivada no es real.")
            value = float(evaluated)
        except MathExpressionError:
            raise
        except Exception as exc:
            raise MathExpressionError(
                "La derivada no se pudo evaluar para el valor indicado."
            ) from exc

        if not math.isfinite(value):
            raise MathExpressionError("El resultado de la derivada no es finito.")

        return value

    @classmethod
    @lru_cache(maxsize=128)
    def second_derivative(cls, expression: str) -> sp.Expr:
        """Return the symbolic second derivative of a restricted expression."""
        return sp.diff(cls.parse(expression), cls._x, 2)

    def evaluate_second_derivative(self, expression: str, x: float) -> float:
        try:
            evaluated = self.second_derivative(expression).subs(
                self._x, sp.Float(x)
            ).evalf()
            if evaluated.is_real is False:
                raise MathExpressionError(
                    "El resultado de la segunda derivada no es real."
                )
            value = float(evaluated)
        except MathExpressionError:
            raise
        except Exception as exc:
            raise MathExpressionError(
                "La segunda derivada no se pudo evaluar para el valor indicado."
            ) from exc

        if not math.isfinite(value):
            raise MathExpressionError(
                "El resultado de la segunda derivada no es finito."
            )

        return value

    def sample(
        self, expression: str, start: float, end: float, amount: int = 141
    ) -> list[dict[str, float]]:
        """Create plot points, omitting values outside a function's domain."""
        if amount < 2:
            amount = 2

        distance = end - start
        points = []
        for index in range(amount):
            x = start + distance * index / (amount - 1)
            try:
                y = self.evaluate(expression, x)
            except MathExpressionError:
                continue
            points.append({"x": x, "y": y})

        return points

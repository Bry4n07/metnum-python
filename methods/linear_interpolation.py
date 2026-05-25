"""Two-point linear interpolation."""

from __future__ import annotations


class LinearInterpolationMethod:
    def solve(self, x: float, x1: float, y1: float, x2: float, y2: float) -> dict:
        denominator = x2 - x1
        if denominator == 0.0:
            return {
                "success": False,
                "method": "linear_interpolation",
                "x": x,
                "result": None,
                "message": "No se puede interpolar: x1 no puede ser igual a x2.",
                "steps": [],
                "procedure": [],
            }

        numerator = (x - x1) * (y2 - y1)
        slope = (y2 - y1) / denominator
        result = y1 + (numerator / denominator)

        return {
            "success": True,
            "method": "linear_interpolation",
            "x": x,
            "result": result,
            "message": "Interpolación Lineal calculada correctamente.",
            "steps": [
                {
                    "x": x,
                    "x1": x1,
                    "y1": y1,
                    "x2": x2,
                    "y2": y2,
                    "numerator": numerator,
                    "denominator": denominator,
                    "slope": slope,
                    "result": result,
                }
            ],
            "procedure": [
                {
                    "title": "Fórmula general",
                    "lines": [
                        {
                            "template": "y = y1 + ((x - x1)(y2 - y1)) / (x2 - x1)",
                            "values": {},
                        }
                    ],
                },
                {
                    "title": "Sustitución",
                    "lines": [
                        {
                            "template": "y = {y1} + (({x} - {x1})({y2} - {y1})) / ({x2} - {x1})",
                            "values": {
                                "x": x,
                                "x1": x1,
                                "y1": y1,
                                "x2": x2,
                                "y2": y2,
                            },
                        }
                    ],
                },
                {
                    "title": "Desarrollo",
                    "lines": [
                        {
                            "template": "m = (y2 - y1) / (x2 - x1)",
                            "values": {},
                        },
                        {
                            "template": "m = ({y2} - {y1}) / ({x2} - {x1})",
                            "values": {"x1": x1, "y1": y1, "x2": x2, "y2": y2},
                        },
                        {"template": "m = {slope}", "values": {"slope": slope}},
                        {
                            "template": "y = {y1} + ({x} - {x1}) * {slope}",
                            "values": {
                                "y1": y1,
                                "x": x,
                                "x1": x1,
                                "slope": slope,
                            },
                        },
                    ],
                },
                {
                    "title": "Resultado",
                    "lines": [
                        {"template": "y = {result}", "values": {"result": result}}
                    ],
                },
            ],
        }

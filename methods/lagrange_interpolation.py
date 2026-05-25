"""Two-point Lagrange interpolation."""

from __future__ import annotations


class LagrangeInterpolationMethod:
    def solve(self, x: float, x0: float, y0: float, x1: float, y1: float) -> dict:
        denominator = x0 - x1
        if denominator == 0.0:
            return {
                "success": False,
                "method": "lagrange_interpolation",
                "x": x,
                "result": None,
                "message": "No se puede interpolar: x0 no puede ser igual a x1.",
                "steps": [],
                "procedure": [],
            }

        l0 = (x - x1) / denominator
        l1 = (x - x0) / (x1 - x0)
        term0 = y0 * l0
        term1 = y1 * l1
        result = term0 + term1

        return {
            "success": True,
            "method": "lagrange_interpolation",
            "x": x,
            "result": result,
            "message": "Interpolación de Lagrange calculada correctamente.",
            "steps": [
                {
                    "x": x,
                    "x0": x0,
                    "y0": y0,
                    "x1": x1,
                    "y1": y1,
                    "l0": l0,
                    "l1": l1,
                    "term0": term0,
                    "term1": term1,
                    "result": result,
                }
            ],
            "procedure": [
                {
                    "title": "Fórmulas generales",
                    "lines": [
                        {
                            "template": "L0 = (x - x1) / (x0 - x1)",
                            "values": {},
                        },
                        {
                            "template": "L1 = (x - x0) / (x1 - x0)",
                            "values": {},
                        },
                        {
                            "template": "P(x) = y0L0 + y1L1",
                            "values": {},
                        },
                    ],
                },
                {
                    "title": "Sustitución",
                    "lines": [
                        {
                            "template": "L0 = ({x} - {x1}) / ({x0} - {x1})",
                            "values": {"x": x, "x0": x0, "x1": x1},
                        },
                        {
                            "template": "L1 = ({x} - {x0}) / ({x1} - {x0})",
                            "values": {"x": x, "x0": x0, "x1": x1},
                        },
                    ],
                },
                {
                    "title": "Desarrollo",
                    "lines": [
                        {"template": "L0 = {l0}", "values": {"l0": l0}},
                        {"template": "L1 = {l1}", "values": {"l1": l1}},
                        {
                            "template": "P({x}) = {y0}({l0}) + {y1}({l1})",
                            "values": {
                                "x": x,
                                "y0": y0,
                                "l0": l0,
                                "y1": y1,
                                "l1": l1,
                            },
                        },
                    ],
                },
                {
                    "title": "Resultado",
                    "lines": [
                        {
                            "template": "P({x}) = {result}",
                            "values": {"x": x, "result": result},
                        }
                    ],
                },
            ],
        }

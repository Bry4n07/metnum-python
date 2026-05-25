import unittest

from methods.bisection import BisectionMethod
from methods.false_position import FalsePositionMethod
from methods.lagrange_interpolation import LagrangeInterpolationMethod
from methods.linear_interpolation import LinearInterpolationMethod
from methods.muller import MullerMethod
from methods.multiple_roots import MultipleRootsMethod
from methods.newton import NewtonMethod
from methods.secant import SecantMethod
from services.math_evaluator import MathEvaluator, MathExpressionError


class LaravelParityTest(unittest.TestCase):
    def setUp(self):
        self.evaluator = MathEvaluator()

    def test_bisection_matches_laravel_reference_result(self):
        result = BisectionMethod(self.evaluator).solve(
            "x^3 - x - 2", 0.0, 2.0, 0.001, 100
        )

        self.assertTrue(result["success"])
        self.assertEqual(result["method"], "bisection")
        self.assertEqual(result["root"], 1.5205078125)
        self.assertEqual(result["iterations"], 11)
        self.assertIsNone(result["steps"][0]["t"])
        self.assertEqual(result["steps"][-1]["t"], 0.0009765625)

    def test_false_position_matches_laravel_reference_result(self):
        result = FalsePositionMethod(self.evaluator).solve(
            "x^3 - x - 2", 0.0, 2.0, 0.001, 100
        )

        self.assertTrue(result["success"])
        self.assertEqual(result["method"], "false_position")
        self.assertAlmostEqual(result["root"], 1.5211202663776955, places=14)
        self.assertEqual(result["iterations"], 8)
        self.assertAlmostEqual(result["steps"][-1]["t"], 0.0006385861164426299)

    def test_closed_methods_reject_an_interval_without_sign_change(self):
        for method in (
            BisectionMethod(self.evaluator),
            FalsePositionMethod(self.evaluator),
        ):
            with self.subTest(method=method.__class__.__name__):
                result = method.solve("x^2 + 1", -1.0, 1.0)
                self.assertFalse(result["success"])
                self.assertIsNone(result["root"])
                self.assertEqual(result["iterations"], 0)
                self.assertEqual(result["steps"], [])


class MathEvaluatorTest(unittest.TestCase):
    def setUp(self):
        self.evaluator = MathEvaluator()

    def test_supported_expression_forms(self):
        self.assertAlmostEqual(self.evaluator.evaluate("x^2 - 2", 2), 2.0)
        self.assertAlmostEqual(self.evaluator.evaluate("pow(x,2) - 2", 2), 2.0)
        self.assertAlmostEqual(self.evaluator.evaluate("sin(x)", 0), 0.0)
        self.assertAlmostEqual(self.evaluator.evaluate("cos(x)", 0), 1.0)
        self.assertAlmostEqual(self.evaluator.evaluate("tan(x)", 0), 0.0)
        self.assertAlmostEqual(self.evaluator.evaluate("sqrt(x)", 4), 2.0)
        self.assertAlmostEqual(self.evaluator.evaluate("log(x)", 1), 0.0)
        self.assertAlmostEqual(self.evaluator.evaluate("exp(x)", 0), 1.0)

    def test_unary_operator_precedence_matches_laravel_evaluator(self):
        self.assertEqual(self.evaluator.evaluate("-x^2 + 3", 2), 7.0)
        self.assertEqual(self.evaluator.evaluate("-(x + 1)^2", 2), 9.0)
        self.assertEqual(self.evaluator.evaluate("2^-x", 2), 0.25)

    def test_unknown_functions_are_rejected(self):
        with self.assertRaises(MathExpressionError):
            self.evaluator.evaluate("gamma(x)", 2)

    def test_symbolic_first_derivative_is_evaluated_safely(self):
        self.assertAlmostEqual(
            self.evaluator.evaluate_first_derivative("x^2 - 2", 1.5), 3.0
        )

    def test_symbolic_second_derivative_is_evaluated_safely(self):
        self.assertAlmostEqual(
            self.evaluator.evaluate_second_derivative("x^3 - 2*x^2 + x", 0.8),
            0.8,
        )


class OpenMethodsTest(unittest.TestCase):
    def setUp(self):
        self.evaluator = MathEvaluator()

    def test_newton_converges_with_symbolic_derivative(self):
        result = NewtonMethod(self.evaluator).solve("x^2 - 2", 1.5, 0.001, 100)

        self.assertTrue(result["success"])
        self.assertEqual(result["method"], "newton")
        self.assertAlmostEqual(result["root"], 1.4142135623746899, places=14)
        self.assertEqual(result["iterations"], 3)
        self.assertEqual(
            set(result["steps"][0]),
            {"iteration", "x", "fx", "dfx", "x_next", "error"},
        )

    def test_newton_stops_when_the_derivative_is_zero(self):
        result = NewtonMethod(self.evaluator).solve("x^3", 0.0)

        self.assertFalse(result["success"])
        self.assertEqual(result["iterations"], 0)
        self.assertEqual(result["steps"], [])
        self.assertIn("f'(x) es cero", result["message"])

    def test_secant_converges_from_two_initial_values(self):
        result = SecantMethod(self.evaluator).solve("x^2 - 2", 1.0, 2.0, 0.001, 100)

        self.assertTrue(result["success"])
        self.assertEqual(result["method"], "secant")
        self.assertAlmostEqual(result["root"], 1.41421143847487, places=14)
        self.assertEqual(result["iterations"], 4)
        self.assertEqual(
            set(result["steps"][0]),
            {"iteration", "x0", "x1", "fx0", "fx1", "x_next", "error"},
        )

    def test_secant_stops_when_denominator_is_zero(self):
        result = SecantMethod(self.evaluator).solve("x^2", 1.0, -1.0)

        self.assertFalse(result["success"])
        self.assertEqual(result["iterations"], 0)
        self.assertEqual(result["steps"], [])
        self.assertIn("f(x1) - f(x0) es cero", result["message"])

    def test_muller_converges_from_three_initial_values(self):
        result = MullerMethod(self.evaluator).solve(
            "x^3 + 2*x^2 + 10*x - 20", 0.0, 1.0, 2.0, 0.001, 100
        )

        self.assertTrue(result["success"])
        self.assertEqual(result["method"], "muller")
        self.assertAlmostEqual(result["root"], 1.3688080368924294, places=14)
        self.assertEqual(result["iterations"], 3)
        self.assertLessEqual(result["steps"][-1]["err"], 0.001)
        self.assertEqual(
            set(result["steps"][0]),
            {
                "iteration",
                "x0",
                "x1",
                "x2",
                "f_x0",
                "f_x1",
                "f_x2",
                "h0",
                "h1",
                "d0",
                "d1",
                "a",
                "b",
                "c",
                "x3",
                "err",
            },
        )

    def test_muller_rejects_a_negative_discriminant_for_real_roots(self):
        result = MullerMethod(self.evaluator).solve("x^2 + 1", -1.0, 0.0, 1.0)

        self.assertFalse(result["success"])
        self.assertEqual(result["steps"], [])
        self.assertIn("discriminante es negativo", result["message"])

    def test_muller_stops_when_denominator_is_zero(self):
        result = MullerMethod(self.evaluator).solve("1", 0.0, 1.0, 2.0)

        self.assertFalse(result["success"])
        self.assertEqual(result["steps"], [])
        self.assertIn("denominador es cero", result["message"])


class MultipleRootsMethodTest(unittest.TestCase):
    def setUp(self):
        self.evaluator = MathEvaluator()

    def test_multiple_roots_detects_exact_values_and_builds_separate_tables(self):
        result = MultipleRootsMethod(self.evaluator).solve(
            "x^3 - 6*x^2 + 11*x - 6", 0.001, 100
        )

        self.assertTrue(result["success"])
        self.assertEqual(result["method"], "multiple_roots")
        self.assertEqual(result["derivative"], "3*x^2 - 12*x + 11")
        self.assertEqual(result["second_derivative"], "6*x - 12")
        self.assertEqual(len(result["search_table"]), 19)
        self.assertEqual(result["search_table"][0]["x"], -9.0)
        self.assertEqual(result["search_table"][-1]["x"], 9.0)
        self.assertEqual(result["search_table"][10]["interval_or_exact"], "Raíz exacta")
        self.assertEqual(
            [item["xi"] for item in result["suggested_roots"]],
            [1.0, 2.0, 3.0],
        )
        self.assertEqual(len(result["tables"]), 3)
        self.assertEqual(
            [table["initial_xi"] for table in result["tables"]],
            [1.0, 2.0, 3.0],
        )
        self.assertEqual(
            [table["final_xr"] for table in result["tables"]],
            [1.0, 2.0, 3.0],
        )
        self.assertTrue(all(len(table["iterations"]) == 1 for table in result["tables"]))
        self.assertIsNone(result["tables"][0]["iterations"][0]["error"])
        self.assertEqual(result["tables"][0]["iterations"][0]["status"], "Raíz exacta")
        self.assertEqual(
            set(result["tables"][0]["iterations"][0]),
            {"iteration", "xi", "fx", "dfx", "ddfx", "xr", "error", "status"},
        )
        self.assertEqual(
            [item["xr"] for item in result["final_roots"]],
            [1.0, 2.0, 3.0],
        )
        self.assertTrue(
            all(abs(item["y"]) <= 1e-10 for item in result["final_roots"])
        )
        self.assertEqual(len(result["chart_points"]), 181)

    def test_one_sign_change_pair_uses_both_endpoints_instead_of_midpoint(self):
        result = MultipleRootsMethod(self.evaluator).solve("exp(x) - 4", 0.001, 100)

        self.assertTrue(result["success"])
        self.assertEqual(
            [item["xi"] for item in result["suggested_roots"]], [1.0, 2.0]
        )
        self.assertNotIn(1.5, [item["xi"] for item in result["suggested_roots"]])
        self.assertEqual(
            [table["initial_xi"] for table in result["tables"]], [1.0, 2.0]
        )
        self.assertEqual(len(result["tables"]), 2)
        pair_rows = {
            row["x"]: row for row in result["search_table"] if row["x"] in {1.0, 2.0}
        }
        self.assertEqual(pair_rows[1.0]["interval_or_exact"], "Intervalo [1, 2]")
        self.assertEqual(pair_rows[2.0]["interval_or_exact"], "Intervalo [1, 2]")

    def test_two_sign_change_pairs_generate_four_endpoint_tables(self):
        result = MultipleRootsMethod(self.evaluator).solve("x^2 - 2", 0.001, 100)

        self.assertTrue(result["success"])
        self.assertEqual(
            [item["xi"] for item in result["suggested_roots"]],
            [-2.0, -1.0, 1.0, 2.0],
        )
        self.assertEqual(
            [table["initial_xi"] for table in result["tables"]],
            [-2.0, -1.0, 1.0, 2.0],
        )
        self.assertNotIn(-1.5, [item["xi"] for item in result["suggested_roots"]])
        self.assertNotIn(1.5, [item["xi"] for item in result["suggested_roots"]])
        first_steps = result["tables"][0]["iterations"]
        self.assertIsNone(first_steps[0]["error"])
        self.assertAlmostEqual(
            first_steps[1]["error"],
            abs(first_steps[1]["xr"] - first_steps[0]["xr"]),
        )

    def test_multiple_roots_returns_clear_error_when_scan_finds_no_candidate(self):
        result = MultipleRootsMethod(self.evaluator).solve("x^2 + 1")

        self.assertFalse(result["success"])
        self.assertEqual(result["suggested_roots"], [])
        self.assertEqual(result["tables"], [])
        self.assertEqual(result["final_roots"], [])
        self.assertEqual(result["chart_points"], [])
        self.assertIn("No se encontraron", result["message"])

    def test_multiple_roots_limits_automatic_tables_to_four(self):
        result = MultipleRootsMethod(self.evaluator).solve(
            "(x + 2)*(x + 1)*x*(x - 1)*(x - 2)"
        )

        self.assertEqual(len(result["tables"]), 4)
        self.assertEqual(
            [item["xr"] for item in result["final_roots"]],
            [-2.0, -1.0, 0.0, 1.0],
        )


class InterpolationMethodsTest(unittest.TestCase):
    def test_linear_interpolation_calculates_the_expected_value(self):
        result = LinearInterpolationMethod().solve(3.0, 2.0, 4.0, 5.0, 10.0)

        self.assertTrue(result["success"])
        self.assertEqual(result["method"], "linear_interpolation")
        self.assertEqual(result["x"], 3.0)
        self.assertEqual(result["result"], 6.0)
        self.assertEqual(result["steps"][0]["slope"], 2.0)
        self.assertEqual(
            [block["title"] for block in result["procedure"]],
            ["Fórmula general", "Sustitución", "Desarrollo", "Resultado"],
        )
        self.assertEqual(
            result["procedure"][2]["lines"][2]["values"]["slope"], 2.0
        )
        self.assertEqual(
            result["procedure"][3]["lines"][0]["values"]["result"], 6.0
        )
        self.assertEqual(
            set(result["steps"][0]),
            {
                "x",
                "x1",
                "y1",
                "x2",
                "y2",
                "numerator",
                "denominator",
                "slope",
                "result",
            },
        )

    def test_linear_interpolation_rejects_equal_x_values(self):
        result = LinearInterpolationMethod().solve(3.0, 2.0, 4.0, 2.0, 10.0)

        self.assertFalse(result["success"])
        self.assertEqual(result["steps"], [])
        self.assertEqual(result["procedure"], [])
        self.assertIn("x1 no puede ser igual a x2", result["message"])

    def test_lagrange_interpolation_calculates_the_expected_value(self):
        result = LagrangeInterpolationMethod().solve(3.0, 2.0, 4.0, 5.0, 10.0)

        self.assertTrue(result["success"])
        self.assertEqual(result["method"], "lagrange_interpolation")
        self.assertEqual(result["x"], 3.0)
        self.assertEqual(result["result"], 6.0)
        self.assertAlmostEqual(result["steps"][0]["l0"], 2.0 / 3.0)
        self.assertAlmostEqual(result["steps"][0]["l1"], 1.0 / 3.0)
        self.assertEqual(
            [block["title"] for block in result["procedure"]],
            ["Fórmulas generales", "Sustitución", "Desarrollo", "Resultado"],
        )
        self.assertAlmostEqual(
            result["procedure"][2]["lines"][0]["values"]["l0"], 2.0 / 3.0
        )
        self.assertEqual(
            result["procedure"][3]["lines"][0]["values"]["result"], 6.0
        )
        self.assertEqual(
            set(result["steps"][0]),
            {
                "x",
                "x0",
                "y0",
                "x1",
                "y1",
                "l0",
                "l1",
                "term0",
                "term1",
                "result",
            },
        )

    def test_lagrange_interpolation_rejects_equal_x_values(self):
        result = LagrangeInterpolationMethod().solve(3.0, 2.0, 4.0, 2.0, 10.0)

        self.assertFalse(result["success"])
        self.assertEqual(result["steps"], [])
        self.assertEqual(result["procedure"], [])
        self.assertIn("x0 no puede ser igual a x1", result["message"])


if __name__ == "__main__":
    unittest.main()

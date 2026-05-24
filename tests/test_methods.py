import unittest

from methods.bisection import BisectionMethod
from methods.false_position import FalsePositionMethod
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


if __name__ == "__main__":
    unittest.main()

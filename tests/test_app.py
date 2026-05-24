import unittest

from app import app


class CalculateApiTest(unittest.TestCase):
    def setUp(self):
        app.config.update(TESTING=True)
        self.client = app.test_client()

    def test_calculation_returns_required_contract_and_chart_points(self):
        response = self.client.post(
            "/api/calculate",
            json={
                "method": "bisection",
                "function": "x^3 - x - 2",
                "a": 0,
                "b": 2,
            },
        )

        self.assertEqual(response.status_code, 200)
        result = response.get_json()
        for key in (
            "success",
            "method",
            "root",
            "tolerance",
            "iterations",
            "message",
            "steps",
        ):
            self.assertIn(key, result)
        self.assertEqual(result["tolerance"], 0.001)
        self.assertTrue(result["chart_points"])

    def test_sign_change_validation_returns_clear_method_error(self):
        response = self.client.post(
            "/api/calculate",
            json={
                "method": "false_position",
                "function": "x^2 + 1",
                "a": -1,
                "b": 1,
            },
        )

        self.assertEqual(response.status_code, 200)
        result = response.get_json()
        self.assertFalse(result["success"])
        self.assertIn("no hay cambio de signo", result["message"])
        self.assertEqual(result["steps"], [])

    def test_invalid_function_returns_controlled_error(self):
        response = self.client.post(
            "/api/calculate",
            json={
                "method": "bisection",
                "function": "funcion_desconocida(x)",
                "a": 0,
                "b": 2,
            },
        )

        self.assertEqual(response.status_code, 422)
        result = response.get_json()
        self.assertFalse(result["success"])
        self.assertEqual(result["steps"], [])
        self.assertIn("funciones no permitidas", result["message"])


if __name__ == "__main__":
    unittest.main()


import unittest
from pathlib import Path

from app import app


class CalculateApiTest(unittest.TestCase):
    def setUp(self):
        app.config.update(TESTING=True)
        self.client = app.test_client()

    def test_calculation_returns_required_contract_without_chart_points(self):
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
        self.assertNotIn("chart_points", result)

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

    def test_newton_endpoint_receives_x0_and_returns_newton_steps(self):
        response = self.client.post(
            "/api/calculate",
            json={
                "method": "newton",
                "function": "x^2 - 2",
                "x0": 1.5,
            },
        )

        self.assertEqual(response.status_code, 200)
        result = response.get_json()
        self.assertTrue(result["success"])
        self.assertEqual(result["method"], "newton")
        self.assertEqual(
            set(result["steps"][0]),
            {"iteration", "x", "fx", "dfx", "x_next", "error"},
        )

    def test_secant_endpoint_receives_two_initial_values(self):
        response = self.client.post(
            "/api/calculate",
            json={
                "method": "secant",
                "function": "x^2 - 2",
                "x0": 1,
                "x1": 2,
            },
        )

        self.assertEqual(response.status_code, 200)
        result = response.get_json()
        self.assertTrue(result["success"])
        self.assertEqual(result["method"], "secant")
        self.assertEqual(
            set(result["steps"][0]),
            {"iteration", "x0", "x1", "fx0", "fx1", "x_next", "error"},
        )

    def test_muller_endpoint_receives_three_initial_values(self):
        response = self.client.post(
            "/api/calculate",
            json={
                "method": "muller",
                "function": "x^3 + 2*x^2 + 10*x - 20",
                "x0": 0,
                "x1": 1,
                "x2": 2,
            },
        )

        self.assertEqual(response.status_code, 200)
        result = response.get_json()
        self.assertTrue(result["success"])
        self.assertEqual(result["method"], "muller")
        self.assertIn("x3", result["steps"][0])
        self.assertIn("err", result["steps"][0])

    def test_linear_interpolation_endpoint_does_not_require_a_function(self):
        response = self.client.post(
            "/api/calculate",
            json={
                "method": "linear_interpolation",
                "x": 3,
                "x1": 2,
                "y1": 4,
                "x2": 5,
                "y2": 10,
            },
        )

        self.assertEqual(response.status_code, 200)
        result = response.get_json()
        self.assertTrue(result["success"])
        self.assertEqual(result["result"], 6.0)
        self.assertEqual(result["steps"][0]["slope"], 2.0)
        self.assertEqual(
            [block["title"] for block in result["procedure"]],
            ["Fórmula general", "Sustitución", "Desarrollo", "Resultado"],
        )
        self.assertNotIn("tolerance", result)
        self.assertNotIn("chart_points", result)

    def test_lagrange_endpoint_does_not_require_a_function(self):
        response = self.client.post(
            "/api/calculate",
            json={
                "method": "lagrange_interpolation",
                "x": 3,
                "x0": 2,
                "y0": 4,
                "x1": 5,
                "y1": 10,
            },
        )

        self.assertEqual(response.status_code, 200)
        result = response.get_json()
        self.assertTrue(result["success"])
        self.assertEqual(result["result"], 6.0)
        self.assertEqual(
            [block["title"] for block in result["procedure"]],
            ["Fórmulas generales", "Sustitución", "Desarrollo", "Resultado"],
        )
        self.assertNotIn("tolerance", result)
        self.assertNotIn("chart_points", result)

    def test_interpolation_endpoints_validate_their_distinct_x_values(self):
        payloads = (
            {
                "method": "linear_interpolation",
                "x": 3,
                "x1": 2,
                "y1": 4,
                "x2": 2,
                "y2": 10,
            },
            {
                "method": "lagrange_interpolation",
                "x": 3,
                "x0": 2,
                "y0": 4,
                "x1": 2,
                "y1": 10,
            },
        )
        for payload in payloads:
            with self.subTest(method=payload["method"]):
                result = self.client.post("/api/calculate", json=payload).get_json()
                self.assertFalse(result["success"])
                self.assertIn("no puede ser igual", result["message"])
                self.assertEqual(result["steps"], [])
                self.assertEqual(result["procedure"], [])

    def test_interpolation_endpoint_validates_numeric_values(self):
        response = self.client.post(
            "/api/calculate",
            json={
                "method": "linear_interpolation",
                "x": "dato",
                "x1": 2,
                "y1": 4,
                "x2": 5,
                "y2": 10,
            },
        )

        self.assertEqual(response.status_code, 422)
        result = response.get_json()
        self.assertFalse(result["success"])
        self.assertIsNone(result["result"])
        self.assertEqual(result["procedure"], [])
        self.assertIn("numérico", result["message"])

    def test_multiple_roots_endpoint_detects_roots_without_x0(self):
        response = self.client.post(
            "/api/calculate",
            json={
                "method": "multiple_roots",
                "function": "x^3 - 6*x^2 + 11*x - 6",
            },
        )

        self.assertEqual(response.status_code, 200)
        result = response.get_json()
        self.assertTrue(result["success"])
        self.assertEqual(result["method"], "multiple_roots")
        self.assertEqual(result["derivative"], "3*x^2 - 12*x + 11")
        self.assertEqual(result["second_derivative"], "6*x - 12")
        self.assertEqual(len(result["search_table"]), 19)
        self.assertEqual(result["search_table"][0]["x"], -9.0)
        self.assertEqual(result["search_table"][-1]["x"], 9.0)
        self.assertEqual(result["search_table"][10]["interval_or_exact"], "Raíz exacta")
        self.assertEqual(
            [item["xi"] for item in result["suggested_roots"]], [1.0, 2.0, 3.0]
        )
        self.assertEqual(len(result["tables"]), 3)
        self.assertEqual(
            set(result["tables"][0]["iterations"][0]),
            {"iteration", "xi", "fx", "dfx", "ddfx", "xr", "error", "status"},
        )
        self.assertEqual(
            [item["xr"] for item in result["final_roots"]], [1.0, 2.0, 3.0]
        )
        self.assertEqual(len(result["chart_points"]), 181)

    def test_multiple_roots_invalid_function_keeps_multiple_table_contract(self):
        response = self.client.post(
            "/api/calculate",
            json={
                "method": "multiple_roots",
                "function": "funcion_desconocida(x)",
            },
        )

        self.assertEqual(response.status_code, 422)
        result = response.get_json()
        self.assertFalse(result["success"])
        self.assertEqual(result["suggested_roots"], [])
        self.assertEqual(result["tables"], [])
        self.assertEqual(result["final_roots"], [])
        self.assertEqual(result["chart_points"], [])
        self.assertIn("funciones no permitidas", result["message"])

    def test_multiple_roots_sign_change_pair_uses_endpoint_tables(self):
        response = self.client.post(
            "/api/calculate",
            json={
                "method": "multiple_roots",
                "function": "exp(x) - 4",
            },
        )

        self.assertEqual(response.status_code, 200)
        result = response.get_json()
        self.assertEqual(
            [item["xi"] for item in result["suggested_roots"]], [1.0, 2.0]
        )
        self.assertNotIn(1.5, [item["xi"] for item in result["suggested_roots"]])
        self.assertEqual(
            [table["initial_xi"] for table in result["tables"]], [1.0, 2.0]
        )

    def test_chart_data_is_not_generated_for_other_methods(self):
        payloads = (
            {
                "method": "false_position",
                "function": "x^3 - x - 2",
                "a": 0,
                "b": 2,
            },
            {"method": "newton", "function": "x^2 - 2", "x0": 1.5},
            {"method": "secant", "function": "x^2 - 2", "x0": 1, "x1": 2},
            {
                "method": "muller",
                "function": "x^3 + 2*x^2 + 10*x - 20",
                "x0": 0,
                "x1": 1,
                "x2": 2,
            },
            {
                "method": "linear_interpolation",
                "x": 3,
                "x1": 2,
                "y1": 4,
                "x2": 5,
                "y2": 10,
            },
            {
                "method": "lagrange_interpolation",
                "x": 3,
                "x0": 2,
                "y0": 4,
                "x1": 5,
                "y1": 10,
            },
        )
        for payload in payloads:
            with self.subTest(method=payload["method"]):
                result = self.client.post("/api/calculate", json=payload).get_json()
                self.assertNotIn("chart_points", result)

    def test_current_views_do_not_render_footer_phases_or_history(self):
        for route in ("/", "/calculadora"):
            with self.subTest(route=route):
                html = self.client.get(route).get_data(as_text=True).lower()
                self.assertNotIn("<footer", html)
                self.assertNotIn("fase", html)
                self.assertNotIn("historial", html)
                self.assertNotIn("localstorage", html)
                self.assertNotIn(">desarrollo<", html)

        calculator_html = self.client.get("/calculadora").get_data(as_text=True).lower()
        self.assertIn("chart.js", calculator_html)
        self.assertIn('id="multiple-roots-chart-panel" hidden', calculator_html)
        self.assertIn('value="newton"', calculator_html)
        self.assertIn('value="secant"', calculator_html)
        self.assertIn('value="muller"', calculator_html)
        self.assertIn('value="multiple_roots"', calculator_html)
        self.assertIn('value="linear_interpolation"', calculator_html)
        self.assertIn('value="lagrange_interpolation"', calculator_html)
        self.assertIn("raíces múltiples", calculator_html)
        self.assertIn('id="search-table"', calculator_html)
        self.assertIn('id="derivative-expression"', calculator_html)
        self.assertIn('id="second-derivative-expression"', calculator_html)
        self.assertIn('id="interpolation-procedure-panel" hidden', calculator_html)
        self.assertNotIn('value="x^3 - x - 2"', calculator_html)
        self.assertNotIn('value="0.001"', calculator_html)
        self.assertNotIn('value="100"', calculator_html)
        self.assertIn('placeholder="ej: x^3 - x - 2"', calculator_html)
        self.assertIn('placeholder="ej: 0.001"', calculator_html)
        self.assertIn('placeholder="ej: 100"', calculator_html)
        procedure_markup = calculator_html.split(
            'id="interpolation-procedure-panel" hidden', 1
        )[1].split("</section>", 1)[0]
        self.assertNotIn("<table", procedure_markup)

        js = (
            Path(app.static_folder) / "js" / "app.js"
        ).read_text(encoding="utf-8")
        self.assertIn('type: "line"', js)
        self.assertIn('type: "scatter"', js)
        self.assertNotIn('type: "bar"', js)
        self.assertIn("functionField.hidden = interpolation", js)
        self.assertIn("toleranceField.hidden = interpolation", js)
        self.assertIn("iterationField.hidden = interpolation", js)
        self.assertIn("renderProcedure(result, displayMethod)", js)
        self.assertIn("interpolationProcedurePanel.hidden = false", js)
        self.assertIn('label: "Valor inicial (xi)"', js)
        self.assertIn('label: "Valor anterior (xᵢ₋₁)"', js)
        self.assertIn('label: "Valor actual (xi)"', js)
        self.assertIn('formula: "xr = xi - f(xi) / f\'(xi)"', js)
        self.assertIn(
            'formula: "xr = xi - f(xi)(xi - xᵢ₋₁) / (f(xi) - f(xᵢ₋₁))"',
            js,
        )
        self.assertIn('{ key: "x", label: "xi" }', js)
        self.assertIn('{ key: "x_next", label: "xr" }', js)
        self.assertIn('{ key: "x0", label: "xᵢ₋₁" }', js)
        self.assertIn("input.placeholder = field.placeholder", js)
        self.assertNotIn("input.value = field.value", js)
        self.assertIn("functionInput.value = \"\";", js)
        self.assertIn("resetResultPanels(methodKey)", js)
        self.assertIn("currentCalculation !== calculationVersion", js)
        self.assertNotIn(
            'linear_interpolation: [\n        { key: "x", label: "x" }', js
        )
        self.assertNotIn(
            'lagrange_interpolation: [\n        { key: "x", label: "x" }', js
        )

        css = (
            Path(app.static_folder) / "css" / "styles.css"
        ).read_text(encoding="utf-8")
        self.assertIn('input[type="number"]::-webkit-outer-spin-button', css)
        self.assertIn('input[type="number"]::-webkit-inner-spin-button', css)
        self.assertIn("-moz-appearance: textfield", css)

    def test_validation_messages_are_presented_in_spanish(self):
        response = self.client.post(
            "/api/calculate",
            json={
                "method": "newton",
                "function": "x^2 - 2",
                "x0": "valor",
            },
        )
        self.assertIn("numérico", response.get_json()["message"])

        response = self.client.post(
            "/api/calculate",
            json={
                "method": "multiple_roots",
                "function": "x^2 - 2",
                "tolerance": 0,
            },
        )
        self.assertIn("tolerancia", response.get_json()["message"])


if __name__ == "__main__":
    unittest.main()

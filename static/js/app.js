const methods = {
    bisection: {
        title: "Bisección",
        description: "Divide el intervalo en mitades y conserva la parte donde continúa el cambio de signo.",
        formula: "xr = (a + b) / 2",
        fields: [
            { key: "a", label: "Límite inferior (a / xi)", value: 0 },
            { key: "b", label: "Límite superior (b / xu)", value: 2 },
        ],
    },
    false_position: {
        title: "Regla Falsa",
        description: "Obtiene xr con la secante trazada entre los extremos del intervalo.",
        formula: "xr = (a·f(b) - b·f(a)) / (f(b) - f(a))",
        fields: [
            { key: "a", label: "Límite inferior (a / xi)", value: 0 },
            { key: "b", label: "Límite superior (b / xu)", value: 2 },
        ],
    },
};

const columns = [
    { key: "iteration", label: "i" },
    { key: "a", label: "a" },
    { key: "b", label: "b" },
    { key: "f_a", label: "f(a)" },
    { key: "f_b", label: "f(b)" },
    { key: "xr", label: "xr" },
    { key: "f_xr", label: "f(xr)" },
    { key: "t", label: "T" },
];

const form = document.querySelector("#calculation-form");
const methodSelect = document.querySelector("#method");
const methodDescription = document.querySelector("#method-description");
const dynamicFields = document.querySelector("#dynamic-fields");
const submitButton = document.querySelector("#submit-button");
const badge = document.querySelector("#result-badge");
const summary = document.querySelector("#result-summary");
const countLabel = document.querySelector("#steps-count");
const table = document.querySelector("#steps-table");
const chartCanvas = document.querySelector("#function-chart");
const chartEmpty = document.querySelector("#chart-empty");
let chartInstance = null;

function formatNumber(value) {
    if (value === null || value === undefined || value === "") {
        return "-";
    }

    const number = Number(value);
    if (!Number.isFinite(number)) {
        return String(value);
    }

    return number.toLocaleString("en-US", {
        maximumSignificantDigits: 12,
        useGrouping: false,
    });
}

function createElement(tag, className, text) {
    const element = document.createElement(tag);
    if (className) {
        element.className = className;
    }
    if (text !== undefined) {
        element.textContent = text;
    }
    return element;
}

function renderFields(methodKey) {
    const selected = methods[methodKey] || methods.bisection;
    dynamicFields.replaceChildren();

    const title = createElement("strong", "", selected.title);
    const copy = document.createTextNode(`${selected.description} Criterio: ${selected.formula}.`);
    methodDescription.replaceChildren(title, copy);

    selected.fields.forEach((field) => {
        const label = createElement("label", "field");
        const caption = createElement("span", "", field.label);
        const input = document.createElement("input");
        input.type = "number";
        input.step = "any";
        input.id = field.key;
        input.name = field.key;
        input.value = field.value;
        input.required = true;
        label.append(caption, input);
        dynamicFields.appendChild(label);
    });
}

function setBadge(success) {
    badge.className = `status-badge ${success ? "success" : "error"}`;
    badge.textContent = success ? "Convergió" : "Sin convergencia";
}

function renderSummary(result) {
    setBadge(result.success);
    summary.className = "result-content";
    summary.replaceChildren();

    const rootBox = createElement("div", "root-display");
    rootBox.append(
        createElement("span", "", "Raíz aproximada"),
        createElement("strong", "", formatNumber(result.root))
    );

    const metrics = createElement("div", "metrics");
    const iteration = createElement("div", "metric");
    iteration.append(
        createElement("span", "", "Iteraciones"),
        createElement("strong", "", String(result.iterations))
    );
    const tolerance = createElement("div", "metric");
    tolerance.append(
        createElement("span", "", "Tolerancia"),
        createElement("strong", "", formatNumber(result.tolerance))
    );
    metrics.append(iteration, tolerance);

    const message = createElement(
        "p",
        `result-message ${result.success ? "" : "error"}`,
        result.message
    );
    summary.append(rootBox, metrics, message);
}

function renderSteps(steps) {
    const head = table.querySelector("thead");
    const body = table.querySelector("tbody");
    const headerRow = document.createElement("tr");

    columns.forEach((column) => {
        headerRow.appendChild(createElement("th", "", column.label));
    });
    head.replaceChildren(headerRow);
    body.replaceChildren();

    if (!steps.length) {
        const row = createElement("tr", "placeholder-row");
        const cell = createElement("td", "", "No hay iteraciones para mostrar.");
        cell.colSpan = columns.length;
        row.appendChild(cell);
        body.appendChild(row);
    } else {
        steps.forEach((step) => {
            const row = document.createElement("tr");
            columns.forEach((column) => {
                const value = column.key === "iteration"
                    ? String(step[column.key])
                    : formatNumber(step[column.key]);
                row.appendChild(createElement("td", "", value));
            });
            body.appendChild(row);
        });
    }

    countLabel.textContent = `${steps.length} ${steps.length === 1 ? "fila" : "filas"}`;
}

function clearChart(message) {
    if (chartInstance) {
        chartInstance.destroy();
        chartInstance = null;
    }
    chartCanvas.hidden = true;
    chartEmpty.hidden = false;
    chartEmpty.textContent = message;
}

function renderChart(result) {
    const values = Array.isArray(result.chart_points) ? result.chart_points : [];
    if (!values.length) {
        clearChart("No existen puntos reales para graficar en este intervalo.");
        return;
    }

    if (typeof Chart === "undefined") {
        clearChart("No se pudo cargar Chart.js; el cálculo y la tabla siguen disponibles.");
        return;
    }

    if (chartInstance) {
        chartInstance.destroy();
    }

    chartEmpty.hidden = true;
    chartCanvas.hidden = false;
    const approximations = (result.steps || []).map((step) => ({
        x: step.xr,
        y: step.f_xr,
    }));

    chartInstance = new Chart(chartCanvas, {
        type: "line",
        data: {
            datasets: [
                {
                    label: "f(x)",
                    data: values,
                    parsing: false,
                    borderColor: "#087f70",
                    borderWidth: 2,
                    pointRadius: 0,
                    tension: 0.12,
                },
                {
                    label: "Aproximaciones xr",
                    data: approximations,
                    parsing: false,
                    showLine: false,
                    pointRadius: 3.4,
                    pointHoverRadius: 5,
                    pointBackgroundColor: "#db744b",
                },
            ],
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            interaction: { intersect: false, mode: "nearest" },
            plugins: {
                legend: {
                    align: "start",
                    labels: { usePointStyle: true, boxWidth: 8 },
                },
            },
            scales: {
                x: {
                    type: "linear",
                    title: { display: true, text: "x" },
                    grid: { color: "rgba(16, 37, 36, 0.06)" },
                },
                y: {
                    title: { display: true, text: "f(x)" },
                    grid: { color: "rgba(16, 37, 36, 0.06)" },
                },
            },
        },
    });
}

function payloadFromForm() {
    return {
        method: methodSelect.value,
        function: document.querySelector("#function").value,
        a: document.querySelector("#a").value,
        b: document.querySelector("#b").value,
        tolerance: document.querySelector("#tolerance").value,
        max_iterations: document.querySelector("#max_iterations").value,
    };
}

async function calculate(event) {
    event.preventDefault();
    submitButton.disabled = true;
    submitButton.textContent = "Calculando...";

    try {
        const response = await fetch("/api/calculate", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payloadFromForm()),
        });
        const result = await response.json();
        renderSummary(result);
        renderSteps(result.steps || []);
        renderChart(result);
    } catch (error) {
        const result = {
            success: false,
            root: null,
            tolerance: document.querySelector("#tolerance").value,
            iterations: 0,
            message: "No se pudo comunicar con el servidor.",
            steps: [],
            chart_points: [],
        };
        renderSummary(result);
        renderSteps([]);
        clearChart("La gráfica no está disponible sin una respuesta del servidor.");
    } finally {
        submitButton.disabled = false;
        submitButton.textContent = "Calcular raíz";
    }
}

if (form) {
    const requestedMethod = new URLSearchParams(window.location.search).get("method");
    if (requestedMethod && methods[requestedMethod]) {
        methodSelect.value = requestedMethod;
    }

    renderFields(methodSelect.value);
    methodSelect.addEventListener("change", () => renderFields(methodSelect.value));
    form.addEventListener("submit", calculate);
}

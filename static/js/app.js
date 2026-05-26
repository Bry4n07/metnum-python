const methods = {
    bisection: {
        title: "Bisección",
        kind: "Método cerrado",
        description: "Divide el intervalo en mitades y conserva la parte donde continúa el cambio de signo.",
        formula: "xr = (a + b) / 2",
        note: {
            label: "Condición inicial",
            title: "Cambio de signo",
            intro: "Para aplicar Bisección o Regla Falsa se debe cumplir:",
            formula: "f(a) · f(b) < 0",
            detail: "Si el intervalo no cumple la condición, el cálculo se detiene antes de iterar.",
        },
        fields: [
            { key: "a", label: "a", placeholder: "Ej: 0" },
            { key: "b", label: "b", placeholder: "Ej: 2" },
        ],
    },
    false_position: {
        title: "Regla Falsa",
        kind: "Método cerrado",
        description: "Obtiene xr con la secante trazada entre los extremos del intervalo.",
        formula: "xr = (a·f(b) - b·f(a)) / (f(b) - f(a))",
        note: {
            label: "Condición inicial",
            title: "Cambio de signo",
            intro: "Para aplicar Bisección o Regla Falsa se debe cumplir:",
            formula: "f(a) · f(b) < 0",
            detail: "Si el intervalo no cumple la condición, el cálculo se detiene antes de iterar.",
        },
        fields: [
            { key: "a", label: "a", placeholder: "Ej: 0" },
            { key: "b", label: "b", placeholder: "Ej: 2" },
        ],
    },
    newton: {
        title: "Newton",
        kind: "Método abierto",
        description: "Usa la pendiente de la función para avanzar desde un valor inicial.",
        formula: "xr = xi - f(xi) / f'(xi)",
        note: {
            label: "Derivada automática",
            title: "Newton",
            intro: "La derivada se obtiene de forma simbólica y segura con SymPy:",
            formula: "xr = xi - f(xi) / f'(xi)",
            detail: "El cálculo se detiene si la derivada evaluada es cero.",
        },
        fields: [
            { key: "x0", label: "Valor inicial (xi)", placeholder: "Ej: 1.5" },
        ],
    },
    secant: {
        title: "Secante",
        kind: "Método abierto",
        description: "Aproxima la pendiente usando dos valores iniciales de la función.",
        formula: "xr = xi - f(xi)(xi - xᵢ₋₁) / (f(xi) - f(xᵢ₋₁))",
        note: {
            label: "Valores iniciales",
            title: "Secante",
            intro: "El método aproxima la siguiente raíz mediante dos evaluaciones:",
            formula: "xr = xi - f(xi)(xi - xᵢ₋₁) / (f(xi) - f(xᵢ₋₁))",
            detail: "El cálculo se detiene si la diferencia de funciones es cero.",
        },
        fields: [
            { key: "x0", label: "Valor anterior (x_1)", placeholder: "Ej: 1" },
            { key: "x1", label: "Valor actual (xi)", placeholder: "Ej: 2" },
        ],
    },
    muller: {
        title: "Müller",
        kind: "Método abierto",
        description: "Aproxima la raíz mediante una parábola construida desde tres valores iniciales.",
        formula: "x3 = x2 + (-2c) / D",
        note: {
            label: "Tres valores iniciales",
            title: "Müller",
            intro: "Se construye una aproximación cuadrática con:",
            formula: "D = b ± sqrt(b^2 - 4ac)",
            detail: "Esta versión se detiene si el discriminante es negativo, porque trabaja solo con raíces reales.",
        },
        fields: [
            { key: "x0", label: "Valor inicial (x0)", placeholder: "Ej: 0" },
            { key: "x1", label: "Valor inicial (x1)", placeholder: "Ej: 1" },
            { key: "x2", label: "Valor inicial (x2)", placeholder: "Ej: 2" },
        ],
    },
    linear_interpolation: {
        title: "Interpolación Lineal",
        kind: "Interpolación",
        description: "Estima el valor de y entre dos puntos conocidos.",
        formula: "y = y1 + ((x - x1)(y2 - y1)) / (x2 - x1)",
        interpolation: true,
        resultLabel: "y interpolada",
        note: {
            label: "Dos puntos",
            title: "Interpolación Lineal",
            intro: "La pendiente conecta directamente ambos datos:",
            formula: "m = (y2 - y1) / (x2 - x1)",
            detail: "Los valores x1 y x2 deben ser diferentes.",
        },
        fields: [
            { key: "x", label: "Valor a interpolar (x)", placeholder: "Ej: 3" },
            { key: "x1", label: "x1", placeholder: "Ej: 2" },
            { key: "y1", label: "y1", placeholder: "Ej: 4" },
            { key: "x2", label: "x2", placeholder: "Ej: 5" },
            { key: "y2", label: "y2", placeholder: "Ej: 10" },
        ],
    },
    lagrange_interpolation: {
        title: "Interpolación de Lagrange",
        kind: "Interpolación",
        description: "Calcula P(x) con los polinomios base de dos puntos.",
        formula: "P(x) = y0·L0 + y1·L1",
        interpolation: true,
        resultLabel: "P(x)",
        note: {
            label: "Dos puntos",
            title: "Lagrange",
            intro: "Los polinomios base se evalúan como:",
            formula: "L0 = (x - x1)/(x0 - x1), L1 = (x - x0)/(x1 - x0)",
            detail: "Los valores x0 y x1 deben ser diferentes.",
        },
        fields: [
            { key: "x", label: "Valor a interpolar (x)", placeholder: "Ej: 3" },
            { key: "x0", label: "x0", placeholder: "Ej: 2" },
            { key: "y0", label: "y0", placeholder: "Ej: 4" },
            { key: "x1", label: "x1", placeholder: "Ej: 5" },
            { key: "y1", label: "y1", placeholder: "Ej: 10" },
        ],
    },
    multiple_roots: {
        title: "Raíces Múltiples",
        kind: "Método abierto",
        description: "Busca valores sugeridos y genera una tabla por cada raíz detectada.",
        formula: "xr = xi - f(xi)f'(xi) / (f'(xi)^2 - f(xi)f''(xi))",
        note: {
            label: "Búsqueda automática",
            title: "Raíces Múltiples",
            intro: "Se explora de -9 a 9 con paso 1 para sugerir hasta cuatro xi:",
            formula: "T = |xr actual - xr anterior|",
            detail: "Cada extremo de un intervalo detectado genera su propia tabla; no se usa el punto medio.",
        },
        fields: [],
    },
};

const columnsByMethod = {
    bisection: [
        { key: "iteration", label: "i" },
        { key: "a", label: "a" },
        { key: "b", label: "b" },
        { key: "f_a", label: "f(a)" },
        { key: "f_b", label: "f(b)" },
        { key: "xr", label: "xr" },
        { key: "f_xr", label: "f(xr)" },
        { key: "t", label: "T" },
    ],
    false_position: [
        { key: "iteration", label: "i" },
        { key: "a", label: "a" },
        { key: "b", label: "b" },
        { key: "f_a", label: "f(a)" },
        { key: "f_b", label: "f(b)" },
        { key: "xr", label: "xr" },
        { key: "f_xr", label: "f(xr)" },
        { key: "t", label: "T" },
    ],
    newton: [
        { key: "iteration", label: "i" },
        { key: "x", label: "xi" },
        { key: "fx", label: "f(xi)" },
        { key: "dfx", label: "f'(xi)" },
        { key: "x_next", label: "xr" },
        { key: "error", label: "T" },
    ],
    secant: [
        { key: "iteration", label: "i" },
        { key: "x0", label: "x_1" },
        { key: "x1", label: "xi" },
        { key: "fx0", label: "f(x_1)" },
        { key: "fx1", label: "f(xi)" },
        { key: "x_next", label: "xr" },
        { key: "error", label: "T" },
    ],
    muller: [
        { key: "iteration", label: "i" },
        { key: "x0", label: "x0" },
        { key: "x1", label: "x1" },
        { key: "x2", label: "x2" },
        { key: "f_x0", label: "f(x0)" },
        { key: "f_x1", label: "f(x1)" },
        { key: "f_x2", label: "f(x2)" },
        { key: "h0", label: "h0" },
        { key: "h1", label: "h1" },
        { key: "d0", label: "d0" },
        { key: "d1", label: "d1" },
        { key: "a", label: "a" },
        { key: "b", label: "b" },
        { key: "c", label: "c" },
        { key: "x3", label: "x3" },
        { key: "err", label: "Err" },
    ],
    multiple_roots: [
        { key: "iteration", label: "i" },
        { key: "xi", label: "xi" },
        { key: "fx", label: "f(xi)" },
        { key: "dfx", label: "f'(xi)" },
        { key: "ddfx", label: "f''(xi)" },
        { key: "xr", label: "xr" },
        { key: "error", label: "T" },
        { key: "status", label: "Estado" },
    ],
};

const form = document.querySelector("#calculation-form");
const methodSelect = document.querySelector("#method");
const methodDescription = document.querySelector("#method-description");
const methodInfo = document.querySelector("#method-info");
const functionField = document.querySelector(".function-field");
const functionInput = document.querySelector("#function");
const syntaxNote = document.querySelector("#syntax-note");
const dynamicFields = document.querySelector("#dynamic-fields");
const toleranceField = document.querySelector(".tolerance-field");
const toleranceInput = document.querySelector("#tolerance");
const iterationField = document.querySelector(".iteration-field");
const maximumIterationsInput = document.querySelector("#max_iterations");
const methodKind = document.querySelector("#method-kind");
const methodNoteLabel = document.querySelector("#method-note-label");
const methodNoteTitle = document.querySelector("#method-note-title");
const methodNoteIntro = document.querySelector("#method-note-intro");
const methodNoteFormula = document.querySelector("#method-note-formula");
const methodNoteDetail = document.querySelector("#method-note-detail");
const submitButton = document.querySelector("#submit-button");
const badge = document.querySelector("#result-badge");
const summary = document.querySelector("#result-summary");
const countLabel = document.querySelector("#steps-count");
const table = document.querySelector("#steps-table");
const singleStepsPanel = document.querySelector("#single-steps-panel");
const interpolationProcedurePanel = document.querySelector("#interpolation-procedure-panel");
const procedureTitle = document.querySelector("#procedure-title");
const procedureBlocks = document.querySelector("#procedure-blocks");
const multipleResultsPanel = document.querySelector("#multiple-results-panel");
const multipleTablesCount = document.querySelector("#multiple-tables-count");
const functionExpression = document.querySelector("#function-expression");
const derivativeExpression = document.querySelector("#derivative-expression");
const secondDerivativeExpression = document.querySelector("#second-derivative-expression");
const searchTableBody = document.querySelector("#search-table tbody");
const suggestionsCount = document.querySelector("#suggestions-count");
const rootsSummaryBody = document.querySelector("#roots-summary-table tbody");
const multipleTables = document.querySelector("#multiple-tables");
const chartPanel = document.querySelector("#multiple-roots-chart-panel");
const chartCanvas = document.querySelector("#multiple-roots-chart");
let chartInstance = null;
let calculationVersion = 0;

function isInterpolation(methodKey) {
    return Boolean(methods[methodKey] && methods[methodKey].interpolation);
}

function formatNumber(value) {
    if (value === null || value === undefined || value === "") {
        return "-";
    }

    const number = Number(value);
    if (!Number.isFinite(number)) {
        return String(value);
    }

    return number.toLocaleString("en-US", {
        maximumFractionDigits: 4,
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

function resetResultPanels(methodKey) {
    hideChart();
    badge.className = "status-badge neutral";
    badge.textContent = "Sin cálculo";
    summary.className = "empty-state";
    const emphasis = createElement("strong", "", "Calcular");
    summary.replaceChildren(
        document.createTextNode("Ingresa los datos y presiona "),
        emphasis,
        document.createTextNode(".")
    );
    renderSteps([], methodKey);
    renderProcedure({ procedure: [] }, methodKey);
    renderMultipleResults({
        function: "",
        derivative: "",
        second_derivative: "",
        search_table: [],
        suggested_roots: [],
        tables: [],
        final_roots: [],
    });
}

function renderFields(methodKey) {
    const selected = methods[methodKey] || methods.bisection;
    const interpolation = isInterpolation(methodKey);
    resetResultPanels(methodKey);
    dynamicFields.replaceChildren();
    dynamicFields.hidden = selected.fields.length === 0;
    dynamicFields.classList.toggle("single-field", selected.fields.length === 1);
    dynamicFields.classList.toggle("triple-field", selected.fields.length === 3);
    dynamicFields.classList.toggle("five-field", selected.fields.length === 5);
    methodInfo.classList.toggle("without-function", interpolation);
    functionField.hidden = interpolation;
    functionInput.disabled = interpolation;
    functionInput.required = !interpolation;
    syntaxNote.hidden = interpolation;
    toleranceField.hidden = interpolation;
    toleranceInput.disabled = interpolation;
    iterationField.hidden = interpolation;
    maximumIterationsInput.disabled = interpolation;
    submitButton.textContent = interpolation ? "Interpolar" : "Calcular raíz";

    const title = createElement("strong", "", selected.title);
    const copy = document.createTextNode(`${selected.description} Criterio: ${selected.formula}.`);
    methodDescription.replaceChildren(title, copy);
    methodKind.textContent = selected.kind;
    methodNoteLabel.textContent = selected.note.label;
    methodNoteTitle.textContent = selected.note.title;
    methodNoteIntro.textContent = selected.note.intro;
    methodNoteFormula.textContent = selected.note.formula;
    methodNoteDetail.textContent = selected.note.detail;

    selected.fields.forEach((field) => {
        const label = createElement("label", "field");
        const caption = createElement("span", "", field.label);
        const input = document.createElement("input");
        input.type = "number";
        input.step = "any";
        input.id = field.key;
        input.name = field.key;
        input.placeholder = field.placeholder;
        input.required = true;
        label.append(caption, input);
        dynamicFields.appendChild(label);
    });

    if (interpolation) {
        singleStepsPanel.hidden = true;
        multipleResultsPanel.hidden = true;
        interpolationProcedurePanel.hidden = false;
        renderProcedure({ procedure: [] }, methodKey);
    } else if (methodKey === "multiple_roots") {
        singleStepsPanel.hidden = true;
        interpolationProcedurePanel.hidden = true;
        multipleResultsPanel.hidden = false;
        renderMultipleResults({ search_table: [], suggested_roots: [], tables: [], final_roots: [] });
    } else {
        singleStepsPanel.hidden = false;
        interpolationProcedurePanel.hidden = true;
        multipleResultsPanel.hidden = true;
        renderSteps([], methodKey);
    }
}

function setBadge(success, methodKey) {
    badge.className = `status-badge ${success ? "success" : "error"}`;
    badge.textContent = isInterpolation(methodKey)
        ? (success ? "Calculado" : "Sin resultado")
        : (success ? "Convergió" : "Sin convergencia");
}

function renderSummary(result) {
    const interpolation = isInterpolation(result.method);
    const selected = methods[result.method] || {};
    setBadge(result.success, result.method);
    summary.className = "result-content";
    summary.replaceChildren();

    const rootBox = createElement("div", "root-display");
    const isMultipleRoots = (
        result.method === "multiple_roots" && Array.isArray(result.final_roots)
    );
    rootBox.append(
        createElement(
            "span",
            "",
            interpolation
                ? selected.resultLabel
                : (isMultipleRoots ? "Raíces finales" : "Raíz aproximada")
        ),
        createElement(
            "strong",
            "",
            interpolation
                ? formatNumber(result.result)
                : isMultipleRoots && result.final_roots.length
                ? result.final_roots.map((root) => formatNumber(root.xr)).join(", ")
                : formatNumber(result.root)
        )
    );

    const metrics = createElement("div", "metrics");
    if (interpolation) {
        metrics.classList.add("single-metric");
        const xMetric = createElement("div", "metric");
        xMetric.append(
            createElement("span", "", "x evaluado"),
            createElement("strong", "", formatNumber(result.x))
        );
        metrics.append(xMetric);
    } else {
        const iteration = createElement("div", "metric");
        iteration.append(
            createElement("span", "", isMultipleRoots ? "Tablas" : "Iteraciones"),
            createElement(
                "strong",
                "",
                formatNumber(isMultipleRoots ? result.tables.length : result.iterations)
            )
        );
        const tolerance = createElement("div", "metric");
        tolerance.append(
            createElement("span", "", "Tolerancia"),
            createElement("strong", "", formatNumber(result.tolerance))
        );
        metrics.append(iteration, tolerance);
    }

    const message = createElement(
        "p",
        `result-message ${result.success ? "" : "error"}`,
        result.message
    );
    summary.append(rootBox, metrics, message);
}

function renderSteps(steps, methodKey) {
    const head = table.querySelector("thead");
    const body = table.querySelector("tbody");
    const headerRow = document.createElement("tr");
    const columns = columnsByMethod[methodKey] || columnsByMethod.bisection;

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

function formatProcedureLine(line) {
    const values = line.values || {};
    return line.template.replace(/\{([a-z0-9_]+)\}/gi, (match, key) => (
        Object.hasOwn(values, key) ? formatNumber(values[key]) : match
    ));
}

function renderProcedure(result, methodKey) {
    const selected = methods[methodKey] || {};
    const blocks = Array.isArray(result.procedure) ? result.procedure : [];
    procedureTitle.textContent = selected.title || "Interpolación";
    procedureBlocks.replaceChildren();

    if (!blocks.length) {
        procedureBlocks.appendChild(
            createElement(
                "div",
                "empty-state procedure-empty",
                "Realiza una interpolación válida para ver el procedimiento matemático."
            )
        );
        return;
    }

    blocks.forEach((block) => {
        const card = createElement("article", "procedure-card");
        card.appendChild(createElement("h3", "", block.title));
        const lines = createElement("div", "procedure-lines");
        block.lines.forEach((line) => {
            lines.appendChild(
                createElement("code", "", formatProcedureLine(line))
            );
        });
        card.appendChild(lines);
        procedureBlocks.appendChild(card);
    });
}

function renderMultipleResults(result) {
    const tables = Array.isArray(result.tables) ? result.tables : [];
    const searchRows = Array.isArray(result.search_table) ? result.search_table : [];
    const finalRoots = Array.isArray(result.final_roots) ? result.final_roots : [];
    const suggestedRoots = Array.isArray(result.suggested_roots) ? result.suggested_roots : [];
    functionExpression.textContent = result.function || "-";
    derivativeExpression.textContent = result.derivative || "-";
    secondDerivativeExpression.textContent = result.second_derivative || "-";
    searchTableBody.replaceChildren();
    rootsSummaryBody.replaceChildren();
    multipleTables.replaceChildren();
    multipleTablesCount.textContent = `${tables.length} ${tables.length === 1 ? "tabla" : "tablas"}`;
    suggestionsCount.textContent = `${suggestedRoots.length} xi sugerido${suggestedRoots.length === 1 ? "" : "s"}`;

    if (!searchRows.length) {
        const row = createElement("tr", "placeholder-row");
        const cell = createElement("td", "", "Realiza un cálculo para ver la búsqueda automática.");
        cell.colSpan = 6;
        row.appendChild(cell);
        searchTableBody.appendChild(row);
    } else {
        searchRows.forEach((entry) => {
            const row = document.createElement("tr");
            [
                formatNumber(entry.x),
                formatNumber(entry.fx),
                entry.sign,
                entry.interval_or_exact || "-",
                formatNumber(entry.suggested_xi),
                entry.n === null ? "-" : String(entry.n),
            ].forEach((value) => row.appendChild(createElement("td", "", value)));
            searchTableBody.appendChild(row);
        });
    }

    if (!finalRoots.length) {
        const row = createElement("tr", "placeholder-row");
        const cell = createElement("td", "", "No hay resultados finales para mostrar.");
        cell.colSpan = 3;
        row.appendChild(cell);
        rootsSummaryBody.appendChild(row);
    } else {
        finalRoots.forEach((entry) => {
            const summaryRow = document.createElement("tr");
            [
                String(entry.table),
                formatNumber(entry.xr),
                formatNumber(entry.y),
            ].forEach((value) => summaryRow.appendChild(createElement("td", "", value)));
            rootsSummaryBody.appendChild(summaryRow);
        });
    }

    tables.forEach((entry) => {
        const panel = createElement("section", "steps-panel card generated-table-panel");
        const heading = createElement("div", "card-heading");
        const headingText = createElement("div");
        headingText.append(
            createElement("p", "overline", `Tabla ${entry.table_number}`),
            createElement("h2", "", `xi inicial: ${formatNumber(entry.initial_xi)}`)
        );
        heading.append(
            headingText,
            createElement(
                "span",
                `status-badge ${entry.success ? "success" : "error"}`,
                entry.success ? "Convergió" : "Sin convergencia"
            )
        );
        panel.appendChild(heading);

        const wrapper = createElement("div", "table-wrapper");
        const iterationTable = document.createElement("table");
        const head = document.createElement("thead");
        const headerRow = document.createElement("tr");
        columnsByMethod.multiple_roots.forEach((column) => {
            headerRow.appendChild(createElement("th", "", column.label));
        });
        head.appendChild(headerRow);
        const body = document.createElement("tbody");
        entry.iterations.forEach((step) => {
            const row = document.createElement("tr");
            columnsByMethod.multiple_roots.forEach((column) => {
                const value = ["iteration", "status"].includes(column.key)
                    ? String(step[column.key])
                    : formatNumber(step[column.key]);
                row.appendChild(createElement("td", "", value));
            });
            body.appendChild(row);
        });
        iterationTable.append(head, body);
        wrapper.appendChild(iterationTable);
        panel.appendChild(wrapper);
        multipleTables.appendChild(panel);
    });
}

function hideChart() {
    if (chartInstance) {
        chartInstance.destroy();
        chartInstance = null;
    }
    if (chartPanel) {
        chartPanel.hidden = true;
    }
}

function renderChart(result) {
    hideChart();

    if (
        result.method !== "multiple_roots"
        || !result.success
        || !Array.isArray(result.chart_points)
        || result.chart_points.length === 0
        || !Array.isArray(result.final_roots)
        || result.final_roots.length === 0
        || typeof Chart === "undefined"
    ) {
        return;
    }

    chartPanel.hidden = false;
    chartInstance = new Chart(chartCanvas, {
        type: "scatter",
        data: {
            datasets: [
                {
                    type: "line",
                    label: "f(x)",
                    data: result.chart_points,
                    parsing: false,
                    borderColor: "#d45d43",
                    backgroundColor: "rgba(212, 93, 67, 0.1)",
                    borderWidth: 2,
                    pointRadius: 0,
                    tension: 0.12,
                },
                {
                    type: "scatter",
                    label: "xr final",
                    data: result.final_roots.map((entry) => ({ x: entry.xr, y: entry.y })),
                    parsing: false,
                    backgroundColor: "#1c3154",
                    borderColor: "#fffdf9",
                    borderWidth: 2,
                    pointRadius: 6,
                },
            ],
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    labels: { color: "#596277", usePointStyle: true },
                },
                tooltip: {
                    callbacks: {
                        label: (context) => (
                            `${context.dataset.label}: `
                            + `(${formatNumber(context.parsed.x)}, ${formatNumber(context.parsed.y)})`
                        ),
                    },
                },
            },
            scales: {
                x: {
                    type: "linear",
                    title: { display: true, text: "x", color: "#596277" },
                    ticks: { color: "#596277", callback: (value) => formatNumber(value) },
                    grid: { color: "rgba(22, 35, 58, 0.08)" },
                },
                y: {
                    title: { display: true, text: "f(x)", color: "#596277" },
                    ticks: { color: "#596277", callback: (value) => formatNumber(value) },
                    grid: { color: "rgba(22, 35, 58, 0.08)" },
                },
            },
        },
    });
}

function payloadFromForm() {
    const selected = methods[methodSelect.value] || methods.bisection;
    const payload = {
        method: methodSelect.value,
    };

    if (!selected.interpolation) {
        payload.function = functionInput.value;
        payload.tolerance = toleranceInput.value;
        payload.max_iterations = maximumIterationsInput.value;
    }

    selected.fields.forEach((field) => {
        payload[field.key] = document.querySelector(`#${field.key}`).value;
    });

    return payload;
}

async function calculate(event) {
    event.preventDefault();
    const currentCalculation = ++calculationVersion;
    submitButton.disabled = true;
    submitButton.textContent = "Calculando...";

    try {
        const response = await fetch("/api/calculate", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payloadFromForm()),
        });
        const result = await response.json();
        if (currentCalculation !== calculationVersion) {
            return;
        }
        renderSummary(result);
        const displayMethod = result.method || methodSelect.value;
        if (isInterpolation(displayMethod)) {
            singleStepsPanel.hidden = true;
            multipleResultsPanel.hidden = true;
            interpolationProcedurePanel.hidden = false;
            renderProcedure(result, displayMethod);
        } else if (displayMethod === "multiple_roots") {
            singleStepsPanel.hidden = true;
            interpolationProcedurePanel.hidden = true;
            multipleResultsPanel.hidden = false;
            renderMultipleResults(result);
        } else {
            singleStepsPanel.hidden = false;
            interpolationProcedurePanel.hidden = true;
            multipleResultsPanel.hidden = true;
            renderSteps(result.steps || [], displayMethod);
        }
        renderChart(result);
    } catch (error) {
        if (currentCalculation !== calculationVersion) {
            return;
        }
        const result = {
            success: false,
            method: methodSelect.value,
            root: null,
            result: null,
            x: null,
            final_roots: [],
            tables: [],
            tolerance: document.querySelector("#tolerance").value,
            iterations: 0,
            message: "No se pudo comunicar con el servidor.",
            steps: [],
            procedure: [],
        };
        renderSummary(result);
        if (isInterpolation(methodSelect.value)) {
            singleStepsPanel.hidden = true;
            multipleResultsPanel.hidden = true;
            interpolationProcedurePanel.hidden = false;
            renderProcedure(result, methodSelect.value);
        } else if (methodSelect.value === "multiple_roots") {
            interpolationProcedurePanel.hidden = true;
            renderMultipleResults({
                search_table: [],
                suggested_roots: [],
                tables: [],
                final_roots: [],
            });
        } else {
            interpolationProcedurePanel.hidden = true;
            renderSteps([], methodSelect.value);
        }
        hideChart();
    } finally {
        if (currentCalculation === calculationVersion) {
            submitButton.disabled = false;
            submitButton.textContent = isInterpolation(methodSelect.value)
                ? "Interpolar"
                : "Calcular raíz";
        }
    }
}

if (form) {
    const requestedMethod = new URLSearchParams(window.location.search).get("method");
    if (requestedMethod && methods[requestedMethod]) {
        methodSelect.value = requestedMethod;
    }

    renderFields(methodSelect.value);
    methodSelect.addEventListener("change", () => {
        calculationVersion += 1;
        submitButton.disabled = false;
        functionInput.value = "";
        toleranceInput.value = "0.001";
        maximumIterationsInput.value = "100";
        renderFields(methodSelect.value);
    });
    form.addEventListener("submit", calculate);
}

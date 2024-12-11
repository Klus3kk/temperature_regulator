document.addEventListener("DOMContentLoaded", () => {
    const sliders = {
        Q_max: document.getElementById("Q_max"),
        C_v: document.getElementById("C_v"),
        T_amb: document.getElementById("T_amb"),
        k_g: document.getElementById("k_g"),
        k_w: document.getElementById("k_w"),
        u: document.getElementById("control-signal"),
    };

    const values = {
        Q_max: document.getElementById("Q_max_value"),
        C_v: document.getElementById("C_v_value"),
        T_amb: document.getElementById("T_amb_value"),
        T_amb_celsius: document.getElementById("T_amb_celsius"),
        k_g: document.getElementById("k_g_value"),
        k_w: document.getElementById("k_w_value"),
        u: document.getElementById("control_value"),
    };

    const updateParamsButton = document.getElementById("update-params");
    const updateMessage = document.getElementById("update-message");
    const plotDiv = document.getElementById("plot");

    Object.keys(sliders).forEach((key) => {
        sliders[key].addEventListener("input", () => {
            values[key].textContent = sliders[key].value;
            if (key === "T_amb") {
                values.T_amb_celsius.textContent = (sliders.T_amb.value - 273).toFixed(1);
            }
        });
    });

    const updateGraph = () => {
        fetch("/plot")
            .then((response) => response.json())
            .then((data) => {
                data.layout.plot_bgcolor = "#222222";
                data.layout.paper_bgcolor = "#121212";
                data.layout.font = { color: "#e0e0e0" };
                data.layout.xaxis = { gridcolor: "#444" };
                data.layout.yaxis = { gridcolor: "#444" };
                Plotly.react(plotDiv, data.data, data.layout);
            })
            .catch((err) => console.error("Error updating graph:", err));
    };

    updateParamsButton.addEventListener("click", () => {
        const params = {};
        Object.keys(sliders).forEach((key) => {
            params[key] = parseFloat(sliders[key].value);
        });

        fetch("/update-params", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(params),
        })
            .then(() => {
                updateMessage.style.display = "block";
                setTimeout(() => {
                    updateMessage.style.display = "none";
                }, 2000);
                updateGraph();
            })
            .catch((err) => console.error("Error updating parameters:", err));
    });

    sliders.u.addEventListener("input", () => {
        const u = parseFloat(sliders.u.value);
        fetch("/update", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ u }),
        }).then(() => updateGraph());
    });

    // Handle window resizing for responsive plot
    window.addEventListener("resize", () => {
        Plotly.Plots.resize(plotDiv);
    });

    updateGraph();
});

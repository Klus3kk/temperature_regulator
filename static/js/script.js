document.addEventListener("DOMContentLoaded", () => {
    // Sliders and values
    const sliders = {
        T_target: document.getElementById("T_target"),
        T_amb: document.getElementById("T_amb"),
    };

    const values = {
        T_target: document.getElementById("T_target_value"),
        T_amb: document.getElementById("T_amb_value"),
    };

    // Elements for update and graphs
    const updateParamsButton = document.getElementById("update-params");
    const updateMessage = document.getElementById("update-message");
    const tempPlotDiv = document.getElementById("temp-plot");
    const heatPlotDiv = document.getElementById("heat-plot");
    const heatBalancePlotDiv = document.getElementById("heat-balance-plot");

    // Update displayed values dynamically
    Object.keys(sliders).forEach((key) => {
        sliders[key].addEventListener("input", () => {
            values[key].textContent = sliders[key].value;
        });
    });

    // Fetch and update all graphs
    const updateGraphs = () => {
        const layoutConfig = {
            plot_bgcolor: "#222222",
            paper_bgcolor: "#121212",
            font: { color: "#e0e0e0" },
            xaxis: { gridcolor: "#444" },
            yaxis: { gridcolor: "#444" },
        };

        // Fetch temperature graph data
        fetch("/temp-plot")
            .then((response) => response.json())
            .then((data) => {
                data.layout = { ...data.layout, ...layoutConfig };
                Plotly.react(tempPlotDiv, data.data, data.layout);
            })
            .catch((err) => console.error("Error updating temperature graph:", err));

        // Fetch heat loss graph data
        fetch("/heat-plot")
            .then((response) => response.json())
            .then((data) => {
                data.layout = { ...data.layout, ...layoutConfig };
                Plotly.react(heatPlotDiv, data.data, data.layout);
            })
            .catch((err) => console.error("Error updating heat loss graph:", err));

        // Fetch heat balance graph data
        fetch("/heat-balance-plot")
            .then((response) => response.json())
            .then((data) => {
                data.layout = { ...data.layout, ...layoutConfig };
                Plotly.react(heatBalancePlotDiv, data.data, data.layout);
            })
            .catch((err) => console.error("Error updating heat balance graph:", err));
    };

    // Update parameters when the button is clicked
    updateParamsButton.addEventListener("click", () => {
        const params = {};

        // Gather slider values (convert to Kelvin)
        Object.keys(sliders).forEach((key) => {
            const valueCelsius = parseFloat(sliders[key].value);
            const valueKelvin = valueCelsius + 273;
            params[key] = valueKelvin;
        });

        fetch("/update-params", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(params),
        })
            .then(() => {
                // Show confirmation message
                updateMessage.style.display = "block";
                setTimeout(() => {
                    updateMessage.style.display = "none";
                }, 2000);

                // Update graphs
                updateGraphs();
            })
            .catch((err) => console.error("Error updating parameters:", err));
    });

    // Adjust plot sizes when resizing the window
    window.addEventListener("resize", () => {
        Plotly.Plots.resize(tempPlotDiv);
        Plotly.Plots.resize(heatPlotDiv);
        Plotly.Plots.resize(heatBalancePlotDiv);
    });

    // Initial graph rendering
    updateGraphs();
});

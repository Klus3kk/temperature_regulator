document.addEventListener("DOMContentLoaded", () => {
    // Sliders and values
    const sliders = {
        T_target: document.getElementById("T_target"),
        T_amb: document.getElementById("T_amb"),
        T_p: document.getElementById("T_p"),
        T_i: document.getElementById("T_i"),
        K_p: document.getElementById("K_p"),
    };

    const values = {
        T_target: document.getElementById("T_target_value"),
        T_amb: document.getElementById("T_amb_value"),
        T_p: document.getElementById("T_p_value"),
        T_i: document.getElementById("T_i_value"),
        K_p: document.getElementById("K_p_value"),
    };

    // Elements for update and graphs
    const updateParamsButton = document.getElementById("update-params");
    const updateMessage = document.getElementById("update-message");
    const tempPlotDiv = document.getElementById("temp-plot");
    const heatPlotDiv = document.getElementById("heat-plot");
    const signalPlotDiv = document.getElementById("signal-plot");
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
                // I know the code looked better, but then axis titles weren't visible. Please don't change it
                data.layout.xaxis = {
                    ...data.layout.xaxis,
                    gridcolor: layoutConfig.xaxis.gridcolor,
                };
                data.layout.yaxis = {
                    ...data.layout.yaxis,
                    gridcolor: layoutConfig.yaxis.gridcolor,
                };
                data.layout.plot_bgcolor = layoutConfig.plot_bgcolor;
                data.layout.paper_bgcolor = layoutConfig.paper_bgcolor;
                data.layout.font = layoutConfig.font;
                Plotly.react(tempPlotDiv, data.data, data.layout);
            })
            .catch((err) => console.error("Error updating temperature graph:", err));

        // Fetch heat loss graph data
        // fetch("/heat-plot")
        //     .then((response) => response.json())
        //     .then((data) => {
        //         data.layout = { ...data.layout, ...layoutConfig };
        //         Plotly.react(heatPlotDiv, data.data, data.layout);
        //     })
        //     .catch((err) => console.error("Error updating heat loss graph:", err));

        //commented this plot, because it's no longer needed i guess

        // Fetch heat balance graph data
        fetch("/heat-balance-plot")
            .then((response) => response.json())
            .then((data) => {
                 data.layout.xaxis = {
                    ...data.layout.xaxis,
                    gridcolor: layoutConfig.xaxis.gridcolor,
                };
                data.layout.yaxis = {
                    ...data.layout.yaxis,
                    gridcolor: layoutConfig.yaxis.gridcolor,
                };
                data.layout.plot_bgcolor = layoutConfig.plot_bgcolor;
                data.layout.paper_bgcolor = layoutConfig.paper_bgcolor;
                data.layout.font = layoutConfig.font;
                Plotly.react(heatBalancePlotDiv, data.data, data.layout);
            })
            .catch((err) => console.error("Error updating heat balance graph:", err));

            fetch("/signal-plot")
            .then((response) => response.json())
            .then((data) => {
                 data.layout.xaxis = {
                    ...data.layout.xaxis,
                    gridcolor: layoutConfig.xaxis.gridcolor,
                };
                data.layout.yaxis = {
                    ...data.layout.yaxis,
                    gridcolor: layoutConfig.yaxis.gridcolor,
                };
                data.layout.plot_bgcolor = layoutConfig.plot_bgcolor;
                data.layout.paper_bgcolor = layoutConfig.paper_bgcolor;
                data.layout.font = layoutConfig.font;
                Plotly.react(signalPlotDiv, data.data, data.layout);
            })
            .catch((err) => console.error("Error updating singal graph:", err));

    };

    // Update parameters when the button is clicked
    updateParamsButton.addEventListener("click", () => {
        const params = {};

        // Gather slider values (convert to Kelvin)
        Object.keys(sliders).forEach((key) => {
            if (key === "T_target" || key === "T_amb") {
                const valueCelsius = parseFloat(sliders[key].value);
                const valueKelvin = valueCelsius + 273;
                params[key] = valueKelvin;
            } else {
                params[key] = parseFloat(sliders[key].value);
            }
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

                updateSimulation();
            })
            .catch((err) => console.error("Error updating parameters:", err));
    });

    const updateSimulation = () => {
        fetch("/update", {
            method: "POST",
            headers: { "Content-type": "application/json" },
        }).then(() => updateGraphs());
    };

    // Adjust plot sizes when resizing the window
    window.addEventListener("resize", () => {
        Plotly.Plots.resize(tempPlotDiv);
        Plotly.Plots.resize(heatPlotDiv);
        Plotly.Plots.resize(heatBalancePlotDiv);
        Plotly.Plots.resize(signalPlotDiv);
    });

    // Initial graph rendering
    updateSimulation()
});

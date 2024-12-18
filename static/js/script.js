document.addEventListener("DOMContentLoaded", () => {
    const sliders = {
        T_target: document.getElementById("T_target"),
        T_amb: document.getElementById("T_amb"),
    };

    const values = {
        T_target: document.getElementById("T_target_value"),
        T_amb: document.getElementById("T_amb_value"),
    };

    const updateParamsButton = document.getElementById("update-params");
    const updateMessage = document.getElementById("update-message");
    const tempPlotDiv = document.getElementById("temp-plot");
    const heatPlotDiv = document.getElementById("heat-plot");

    Object.keys(sliders).forEach((key) => {
        sliders[key].addEventListener("input", () => {
            values[key].textContent = sliders[key].value;
        });
    });

    const updateGraphs = () => {
        const plotBgColor = "#222222";
        const paperBgColor =  "#121212";
        const fontColor = "#e0e0e0";
        const xGridColor = "#444";
        const yGridColor = "#444";
        fetch("/temp-plot")
            .then((response) => response.json())
            .then((data) => {
                data.layout.plot_bgcolor = plotBgColor;
                data.layout.paper_bgcolor = paperBgColor;
                data.layout.font = { color: fontColor };
                data.layout.xaxis = {
                    ...data.layout.xaxis,
                    gridcolor: xGridColor,
                };
                data.layout.yaxis = {
                    ...data.layout.yaxis,
                    gridcolor: yGridColor,
                };
                Plotly.react(tempPlotDiv, data.data, data.layout);
            })
            .catch((err) => console.error("Error updating temperature graph:", err));
        fetch("/heat-plot")
            .then((response) => response.json())
            .then((data) => {
                data.layout.plot_bgcolor = plotBgColor;
                data.layout.paper_bgcolor = paperBgColor;
                data.layout.font = { color: fontColor };
                data.layout.xaxis = {
                    ...data.layout.xaxis,
                    gridcolor: xGridColor,
                };
                data.layout.yaxis = {
                    ...data.layout.yaxis,
                    gridcolor: yGridColor,
                };
                Plotly.react(heatPlotDiv, data.data, data.layout);
            })
            .catch((err) => console.error("Error updating temperature graph:", err));
    };

    updateParamsButton.addEventListener("click", () => {
        const params = {};
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
                updateMessage.style.display = "block";
                setTimeout(() => {
                    updateMessage.style.display = "none";
                }, 2000);
                updateGraphs();
            })
            .catch((err) => console.error("Error updating parameters:", err));
    });

    // Handle window resizing for responsive plot
    window.addEventListener("resize", () => {
        Plotly.Plots.resize(tempPlotDiv);
    });

    updateGraphs();
});

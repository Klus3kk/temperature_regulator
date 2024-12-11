document.addEventListener('DOMContentLoaded', () => {
    const signalSlider = document.getElementById('signal_slider');
    const volumeSlider = document.getElementById('volume_slider');
    const kGSlider = document.getElementById('k_g_slider');
    const kWSlider = document.getElementById('k_w_slider');
    const tAmbSlider = document.getElementById('t_amb_slider');
    const updateButton = document.getElementById('update_button');

    const signalValue = document.getElementById('signal_value');
    const volumeValue = document.getElementById('volume_value');
    const kGValue = document.getElementById('k_g_value');
    const kWValue = document.getElementById('k_w_value');
    const tAmbValue = document.getElementById('t_amb_value');
    const tAmbCelsius = document.getElementById('t_amb_celsius');

    // Update values dynamically as sliders/pickers are adjusted
    signalSlider.addEventListener('input', () => {
        signalValue.textContent = signalSlider.value;
    });

    volumeSlider.addEventListener('input', () => {
        volumeValue.textContent = volumeSlider.value;
    });

    kGSlider.addEventListener('input', () => {
        kGValue.textContent = kGSlider.value;
    });

    kWSlider.addEventListener('input', () => {
        kWValue.textContent = kWSlider.value;
    });

    tAmbSlider.addEventListener('input', () => {
        const kelvin = tAmbSlider.value;
        const celsius = (kelvin - 273).toFixed(1);
        tAmbValue.textContent = kelvin;
        tAmbCelsius.textContent = celsius;
    });

    // Send data to backend when the button is clicked
    updateButton.addEventListener('click', () => {
        const params = {
            u: parseFloat(signalSlider.value),
            V: parseFloat(volumeSlider.value),
            k_g: parseFloat(kGSlider.value),
            k_w: parseFloat(kWSlider.value),
            T_amb: parseInt(tAmbSlider.value)
        };

        fetch('/update-params', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(params)
        });
        updatePlot()
    });

    // Fetch and update plot dynamically
    const updatePlot = () => {
        fetch('/plot')
            .then(response => response.json())
            .then(data => {
                const plotDiv = document.getElementById('plot');
                Plotly.react(plotDiv, data.data, data.layout);
            });
    };
});

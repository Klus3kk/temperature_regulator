from flask import Flask, request, jsonify, render_template
from modules.simulation import (
    calculate_heat_loss_glass,
    calculate_heat_loss_walls,
    calculate_total_heat_loss,
    calculate_next_temperature
)

app = Flask(__name__)

simulation_state = {
    "temperature": 293,
    "time": 0,
    "control_signal": 0,
    "history": {"time": [0], "temperature": [293]}
}

simulation_params = {
    "Q_max": 1000,
    "C_v": 900,
    "d": 1.1225,
    "V": 0.5,
    "T_p": 1,
    "k_g": 0.8,
    "k_w": 0.5,
    "T_amb": 293
}


@app.route('/')
def index():
    """Serves the main HTML page"""
    return render_template('index.html')


@app.route('/update', methods=['POST'])
def update_simulation():
    global simulation_state, simulation_params
    data = request.json
    simulation_state["control_signal"] = data.get("u", 0)

    # Calculate total heat loss
    Q_loss = calculate_total_heat_loss(
        simulation_state["temperature"],
        simulation_params["T_amb"],
        simulation_params["k_g"],
        simulation_params["k_w"]
    )

    # Update temperature
    new_temperature = calculate_next_temperature(
        simulation_state["temperature"],
        simulation_state["control_signal"],
        simulation_params["Q_max"],
        Q_loss,
        simulation_params["C_v"],
        simulation_params["d"],
        simulation_params["V"],
        simulation_params["T_p"]
    )

    simulation_state["temperature"] = new_temperature
    simulation_state["time"] += simulation_params["T_p"]

    # Append new data to history
    simulation_state["history"]["time"].append(simulation_state["time"])
    simulation_state["history"]["temperature"].append(new_temperature)

    return jsonify({
        "time": simulation_state["time"],
        "temperature": simulation_state["temperature"]
    })


@app.route('/plot', methods=['GET'])
def get_plot_data():
    return jsonify({
        "data": [
            {
                "x": simulation_state["history"]["time"],
                "y": simulation_state["history"]["temperature"],
                "type": "scatter",
                "mode": "lines",
                "name": "Temperature"
            }
        ],
        "layout": {
            "title": "Temperature Over Time",
            "xaxis": {"title": "Time (s)"},
            "yaxis": {"title": "Temperature (K)"}
        }
    })


@app.route('/update-params', methods=['POST'])
def update_params():
    global simulation_params
    data = request.json
    for key, value in data.items():
        if key in simulation_params:
            simulation_params[key] = value
    return jsonify({
        "message": "Parameters updated successfully",
        "parameters": simulation_params
    })


if __name__ == '__main__':
    app.run(debug=True)

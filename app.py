from flask import Flask, request, jsonify, render_template
from modules.simulation import (
    calculate_heat_loss_glass,
    calculate_heat_loss_walls,
    calculate_total_heat_loss,
    calculate_next_temperature,
    calculate_control_signal
)

app = Flask(__name__)

simulation_state = {
    "temperature": 293,
    "time": 0,
    "heat_loss": 0,
    "control_signal": 0,
    "supplied_heat": 0,
    "temp_history": {"time": [0], "temperature": [293]},
    "heat_history": {"time": [0], "heat_loss": [0]},
    "heat_balance_history": {"time": [0], "supplied": [0], "lost": [0]},
}

simulation_params = {
    "S_time": 1000,  # Simulation duration
    "Q_max": 750,  # Maximum heater power in W
    "C_v": 1200,  # Specific heat capacity of air (J/(kg*K))
    "d": 1.2,  # Air density in kg/m^3
    "V": 0.5,  # Volume in m^3
    "T_p": 0.5,  # Time step in seconds /// okres próbkowania
    "k_g": 5,  # Heat transfer coefficient for glass
    "k_w": 2,  # Heat transfer coefficient for walls
    "T_amb": 293,  # Ambient temperature (K)
    "T_target": 303,  # Target temperature (K)
    "K_p": 0.0002,  # PID controller proportional gain
    "T_i": 0.9,  # PID controller integral gain /// czas zdwojenia
    "T_d": 0.05, # PID controller derivative gain /// czas wyprzedzenia
    "error_sum": 0,  # Integral error for PID controller
    "last_error": 0, # Derivative error for PID controller
}

@app.route("/")
def index():
    """Serves the main HTML page"""
    return render_template("index.html")


@app.route("/update", methods=["POST"])
def update_simulation():
    global simulation_state, simulation_params

   # Reset history
    simulation_state["temp_history"] = {"time": [0], "temperature": [simulation_params["T_amb"]]}
    simulation_state["heat_history"] = {"time": [0], "heat_loss": [0]}
    simulation_state["heat_balance_history"] = {"time": [0], "supplied": [0], "lost": [0]}
    simulation_state["time"] = 0
    simulation_state["temperature"] = simulation_params["T_amb"]

    # Debug print for incoming updates
    print("Before Update:", simulation_state)
    for _ in range(int(simulation_params["S_time"] / simulation_params["T_p"]) + 1):
        control_signal, simulation_params["error_sum"], simulation_params["last_error"] = calculate_control_signal(
            simulation_params["T_target"],
            simulation_state["temperature"],
            simulation_params["K_p"],
            simulation_params["T_i"],
            simulation_params["T_d"],
            simulation_params["T_p"],
            simulation_params["error_sum"],
            simulation_params["last_error"]
        )
        simulation_state["control_signal"] = control_signal

        Q_loss = calculate_total_heat_loss(
            simulation_state["temperature"],
            simulation_params["T_amb"],
            simulation_params["k_g"],
            simulation_params["k_w"],
        )
        Q_supplied = control_signal * simulation_params["Q_max"]
        new_temperature = calculate_next_temperature(
            simulation_state["temperature"],
            control_signal,
            simulation_params["Q_max"],
            Q_loss,
            simulation_params["C_v"],
            simulation_params["d"],
            simulation_params["V"],
            simulation_params["T_p"],
        )

        simulation_state["heat_loss"] = Q_loss
        simulation_state["supplied_heat"] = Q_supplied
        simulation_state["temperature"] = new_temperature
        simulation_state["time"] += simulation_params["T_p"]

        # Append to history
        simulation_state["temp_history"]["time"].append(simulation_state["time"])
        simulation_state["temp_history"]["temperature"].append(new_temperature)
        simulation_state["heat_history"]["time"].append(simulation_state["time"])
        simulation_state["heat_history"]["heat_loss"].append(Q_loss)
        simulation_state["heat_balance_history"]["time"].append(simulation_state["time"])
        simulation_state["heat_balance_history"]["supplied"].append(Q_supplied)
        simulation_state["heat_balance_history"]["lost"].append(Q_loss)

    # Debug print after update
    print("After Update:", simulation_state)

    return jsonify({
        "time": simulation_state["time"],
        "temperature": simulation_state["temperature"],
        "heat_loss": simulation_state["heat_loss"],
        "control_signal": simulation_state["control_signal"],
    })



@app.route("/temp-plot", methods=["GET"])
def get_temp_plot_data():
    temp_in_celsius = [
        temp - 273.15 for temp in simulation_state["temp_history"]["temperature"]
    ]
    return jsonify({
        "data": [
            {
                "x": simulation_state["temp_history"]["time"],
                "y": temp_in_celsius,
                "type": "scatter",
                "mode": "lines",
                "name": "Temperature",
            }
        ],
        "layout": {
            "title": "Temperature Over Time",
            "xaxis": {"title": "Time (s)"},
            "yaxis": {"title": "Temperature (°C)"},
        },
    })


@app.route("/heat-balance-plot", methods=["GET"])
def get_heat_balance_plot_data():
    return jsonify({
        "data": [
            {
                "x": simulation_state["heat_balance_history"]["time"],
                "y": simulation_state["heat_balance_history"]["supplied"],
                "type": "scatter",
                "mode": "lines",
                "name": "Heat Supplied",
            },
            {
                "x": simulation_state["heat_balance_history"]["time"],
                "y": simulation_state["heat_balance_history"]["lost"],
                "type": "scatter",
                "mode": "lines",
                "name": "Heat Lost",
            },
        ],
        "layout": {
            "title": "Heat Supplied vs Heat Lost Over Time",
            "xaxis": {"title": "Time (s)"},
            "yaxis": {"title": "Heat (J)"},
        },
    })


@app.route("/update-params", methods=["POST"])
def update_params():
    global simulation_params
    data = request.json
    for key, value in data.items():
        if key in simulation_params:
            simulation_params[key] = value
    return jsonify({
        "message": "Parameters updated successfully",
        "parameters": simulation_params,
    })


if __name__ == "__main__":
    app.run(debug=True)

"""Flask App (/update for taking data u(t), updating the simulation, /plot for data to plot)"""
from flask import Flask, request, jsonify 
from modules.simulation import (
    calculate_heat_loss_glass,
    calculate_heat_loss_walls,
    calculate_total_heat_loss,
    calculate_next_temperature
)

app = Flask(__name__)

# Global variables for simulation state
simulation_state = {
    "temperature": 293, # Initial temperature (K)
    "time": 0,          # Simulation time
    "control_signal": 0 # Control signal u
}

# Simulation parameters
simulation_params = {
    "Q_max": 1000,  # Maximum heater power (W)
    "C_v": 900,     # Specific heat capacity (J/(K·kg))
    "d": 1.1225,    # Air density (kg/m^3)
    "V": 0.5,       # Volume of the incubator (m^3)
    "T_p": 1,       # Time step (s)
    "k_g": 0.8,     # Heat transfer coefficient for glass (W/K)
    "k_w": 0.5,     # Heat transfer coefficient for walls (W/K)
    "T_amb": 293    # Ambient temperature (K)
}

@app.route('/update', methods=['POST'])
def update_simulation():
    """Updates the simulation state based on the provided control signal"""
    global simulation_state, simulation_params

    # Getting control signal from frontend
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
    simulation_state["temperature"] = calculate_next_temperature(
        simulation_state["temperature"],
        simulation_state["control_signal"],
        simulation_params["Q_max"],
        Q_loss,
        simulation_params["C_v"],
        simulation_params["d"],
        simulation_params["V"],
        simulation_params["T_p"]
    )

    # Increment time
    simulation_state["time"] += simulation_params["T_p"]

    return jsonify({
        "time": simulation_state["time"],
        "temperature": simulation_state["temperature"]
    })
    
@app.route('/plot', methods=['GET'])
def get_plot_data():
    """Provide data for Plotly visualization"""
    plot_data = {
        "data": [
            {
                "x": [0,1,2],
                "y": [293, 295, 297],
                "type": "line",
                "name": "Temperature"
            }
        ],
        "layout": {
            "title": "Temperature Over Time",
            "xaxis": {"title": "Time (s)"},
            "yaxis": {"title": "Temperature (K)"}
        }
    }
    return jsonify(plot_data)
"""Temperature Simulation Logic"""
def calculate_heat_loss_glass(T, T_amb, k_g):
    """
    Calculate heat loss through the glass.
    Parameters:
    * T (float): Current temperature measured in K,
    * T_amb (float): Ambient temperature measured in K,
    * k_g (float): Heat transfer coefficient for glass in W/K.
    Returns:
    * float : Heat loss through the glass in W.
    """
    return k_g * (T - T_amb)

def calculate_heat_loss_walls(T, T_amb, k_w):
    """
    Calculate heat loss through the walls.
    Parameters:
    * T (float): Current temperature measured in K,
    * T_amb (float): Ambient temperature measured in K,
    * k_w (float): Heat transfer coefficient for walls in W/K.
    Returns:
    * float : Heat loss through the walls in W.
    """
    return k_w * (T - T_amb)

def calculate_total_heat_loss(T, T_amb, k_g, k_w):
    """
    Calculate the total heat loss of the incubator.
    Parameters:
    * T (float): Current temperature measured in K,
    * T_amb (float): Ambient temperature measured in K,
    * k_w (float): Heat transfer coefficient for walls in W/K.
    * k_g (float): Heat transfer coefficient for glass in W/K.
    Returns:
    * float : Heat loss through the walls in W.
    """
    Q_loss_glass = calculate_heat_loss_glass(T, T_amb, k_g)
    Q_loss_walls = calculate_heat_loss_walls(T, T_amb, k_w)
    return Q_loss_glass + Q_loss_walls

def calculate_next_temperature(T, u, Q_max, Q_loss, C_v, d, V, T_p):
    """
    Calculate the next temperature based on the given parameters.
    Parameters:
    * T (float): Current temperature measured in K,
    * u (float): Control signal (0 <= u <= 1),
    * Q_max (float): Maximum heater power in W,
    * Q_loss (float): Total heat loss in W,
    * C_v (float): Specific heat capacity of air (J/(kg*K)),
    * d (float): Air density in kg/m^3,
    * V (float): Volume of the incubator in m^3,
    * T_p (float): Time step in seconds.
    Returns:
    * float: Next temperature in K.
    """
    delta_T = ((u / 2 * Q_max - Q_loss) * T_p) / (C_v * d * V * 3)
    return T + delta_T


def calculate_control_signal(T_target, T_current, K_p, T_i, T_d, T_p, error_sum, last_error):
    """
    Calculates the control signal using a PID controller.

    Parameters:
        T_target (float): Desired target temperature.
        T_current (float): Current temperature.
        K_p (float): Proportional gain.
        T_i (float): Integral time constant.
        T_p (float): Sampling time.
        error_sum (float): Accumulated error for the integral component.
        last_error (float): Error from the previous step for derivative calculation.

    Returns:
        float: The calculated control signal clamped to [0, 1].
        float: Updated error_sum for the next iteration.
        float: Current error to be used as last_error in the next iteration.
    """
    error = T_target - T_current

    # Proportional term
    P = K_p * error

    # Integral term
    if T_i != 0:
        error_sum += error * T_p # Acumulate error over time
        # Anti wind-up
        max_integral = 1 / (K_p * (1 / T_i))
        error_sum = max(-max_integral, min(error_sum, max_integral))
        I = K_p * (1 / T_i) * error_sum
    else:
        I = 0

    D = K_p * T_d * ((error - last_error) / T_p)

    # Compute total control signal
    control_signal = P + I + D

    # Clamp control signal to [0, 1]
    control_signal = max(0, min(control_signal, 1))

    return control_signal, error_sum, error


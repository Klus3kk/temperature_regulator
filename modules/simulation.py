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
    delta_T = ((u * Q_max - Q_loss) * T_p) / (C_v * d * V)
    return T + delta_T


def calculate_control_signal(T_target, T_current, K_p, K_i, error_sum, T_p):
    """
    Calculates the control signal using a PI controller.
    """
    error = T_target - T_current
    error_sum += error * T_p  # Integral component
    control_signal = K_p * error + K_i * error_sum
    return max(0, min(control_signal, 1)), error_sum  # Signal clamped to [0, 1]

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
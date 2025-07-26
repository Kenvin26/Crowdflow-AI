import numpy as np

def compute_cpi(density_map, movement_map, emotion_map=None):
    # density_map: 2D array (people/m^2)
    # movement_map: 2D array (speed or flow)
    # emotion_map: 2D array (stress/panic, optional)
    # CPI = weighted sum (example)
    cpi = 0.5 * density_map + 0.3 * movement_map
    if emotion_map is not None:
        cpi += 0.2 * emotion_map
    return cpi

# Example usage:
# cpi = compute_cpi(density, movement, emotion) 
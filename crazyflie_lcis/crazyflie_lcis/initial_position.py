import numpy as np

def generate_random_positions(n, p_min, p_max, min_distance):
    """
    Generate random initial positions for robots with constraints.
    
    Args:
        n (int): Number of robots.
        p_min (list): Minimum bounds for the positions [x_min, y_min, z_min].
        p_max (list): Maximum bounds for the positions [x_max, y_max, z_max].
        min_distance (float): Minimum distance required between any two robots.

    Returns:
        numpy.ndarray: Array of shape (n, 3) with the generated positions.
    """
    positions = []
    
    while len(positions) < n:
        # Generate a random position
        pos = np.random.uniform(low=p_min, high=p_max)
        
        # Check if the position is valid (maintains the minimum distance)
        if all(np.linalg.norm(pos - existing_pos) >= min_distance for existing_pos in positions):
            positions.append(pos)
    
    return np.array(positions)
import numpy as np

def recommend_exits(density_map, predicted_paths, exits):
    # density_map: 2D array
    # predicted_paths: list of arrays (per-person or per-group)
    # exits: list of (x, y) exit locations
    # Placeholder: recommend exit with lowest predicted density along path
    scores = []
    for exit in exits:
        score = 0
        for path in predicted_paths:
            # Simple: sum density along path to exit
            for pt in path:
                x, y = int(pt[0]), int(pt[1])
                score += density_map[y, x]
        scores.append(score)
    best_exit = exits[np.argmin(scores)]
    return best_exit

# Example usage:
# best = recommend_exits(density, paths, exits) 
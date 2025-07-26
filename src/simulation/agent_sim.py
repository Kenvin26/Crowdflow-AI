import numpy as np

class Agent:
    def __init__(self, pos, goal):
        self.pos = np.array(pos)
        self.goal = np.array(goal)

    def step(self):
        # Move towards goal (placeholder)
        direction = self.goal - self.pos
        if np.linalg.norm(direction) > 0:
            self.pos += direction / np.linalg.norm(direction)

class CrowdSimulator:
    def __init__(self, agents):
        self.agents = agents

    def step(self):
        for agent in self.agents:
            agent.step()

# Example usage:
# agents = [Agent((0,0), (10,10)) for _ in range(100)]
# sim = CrowdSimulator(agents)
# for _ in range(100): sim.step() 
"""
Basic Mesa Grid Model for Learning

A minimal 20x20 grid environment with:
- Random fruits (30-50)
- Random obstacles (10-15)
- Random walking agents (10)
"""

import random
from mesa import Model
from mesa.discrete_space import OrthogonalMooreGrid

from .agents import RandomWalkAgent, Fruit, Obstacle


class BasicGridModel(Model):
    """
    A basic Mesa model with a 20x20 grid containing fruits, obstacles, and randomly moving agents.
    """

    def __init__(self, width=20, height=20, num_agents=10, num_fruits=40, num_obstacles=12, seed=None):
        super().__init__(seed=seed)

        # Grid setup - bounded (no wrap-around)
        self.grid = OrthogonalMooreGrid((width, height), torus=False, random=self.random)

        # Model parameters
        self.num_agents = num_agents
        self.num_fruits = num_fruits
        self.num_obstacles = num_obstacles

        # Step counter
        self.step_count = 0

        # Create and place obstacles first
        self._create_obstacles()

        # Create and place fruits
        self._create_fruits()

        # Create and place agents
        self._create_agents()

        self.running = True

    def _create_obstacles(self):
        """Create and randomly place obstacles on the grid."""
        # Select random empty cells for obstacles
        empty_cells = list(self.grid.empties)
        selected_cells = self.random.sample(empty_cells, min(self.num_obstacles, len(empty_cells)))

        for i, cell in enumerate(selected_cells):
            obstacle = Obstacle(self, cell)

    def _create_fruits(self):
        """Create and randomly place fruits on the grid."""
        # Select random empty cells for fruits (avoiding obstacles)
        empty_cells = [cell for cell in self.grid.empties if not any(isinstance(agent, Obstacle) for agent in cell.agents)]
        selected_cells = self.random.sample(empty_cells, min(self.num_fruits, len(empty_cells)))

        for i, cell in enumerate(selected_cells):
            fruit = Fruit(self, cell)

    def _create_agents(self):
        """Create and randomly place agents on the grid."""
        # Select random empty cells for agents (avoiding obstacles and fruits)
        empty_cells = [cell for cell in self.grid.empties if not any(isinstance(agent, (Obstacle, Fruit)) for agent in cell.agents)]
        selected_cells = self.random.sample(empty_cells, min(self.num_agents, len(empty_cells)))

        for i, cell in enumerate(selected_cells):
            agent = RandomWalkAgent(self, cell)

    def step(self):
        """Advance the model by one step."""
        self.step_count += 1
        # Only step the RandomWalkAgents (fruits and obstacles are static)
        random_walk_agents = [agent for agent in self.agents if isinstance(agent, RandomWalkAgent)]
        self.random.shuffle(random_walk_agents)
        for agent in random_walk_agents:
            agent.step()
"""
Basic Mesa Grid Model for Learning

A minimal 20x20 grid environment with:
- Random fruits (30-50)
- Random obstacles (10-15)
- Random walking agents (10)
"""

import random
from mesa import Model
from mesa.space import MultiGrid
from mesa.time import RandomActivation

from .agents import RandomWalkAgent, Fruit, Obstacle


class BasicGridModel(Model):
    """
    A basic Mesa model with a 20x20 grid containing fruits, obstacles, and randomly moving agents.
    """

    def __init__(self, width=20, height=20, num_agents=10, num_fruits=40, num_obstacles=12):
        super().__init__()

        # Grid setup - bounded (no wrap-around)
        self.grid = MultiGrid(width, height, torus=False)

        # Scheduler for agents
        self.schedule = RandomActivation(self)

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

    def _create_obstacles(self):
        """Create and randomly place obstacles on the grid."""
        obstacle_id = 1000  # Start with high ID to avoid conflicts
        for i in range(self.num_obstacles):
            obstacle = Obstacle(obstacle_id + i, self)

            # Find empty cell for obstacle
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)

            # Keep trying until we find an empty cell
            while not self.grid.is_cell_empty((x, y)):
                x = self.random.randrange(self.grid.width)
                y = self.random.randrange(self.grid.height)

            self.grid.place_agent(obstacle, (x, y))

    def _create_fruits(self):
        """Create and randomly place fruits on the grid."""
        fruit_id = 2000  # Start with high ID to avoid conflicts
        for i in range(self.num_fruits):
            fruit = Fruit(fruit_id + i, self)

            # Find empty cell for fruit
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)

            # Keep trying until we find an empty cell
            while not self.grid.is_cell_empty((x, y)):
                x = self.random.randrange(self.grid.width)
                y = self.random.randrange(self.grid.height)

            self.grid.place_agent(fruit, (x, y))

    def _create_agents(self):
        """Create and randomly place agents on the grid."""
        for i in range(self.num_agents):
            agent = RandomWalkAgent(i, self)

            # Find empty cell for agent
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)

            # Keep trying until we find an empty cell
            while not self.grid.is_cell_empty((x, y)):
                x = self.random.randrange(self.grid.width)
                y = self.random.randrange(self.grid.height)

            self.grid.place_agent(agent, (x, y))
            self.schedule.add(agent)

    def step(self):
        """Advance the model by one step."""
        self.step_count += 1
        self.schedule.step()
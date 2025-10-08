"""
Basic agents for the Mesa learning environment.
"""

from mesa.discrete_space import CellAgent


class RandomWalkAgent(CellAgent):
    """
    An agent that moves randomly around the grid.
    - Yellow colored circle in visualization
    - Uses Moore neighborhood (8-directional movement)
    - Cannot move into cells with obstacles or other agents
    - Ignores fruits at this moment
    """

    def __init__(self, model, cell):
        super().__init__(model)
        self.cell = cell

    def step(self):
        """Move randomly to a neighboring cell if possible."""
        # Get all neighboring cells
        neighbors = list(self.cell.neighborhood)

        # Filter out cells with obstacles or other RandomWalkAgents
        valid_cells = []
        for neighbor_cell in neighbors:
            # Check if cell has obstacles or other RandomWalkAgents
            has_obstacle_or_agent = any(
                isinstance(agent, (Obstacle, RandomWalkAgent)) for agent in neighbor_cell.agents
            )
            if not has_obstacle_or_agent:
                valid_cells.append(neighbor_cell)

        # Move to a random valid cell if any exist
        if valid_cells:
            new_cell = self.random.choice(valid_cells)
            self.cell = new_cell


class Fruit(CellAgent):
    """
    A fruit object on the grid.
    - Red colored circle in visualization
    - Static (doesn't move)
    - Agents ignore these for now
    """

    def __init__(self, model, cell):
        super().__init__(model)
        self.cell = cell

    def step(self):
        """Fruits don't do anything - they're static."""
        pass


class Obstacle(CellAgent):
    """
    An obstacle on the grid.
    - Black colored square in visualization
    - Static (doesn't move)
    - Blocks agent movement
    """

    def __init__(self, model, cell):
        super().__init__(model)
        self.cell = cell

    def step(self):
        """Obstacles don't do anything - they're static."""
        pass
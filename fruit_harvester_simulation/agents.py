"""
Basic agents for the Mesa learning environment.
"""

import random
from mesa import Agent


class RandomWalkAgent(Agent):
    """
    An agent that moves randomly around the grid.
    - Yellow colored circle in visualization
    - Uses Moore neighborhood (8-directional movement)
    - Cannot move into cells with obstacles or other agents
    - Ignores fruits (this is just for learning Mesa)
    """

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        """Move randomly to a neighboring cell if possible."""
        # Get all possible moves (Moore neighborhood)
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,  # Include diagonals
            include_center=False  # Don't stay in place
        )

        # Filter out cells with obstacles or other agents
        valid_steps = []
        for cell in possible_steps:
            cell_contents = self.model.grid.get_cell_list_contents([cell])
            # Check if cell has obstacles or other RandomWalkAgents
            has_obstacle_or_agent = any(
                isinstance(agent, (Obstacle, RandomWalkAgent)) for agent in cell_contents
            )
            if not has_obstacle_or_agent:
                valid_steps.append(cell)

        # Move to a random valid cell if any exist
        if valid_steps:
            new_position = self.model.random.choice(valid_steps)
            self.model.grid.move_agent(self, new_position)


class Fruit(Agent):
    """
    A fruit object on the grid.
    - Red colored circle in visualization
    - Static (doesn't move)
    - Agents ignore these for now
    """

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        """Fruits don't do anything - they're static."""
        pass


class Obstacle(Agent):
    """
    An obstacle on the grid.
    - Black colored square in visualization
    - Static (doesn't move)
    - Blocks agent movement
    """

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        """Obstacles don't do anything - they're static."""
        pass
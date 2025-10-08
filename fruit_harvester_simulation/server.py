"""
Mesa visualization server for the basic grid environment using SolaraViz.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mesa.visualization import SolaraViz, SpaceRenderer
from mesa.visualization.components import AgentPortrayalStyle

from fruit_harvester_simulation.model import BasicGridModel
from fruit_harvester_simulation.agents import RandomWalkAgent, Fruit, Obstacle


def agent_portrayal(agent):
    """Define how agents are displayed in the visualization."""
    if isinstance(agent, RandomWalkAgent):
        # Yellow circles for agents
        return AgentPortrayalStyle(
            color="yellow",
            marker="o",  # circle
            size=80
        )

    elif isinstance(agent, Fruit):
        # Red circles for fruits
        return AgentPortrayalStyle(
            color="red",
            marker="o",  # circle
            size=60
        )

    elif isinstance(agent, Obstacle):
        # Black squares for obstacles
        return AgentPortrayalStyle(
            color="black",
            marker="s",  # square
            size=100
        )

    # Default style
    return AgentPortrayalStyle()


# Model parameters for the web interface
model_params = {}


# Create the model instance
model = BasicGridModel()

# Create the space renderer
renderer = SpaceRenderer(model, backend="altair")
renderer.draw_structure(grid_color="lightgray", grid_opacity=0.5)
renderer.draw_agents(agent_portrayal=agent_portrayal)

# Create the SolaraViz page with minimal controls
page = SolaraViz(
    model,
    renderer,
    components=[],
    model_params=model_params,
    name="Basic Mesa Grid Environment",
    play_interval=1000,  # Set default play interval
)

# This is needed for Solara to find the page
page  # noqa
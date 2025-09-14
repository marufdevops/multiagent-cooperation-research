"""
Mesa visualization server for the basic grid learning environment using SolaraViz.
"""

from mesa.visualization import SolaraViz, SpaceRenderer
from mesa.visualization.components import AgentPortrayalStyle

from .model import BasicGridModel
from .agents import RandomWalkAgent, Fruit, Obstacle


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
model_params = {
    "seed": {
        "type": "InputText",
        "value": 42,
        "label": "Random Seed",
    },
    "width": {
        "type": "SliderInt",
        "value": 20,
        "label": "Grid Width:",
        "min": 10,
        "max": 30,
        "step": 1,
    },
    "height": {
        "type": "SliderInt",
        "value": 20,
        "label": "Grid Height:",
        "min": 10,
        "max": 30,
        "step": 1,
    },
    "num_agents": {
        "type": "SliderInt",
        "value": 10,
        "label": "Number of Agents:",
        "min": 1,
        "max": 20,
        "step": 1,
    },
    "num_fruits": {
        "type": "SliderInt",
        "value": 40,
        "label": "Number of Fruits:",
        "min": 10,
        "max": 100,
        "step": 5,
    },
    "num_obstacles": {
        "type": "SliderInt",
        "value": 12,
        "label": "Number of Obstacles:",
        "min": 0,
        "max": 50,
        "step": 1,
    },
}


# Create the model instance
model = BasicGridModel()

# Create the space renderer
renderer = SpaceRenderer(model, backend="altair")
renderer.draw_structure(grid_color="lightgray", grid_opacity=0.5)
renderer.draw_agents(agent_portrayal=agent_portrayal)

# Create the SolaraViz page
page = SolaraViz(
    model,
    renderer,
    components=[],  # No additional components for now
    model_params=model_params,
    name="Basic Mesa Grid Learning Environment",
)

# This is needed for Solara to find the page
page  # noqa
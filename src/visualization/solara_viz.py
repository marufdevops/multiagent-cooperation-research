"""
Solara Visualization for Fruit Harvesting Simulation.

This module provides an interactive web-based visualization of the multi-agent
fruit harvesting simulation using Mesa's Solara visualization framework.

The visualization allows:
- Real-time observation of agent behavior
- Interactive parameter adjustment (grid size, agents, communication range)
- Visual verification of simulation correctness

USAGE:
    /opt/anaconda3/bin/python scripts/run_visualization.py
    # or
    solara run src/visualization/solara_viz.py --port 8765

COLOR SCHEME:
- Red circles: Harvester agents (size grows with harvest count)
- Green squares: Available fruit
- Gray squares: Harvested fruit
"""
import sys
import os

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from mesa.visualization import SolaraViz
from models.harvest_model import HarvestModel
from agents.harvester_agent import HarvesterAgent
from agents.fruit import Fruit


def agent_portrayal(agent):
    """
    Define visual representation for each agent type.

    This function is called by Mesa's visualization system to determine
    how each agent should be rendered on the grid.

    Args:
        agent: A Mesa Agent instance (HarvesterAgent or Fruit)

    Returns:
        dict: Visualization properties with keys:
            - color: Hex color string
            - size: Marker size in pixels
            - marker: Shape ('o' for circle, 's' for square)
    """
    if isinstance(agent, HarvesterAgent):
        # Agents: Red circles, size increases with harvest success
        return {
            "color": "#f41414",  # Red
            "size": 30 + agent.harvested * 2,  # Grows with success
            "marker": "o",  # Circle
            "zorder": 1,  # Ensure agents are above fruit
        }
    elif isinstance(agent, Fruit):
        if agent.available:
            # Available fruit: Green squares
            return {
                "color": "#2ca02c",  # Green
                "size": 15,
                "marker": "s",  # Square
                "zorder": 0,  # Ensure fruit is below agents
            }
        else:
            # Harvested fruit: Small gray squares
            return {
                "color": "#d3d3d3",  # Light gray
                "size": 8,
                "marker": "s",
                "zorder": 0,  # Ensure fruit is below agents
            }
    return {}


def make_model(params):
    """
    Factory function to create HarvestModel from UI parameters.

    This function handles the parameter format conversion needed by Solara.
    Parameters can come in two formats:
    - Raw values (from programmatic use)
    - Dict with "value" key (from Solara UI widgets)

    Args:
        params: Dictionary of model parameters

    Returns:
        HarvestModel: Configured model instance
    """
    def get_param_value(param_dict, key, default):
        """Extract value from raw or widget parameter format."""
        if key not in param_dict:
            return default
        param = param_dict[key]
        if isinstance(param, dict) and "value" in param:
            return param["value"]
        return param

    return HarvestModel(
        width=get_param_value(params, "width", 20),
        height=get_param_value(params, "height", 20),
        num_agents=get_param_value(params, "num_agents", 5),
        fruit_density=get_param_value(params, "fruit_density", 0.2),
        comm_range=get_param_value(params, "comm_range", 2),
    )


# These parameters define the interactive controls shown in the web interface.
# Users can adjust these while the simulation is running to explore behavior.

model_params = {
    "width": {
        "type": "SliderInt",
        "value": 20,
        "label": "Grid Width",
        "min": 10,
        "max": 50,
        "step": 5,
    },
    "height": {
        "type": "SliderInt",
        "value": 20,
        "label": "Grid Height",
        "min": 10,
        "max": 50,
        "step": 5,
    },
    "num_agents": {
        "type": "SliderInt",
        "value": 5,
        "label": "Number of Agents",
        "min": 1,
        "max": 30,
        "step": 1,
    },
    "fruit_density": {
        "type": "SliderFloat",
        "value": 0.2,
        "label": "Fruit Density",
        "min": 0.05,
        "max": 0.5,
        "step": 0.05,
    },
    "comm_range": {
        "type": "SliderInt",
        "value": 2,
        "label": "Communication Range",
        "min": 0,  # 0 = no communication (control condition)
        "max": 8,  # Maximum experimental range
        "step": 1,
    },
}

# Create the Mesa Solara visualization with default parameters.
# The visualization will be updated when parameters change in the UI.

# Initial model instance with default parameters
model = HarvestModel()

# Configure the spatial renderer
from mesa.visualization import SpaceRenderer
renderer = SpaceRenderer(model, backend="matplotlib")
renderer.draw_agents(agent_portrayal)

# Create the Solara visualization page
page = SolaraViz(
    model,
    renderer,
    model_params=model_params,
    name="Fruit Harvesting Simulation",
)


if __name__ == "__main__":
    # This is executed when running with: python src/visualization/solara_viz.py
    # Use `solara run` instead for proper server execution
    page


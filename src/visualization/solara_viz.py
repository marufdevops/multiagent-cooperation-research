"""
Solara visualization components for harvest model.
Uses Mesa 3.0 SolaraViz with make_space_component and make_plot_component.
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
    Define agent portrayal as dictionary with color/size/marker keys.
    Mesa 3.0 convention for Solara visualization.
    """
    if isinstance(agent, HarvesterAgent):
        # Agents: blue circles, size based on harvest count
        return {
            "color": "#1f77b4",
            "size": 20 + agent.harvested * 2,
            "marker": "o",
        }
    elif isinstance(agent, Fruit):
        # Fruit: green if available, gray if harvested
        if agent.available:
            return {
                "color": "#2ca02c",
                "size": 15,
                "marker": "s",
            }
        else:
            return {
                "color": "#d3d3d3",
                "size": 8,
                "marker": "s",
            }
    return {}


def make_model(params):
    """Create model instance from parameters."""
    return HarvestModel(
        width=params.get("width", 20),
        height=params.get("height", 20),
        num_agents=params.get("num_agents", 5),
        fruit_density=params.get("fruit_density", 0.2),
        comm_range=params.get("comm_range", 2),
        dynamics=params.get("dynamics", "Static"),
        regen_prob=params.get("regen_prob", 0.0),
        seed=params.get("seed", None),
    )


# Model parameters for Solara UI
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
        "min": 0,
        "max": 8,
        "step": 1,
    },
    "dynamics": {
        "type": "Select",
        "value": "Static",
        "values": ["Static", "Replenishing"],
        "label": "Resource Dynamics",
    },
    "regen_prob": {
        "type": "SliderFloat",
        "value": 0.0,
        "label": "Regeneration Probability",
        "min": 0.0,
        "max": 0.2,
        "step": 0.01,
    },
    "seed": {
        "type": "InputText",
        "value": None,
        "label": "Random Seed (optional)",
    },
}


# Create visualization page
# Note: In Mesa 3.3.0, SolaraViz expects agent_portrayal directly, not wrapped in make_space_component
page = SolaraViz(
    HarvestModel,
    model_params=model_params,
    agent_portrayal=agent_portrayal,
    name="Fruit Harvesting Simulation",
)


if __name__ == "__main__":
    # Run Solara server
    page


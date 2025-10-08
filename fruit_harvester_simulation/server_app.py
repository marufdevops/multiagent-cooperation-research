"""
Mesa 3.0 compatible visualization server for the fruit harvesting simulation.

This module provides a web-based visualization using SolaraViz that shows:
- Agent positions and strategies (cooperative vs competitive)
- Real-time metrics (fruits harvested, messages sent)
- Interactive parameter controls

It is robust to the initial render (before the model instance is created) by
wrapping components so they don't crash when SolaraViz passes the model class.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mesa.visualization import SolaraViz, make_space_component, make_plot_component
from fruit_harvester_simulation.model import OrchardModel
import solara


def agent_portrayal(agent):
    """Define how agents appear in the visualization."""
    portrayal = {"size": 20, "marker": "o"}
    if hasattr(agent, "strategy"):
        portrayal["color"] = "cyan" if agent.strategy == "cooperative" else "magenta"
    else:
        portrayal["color"] = "gray"
    return portrayal


# Model parameters for the UI (dict style supported by Mesa 3.x)
model_params = {
    "width": {"type": "SliderInt", "value": 25, "label": "Grid Width", "min": 15, "max": 40, "step": 1},
    "height": {"type": "SliderInt", "value": 25, "label": "Grid Height", "min": 15, "max": 40, "step": 1},
    "num_agents": {"type": "SliderInt", "value": 15, "label": "Number of Agents", "min": 5, "max": 30, "step": 1},
    "communication_range": {"type": "SliderFloat", "value": 3.0, "label": "Communication Range", "min": 1.0, "max": 8.0, "step": 0.5},
    "cooperative_share": {"type": "SliderFloat", "value": 0.8, "label": "Cooperative Share", "min": 0.0, "max": 1.0, "step": 0.1},
    "initial_fruit_density": {"type": "SliderFloat", "value": 0.3, "label": "Initial Fruit Density", "min": 0.1, "max": 0.6, "step": 0.05},
    "regeneration_prob": {"type": "SliderFloat", "value": 0.1, "label": "Fruit Regeneration Probability", "min": 0.01, "max": 0.3, "step": 0.01},
}


def show_stats(model):
    """Display current simulation statistics, robust before model instantiation."""
    if isinstance(model, type):
        return solara.Text("Configure parameters and press Play \u25B6 to start the model.")
    if not hasattr(model, "agents") or not model.agents:
        return solara.Text("Initializing simulation...")

    total_fruits = sum(getattr(a, "fruits_collected", 0) for a in model.agents)
    total_messages = getattr(model, "total_messages_sent", 0)
    steps = getattr(model, "steps", 0)

    coop_agents = sum(1 for a in model.agents if getattr(a, "strategy", "") == "cooperative")
    comp_agents = len(model.agents) - coop_agents

    return solara.Markdown(
        f"""
**Step:** {steps} | **Total Fruits:** {total_fruits} | **Messages:** {total_messages}

**Agents:** {coop_agents} Cooperative, {comp_agents} Competitive
"""
    )


# Wrap components to avoid errors before model instance exists
_space_component_inner = make_space_component(agent_portrayal)


def space_component_safe(model):
    if isinstance(model, type):
        return solara.Text("Configure parameters and press Play \u25B6")
    return _space_component_inner(model)


_harvest_plot_inner, _ = make_plot_component("Total_Fruits_Harvested")
_messages_plot_inner, _ = make_plot_component("Total_Messages_Sent")


def harvest_plot_safe(model):
    if isinstance(model, type):
        return solara.Text("")
    return _harvest_plot_inner(model)


def messages_plot_safe(model):
    if isinstance(model, type):
        return solara.Text("")
    return _messages_plot_inner(model)


# Create the SolaraViz page (Mesa 3.0 style)
page = SolaraViz(
    OrchardModel,
    components=[
        space_component_safe,
        harvest_plot_safe,
        messages_plot_safe,
        show_stats,
    ],
    model_params=model_params,
    name="Multi-Agent Fruit Harvesting Simulation",
    play_interval=800,
)


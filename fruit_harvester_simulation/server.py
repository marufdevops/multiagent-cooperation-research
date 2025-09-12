"""
Mesa visualization server for the basic grid learning environment.
"""

from mesa.visualization.modules import CanvasGrid, TextElement
from mesa.visualization.ModularVisualization import ModularServer

from .model import BasicGridModel
from .agents import RandomWalkAgent, Fruit, Obstacle


def agent_portrayal(agent):
    """Define how agents are displayed in the visualization."""
    portrayal = {}

    if isinstance(agent, RandomWalkAgent):
        # Yellow circles for agents
        portrayal["Shape"] = "circle"
        portrayal["Color"] = "yellow"
        portrayal["Filled"] = "true"
        portrayal["Layer"] = 2
        portrayal["r"] = 0.8

    elif isinstance(agent, Fruit):
        # Red circles for fruits
        portrayal["Shape"] = "circle"
        portrayal["Color"] = "red"
        portrayal["Filled"] = "true"
        portrayal["Layer"] = 1
        portrayal["r"] = 0.6

    elif isinstance(agent, Obstacle):
        # Black squares for obstacles
        portrayal["Shape"] = "rect"
        portrayal["Color"] = "black"
        portrayal["Filled"] = "true"
        portrayal["Layer"] = 0
        portrayal["w"] = 1
        portrayal["h"] = 1

    return portrayal


class StepCountElement(TextElement):
    """Display the current step count."""

    def render(self, model):
        return f"Step: {model.step_count}"


def launch_server():
    """Launch the Mesa visualization server."""
    # Create the grid visualization
    grid = CanvasGrid(agent_portrayal, 20, 20, 500, 500)

    # Create the step counter
    step_counter = StepCountElement()

    # Create the server
    server = ModularServer(
        BasicGridModel,
        [grid, step_counter],
        "Basic Mesa Grid Learning Environment",
        {
            "width": 20,
            "height": 20,
            "num_agents": 10,
            "num_fruits": 40,
            "num_obstacles": 12
        }
    )

    server.port = 8521
    return server


if __name__ == "__main__":
    server = launch_server()
    server.launch()
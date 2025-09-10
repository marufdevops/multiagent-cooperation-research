from __future__ import annotations
from typing import Dict, Any

from mesa.visualization.modules import CanvasGrid, TextElement
from mesa.visualization.ModularVisualization import ModularServer

from .environment import OrchardModel
from .agents import HarvesterAgent, CellPatch


def _fruit_to_color(amount: int, max_amount: int) -> str:
    """Map fruit amount to a light-to-deep orange color."""
    if max_amount <= 0:
        return "#FFFFFF"
    frac = max(0.0, min(1.0, amount / float(max_amount)))
    # Base (no fruit) is near-white; more fruit -> deeper orange
    r = 255
    g = int(235 - 150 * frac)
    b = int(200 - 180 * frac)
    return f"#{r:02X}{g:02X}{b:02X}"


def portrayal(agent) -> Dict[str, Any]:
    # Background cell patch
    if isinstance(agent, CellPatch):
        x, y = agent.pos
        model: OrchardModel = agent.model  # type: ignore
        amount = model.get_fruit_at((x, y))
        color = _fruit_to_color(amount, model.max_fruit_per_cell)
        return {
            "Shape": "rect",
            "w": 1,
            "h": 1,
            "Filled": "true",
            "Color": color,
            "Layer": 0,
        }

    # Harvester agent
    if isinstance(agent, HarvesterAgent):
        color = "#00CED1" if agent.strategy == "cooperative" else "#FF00FF"
        return {
            "Shape": "circle",
            "r": 0.5,
            "Filled": "true",
            "Color": color,
            "Layer": 1,
            "stroke_color": "#000000",
            "text": str(agent.unique_id),
            "text_color": "#000000",
        }

    # Fallback: do not draw
    return {}


class InfoElement(TextElement):
    def render(self, model: OrchardModel) -> str:  # type: ignore[override]
        total_collected = sum(
            a.fruit_collected for a in model.schedule.agents if isinstance(a, HarvesterAgent)
        )
        return f"Step: {int(model.schedule.time)} | Agents: {len(model.schedule.agents)} | Total Collected: {total_collected}"


def launch(width=20, height=20, num_agents=20, comm_range=4):
    grid = CanvasGrid(
        portrayal, width, height,
        25 * width, 25 * height
    )
    info = InfoElement()

    server = ModularServer(
        OrchardModel,
        [grid, info],
        "Fruit Harvesting (Mesa UI)",
        {
            "width": width,
            "height": height,
            "num_agents": num_agents,
            "comm_range": comm_range,
            "cooperative_share": 1.0,
            "fruit_spawn_prob": 0.08,
            "regen_prob": 0.02,
            "max_fruit_per_cell": 3,
            "default_ttl": 0,
        },
    )
    server.port = 8521
    server.launch()


if __name__ == "__main__":
    launch()


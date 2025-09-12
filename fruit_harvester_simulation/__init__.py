"""
Basic Mesa Grid Environment for Learning

A minimal Mesa simulation to understand the framework's capabilities.
Features:
- 20x20 bounded grid
- Random fruits (red circles)
- Random obstacles (black squares)
- Agents with random movement (yellow circles)
"""

from .model import BasicGridModel
from .agents import RandomWalkAgent, Fruit, Obstacle

__all__ = ["BasicGridModel", "RandomWalkAgent", "Fruit", "Obstacle"]
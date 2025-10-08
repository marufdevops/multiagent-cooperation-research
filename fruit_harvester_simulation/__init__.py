"""
Multi-Agent Fruit Harvesting Simulation

Mesa 3.0 compatible implementation for studying communication range effects
on cooperation in multi-agent fruit harvesting environments.

Features:
- HarvesterAgent with cooperative/competitive strategies
- Range-bounded communication system
- OrchardModel with fruit dynamics
- Data collection for research analysis
"""

from .model import OrchardModel
from .agents import HarvesterAgent

__all__ = ["OrchardModel", "HarvesterAgent"]
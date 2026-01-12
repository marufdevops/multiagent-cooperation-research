"""
Fruit Resource Agent for Multi-Agent Harvesting Simulation.

This module implements the Fruit class, representing harvestable resources
in a multi-agent foraging simulation investigating communication range effects
on collective harvesting efficiency (Research Question 1).
"""
from mesa import Agent


class Fruit(Agent):
    """
    Static fruit resource that can be harvested exactly once.
    """

    def __init__(self, model):
        """
        Initialize fruit resource in available (unharvested) state.
        """
        super().__init__(model)
        self.is_fruit = True  # Type identifier for efficient cell content filtering
        self.available = True  # Harvest state: True = can be collected
        self.times_harvested = 0  # Verification counter (should never exceed 1)

    def harvest(self):
        """
        Harvest this fruit, making it permanently unavailable.
        """
        if self.available:
            self.available = False
            self.times_harvested += 1

    def step(self):
        """
        Execute one simulation step for this fruit (no-op for static resources).
        """
        pass
"""
Fruit resource for harvesting simulation (Static dynamics only).
"""
from mesa import Agent


class Fruit(Agent):
    """
    Static fruit resource that can be harvested once.

    For RQ1, we use Static dynamics only (no regeneration).
    Once harvested, fruit remains unavailable for the rest of the simulation.
    """

    def __init__(self, model):
        """
        Initialize fruit resource.

        Args:
            model: The model instance
        """
        super().__init__(model=model)
        self.is_fruit = True
        self.available = True
        self.times_harvested = 0

    def harvest(self):
        """
        Harvest this fruit (one-time only for Static dynamics).
        Once harvested, fruit becomes unavailable permanently.
        """
        if self.available:
            self.available = False
            self.times_harvested += 1

    def step(self):
        """
        Fruit step method (no-op for Static dynamics).
        Included for Mesa compatibility but does nothing.
        """
        pass


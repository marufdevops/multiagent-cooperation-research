"""
Fruit resource for harvesting simulation.
"""
from mesa import Agent


class Fruit(Agent):
    """Fruit resource that can be harvested and optionally regenerate."""
    
    def __init__(self, model, regenerates=False, regen_prob=0.0):
        """
        Initialize fruit resource.
        
        Args:
            model: The model instance
            regenerates: Whether fruit can regenerate after harvest
            regen_prob: Probability of regeneration per step (if regenerates=True)
        """
        super().__init__(model)
        self.is_fruit = True
        self.available = True
        self.regenerates = regenerates
        self.regen_prob = regen_prob
        self.times_harvested = 0
        
    def harvest(self):
        """Harvest this fruit."""
        if self.available:
            self.available = False
            self.times_harvested += 1
            
    def step(self):
        """Regenerate fruit if applicable."""
        if self.regenerates and not self.available:
            if self.model.random.random() < self.regen_prob:
                self.available = True


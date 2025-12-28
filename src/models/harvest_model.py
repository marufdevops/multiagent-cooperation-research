"""
Fruit Harvesting Model for RQ1: Communication Range Effects

Implements Static resource dynamics (no regeneration).
Tracks metrics: yield, messages, remaining fruit, coverage.
"""
import random
from mesa import Model
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector

import sys
sys.path.append('..')
from agents.harvester_agent import HarvesterAgent
from agents.fruit import Fruit


class HarvestModel(Model):
    """
    Fruit harvesting model with communication for RQ1.

    This model implements Static resource dynamics only (no regeneration).
    Agents move, harvest fruit, and communicate within a configurable range {comm_range = 2, 4, 6, 8}.

    Parameters:
        width: Grid width
        height: Grid height
        num_agents: Number of harvester agents
        fruit_density: Fraction of cells with fruit (0.0-1.0)
        comm_range: Communication range in cells (Chebyshev distance)
        seed: Random seed for reproducibility
    """
    # Class variable for Solara visualization
    steps = 0

    def __init__(
        self,
        width=20,
        height=20,
        num_agents=5,
        fruit_density=0.2,
        comm_range=2,
        seed=None
    ):
        super().__init__(seed=seed)

        # Parameters
        self.width = width
        self.height = height
        self.num_agents = num_agents
        self.fruit_density = fruit_density
        self.comm_range = comm_range
        
        # Grid
        self.grid = MultiGrid(width, height, torus=False)
        
        # Track fruits separately for efficient lookup
        self.fruits = []
        
        # Initialize fruits
        self._place_fruits()
        
        # Initialize agents
        self._place_agents()
        
        # Tracking variables for metrics
        self.cumulative_messages = 0
        self.steps = 0  # Track current step for visualization

        # Data collection with basic metrics
        self.datacollector = DataCollector(
            model_reporters={
                'total_yield': self._get_total_yield,
                'messages_this_step': self._get_messages_this_step,
                'cumulative_messages': lambda m: m.cumulative_messages,
                'remaining_fruit': self._get_remaining_fruit,
                'coverage': self._get_coverage,
            }
        )

        # Collect initial state
        self.datacollector.collect(self)
        
    def _place_fruits(self):
        """Place fruits on grid according to density (Static dynamics only)."""
        num_fruits = int(self.width * self.height * self.fruit_density)

        # Get all possible positions
        all_positions = [(x, y) for x in range(self.width) for y in range(self.height)]
        fruit_positions = random.sample(all_positions, num_fruits)

        # Create static fruits (no regeneration)
        for pos in fruit_positions:
            fruit = Fruit(self)
            self.grid.place_agent(fruit, pos)
            self.fruits.append(fruit)

    def _place_agents(self):
        """Place harvester agents on grid."""
        for _ in range(self.num_agents):
            agent = HarvesterAgent(self)
            
            # Find empty position
            x = random.randrange(self.width)
            y = random.randrange(self.height)
            
            self.grid.place_agent(agent, (x, y))
    
    def step(self):
        """Execute one step of the model using Mesa 3.0"""
        # Reset per-step message counters
        for agent in self.agents:
            if isinstance(agent, HarvesterAgent):
                agent.messages_sent = 0

        self.agents.shuffle_do('step')

        # Update cumulative message count
        self.cumulative_messages += self._get_messages_this_step()

        # Increment step counter
        self.steps += 1

        # Collect data
        self.datacollector.collect(self)
    
    def run_model(self, steps=100):
        """Run model for specified number of steps."""
        for _ in range(steps):
            self.step()

    # Metric calculation methods
    def _get_total_yield(self):
        """Get total harvested fruit across all agents."""
        return sum(a.harvested for a in self.agents if isinstance(a, HarvesterAgent))

    def _get_messages_this_step(self):
        """Get messages sent this step."""
        return sum(a.messages_sent for a in self.agents if isinstance(a, HarvesterAgent))

    def _get_remaining_fruit(self):
        """Get count of available fruit."""
        return sum(1 for f in self.fruits if f.available)

    def _get_coverage(self):
        """Get total unique cells visited by all agents."""
        all_visited = set()
        for agent in self.agents:
            if isinstance(agent, HarvesterAgent):
                all_visited.update(agent.visited_cells)
        return len(all_visited)


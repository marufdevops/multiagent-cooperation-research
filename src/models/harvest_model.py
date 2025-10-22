"""
Fruit Harvesting Model - Full version (Weeks 3-4).
Mesa 3.0 conventions: model.agents.shuffle_do('step'), no unique_id in constructors.
Includes comprehensive metrics collection and network analysis.
"""
import random
import numpy as np
from mesa import Model
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector

import sys
sys.path.append('..')
from agents.harvester_agent import HarvesterAgent
from agents.fruit import Fruit


class HarvestModel(Model):
    """
    Minimal sandbox model for fruit harvesting with communication.

    Parameters:
        width: Grid width
        height: Grid height
        num_agents: Number of harvester agents
        fruit_density: Fraction of cells with fruit (0.0-1.0)
        comm_range: Communication range in cells (Chebyshev distance)
        dynamics: 'Static' or 'Replenishing'
        regen_prob: Regeneration probability per step (for Replenishing)
        seed: Random seed for reproducibility
    """

    # Class variable for Solara visualization
    steps = 0

    def __init__(
        self,
        *,
        width=20,
        height=20,
        num_agents=5,
        fruit_density=0.2,
        comm_range=2,
        dynamics='Static',
        regen_prob=0.0,
        seed=None
    ):
        super().__init__(seed=seed)
        
        # Parameters
        self.width = width
        self.height = height
        self.num_agents = num_agents
        self.fruit_density = fruit_density
        self.comm_range = comm_range
        self.dynamics = dynamics
        self.regen_prob = regen_prob if dynamics == 'Replenishing' else 0.0
        
        # Grid (non-toroidal)
        self.grid = MultiGrid(width, height, torus=False)
        
        # Track fruits separately for efficient lookup
        self.fruits = []
        
        # Initialize fruits
        self._place_fruits()
        
        # Initialize agents
        self._place_agents()
        
        # Tracking variables for metrics
        self.cumulative_messages = 0
        self.total_harvested_cells = 0
        self.steps = 0  # Track current step for visualization

        # Data collection with comprehensive metrics
        self.datacollector = DataCollector(
            model_reporters={
                'total_yield': self._get_total_yield,
                'messages_this_step': self._get_messages_this_step,
                'cumulative_messages': lambda m: m.cumulative_messages,
                'remaining_fruit': self._get_remaining_fruit,
                'harvested_cells_this_step': self._get_harvested_this_step,
                'largest_component_ratio': self._get_largest_component_ratio,
                'avg_hops': self._get_avg_hops,
                'mean_agent_load': self._get_mean_agent_load,
                'gini_yield': self._get_gini_yield,
                'avg_travel_distance': self._get_avg_travel_distance,
            },
            agent_reporters={
                'harvested': lambda a: a.harvested if isinstance(a, HarvesterAgent) else None,
                'messages_sent': lambda a: a.messages_sent if isinstance(a, HarvesterAgent) else None,
                'messages_received': lambda a: a.messages_received if isinstance(a, HarvesterAgent) else None,
            }
        )

        # Collect initial state
        self.datacollector.collect(self)
        
    def _place_fruits(self):
        """Place fruits on grid according to density."""
        num_fruits = int(self.width * self.height * self.fruit_density)
        
        # Get all possible positions
        all_positions = [(x, y) for x in range(self.width) for y in range(self.height)]
        fruit_positions = random.sample(all_positions, num_fruits)
        
        regenerates = (self.dynamics == 'Replenishing')
        
        for pos in fruit_positions:
            fruit = Fruit(self, regenerates=regenerates, regen_prob=self.regen_prob)
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
        """Execute one step of the model using Mesa 3.0 convention."""
        # Reset per-step message counters
        for agent in self.agents:
            if isinstance(agent, HarvesterAgent):
                agent.messages_sent = 0
        
        # Agents act (Mesa 3.0 convention: shuffle_do)
        self.agents.shuffle_do('step')

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

    def _get_harvested_this_step(self):
        """Get number of cells harvested this step."""
        # Track change in total yield
        current_yield = self._get_total_yield()
        harvested = current_yield - self.total_harvested_cells
        self.total_harvested_cells = current_yield
        return harvested

    def _get_largest_component_ratio(self):
        """
        Calculate ratio of agents in largest connected component.
        Uses communication range to define connectivity.
        """
        if self.comm_range == 0:
            return 0.0

        agents = [a for a in self.agents if isinstance(a, HarvesterAgent)]
        if not agents:
            return 0.0

        # Build adjacency list
        adj = {i: set() for i in range(len(agents))}
        for i, agent1 in enumerate(agents):
            for j, agent2 in enumerate(agents):
                if i != j:
                    dist = self._chebyshev_distance(agent1.pos, agent2.pos)
                    if dist <= self.comm_range:
                        adj[i].add(j)
                        adj[j].add(i)

        # Find largest component using DFS
        visited = set()
        max_component_size = 0

        for start in range(len(agents)):
            if start in visited:
                continue

            # DFS
            stack = [start]
            component_size = 0
            while stack:
                node = stack.pop()
                if node in visited:
                    continue
                visited.add(node)
                component_size += 1
                for neighbor in adj[node]:
                    if neighbor not in visited:
                        stack.append(neighbor)

            max_component_size = max(max_component_size, component_size)

        return max_component_size / len(agents) if agents else 0.0

    def _get_avg_hops(self):
        """
        Calculate average hop distance for message delivery.
        Simplified: return average communication range utilization.
        """
        if self.comm_range == 0:
            return 0.0

        agents = [a for a in self.agents if isinstance(a, HarvesterAgent)]
        if not agents:
            return 0.0

        total_dist = 0
        count = 0

        for agent in agents:
            neighbors = self.grid.get_neighbors(
                agent.pos,
                moore=True,
                include_center=False,
                radius=self.comm_range
            )
            agent_neighbors = [n for n in neighbors if isinstance(n, HarvesterAgent)]

            for neighbor in agent_neighbors:
                dist = self._chebyshev_distance(agent.pos, neighbor.pos)
                total_dist += dist
                count += 1

        return total_dist / count if count > 0 else 0.0

    def _get_mean_agent_load(self):
        """Get mean harvest count per agent."""
        agents = [a for a in self.agents if isinstance(a, HarvesterAgent)]
        if not agents:
            return 0.0
        return sum(a.harvested for a in agents) / len(agents)

    def _get_gini_yield(self):
        """Calculate Gini coefficient of harvest distribution."""
        agents = [a for a in self.agents if isinstance(a, HarvesterAgent)]
        if not agents:
            return 0.0

        harvests = sorted([a.harvested for a in agents])
        n = len(harvests)

        if sum(harvests) == 0:
            return 0.0

        # Gini coefficient formula
        cumsum = 0
        for i, h in enumerate(harvests):
            cumsum += (i + 1) * h

        return (2 * cumsum) / (n * sum(harvests)) - (n + 1) / n

    def _get_avg_travel_distance(self):
        """Calculate average travel distance per agent."""
        agents = [a for a in self.agents if isinstance(a, HarvesterAgent)]
        if not agents:
            return 0.0
        return sum(a.travel_distance for a in agents) / len(agents)

    def _chebyshev_distance(self, pos1, pos2):
        """Calculate Chebyshev distance between two positions."""
        return max(abs(pos1[0] - pos2[0]), abs(pos1[1] - pos2[1]))


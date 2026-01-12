"""
Multi-Agent Fruit Harvesting Model for Communication Range Analysis (RQ1).

This module implements the core simulation model for a multi-agent fruit
harvesting system with configurable communication capabilities. It serves as the
experimental platform for Research Question 1: "How does communication range
affect harvesting efficiency in multi-agent foraging systems?"
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
    Multi-agent fruit harvesting simulation with configurable communication range.
    
    A Mesa-based agent-based model simulating a team of harvester agents
    collecting fruit from a grid environment. Agents can share fruit location
    information with nearby teammates within a configurable communication range.

    Attributes:
        width (int): Grid width in cells (current experiments: 100)
        height (int): Grid height in cells (current experiments: 100)
        num_agents (int): Number of harvester agents (experiments: 10 or 20)
        fruit_density (float): Fraction of cells with fruit, range [0.0, 1.0]
                              (experiments: 0.15 or 0.25)
        comm_range (int): Communication range in Chebyshev distance
                         (experiments: 0, 2, 4, 6, 8)
        use_clustered_resources (bool): If True, fruit placed in Gaussian clusters;
                                       if False, uniform random distribution
        num_clusters (int): Number of fruit clusters (default: 8)
        cluster_spread (float): Gaussian std dev for cluster spread (default: 5)
        grid (MultiGrid): Mesa spatial grid containing agents and fruit
        fruits (list): All Fruit agents for O(n) iteration vs. O(width*height)
        cumulative_messages (int): Total messages sent across all simulation steps
        simulation_complete (bool): True when all fruit harvested
        completion_step (int): Step number when simulation completed (or None)
        datacollector (DataCollector): Mesa data collection for metrics
    """
    # Class variable for Solara visualization compatibility
    steps = 0

    def __init__(
        self,
        width=20,
        height=20,
        num_agents=5,
        fruit_density=0.2,
        comm_range=2,
        seed=None,
        use_clustered_resources=True,
        num_clusters=8,
        cluster_spread=5
    ):
        """
        Initialize the multi-agent fruit harvesting simulation model.

        Creates the complete simulation environment including grid, fruit
        resources, harvester agents, and data collection infrastructure.

        Args:
            width (int): Grid width in cells. Default 20 for testing, experiments
                        use 100. Must be positive.
            height (int): Grid height in cells. Default 20 for testing, experiments
                         use 100. Must be positive.
            num_agents (int): Number of HarvesterAgent instances to create.
                             Experiments use 10 or 20. Must be ≤ grid cells.
            fruit_density (float): Fraction of grid cells to fill with fruit.
                                  Range [0.0, 1.0]. Experiments use 0.15 or 0.25.
                                  Total fruit = int(width * height * fruit_density).
            comm_range (int): Communication range in Chebyshev distance (cells).
                             0 = no communication (control condition)
                             2, 4, 6, 8 = experimental conditions
                             Must be non-negative.
            seed (int, optional): Random seed for reproducibility. If None, uses
                                 system randomness. Experiments use fixed seeds
                                 for each replication.
            use_clustered_resources (bool): If True, place fruit in Gaussian clusters
                                           around random centers. If False, uniform
                                           random placement. Default True.
            num_clusters (int): Number of fruit clusters when use_clustered_resources=True.
                               Default 8. Ignored if use_clustered_resources=False.
            cluster_spread (float): Standard deviation of Gaussian cluster spread.
                                   Default 5.0 cells. Larger values = more dispersed
                                   clusters. Ignored if use_clustered_resources=False.
        """
        super().__init__(seed=seed)

        # Store configuration parameters
        self.width = width
        self.height = height
        self.num_agents = num_agents
        self.fruit_density = fruit_density
        self.comm_range = comm_range
        self.use_clustered_resources = use_clustered_resources
        self.num_clusters = num_clusters
        self.cluster_spread = cluster_spread

        # Create spatial grid
        # MultiGrid allows multiple objects per cell (agents + fruit can coexist)
        # torus=False means agents cannot wrap around edges
        self.grid = MultiGrid(width, height, torus=False)

        # Maintain separate fruit list for O(n) iteration instead of O(width*height)
        self.fruits = []

        # Place fruit and agents on the grid
        if use_clustered_resources:
            self._place_fruits_clustered()
        else:
            self._place_fruits()
        self._place_agents()

        # Initialize metric tracking variables
        self.cumulative_messages = 0  # Running total of all messages sent
        self.steps = 0  # Current simulation step (for visualization)
        self.simulation_complete = False  # True when all fruit collected
        self.completion_step = None  # Step number when simulation completed

        # Configure Mesa's DataCollector for metric tracking
        # These metrics are collected at each step and stored in a DataFrame
        self.datacollector = DataCollector(
            model_reporters={
                'total_yield': self._get_total_yield,
                'messages_this_step': self._get_messages_this_step,
                'cumulative_messages': lambda m: m.cumulative_messages,
                'remaining_fruit': self._get_remaining_fruit,
                'coverage': self._get_coverage,
            }
        )

        # Collect initial state (step 0)
        self.datacollector.collect(self)
        
    def _place_fruits(self):
        """
        Place fruit agents uniformly at random on the grid.
        """
        num_fruits = int(self.width * self.height * self.fruit_density)

        # Generate all possible grid positions
        all_positions = [(x, y) for x in range(self.width) for y in range(self.height)]

        # Randomly select positions without replacement for uniform distribution
        fruit_positions = random.sample(all_positions, num_fruits)

        # Create Fruit agents and place on grid
        for pos in fruit_positions:
            fruit = Fruit(self)
            self.grid.place_agent(fruit, pos)
            self.fruits.append(fruit)  # Also track in list for efficient iteration

    def _place_fruits_clustered(self):
        """
        Place fruit agents in Gaussian clusters to create patchy resource distribution.
        """
        num_fruits = int(self.width * self.height * self.fruit_density)
        fruits_per_cluster = max(1, num_fruits // self.num_clusters)

        # Generate all possible grid positions for cluster center selection
        all_positions = [(x, y) for x in range(self.width) for y in range(self.height)]

        # Randomly select cluster centers
        cluster_centers = random.sample(all_positions, min(self.num_clusters, len(all_positions)))

        fruit_count = 0
        for center_x, center_y in cluster_centers:
            # Place fruits around this cluster center
            for _ in range(fruits_per_cluster):
                if fruit_count >= num_fruits:
                    break

                # Use Gaussian distribution around cluster center
                x = int(np.clip(
                    np.random.normal(center_x, self.cluster_spread),
                    0,
                    self.width - 1
                ))
                y = int(np.clip(
                    np.random.normal(center_y, self.cluster_spread),
                    0,
                    self.height - 1
                ))

                fruit = Fruit(self)
                self.grid.place_agent(fruit, (x, y))
                self.fruits.append(fruit)
                fruit_count += 1

            if fruit_count >= num_fruits:
                break

    def _place_agents(self):
        """
        Place harvester agents at random non-overlapping starting positions.
        """
        # Generate all possible grid positions
        all_positions = [(x, y) for x in range(self.width) for y in range(self.height)]

        # Randomly select unique positions for agents
        agent_positions = random.sample(all_positions, min(self.num_agents, len(all_positions)))

        # Create HarvesterAgent instances and place on grid
        for pos in agent_positions:
            agent = HarvesterAgent(self)
            self.grid.place_agent(agent, pos)
    
    def step(self):
        """
        Execute one simulation step (time tick) for all agents.
        """
        # Reset message counters before each step
        for agent in self.agents:
            if isinstance(agent, HarvesterAgent):
                agent.messages_sent = 0

        # Execute all agents in randomized order
        self.agents.shuffle_do('step')

        # Accumulate messages for efficiency metric calculation
        self.cumulative_messages += self._get_messages_this_step()

        # Record metrics for analysis
        self.datacollector.collect(self)

        # Early termination check - stop when all fruit collected
        if self._get_remaining_fruit() == 0:
            self.simulation_complete = True
            self.completion_step = self.steps

    def _wrapped_step(self):
        """
        Override Mesa's internal step wrapper to implement completion-based pause.
        """
        if self.simulation_complete:
            return  # Don't step if simulation is done

        # Call parent implementation to increment step counter and execute step()
        from mesa import Model
        Model._wrapped_step(self)

    def run_model(self, steps=100):
        """
        Run the simulation for a specified number of steps with early termination.
        """
        for _ in range(steps):
            if self.simulation_complete:
                break  # Early termination when all fruit collected
            self.step()

    # =========================================================================
    # METRIC CALCULATION METHODS
    # =========================================================================
    # These methods are called by Mesa's DataCollector at each simulation step
    # to record metrics for later analysis. They compute aggregate statistics
    # across all agents and resources.

    def _get_total_yield(self):
        """
        Calculate total fruit harvested by all agents (primary performance metric).
        """
        return sum(a.harvested for a in self.agents if isinstance(a, HarvesterAgent))

    def _get_messages_this_step(self):
        """
        Count messages sent during the current simulation step.
        """
        return sum(a.messages_sent for a in self.agents if isinstance(a, HarvesterAgent))

    def _get_remaining_fruit(self):
        """
        Count fruit still available for harvesting (completion tracking).
        """
        return sum(1 for f in self.fruits if f.available)

    def _get_coverage(self):
        """
        Calculate total unique grid cells visited by all agents (exploration metric).
        """
        all_visited = set()
        for agent in self.agents:
            if isinstance(agent, HarvesterAgent):
                all_visited.update(agent.visited_cells)
        return len(all_visited)
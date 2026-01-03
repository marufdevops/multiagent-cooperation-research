"""
Fruit Harvesting Model for RQ1: Communication Range Effects

================================================================================
PURPOSE & DESIGN RATIONALE
================================================================================
This module implements the core simulation model for investigating how
communication range affects multi-agent fruit harvesting cooperation (RQ1).

DESIGN DECISIONS:
1. Static Resource Dynamics: Fruit does not regenerate after harvesting. This
   simplifies the analysis by eliminating time-dependent resource dynamics and
   allows us to measure total collection efficiency in a finite scenario.

2. MultiGrid with Occupancy Checks: We use Mesa's MultiGrid (allowing multiple
   agents per cell) but manually prevent HarvesterAgent overlap. This allows
   agents and fruit to coexist in the same cell while preventing agent collision.

3. Chebyshev Distance for Communication: Communication range is measured using
   Chebyshev distance (max of |Δx|, |Δy|), which corresponds to 8-connected
   neighborhoods and is standard in grid-based agent simulations.

4. Metric Collection: We track four key metrics:
   - total_yield: Total fruits harvested (primary performance metric)
   - cumulative_messages: Communication cost
   - remaining_fruit: Completion tracking
   - coverage: Exploration efficiency (unique cells visited)

EXPERIMENTAL DESIGN:
- Grid: 50×50 cells
- Communication ranges: 0 (no communication), 2, 4, 6, 8 cells
- Team sizes: 5, 10, 20 agents
- Fruit densities: 0.15, 0.25
- Episode length: 500 steps (or until all fruit collected)
- Replications: 20 per configuration

================================================================================
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
    Multi-agent fruit harvesting simulation model with configurable communication.

    This model addresses RQ1: "How does communication range affect harvesting
    efficiency in multi-agent systems?"

    The model creates a grid environment with randomly distributed fruit and
    harvester agents. Agents can communicate fruit locations to nearby agents
    within a configurable range, enabling coordination.

    Key Features:
    - Static resource dynamics (fruit does not regenerate)
    - Configurable communication range (0 = no communication)
    - MultiGrid allowing agents and fruit to coexist
    - Comprehensive metric collection for analysis

    Attributes:
        width (int): Grid width in cells
        height (int): Grid height in cells
        num_agents (int): Number of harvester agents
        fruit_density (float): Initial fraction of cells containing fruit (0.0-1.0)
        comm_range (int): Agent communication range in cells (Chebyshev distance)
        grid (MultiGrid): The spatial grid where agents and fruit exist
        fruits (list): List of all Fruit agents for efficient lookup
        cumulative_messages (int): Total messages sent across all steps
        simulation_complete (bool): Flag indicating all fruit has been collected

    Example:
        >>> model = HarvestModel(width=50, height=50, num_agents=10,
        ...                      fruit_density=0.15, comm_range=2, seed=42)
        >>> model.run_model(steps=500)
        >>> data = model.datacollector.get_model_vars_dataframe()
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
        seed=None
    ):
        """
        Initialize the fruit harvesting model.

        Creates a grid environment, places fruit randomly according to density,
        places harvester agents at random non-overlapping positions, and sets up
        data collection for metrics.

        Args:
            width: Grid width in cells (default: 20, experiments use 50)
            height: Grid height in cells (default: 20, experiments use 50)
            num_agents: Number of HarvesterAgent instances to create
            fruit_density: Fraction of grid cells to fill with fruit (0.0-1.0)
            comm_range: Communication range in cells using Chebyshev distance.
                       0 = no communication, 2/4/6/8 = experimental conditions
            seed: Random seed for reproducibility across replications

        Design Notes:
            - MultiGrid is used to allow agents and fruit in same cell
            - HarvesterAgent overlap is prevented via explicit checks in agent movement
            - Non-torus grid (bounded edges) represents a finite orchard
        """
        super().__init__(seed=seed)

        # Store configuration parameters
        self.width = width
        self.height = height
        self.num_agents = num_agents
        self.fruit_density = fruit_density
        self.comm_range = comm_range

        # Create spatial grid
        # MultiGrid allows multiple objects per cell (agents + fruit can coexist)
        # torus=False means agents cannot wrap around edges
        self.grid = MultiGrid(width, height, torus=False)

        # Maintain separate fruit list for O(n) iteration instead of O(width*height)
        self.fruits = []

        # Place fruit and agents on the grid
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
        Place fruit agents randomly on the grid according to density parameter.

        This implements static resource dynamics - fruit is placed once at
        initialization and does not regenerate. The number of fruit is
        determined by: num_fruits = width * height * fruit_density

        Design Notes:
            - Uses random.sample for uniform distribution without replacement
            - Fruit positions are independent of agent positions
            - All fruit starts as available (not harvested)
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

    def _place_agents(self):
        """
        Place harvester agents randomly on the grid at non-overlapping positions.

        Agents are placed at random positions, potentially overlapping with fruit
        (MultiGrid allows this). However, each agent gets a unique starting position
        to avoid immediate collision.

        Design Notes:
            - Agents can start on cells containing fruit
            - No two agents start at the same position
            - Starting positions don't affect experimental fairness due to random placement
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
        Execute one simulation step.

        Each step consists of:
        1. Reset per-step message counters for all agents
        2. Execute all agent actions in random order (move, harvest, communicate)
        3. Update cumulative message count
        4. Collect metrics for this step
        5. Check for simulation completion (all fruit collected)

        Agent Execution Order:
            Uses Mesa's shuffle_do() which randomizes agent order each step.
            This prevents systematic bias from fixed execution order.
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
        Override Mesa's internal step wrapper to implement simulation pause.

        This method is called by Mesa's visualization system. When all fruit
        is collected, we prevent further stepping to avoid wasted computation
        and to clearly show completion in the visualization.

        Note: This is a Mesa internal method override for Solara compatibility.
        """
        if self.simulation_complete:
            return  # Don't step if simulation is done

        # Call parent implementation to increment step counter and execute step()
        from mesa import Model
        Model._wrapped_step(self)

    def run_model(self, steps=100):
        """
        Run the simulation for a specified number of steps.

        The simulation terminates early if all fruit is collected before
        reaching the step limit. This is important for experiments where
        we want to measure completion time.

        Args:
            steps: Maximum number of steps to run (default: 100, experiments use 500)
        """
        for _ in range(steps):
            if self.simulation_complete:
                break  # Early termination when all fruit collected
            self.step()

    # =========================================================================
    # METRIC CALCULATION METHODS
    # =========================================================================
    # These methods are called by DataCollector at each step to record metrics
    # for later analysis. They compute aggregate statistics across all agents.

    def _get_total_yield(self):
        """
        Calculate total fruit harvested by all agents.

        This is the primary performance metric for RQ1. Higher yield indicates
        better harvesting efficiency.

        Returns:
            int: Sum of harvested fruit counts across all HarvesterAgents
        """
        return sum(a.harvested for a in self.agents if isinstance(a, HarvesterAgent))

    def _get_messages_this_step(self):
        """
        Count messages sent during the current step.

        Used to calculate cumulative communication cost and efficiency
        (yield per message).

        Returns:
            int: Total messages sent by all agents this step
        """
        return sum(a.messages_sent for a in self.agents if isinstance(a, HarvesterAgent))

    def _get_remaining_fruit(self):
        """
        Count fruit still available for harvesting.

        Used for completion detection and progress tracking.

        Returns:
            int: Number of Fruit agents with available=True
        """
        return sum(1 for f in self.fruits if f.available)

    def _get_coverage(self):
        """
        Calculate total unique grid cells visited by all agents.

        This measures exploration efficiency - how much of the grid has been
        searched by the team. High coverage with low yield indicates search
        inefficiency; high yield with low coverage indicates good coordination.

        Returns:
            int: Count of unique (x,y) positions visited by any agent
        """
        all_visited = set()
        for agent in self.agents:
            if isinstance(agent, HarvesterAgent):
                all_visited.update(agent.visited_cells)
        return len(all_visited)


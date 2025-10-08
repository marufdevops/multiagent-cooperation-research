"""
Mesa 3.0 compatible OrchardModel implementation for multi-agent fruit harvesting simulation.

This module implements the environment where agents harvest fruits, including:
- Grid-based orchard environment
- Fruit spawning and regeneration mechanics
- Range-bounded message delivery system
- Data collection for analysis
"""

import random
import math
import numpy as np
from mesa import Model
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector

from .agents import HarvesterAgent


class OrchardModel(Model):
    """
    A model representing an orchard environment where agents harvest fruits.

    Mesa 3.0 compatible - uses model.agents.shuffle_do("step") instead of schedulers.
    Supports communication-based cooperation and data collection.
    """

    # Provide a class-level placeholder for SolaraViz pre-init components
    steps = 0

    def __init__(self, *, width=30, height=30, num_agents=20, communication_range=3.0,
                 cooperative_share=1.0, initial_fruit_density=0.3,
                 regeneration_prob=0.1, seed=None):
        """
        Initialize the OrchardModel.

        Args:
            width: Grid width
            height: Grid height
            num_agents: Number of harvester agents
            communication_range: Maximum distance for message delivery
            cooperative_share: Fraction of agents that are cooperative (0.0-1.0)
            initial_fruit_density: Initial fraction of cells with fruits
            regeneration_prob: Probability of fruit regeneration per step
            seed: Random seed for reproducibility
        """
        # Mesa 3.0: Call super().__init__() with seed
        super().__init__(seed=seed)

        # Model parameters
        self.width = width
        self.height = height
        self.num_agents = num_agents
        self.communication_range = communication_range
        self.cooperative_share = cooperative_share
        self.initial_fruit_density = initial_fruit_density
        self.regeneration_prob = regeneration_prob

        # Create grid (Mesa 3.0 compatible)
        self.grid = MultiGrid(width, height, torus=False)

        # Mesa 3.0: No scheduler needed, use model.agents.shuffle_do("step")

        # Fruit map - numpy array for efficient fruit tracking
        self.fruit_map = np.zeros((width, height), dtype=int)

        # Communication and metrics
        self.total_messages_sent = 0

        # Data collection (Mesa 3.0 compatible)
        self.datacollector = DataCollector(
            model_reporters={
                "Total_Fruits_Harvested": lambda m: sum(a.fruits_collected for a in m.agents),
                "Total_Messages_Sent": "total_messages_sent",
                "Step_Count": "steps",
                "Cooperative_Agents": lambda m: sum(1 for a in m.agents if a.strategy == "cooperative"),
                "Competitive_Agents": lambda m: sum(1 for a in m.agents if a.strategy == "competitive"),
                "Average_Fruits_Per_Agent": lambda m: sum(a.fruits_collected for a in m.agents) / len(m.agents) if m.agents else 0,
            },
            agent_reporters={
                "Fruits_Collected": "fruits_collected",
                "Messages_Sent": "messages_sent",
                "Messages_Received": "messages_received",
                "Strategy": "strategy",
                "X": lambda a: a.pos[0] if a.pos else None,
                "Y": lambda a: a.pos[1] if a.pos else None,
            }
        )

        # Initialize environment
        self._spawn_initial_fruits()
        self._create_agents()

        # Collect initial data
        self.datacollector.collect(self)

    def _spawn_initial_fruits(self):
        """Spawn initial fruits randomly across the grid."""
        total_cells = self.width * self.height
        num_fruit_cells = int(total_cells * self.initial_fruit_density)

        # Randomly select cells for fruit placement
        all_positions = [(x, y) for x in range(self.width) for y in range(self.height)]
        fruit_positions = random.sample(all_positions, num_fruit_cells)

        # Place 1-3 fruits per selected cell
        for x, y in fruit_positions:
            self.fruit_map[x, y] = random.randint(1, 3)

    def _create_agents(self):
        """Create and place harvester agents."""
        num_cooperative = int(self.num_agents * self.cooperative_share)

        for i in range(self.num_agents):
            # Determine strategy
            strategy = "cooperative" if i < num_cooperative else "competitive"

            # Create agent (Mesa 3.0: no unique_id parameter)
            agent = HarvesterAgent(
                model=self,
                communication_range=self.communication_range,
                strategy=strategy,
                sensor_radius=2
            )

            # Mesa 3.0: Agents are automatically added to model.agents

    def get_fruit_at(self, pos):
        """Get the number of fruits at a given position."""
        if not pos:
            return 0
        x, y = pos
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.fruit_map[x, y]
        return 0

    def harvest_fruit(self, pos):
        """
        Harvest one fruit from the given position.

        Returns:
            bool: True if fruit was successfully harvested, False otherwise
        """
        if not pos:
            return False

        x, y = pos
        if 0 <= x < self.width and 0 <= y < self.height and self.fruit_map[x, y] > 0:
            self.fruit_map[x, y] -= 1
            return True
        return False

    def regenerate_fruits(self):
        """Regenerate fruits probabilistically across the grid."""
        for x in range(self.width):
            for y in range(self.height):
                # Only regenerate in cells with fewer than 3 fruits
                if self.fruit_map[x, y] < 3 and random.random() < self.regeneration_prob:
                    self.fruit_map[x, y] += 1

    def deliver_messages(self):
        """
        Deliver messages between agents based on communication range.
        Only agents within communication_range can receive messages.
        """
        # Collect all outgoing messages
        all_messages = []
        for agent in self.agents:
            for message in agent.outbox:
                all_messages.append((agent, message))
            agent.outbox.clear()

        # Deliver messages to agents within range
        for sender, message in all_messages:
            if not sender.pos:
                continue

            sender_x, sender_y = sender.pos

            for receiver in self.agents:
                if receiver == sender or not receiver.pos:
                    continue

                receiver_x, receiver_y = receiver.pos

                # Calculate distance
                distance = ((receiver_x - sender_x) ** 2 + (receiver_y - sender_y) ** 2) ** 0.5

                # Deliver message if within range
                if distance <= sender.communication_range:
                    receiver.inbox.append(message.copy())

        # Update total messages sent
        self.total_messages_sent += len(all_messages)

    def step(self):
        """
        Execute one step of the simulation.
        Mesa 3.0: Use model.agents.shuffle_do("step") instead of scheduler.
        """
        # Step all agents (Mesa 3.0 style)
        self.agents.shuffle_do("step")

        # Deliver messages between agents
        self.deliver_messages()

        # Regenerate fruits
        self.regenerate_fruits()

        # Collect data
        self.datacollector.collect(self)

        # Mesa 3.0: steps counter is automatically incremented

    def get_agent_positions(self):
        """Get positions of all agents for visualization."""
        positions = {}
        for agent in self.agents:
            if agent.pos:
                positions[agent.unique_id] = {
                    'pos': agent.pos,
                    'strategy': agent.strategy,
                    'fruits_collected': agent.fruits_collected
                }
        return positions

    def get_fruit_positions(self):
        """Get positions and counts of all fruits for visualization."""
        fruits = {}
        for x in range(self.width):
            for y in range(self.height):
                if self.fruit_map[x, y] > 0:
                    fruits[(x, y)] = self.fruit_map[x, y]
        return fruits
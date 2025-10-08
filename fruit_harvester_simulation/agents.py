"""
Mesa 3.0 compatible HarvesterAgent implementation for multi-agent fruit harvesting simulation.

This module implements agents that can:
- Move around the orchard environment
- Detect and harvest fruits
- Communicate with other agents within range
- Use cooperative or competitive strategies
"""

import random
import math
from mesa import Agent


class HarvesterAgent(Agent):
    """
    An agent that harvests fruits in an orchard environment.

    Mesa 3.0 compatible - no unique_id parameter needed in constructor.
    Supports communication-based cooperation and competitive strategies.
    """

    def __init__(self, model, communication_range=3.0, strategy="cooperative", sensor_radius=2):
        """
        Initialize a HarvesterAgent.

        Args:
            model: The OrchardModel instance
            communication_range: Maximum distance for sending/receiving messages
            strategy: "cooperative" or "competitive" behavior
            sensor_radius: Distance for detecting fruits
        """
        # Mesa 3.0: Call super().__init__() without unique_id
        super().__init__(model)

        # Agent properties
        self.communication_range = communication_range
        self.strategy = strategy
        self.sensor_radius = sensor_radius

        # State variables
        self.fruits_collected = 0
        self.target = None
        self.known_fruit_locations = set()
        self.claimed_locations = set()  # Locations this agent has claimed
        self.others_claims = set()      # Locations claimed by other agents

        # Communication
        self.inbox = []
        self.outbox = []
        self.messages_sent = 0
        self.messages_received = 0

        # Place agent randomly on the grid (Mesa 3.0 compatible)
        x = random.randrange(self.model.width)
        y = random.randrange(self.model.height)
        self.model.grid.place_agent(self, (x, y))

    def step(self):
        """
        Execute one step of the agent's behavior cycle:
        1. Sense environment and process messages
        2. Decide on target and actions
        3. Act (move, harvest)
        4. Communicate (if cooperative)
        """
        self.sense()
        self.decide()
        self.act()
        self.communicate()

    def sense(self):
        """
        Sense the environment: detect nearby fruits and process incoming messages.
        """
        # Detect fruits within sensor radius
        self._detect_fruits()

        # Process incoming messages
        self._process_inbox()

    def _detect_fruits(self):
        """Detect fruits within sensor radius."""
        if not self.pos:
            return

        x, y = self.pos

        # Check all positions within sensor radius
        for dx in range(-self.sensor_radius, self.sensor_radius + 1):
            for dy in range(-self.sensor_radius, self.sensor_radius + 1):
                check_x, check_y = x + dx, y + dy

                # Check bounds
                if (0 <= check_x < self.model.width and
                    0 <= check_y < self.model.height):

                    # Check if there are fruits at this location
                    if self.model.get_fruit_at((check_x, check_y)) > 0:
                        self.known_fruit_locations.add((check_x, check_y))

    def _process_inbox(self):
        """Process incoming messages."""
        for message in self.inbox:
            self.messages_received += 1
            msg_type = message.get("type")

            if msg_type == "HOTSPOT":
                # Another agent found fruits
                location = message.get("location")
                if location:
                    self.known_fruit_locations.add(location)

            elif msg_type == "CLAIM":
                # Another agent claimed a location
                location = message.get("location")
                if location:
                    self.others_claims.add(location)

            elif msg_type == "RELEASE":
                # Another agent released a claim
                location = message.get("location")
                if location and location in self.others_claims:
                    self.others_claims.remove(location)

        # Clear inbox after processing
        self.inbox.clear()

    def decide(self):
        """
        Decide on target location and actions based on strategy.
        """
        # Remove known locations that no longer have fruits
        self.known_fruit_locations = {
            loc for loc in self.known_fruit_locations
            if self.model.get_fruit_at(loc) > 0
        }

        # If current target is invalid, clear it
        if (self.target and
            (self.model.get_fruit_at(self.target) == 0 or
             (self.strategy == "cooperative" and self.target in self.others_claims))):
            self.target = None
            if self.target in self.claimed_locations:
                self.claimed_locations.remove(self.target)

        # Select new target if needed
        if not self.target and self.known_fruit_locations:
            available_locations = self.known_fruit_locations.copy()

            # Cooperative agents avoid others' claims
            if self.strategy == "cooperative":
                available_locations -= self.others_claims

            if available_locations:
                # Choose closest available fruit
                if self.pos:
                    self.target = min(available_locations,
                                    key=lambda loc: self._distance_to(loc))
                else:
                    self.target = random.choice(list(available_locations))

                # Cooperative agents claim their target
                if self.strategy == "cooperative" and self.target:
                    self.claimed_locations.add(self.target)

    def act(self):
        """
        Execute actions: move toward target and harvest fruits.
        """
        if not self.pos:
            return

        # Move toward target
        if self.target:
            self._move_toward(self.target)
        else:
            # Random walk if no target
            self._random_move()

        # Try to harvest fruit at current location
        if self.model.get_fruit_at(self.pos) > 0:
            if self.model.harvest_fruit(self.pos):
                self.fruits_collected += 1

                # Release claim if we harvested our target
                if self.target == self.pos and self.target in self.claimed_locations:
                    self.claimed_locations.remove(self.target)
                    self.target = None

    def communicate(self):
        """
        Send messages to other agents (only if cooperative).
        """
        if self.strategy != "cooperative":
            return

        # Send HOTSPOT messages for newly discovered fruits
        for location in self.known_fruit_locations:
            if self.model.get_fruit_at(location) > 0:
                message = {
                    "type": "HOTSPOT",
                    "location": location,
                    "sender": self.unique_id
                }
                self.outbox.append(message)
                self.messages_sent += 1

        # Send CLAIM messages for newly claimed locations
        for location in self.claimed_locations:
            message = {
                "type": "CLAIM",
                "location": location,
                "sender": self.unique_id
            }
            self.outbox.append(message)
            self.messages_sent += 1

    def _move_toward(self, target):
        """Move one step toward the target location."""
        if not self.pos or not target:
            return

        x, y = self.pos
        target_x, target_y = target

        # Calculate direction
        dx = 0 if target_x == x else (1 if target_x > x else -1)
        dy = 0 if target_y == y else (1 if target_y > y else -1)

        # Calculate new position
        new_x = max(0, min(self.model.width - 1, x + dx))
        new_y = max(0, min(self.model.height - 1, y + dy))

        # Move if the new position is different and valid
        if (new_x, new_y) != (x, y):
            self.model.grid.move_agent(self, (new_x, new_y))

    def _random_move(self):
        """Move randomly to an adjacent cell."""
        if not self.pos:
            return

        possible_moves = self.model.grid.get_neighborhood(
            self.pos, moore=True, include_center=False
        )

        if possible_moves:
            new_position = random.choice(possible_moves)
            self.model.grid.move_agent(self, new_position)

    def _distance_to(self, location):
        """Calculate Euclidean distance to a location."""
        if not self.pos:
            return float('inf')

        x1, y1 = self.pos
        x2, y2 = location
        return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
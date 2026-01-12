"""
This module implements the HarvesterAgent class, representing autonomous
foraging agents that move through a grid environment, collect fruit resources,
and share information with nearby teammates via communication range.
"""
import random
import numpy as np
from mesa import Agent


class HarvesterAgent(Agent):
    """
    Autonomous harvesting agent with local sensing and communication capabilities.

    Attributes:
        harvested (int): Total fruit collected by this agent (primary performance metric)
        messages_sent (int): Messages sent in current step (reset each step by model)
        messages_received (int): Cumulative messages received (lifetime counter)
        current_target (tuple): Target (x,y) position from communication, or None if idle
        travel_distance (int): Total movement steps (for efficiency analysis)
        visited_cells (set): All (x,y) positions visited (for coverage metric)
        empty_cells (set): Positions known to have no available fruit (memory optimization)
        last_pos (tuple): Previous position for distance tracking

    Behavioral Constants:
        SENSING_RADIUS = 2: Local sensing range in Chebyshev distance
        LEVY_FLIGHT_PROB = 0.2: Probability of long-range exploration jump
        LEVY_FLIGHT_RANGE = 10: Maximum distance for Levy flight jumps

    Design Notes:
        - Movement uses Moore neighborhood (8 directions + stay in place)
        - Communication uses Chebyshev distance for range calculation
        - Collision avoidance prevents agent overlap (one agent per cell)
        - Target validation prevents pursuing already-harvested fruit
        - Density heatmap biases exploration toward fruit-cluster areas
    """

    def __init__(self, model):
        """
        Initialize harvester agent with clean state and empty memory.
        Args:
            model (HarvestModel): The parent model instance this agent belongs to.
                                 Required by Mesa's Agent base class.
        """
        super().__init__(model)

        # Performance tracking
        self.harvested = 0  # Fruit collected (primary metric)
        self.messages_sent = 0  # Messages this step (reset each step by model)
        self.messages_received = 0  # Lifetime message count

        # Navigation state
        self.current_target = None  # (x,y) target from communication, or None if idle
        self.travel_distance = 0  # Total movement steps (for efficiency analysis)
        self.last_pos = None  # Previous position for distance tracking
        self.visited_cells = set()  # All visited positions (for coverage metric)

        # Memory for exploration (implements bounded rationality)
        self.empty_cells = set()  # Cells confirmed to have no available fruit
        self.discovered_fruits = set()  # Fruit positions agent has found or been told about

        # Idleness tracking for improved communication targeting
        self.idle_steps = 0  # Steps without finding fruit (indicates need for help)
        self._found_fruit_this_step = False  # Flag set during harvest() for idleness tracking
        
    def step(self):
        """
        Execute one complete behavioral cycle: move, harvest, communicate.
        """
        self.last_pos = self.pos
        self.move()

        # Track metrics for analysis
        if self.last_pos and self.pos != self.last_pos:
            self.travel_distance += 1
        if self.pos:
            self.visited_cells.add(self.pos)

        self.harvest()

        # Update idleness tracking for communication targeting
        if not self._found_fruit_this_step:
            self.idle_steps += 1
        else:
            self.idle_steps = 0

        self.communicate()

    def move(self):
        """
        Execute movement decision using hierarchical priority-based strategy.
        
        Determines next position based on a priority hierarchy of behavioral
        rules, from immediate opportunities (local fruit) to exploration (random walk).
        """
        # Early termination: don't move if simulation is done
        remaining_fruit = sum(1 for f in self.model.fruits if f.available)
        if remaining_fruit == 0:
            return

        # Priority 0: Check if fruit is at current position
        # If so, don't move - let harvest() handle it
        if self.pos:
            cell_contents = self.model.grid.get_cell_list_contents([self.pos])
            for obj in cell_contents:
                if hasattr(obj, 'is_fruit') and obj.is_fruit and obj.available:
                    # Fruit at current position - don't move
                    self.current_target = None
                    return

        # Priority 1: Check for immediately accessible fruit (also discovers them)
        nearby_fruit = self._find_closest_fruit_nearby(search_radius=2)

        if nearby_fruit:
            # If fruit is at current position, don't move - let harvest() handle it
            if nearby_fruit == self.pos:
                self.current_target = None  # Clear any previous target
                # Don't move, just let harvest() collect it
            else:
                # Override any distant target with nearby opportunity
                self.current_target = nearby_fruit
                self._move_toward(nearby_fruit)
                return  # Don't check other targets, focus on nearby fruit

        # Priority 2: Pursue communicated target if still valid
        if self.current_target:
            if self._is_target_valid():
                self._move_toward(self.current_target)
            else:
                # Target was harvested by another agent, clear it
                self.current_target = None
                # Try to find another remembered fruit instead of random exploration
                self._pursue_remembered_or_explore()
        elif self.discovered_fruits:
            # Priority 3: No nearby fruit, no target, but we remember some locations
            self._pursue_remembered_or_explore()
        else:
            # Priority 4: Pure exploration - no known fruit anywhere
            self._move_with_levy_and_density()

    def _pursue_remembered_or_explore(self):
        """
        Try to navigate to a remembered fruit location, or explore if none valid.

        This prevents agents from sitting idle when they have fruit in memory
        but no immediate target or nearby fruit.
        """
        nearest_remembered = self._find_nearest_fruit()  # Uses discovered_fruits
        if nearest_remembered:
            self.current_target = nearest_remembered
            self._move_toward(nearest_remembered)
        else:
            # All remembered fruit was harvested, explore to find more
            self._move_with_levy_and_density()

    def _find_closest_fruit_nearby(self, search_radius=2):
        """
        Find the closest available fruit within a small radius (local sensing).

        Args:
            search_radius: Maximum Chebyshev distance to search (default=2)

        Returns:
            tuple: (x,y) position of closest fruit, or None if no fruit nearby
        """
        if not self.pos:
            return None

        min_dist = float('inf')
        closest = None

        for fruit in self.model.fruits:
            if not fruit.available or fruit.pos in self.empty_cells:
                continue

            dist = self._chebyshev_distance(self.pos, fruit.pos)

            # Only consider fruit within search radius (agent's vision)
            if dist <= search_radius:
                # Remember this fruit location (local sensing -> memory)
                self.discovered_fruits.add(fruit.pos)

                if dist < min_dist:
                    min_dist = dist
                    closest = fruit.pos

        return closest

    def _move_toward(self, target_pos):
        """
        Move one step toward a target position using greedy pathfinding.
        Args:
            target_pos: (x,y) tuple of destination position

        Notes:
            - Movement blocked if target cell contains another HarvesterAgent
            - Target is cleared upon reaching destination
        """
        if not self.pos:
            return

        x, y = self.pos
        tx, ty = target_pos

        # Calculate step direction (greedy toward target)
        dx = 0 if tx == x else (1 if tx > x else -1)
        dy = 0 if ty == y else (1 if ty > y else -1)

        new_pos = (x + dx, y + dy)

        # Validate new position
        if self.model.grid.out_of_bounds(new_pos):
            self.current_target = None
            return

        # Collision avoidance: check for other agents
        cell_contents = self.model.grid.get_cell_list_contents([new_pos])
        has_harvester = any(isinstance(obj, HarvesterAgent) and obj != self for obj in cell_contents)

        if has_harvester:
            return  # Wait for cell to clear

        # Execute movement
        self.model.grid.move_agent(self, new_pos)

        # Clear target upon arrival
        if new_pos == target_pos:
            self.current_target = None

    def _is_target_valid(self):
        """
        Verify that the current target fruit still exists and is available.

        This implements "Target Validation" - preventing agents from wasting
        time traveling to fruit that was already harvested by another agent.

        Returns:
            bool: True if target fruit exists and is available, False otherwise
        """
        if not self.current_target:
            return False

        # Quick check against known empty cells
        if self.current_target in self.empty_cells:
            return False

        # Verify fruit actually exists at target
        for fruit in self.model.fruits:
            if fruit.pos == self.current_target and fruit.available:
                return True

        # Target fruit was harvested, mark location as empty
        self.empty_cells.add(self.current_target)
        return False

    def _move_with_levy_and_density(self):
        """
        Explore using combination of Levy Flight and Density Heatmap.

        This exploration strategy combines two techniques:
        1. Visited Cell Memory: Avoid revisiting cells known to be empty
        2. Density Heatmap: Prefer cells near fruit clusters
        3. Levy Flight: Occasional long jumps to escape local minima

        The algorithm:
        - If unexplored neighbors exist, use density-biased selection
        - If all neighbors are explored/empty, use Levy Flight jump
        """
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,
            include_center=False
        )

        if not possible_steps:
            return

        # Filter using Visited Cell Memory
        unvisited_steps = [s for s in possible_steps if s not in self.empty_cells]

        # Select movement strategy based on local knowledge
        if not unvisited_steps:
            # All neighbors empty - try Levy Flight escape
            new_position = self._levy_flight_jump(possible_steps)
        else:
            # Use density heatmap for informed exploration
            new_position = self._density_biased_move(unvisited_steps)

        # Validate and execute movement
        if new_position and not self.model.grid.out_of_bounds(new_position):
            cell_contents = self.model.grid.get_cell_list_contents([new_position])
            has_harvester = any(isinstance(obj, HarvesterAgent) and obj != self for obj in cell_contents)

            if not has_harvester:
                self.model.grid.move_agent(self, new_position)

    def _levy_flight_jump(self, possible_steps):
        """
        Implement Levy Flight for occasional long-range exploration jumps.

        Levy Flight is a random walk with step sizes drawn from a heavy-tailed
        distribution. This allows occasional long jumps that help discover
        distant fruit clusters not reachable through local exploration.

        Implementation:
        - 80% probability: Normal step (random neighbor)
        - 20% probability: Long jump (2-4 cells in random direction)

        Args:
            possible_steps: List of adjacent cell positions

        Returns:
            tuple: (x,y) position to move to
        """
        # Majority of steps are normal random walk
        if random.random() < 0.8:
            return random.choice(possible_steps)

        # Long-range jump for exploration
        jump_distance = random.randint(2, 4)
        angle = random.uniform(0, 2 * np.pi)
        dx = int(jump_distance * np.cos(angle))
        dy = int(jump_distance * np.sin(angle))

        new_pos = (self.pos[0] + dx, self.pos[1] + dy)

        # Clamp to valid grid coordinates
        new_pos = (
            max(0, min(new_pos[0], self.model.grid.width - 1)),
            max(0, min(new_pos[1], self.model.grid.height - 1))
        )

        return new_pos

    def _density_biased_move(self, candidates):
        """
        Select movement direction biased toward remembered fruit locations.

        Args:
            candidates: List of valid (x,y) positions to consider

        Returns:
            tuple: (x,y) position with highest nearby remembered fruit count
        """
        best_move = None
        best_count = -1

        for candidate in candidates:
            # Count remembered fruit near this candidate
            nearby_remembered = sum(
                1 for fruit_pos in self.discovered_fruits
                if self._chebyshev_distance(candidate, fruit_pos) <= 2
            )

            if nearby_remembered > best_count:
                best_count = nearby_remembered
                best_move = candidate

        # If no remembered fruit nearby, random choice (true exploration)
        return best_move if best_move else random.choice(candidates)

    def _calculate_local_density(self, pos):
        """
        Calculate fruit density in the neighborhood of a position.

        Density is the count of available fruit within a 3x3 area centered
        on the position. This is used by _density_biased_move to prefer
        directions with more fruit.

        Also adds any seen fruit to discovered_fruits (local sensing -> memory).

        Args:
            pos: (x,y) position to evaluate

        Returns:
            int: Count of available fruit in 3x3 neighborhood
        """
        neighborhood = self.model.grid.get_neighborhood(
            pos,
            moore=True,
            include_center=True,
            radius=1
        )

        fruit_count = 0
        for cell in neighborhood:
            if cell not in self.empty_cells:
                cell_contents = self.model.grid.get_cell_list_contents([cell])
                for obj in cell_contents:
                    if hasattr(obj, 'is_fruit') and obj.is_fruit and obj.available:
                        fruit_count += 1
                        # Remember this fruit (local sensing -> memory)
                        self.discovered_fruits.add(obj.pos)

        return fruit_count
    

    def harvest(self):
        """
        Attempt to harvest fruit at current position.
        """
        if not self.pos:
            self._found_fruit_this_step = False
            return

        cell_contents = self.model.grid.get_cell_list_contents([self.pos])

        fruit_found = False
        for obj in cell_contents:
            if hasattr(obj, 'is_fruit') and obj.is_fruit:
                if obj.available:
                    # Discover and harvest the fruit
                    obj.harvest()
                    self.harvested += 1
                    self.current_target = None  # Goal achieved
                    fruit_found = True
                    self._found_fruit_this_step = True  # Track for idleness
                    # Remove from discovered since we just harvested it
                    self.discovered_fruits.discard(self.pos)
                    self.empty_cells.add(self.pos)  # Now empty
                    break  # Only harvest one fruit per step
                else:
                    # Fruit exists but already harvested by another agent
                    self.discovered_fruits.discard(self.pos)
                    self.empty_cells.add(self.pos)  # Mark as empty since fruit is gone
                    fruit_found = True  # There was fruit, just already taken

        # Update Visited Cell Memory
        if not fruit_found and self.pos not in self.empty_cells:
            self.empty_cells.add(self.pos)
            self.discovered_fruits.discard(self.pos)  # Definitely no fruit here

        self._found_fruit_this_step = fruit_found

    def communicate(self):
        """
        Share fruit location information with nearby idle agents.

        IMPROVED COMMUNICATION PROTOCOL with directional information sharing:

        1. DIRECTIONAL COMMUNICATION:
           Only agents with cluster targets (from communication or discovery)
           share information with idle agents. This creates a feedback loop
           where successful agents guide explorers to clusters.

        2. BROADENED IDLENESS DEFINITION:
           An agent is "idle" if:
           - No current target, AND
           - No nearby fruit (within search_radius=2), AND
           - Idle for 2+ steps (indicates stuck in empty area)

           This makes idle agents more receptive to communication.

        3. DISTRIBUTED TARGET ASSIGNMENT:
           Different fruits to different agents to reduce herding.

        4. INTERFERENCE MODEL:
           High communication ranges have message loss due to congestion.

        Communication Protocol:
        1. Check if this agent has valuable information (cluster target)
        2. Find agents within comm_range
        3. Identify truly idle agents (no target, no nearby fruit, idle_steps >= 2)
        4. Get multiple ranked fruits to distribute
        5. Assign different fruits to different agents
        """
        if not self.pos or self.model.comm_range == 0:
            return  # No communication in control condition

        # Only share if we have valuable information (cluster target)
        available_fruits = self._get_ranked_fruits()
        if not available_fruits:
            return  # Nothing to share

        # Find agents within communication range
        neighbors = self.model.grid.get_neighbors(
            self.pos,
            moore=True,
            include_center=False,
            radius=self.model.comm_range
        )

        # Filter to HarvesterAgents only (not fruit)
        agent_neighbors = [n for n in neighbors if isinstance(n, HarvesterAgent)]

        if not agent_neighbors:
            return

        idle_neighbors = []
        for n in agent_neighbors:
            if n.current_target:
                continue  # Has a target, not idle

            # Check for nearby fruit
            nearby = n._find_closest_fruit_nearby(search_radius=2)
            if nearby:
                continue  # Has nearby fruit, not idle

            # Check idle duration
            if n.idle_steps >= 2:
                idle_neighbors.append(n)  # Truly idle

        if not idle_neighbors:
            return  # No truly idle agents

        num_agents_in_range = len(agent_neighbors)

        if self.model.comm_range > 4:
            range_interference = 0.05 * (self.model.comm_range - 4)
            crowd_interference = 0.02 * max(0, num_agents_in_range - 5)
            total_interference = min(range_interference + crowd_interference, 0.5)

            if random.random() < total_interference:
                return  # Message lost to interference

        idle_neighbors.sort(
            key=lambda n: self._chebyshev_distance(n.pos, available_fruits[0])
        )

        # Assign different fruits to different agents
        max_recipients = min(len(idle_neighbors), 5)  # Send to up to 5 agents

        for i, neighbor in enumerate(idle_neighbors[:max_recipients]):
            # Cycle through available fruits to distribute different targets
            fruit_index = i % len(available_fruits)
            target_fruit = available_fruits[fruit_index]

            neighbor.receive_message(target_fruit)
            self.messages_sent += 1

    def _get_ranked_fruits(self):
        """
        Get multiple ranked fruits for distributed target assignment.

        Returns a list of known fruit positions sorted by value score

        Returns:
            list: List of (x,y) fruit positions sorted by value (best first)
        """
        scored_fruits = []

        # Only consider fruit we've discovered
        for fruit_pos in list(self.discovered_fruits):  # Copy to allow modification
            # Skip if we know this cell is empty
            if fruit_pos in self.empty_cells:
                self.discovered_fruits.discard(fruit_pos)
                continue

            # Validate fruit still exists and is available
            fruit_available = False
            for fruit in self.model.fruits:
                if fruit.pos == fruit_pos and fruit.available:
                    fruit_available = True
                    break

            if not fruit_available:
                # Fruit was harvested, remove from our knowledge
                self.discovered_fruits.discard(fruit_pos)
                continue

            # Calculate value score
            distance = self._chebyshev_distance(self.pos, fruit_pos)
            density = self._calculate_local_density(fruit_pos)

            # Score: higher density is better, shorter distance is better
            score = density - (distance * 0.1)
            scored_fruits.append((fruit_pos, score))

        # Sort by score descending (best fruits first)
        scored_fruits.sort(key=lambda x: x[1], reverse=True)

        # Return just the positions (top 10 to limit communication overhead)
        return [pos for pos, _ in scored_fruits[:10]]

    def _find_nearest_fruit(self):
        """
        Find the nearest available fruit position from discovered fruits.
        Returns:
            tuple: (x,y) of nearest known fruit, or None if no fruit known
        """
        min_dist = float('inf')
        nearest = None

        for fruit_pos in list(self.discovered_fruits):
            if fruit_pos in self.empty_cells:
                self.discovered_fruits.discard(fruit_pos)
                continue

            # Validate fruit still available
            fruit_available = False
            for fruit in self.model.fruits:
                if fruit.pos == fruit_pos and fruit.available:
                    fruit_available = True
                    break

            if not fruit_available:
                self.discovered_fruits.discard(fruit_pos)
                continue

            dist = self._chebyshev_distance(self.pos, fruit_pos)
            if dist < min_dist:
                min_dist = dist
                nearest = fruit_pos

        return nearest

    def _chebyshev_distance(self, pos1, pos2):
        """
        Calculate Chebyshev distance between two positions.

        Chebyshev distance = max(|x1-x2|, |y1-y2|)

        Args:
            pos1: (x,y) tuple
            pos2: (x,y) tuple

        Returns:
            int: Chebyshev distance between positions
        """
        return max(abs(pos1[0] - pos2[0]), abs(pos1[1] - pos2[1]))

    def receive_message(self, fruit_pos):
        """
        Receive a message about fruit location from another agent.
        Args:
            fruit_pos: (x,y) position of reported fruit
        """
        self.messages_received += 1
        self.discovered_fruits.add(fruit_pos)
        if not self.current_target:
            self.current_target = fruit_pos


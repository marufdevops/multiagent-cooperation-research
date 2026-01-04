"""
Harvester Agent for fruit collection simulation.

================================================================================
PURPOSE & DESIGN RATIONALE
================================================================================
This module implements the harvester agent that moves through the
grid, collects fruit, and communicates with nearby agents to share information
about fruit locations.

REALISTIC KNOWLEDGE MODEL:
Agents do NOT have global knowledge of fruit locations. They only know about:
1. Fruit they personally discover by visiting a cell
2. Fruit locations received via communication from other agents

This makes communication genuinely valuable - it's the only way to learn about
distant fruit without physically exploring the entire grid.

BEHAVIORAL ALGORITHM:
The agent uses a hierarchical decision process for movement:
1. Check for nearby fruit (radius=2) - local sensing, immediate opportunity
2. Pursue communicated target if valid - coordination via communication
3. Explore using Levy Flight + Density Heatmap

Explanations:
1. Levy Flight: Occasional long-range jumps (20% probability) help escape
   local minima and discover new fruit clusters.

2. Visited Cell Memory: Agents track cells they've visited and found empty.
   This prevents wasteful revisiting of harvested areas.

3. Density Heatmap: When exploring, agents bias movement toward cells with
   higher local fruit density (uses local sensing, not global knowledge).

4. Target Validation: Before moving toward a communicated target, agents
   verify the fruit still exists (hasn't been harvested by another agent).

5. Nearby Fruit Priority: Agents check for nearby fruit (local sensing)
   before pursuing distant communicated targets.

COMMUNICATION PROTOCOL:
- Agents can only share fruit they have discovered (realistic)
- Messages are sent to idle neighbors within communication range
- Communication range is configurable (0 = disabled, 2/4/6/8 = experimental)

================================================================================
"""
import random
import numpy as np
from mesa import Agent


class HarvesterAgent(Agent):
    """
    Harvesting agent that collects fruit and communicates with neighbors.

    This agent implements a sophisticated movement and communication strategy
    designed to efficiently harvest fruit in a multi-agent environment. The
    agent balances local exploitation (harvesting nearby fruit) with global
    exploration (finding new fruit clusters).

    Attributes:
        harvested (int): Total fruit collected by this agent
        messages_sent (int): Messages sent this step (reset each step)
        messages_received (int): Total messages received (lifetime)
        current_target (tuple): Target (x,y) position from communication, or None
        travel_distance (int): Total steps moved (for efficiency analysis)
        visited_cells (set): All (x,y) positions visited (for coverage metric)
        empty_cells (set): Positions known to have no fruit (optimization)

    Design Notes:
        - Movement uses Moore neighborhood (8 directions + stay)
        - Communication uses Chebyshev distance for range calculation
        - Agents cannot overlap (collision avoidance via cell checking)
    """

    def __init__(self, model):
        """
        Initialize harvester agent with default state.

        Args:
            model: The HarvestModel instance this agent belongs to

        The agent starts with no harvested fruit, no target, and empty
        memory of visited/empty cells.
        """
        super().__init__(model)

        # Performance tracking
        self.harvested = 0  # Fruit collected (primary metric)
        self.messages_sent = 0  # Messages this step (reset each step)
        self.messages_received = 0  # Lifetime message count

        # Navigation state
        self.current_target = None  # (x,y) target from communication
        self.travel_distance = 0  # Total movement steps
        self.last_pos = None  # Previous position for distance tracking
        self.visited_cells = set()  # All visited positions (for coverage)

        # Memory for exploration (realistic - no global fruit knowledge)
        self.empty_cells = set()  # Cells confirmed to have no fruit
        self.discovered_fruits = set()  # Fruit positions agent has found or heard about
        
    def step(self):
        """
        Execute one complete agent step: move, harvest, then communicate.

        The step order is important:
        1. Move - Agent relocates based on decision hierarchy
        2. Harvest - Collect fruit if present at new position
        3. Communicate - Share fruit information with nearby agents

        This order ensures agents harvest before communicating, so they
        don't send messages about fruit they're about to collect.
        """
        self.last_pos = self.pos
        self.move()

        # Track metrics for analysis
        if self.last_pos and self.pos != self.last_pos:
            self.travel_distance += 1
        if self.pos:
            self.visited_cells.add(self.pos)

        self.harvest()
        self.communicate()

    def move(self):
        """
        Execute movement decision using hierarchical strategy.

        Decision Hierarchy (in order of priority):
        1. Stop if no fruit remains (simulation complete)
        2. Move to nearby fruit if within search_radius=2 (local sensing)
        3. Move to communicated target if valid
        4. Move to nearest remembered fruit from discovered_fruits
        5. Explore using Levy Flight + Density Heatmap

        Design Rationale:
            - Local fruit priority prevents inefficient long-distance travel
            - Target validation avoids chasing already-harvested fruit
            - Remembered fruit provides direction when no immediate targets
            - Levy Flight + Density exploration balances coverage and efficiency
        """
        # Early termination: don't move if simulation is done
        remaining_fruit = sum(1 for f in self.model.fruits if f.available)
        if remaining_fruit == 0:
            return

        # Priority 1: Check for immediately accessible fruit (also discovers them)
        nearby_fruit = self._find_closest_fruit_nearby(search_radius=2)

        if nearby_fruit:
            # Override any distant target with nearby opportunity
            self.current_target = nearby_fruit
            self._move_toward(nearby_fruit)
        elif self.current_target:
            # Priority 2: Pursue communicated target if still valid
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

        This simulates the agent's "vision" - they can see fruit within search_radius.
        Any fruit seen is added to discovered_fruits (memory) for future navigation.

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

        Uses simple greedy movement: move in the direction that reduces
        distance to target. Diagonal movement is allowed (Moore neighborhood).

        Args:
            target_pos: (x,y) tuple of destination position

        Notes:
            - Movement blocked if target cell contains another HarvesterAgent
            - Target is cleared upon reaching destination
            - Out-of-bounds targets are abandoned
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

        Side Effects:
            - Adds target to empty_cells if fruit not found (optimization)
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
        Select movement direction biased toward fruit-dense areas.

        This implements the Density Heatmap improvement - when exploring,
        prefer to move toward cells that have more fruit in their neighborhood.
        This helps agents find fruit clusters more efficiently.

        Args:
            candidates: List of valid (x,y) positions to consider

        Returns:
            tuple: (x,y) position with highest local fruit density
        """
        best_move = candidates[0]
        best_density = self._calculate_local_density(candidates[0])

        for candidate in candidates[1:]:
            density = self._calculate_local_density(candidate)
            if density > best_density:
                best_density = density
                best_move = candidate

        return best_move

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

        If fruit is present and available, harvest it and increment
        the agent's harvest count. Also updates Visited Cell Memory
        to mark positions without fruit.

        Side Effects:
            - Increments self.harvested if fruit found
            - Marks fruit as unavailable (fruit.harvest())
            - Clears current_target after successful harvest
            - Adds position to empty_cells if no fruit found
        """
        if not self.pos:
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
                    # Remove from discovered since we just harvested it
                    self.discovered_fruits.discard(self.pos)
                    self.empty_cells.add(self.pos)  # Now empty
                    break  # Only harvest one fruit per step
                else:
                    # Fruit exists but already harvested by another agent
                    self.discovered_fruits.discard(self.pos)
                    fruit_found = True  # There was fruit, just already taken

        # Update Visited Cell Memory
        if not fruit_found and self.pos not in self.empty_cells:
            self.empty_cells.add(self.pos)
            self.discovered_fruits.discard(self.pos)  # Definitely no fruit here

    def communicate(self):
        """
        Share fruit location information with nearby idle agents.

        This implements the communication protocol for RQ1. Agents broadcast
        information about known fruit to neighbors within communication range.

        Message Filtering:
        - Only send to agents without a current target (idle agents)
        - Prioritize closer agents (they can reach fruit faster)
        - Limit to top 3 recipients (reduce message flooding)

        Communication Protocol:
        1. Find nearby agents within comm_range (Chebyshev distance)
        2. Find best fruit to share (density + distance score)
        3. Filter to idle recipients only
        4. Send to closest 3 idle agents

        Notes:
            - comm_range=0 disables communication entirely (control condition)
            - Messages are counted for efficiency metric calculation
        """
        if not self.pos or self.model.comm_range == 0:
            return  # No communication in control condition

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

        # Determine best fruit to share
        best_fruit = self._find_best_fruit()

        if not best_fruit:
            return

        # Message filtering: only contact idle agents
        idle_neighbors = [n for n in agent_neighbors if not n.current_target]

        if not idle_neighbors:
            return  # All neighbors busy

        # Prioritize by distance to fruit (closer agents first)
        idle_neighbors.sort(
            key=lambda n: self._chebyshev_distance(n.pos, best_fruit)
        )

        # Send to top 3 closest idle agents
        for neighbor in idle_neighbors[:3]:
            neighbor.receive_message(best_fruit)
            self.messages_sent += 1

    def _find_best_fruit(self):
        """
        Find the highest-value fruit to share with other agents.

        REALISTIC IMPLEMENTATION: Only considers fruit the agent has personally
        discovered or learned about through communication. No global knowledge.

        Value is computed as a combination of:
        - Local fruit density (prefer fruit in clusters)
        - Distance from sender (prefer closer fruit)

        Returns:
            tuple: (x,y) position of best fruit, or None if no known fruit available
        """
        best_fruit = None
        best_score = -float('inf')

        # Only consider fruit we've discovered (realistic - no global knowledge)
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

            if score > best_score:
                best_score = score
                best_fruit = fruit_pos

        return best_fruit

    def _find_nearest_fruit(self):
        """
        Find the nearest available fruit position from discovered fruits.

        REALISTIC IMPLEMENTATION: Only considers fruit the agent has personally
        discovered or learned about through communication. No global knowledge.

        Returns:
            tuple: (x,y) of nearest known fruit, or None if no fruit known
        """
        min_dist = float('inf')
        nearest = None

        # Only consider fruit we've discovered (realistic - no global knowledge)
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
        This corresponds to the number of king moves on a chessboard
        and is the standard distance metric for 8-connected grids.

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

        The agent learns about the fruit location (adds to discovered_fruits)
        and sets it as target if idle. This implements realistic information
        sharing - agents only know about fruit they discover or hear about.

        Args:
            fruit_pos: (x,y) position of reported fruit
        """
        self.messages_received += 1
        # Learn about this fruit location (realistic discovery)
        self.discovered_fruits.add(fruit_pos)
        if not self.current_target:
            self.current_target = fruit_pos


"""
Harvester Agent for fruit collection simulation.

Implements Tier 1 algorithm improvements:

TIER 1:
1. Levy Flight - Power-law distributed step sizes for better exploration
2. Visited Cell Memory - Avoids revisiting empty areas
3. Density Heatmap - Biases movement toward fruit clusters
4. Target Validation - Ensures target fruit still exists
5. Nearby Fruit Priority - Always prioritize close fruit over distant targets
"""
import random
import numpy as np
from mesa import Agent


class HarvesterAgent(Agent):
    """Agent that moves, harvests fruit, and communicates with nearby agents."""

    def __init__(self, model):
        """
        Initialize harvester agent.

        Args:
            model: The model instance
        """
        super().__init__(model)
        self.harvested = 0
        self.messages_sent = 0
        self.messages_received = 0
        self.current_target = None
        self.travel_distance = 0
        self.last_pos = None
        self.visited_cells = set()  # Track unique cells visited

        # Tier 1 Improvements
        self.empty_cells = set()  # Track cells with no fruit (avoid revisiting)
        
    def step(self):
        """Execute one step: move, harvest, communicate."""
        self.last_pos = self.pos
        self.move()

        # Track travel distance and visited cells
        if self.last_pos and self.pos != self.last_pos:
            self.travel_distance += 1
        if self.pos:
            self.visited_cells.add(self.pos)

        self.harvest()
        self.communicate()
        
    def move(self):
        """Move to adjacent cell with Tier 1 improvements."""
        # First, check if there's fruit nearby to harvest (prioritize close fruit)
        nearby_fruit = self._find_closest_fruit_nearby(search_radius=2)

        if nearby_fruit:
            # Move toward nearby fruit instead of distant target
            self.current_target = nearby_fruit
            self._move_toward(nearby_fruit)
        elif self.current_target:
            # Target Validation: Check if target still exists
            if self._is_target_valid():
                # Move toward target
                self._move_toward(self.current_target)
            else:
                # Target was harvested, clear it and search
                self.current_target = None
                self._move_with_levy_and_density()
        else:
            # Levy Flight + Density exploration
            self._move_with_levy_and_density()

    def _find_closest_fruit_nearby(self, search_radius=2):
        """Find closest available fruit within search radius."""
        if not self.pos:
            return None

        min_dist = float('inf')
        closest = None

        for fruit in self.model.fruits:
            if not fruit.available or fruit.pos in self.empty_cells:
                continue

            dist = self._chebyshev_distance(self.pos, fruit.pos)

            # Only consider fruit within search radius
            if dist <= search_radius and dist < min_dist:
                min_dist = dist
                closest = fruit.pos

        return closest

    def _move_toward(self, target_pos):
        """Move one step toward target position (greedy movement)."""
        if not self.pos:
            return

        x, y = self.pos
        tx, ty = target_pos

        # Greedy movement towards the target
        dx = 0 if tx == x else (1 if tx > x else -1)
        dy = 0 if ty == y else (1 if ty > y else -1)

        new_pos = (x + dx, y + dy)

        # Check if new position is valid
        if self.model.grid.out_of_bounds(new_pos):
            self.current_target = None
            return

        # Check if cell is occupied by another HarvesterAgent (prevent agent overlap)
        cell_contents = self.model.grid.get_cell_list_contents([new_pos])
        has_harvester = any(isinstance(obj, HarvesterAgent) and obj != self for obj in cell_contents)

        if has_harvester:
            # Cell occupied by another agent, don't move
            return

        # Move to the new position
        self.model.grid.move_agent(self, new_pos)

        # Clear target if reached
        if new_pos == target_pos:
            self.current_target = None

    def _is_target_valid(self):
        """Check if current target fruit still exists and is available."""
        if not self.current_target:
            return False

        # Check if target is in empty_cells (already harvested)
        if self.current_target in self.empty_cells:
            return False

        # Verify fruit still exists at target location
        for fruit in self.model.fruits:
            if fruit.pos == self.current_target and fruit.available:
                return True

        # Mark as empty if not found
        self.empty_cells.add(self.current_target)
        return False

    def _move_with_levy_and_density(self):
        """Move using Levy Flight biased toward high-density areas."""
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,
            include_center=False
        )

        if not possible_steps:
            return

        # Filter out visited empty cells (Visited Cell Memory)
        unvisited_steps = [s for s in possible_steps if s not in self.empty_cells]

        # If all neighbors are empty, use Levy Flight for long-range jump
        if not unvisited_steps:
            new_position = self._levy_flight_jump(possible_steps)
        else:
            # Bias toward high-density areas (Density Heatmap)
            new_position = self._density_biased_move(unvisited_steps)

        if new_position and not self.model.grid.out_of_bounds(new_position):
            # Check if cell is occupied by another HarvesterAgent (prevent agent overlap)
            cell_contents = self.model.grid.get_cell_list_contents([new_position])
            has_harvester = any(isinstance(obj, HarvesterAgent) and obj != self for obj in cell_contents)

            if not has_harvester:
                # Cell is free of other agents, move to it
                self.model.grid.move_agent(self, new_position)

    def _levy_flight_jump(self, possible_steps):
        """Implement Levy Flight: occasional long-range jumps."""
        # 80% chance of normal move, 20% chance of long-range jump
        if random.random() < 0.8:
            return random.choice(possible_steps)

        # Long-range jump: move 2-4 cells in random direction
        jump_distance = random.randint(2, 4)
        angle = random.uniform(0, 2 * np.pi)
        dx = int(jump_distance * np.cos(angle))
        dy = int(jump_distance * np.sin(angle))

        new_pos = (self.pos[0] + dx, self.pos[1] + dy)

        # Clamp to grid bounds
        new_pos = (
            max(0, min(new_pos[0], self.model.grid.width - 1)),
            max(0, min(new_pos[1], self.model.grid.height - 1))
        )

        return new_pos

    def _density_biased_move(self, candidates):
        """Move toward high-density fruit areas (Density Heatmap)."""
        # Calculate local fruit density for each candidate
        best_move = candidates[0]
        best_density = self._calculate_local_density(candidates[0])

        for candidate in candidates[1:]:
            density = self._calculate_local_density(candidate)
            if density > best_density:
                best_density = density
                best_move = candidate

        return best_move

    def _calculate_local_density(self, pos):
        """Calculate fruit density in neighborhood of position."""
        # Look in 3x3 neighborhood around position
        neighborhood = self.model.grid.get_neighborhood(
            pos,
            moore=True,
            include_center=True,
            radius=1
        )

        fruit_count = 0
        for cell in neighborhood:
            if cell not in self.empty_cells:
                # Count available fruit in this cell
                cell_contents = self.model.grid.get_cell_list_contents([cell])
                for obj in cell_contents:
                    if hasattr(obj, 'is_fruit') and obj.is_fruit and obj.available:
                        fruit_count += 1

        return fruit_count
    

    
    def harvest(self):
        """Harvest fruit at current position if available."""
        if not self.pos:
            return

        cell_contents = self.model.grid.get_cell_list_contents([self.pos])

        fruit_found = False
        for obj in cell_contents:
            if hasattr(obj, 'is_fruit') and obj.is_fruit and obj.available:
                obj.harvest()
                self.harvested += 1
                self.current_target = None
                fruit_found = True
                break

        # If no fruit at this location, mark it as empty (Visited Cell Memory)
        if not fruit_found and self.pos not in self.empty_cells:
            self.empty_cells.add(self.pos)
    
    def communicate(self):
        """Share information with intelligent message filtering."""
        if not self.pos or self.model.comm_range == 0:
            return

        # Find nearby agents within communication range (Chebyshev distance)
        neighbors = self.model.grid.get_neighbors(
            self.pos,
            moore=True,
            include_center=False,
            radius=self.model.comm_range
        )

        # Filter to only HarvesterAgent instances
        agent_neighbors = [n for n in neighbors if isinstance(n, HarvesterAgent)]

        if not agent_neighbors:
            return

        # Find best fruit to share (Tier 2: Message Filtering)
        best_fruit = self._find_best_fruit()

        if not best_fruit:
            return

        # FILTERING: Only send to idle agents (no current target)
        idle_neighbors = [n for n in agent_neighbors if not n.current_target]

        if not idle_neighbors:
            return  # No idle agents, don't send

        # FILTERING: Prioritize by distance (closer agents get priority)
        idle_neighbors.sort(
            key=lambda n: self._chebyshev_distance(n.pos, best_fruit)
        )

        # Send to top 3 closest idle agents (limit broadcast)
        for neighbor in idle_neighbors[:3]:
            neighbor.receive_message(best_fruit)
            self.messages_sent += 1
    
    def _find_best_fruit(self):
        """Find highest-value fruit to share (Tier 2: Message Filtering)."""
        best_fruit = None
        best_score = -float('inf')

        for fruit in self.model.fruits:
            if not fruit.available or fruit.pos in self.empty_cells:
                continue

            # Score = density_bonus - distance_penalty
            distance = self._chebyshev_distance(self.pos, fruit.pos)
            density = self._calculate_local_density(fruit.pos)

            # Prefer closer, denser fruit
            score = density - (distance * 0.1)

            if score > best_score:
                best_score = score
                best_fruit = fruit.pos

        return best_fruit

    def _find_nearest_fruit(self):
        """Find nearest available fruit position (fallback)."""
        min_dist = float('inf')
        nearest = None

        for fruit in self.model.fruits:
            if fruit.available:
                dist = self._chebyshev_distance(self.pos, fruit.pos)
                if dist < min_dist:
                    min_dist = dist
                    nearest = fruit.pos

        return nearest
    
    def _chebyshev_distance(self, pos1, pos2):
        """Calculate Chebyshev distance (max of absolute differences)."""
        return max(abs(pos1[0] - pos2[0]), abs(pos1[1] - pos2[1]))
    
    def receive_message(self, fruit_pos):
        """Receive message about fruit location."""
        self.messages_received += 1
        if not self.current_target:
            self.current_target = fruit_pos


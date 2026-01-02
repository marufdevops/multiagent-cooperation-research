"""
Harvester Agent for fruit collection simulation.

Implements Tier 1 + Tier 2 algorithm improvements:

TIER 1:
1. Levy Flight - Power-law distributed step sizes for better exploration
2. Visited Cell Memory - Avoids revisiting empty areas
3. Density Heatmap - Biases movement toward fruit clusters
4. Target Validation - Ensures target fruit still exists

TIER 2:
5. BFS Exploration - Systematic frontier-based exploration
6. A* Pathfinding - Optimal path to target fruit
7. Message Filtering - Intelligent message routing to idle agents
"""
import random
import numpy as np
from heapq import heappush, heappop
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

        # Tier 2 Improvements
        self.frontier = set()  # BFS frontier cells
        self.path_to_target = []  # A* path queue
        self.use_bfs = True  # Toggle between BFS and Levy Flight
        
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
        """Move to adjacent cell with Tier 1 + Tier 2 improvements."""
        if self.current_target:
            # Target Validation: Check if target still exists
            if self._is_target_valid():
                # Move toward target using A* pathfinding
                self._move_toward_with_astar(self.current_target)
            else:
                # Target was harvested, clear it and search
                self.current_target = None
                self._move_with_bfs()
        else:
            # BFS exploration to find fruit
            self._move_with_bfs()

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

    def _move_with_bfs(self):
        """Move using BFS exploration to systematically find fruit."""
        # Initialize frontier on first call
        if not self.frontier:
            self._initialize_frontier()

        # If frontier is empty, fall back to Levy Flight
        if not self.frontier:
            self._move_with_levy_fallback()
            return

        # Find closest frontier cell
        closest_frontier = min(
            self.frontier,
            key=lambda cell: self._chebyshev_distance(self.pos, cell)
        )

        # Move toward frontier cell using A*
        if not self.path_to_target or self.path_to_target[-1] != closest_frontier:
            self.path_to_target = self._a_star_search(self.pos, closest_frontier)

        # Follow A* path
        if self.path_to_target:
            next_cell = self.path_to_target.pop(0)
            if not self.model.grid.out_of_bounds(next_cell):
                self.model.grid.move_agent(self, next_cell)

        # Expand frontier as we visit new cells
        self._expand_frontier()

    def _initialize_frontier(self):
        """Initialize frontier with cells adjacent to starting position."""
        neighborhood = self.model.grid.get_neighborhood(
            self.pos, moore=True, include_center=False
        )
        self.frontier.update(neighborhood)

    def _expand_frontier(self):
        """Expand frontier as new cells are visited."""
        neighborhood = self.model.grid.get_neighborhood(
            self.pos, moore=True, include_center=False
        )
        for cell in neighborhood:
            if cell not in self.visited_cells and cell not in self.empty_cells:
                self.frontier.add(cell)

        # Remove current cell from frontier (already visited)
        self.frontier.discard(self.pos)

    def _move_with_levy_fallback(self):
        """Fallback to Levy Flight when frontier is exhausted."""
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
    
    def _move_toward_with_astar(self, target_pos):
        """Move toward target using A* pathfinding."""
        # Compute path if not already computed
        if not self.path_to_target or self.path_to_target[-1] != target_pos:
            self.path_to_target = self._a_star_search(self.pos, target_pos)

        # Follow A* path
        if self.path_to_target:
            next_cell = self.path_to_target.pop(0)
            if not self.model.grid.out_of_bounds(next_cell):
                self.model.grid.move_agent(self, next_cell)

        # Clear target if reached
        if self.pos == target_pos:
            self.path_to_target = []
            self.current_target = None

    def _a_star_search(self, start, goal):
        """A* pathfinding algorithm to find optimal path to goal."""
        open_set = []
        heappush(open_set, (0, start))
        came_from = {}
        g_score = {start: 0}
        f_score = {start: self._manhattan_distance(start, goal)}
        closed_set = set()

        while open_set:
            _, current = heappop(open_set)

            if current == goal:
                # Reconstruct path
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                return path[::-1]

            if current in closed_set:
                continue
            closed_set.add(current)

            # Explore neighbors
            neighbors = self.model.grid.get_neighborhood(
                current, moore=True, include_center=False
            )

            for neighbor in neighbors:
                if self.model.grid.out_of_bounds(neighbor) or neighbor in closed_set:
                    continue

                tentative_g = g_score[current] + 1

                if neighbor not in g_score or tentative_g < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g
                    f = tentative_g + self._manhattan_distance(neighbor, goal)
                    f_score[neighbor] = f
                    heappush(open_set, (f, neighbor))

        return []  # No path found

    def _manhattan_distance(self, pos1, pos2):
        """Calculate Manhattan distance between two positions."""
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])
    
    def harvest(self):
        """Harvest fruit at current position if available."""
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
        if self.model.comm_range == 0:
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


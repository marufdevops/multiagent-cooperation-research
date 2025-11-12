"""
Harvester Agent for fruit collection simulation (WORK IN PROGRESS).
Mesa 3.0 convention: no unique_id in constructor, only model and parameters.

TODO: Test with large grids (performance optimization needed?)
TODO: Improve movement strategy (currently greedy + random walk)
FIXME: Agents sometimes cluster in corners - need better exploration
NOTE: Communication uses Chebyshev distance (needs verification)
"""
import random
from mesa import Agent


class HarvesterAgent(Agent):
    """Agent that moves, harvests fruit, and communicates with nearby agents."""
    
    def __init__(self, model):
        """
        Initialize harvester agent.

        Args:
            model: The model instance (Mesa 3.0 convention)
        """
        super().__init__(model)
        self.harvested = 0
        self.messages_sent = 0
        self.messages_received = 0
        self.current_target = None
        self.travel_distance = 0
        self.last_pos = None
        self.visited_cells = set()  # Track unique cells visited
        
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
        """Move to adjacent cell (Moore neighborhood)."""
        if self.current_target:
            # Move toward target
            self._move_toward(self.current_target)
        else:
            # Random walk
            possible_steps = self.model.grid.get_neighborhood(
                self.pos,
                moore=True,
                include_center=False
            )
            if possible_steps:
                new_position = random.choice(possible_steps)
                self.model.grid.move_agent(self, new_position)
    
    def _move_toward(self, target_pos):
        """Move one step toward target position."""
        x, y = self.pos
        tx, ty = target_pos
        
        # Simple greedy movement
        dx = 0 if tx == x else (1 if tx > x else -1)
        dy = 0 if ty == y else (1 if ty > y else -1)
        
        new_pos = (x + dx, y + dy)
        
        # Check if new position is valid
        if self.model.grid.out_of_bounds(new_pos):
            self.current_target = None
            return
            
        self.model.grid.move_agent(self, new_pos)
        
        # Clear target if reached
        if new_pos == target_pos:
            self.current_target = None
    
    def harvest(self):
        """Harvest fruit at current position if available."""
        cell_contents = self.model.grid.get_cell_list_contents([self.pos])
        
        for obj in cell_contents:
            if hasattr(obj, 'is_fruit') and obj.is_fruit and obj.available:
                obj.harvest()
                self.harvested += 1
                self.current_target = None
                break
    
    def communicate(self):
        """Share information with agents within communication range."""
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
        
        # Find nearest fruit to share
        nearest_fruit = self._find_nearest_fruit()
        
        if nearest_fruit:
            # Broadcast fruit location to neighbors
            for neighbor in agent_neighbors:
                if not neighbor.current_target:
                    neighbor.receive_message(nearest_fruit)
                    self.messages_sent += 1
    
    def _find_nearest_fruit(self):
        """Find nearest available fruit position."""
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


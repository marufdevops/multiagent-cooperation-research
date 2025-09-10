from __future__ import annotations
from typing import Tuple, List, Dict, Optional
import random

from mesa import Model
from mesa.space import MultiGrid
from mesa.time import BaseScheduler

from .agents import HarvesterAgent, Message, CellPatch


class OrchardModel(Model):
    """
    Week-2 core Mesa model with:
    - MultiGrid environment with fruit map and simple regeneration
    - Agents (HarvesterAgent) placed randomly
    - Internal message delivery with bounded communication range R (per agent)
    - Staged step: sense -> decide -> deliver -> act -> regenerate
    """

    def __init__(
        self,
        width: int = 20,
        height: int = 20,
        num_agents: int = 10,
        comm_range: int = 3,
        cooperative_share: float = 1.0,
        fruit_spawn_prob: float = 0.05,
        regen_prob: float = 0.01,
        max_fruit_per_cell: int = 3,
        default_ttl: int = 0,
        seed: Optional[int] = None,
    ) -> None:
        super().__init__()
        if seed is not None:
            self.random.seed(seed)
            random.seed(seed)

        self.grid = MultiGrid(width, height, torus=False)
        self.schedule = BaseScheduler(self)

        # Communication
        self.default_ttl = default_ttl
        self._msg_id = 0

        # Fruit map
        self.max_fruit_per_cell = max_fruit_per_cell
        self.fruit_spawn_prob = fruit_spawn_prob
        self.regen_prob = regen_prob
        self.fruit_map: List[List[int]] = [
            [0 for _ in range(height)] for _ in range(width)
        ]
        self._initial_spawn()

        # Place background patches for visualization (one per cell)
        for x in range(self.grid.width):
            for y in range(self.grid.height):
                patch = CellPatch((x, y), self)
                self.grid.place_agent(patch, (x, y))

        # Claimed targets (for cooperative avoidance)
        self.claimed_targets: set[Tuple[int, int]] = set()

        # Create agents
        for i in range(num_agents):
            strategy = "cooperative" if (i / max(1, num_agents) < cooperative_share) else "competitive"
            a = HarvesterAgent(
                unique_id=i,
                model=self,
                communication_range=comm_range,
                strategy=strategy,
                sensor_radius=2,
            )
            self.schedule.add(a)
            # Random empty placement
            placed = False
            while not placed:
                x = self.random.randrange(self.grid.width)
                y = self.random.randrange(self.grid.height)
                if self.is_cell_free((x, y)):
                    self.grid.place_agent(a, (x, y))
                    placed = True

    # ---------------------------- Fruit dynamics ----------------------------
    def _initial_spawn(self) -> None:
        for x in range(self.grid.width):
            for y in range(self.grid.height):
                if random.random() < self.fruit_spawn_prob:
                    self.fruit_map[x][y] = random.randint(1, self.max_fruit_per_cell)

    def regenerate(self) -> None:
        for x in range(self.grid.width):
            for y in range(self.grid.height):
                if self.fruit_map[x][y] < self.max_fruit_per_cell and random.random() < self.regen_prob:
                    self.fruit_map[x][y] += 1

    def get_fruit_at(self, pos: Tuple[int, int]) -> int:
        x, y = pos
        if 0 <= x < self.grid.width and 0 <= y < self.grid.height:
            return self.fruit_map[x][y]
        return 0

    def harvest_at(self, pos: Tuple[int, int], amount: int = 1) -> int:
        x, y = pos
        if 0 <= x < self.grid.width and 0 <= y < self.grid.height:
            harvested = min(amount, self.fruit_map[x][y])
            self.fruit_map[x][y] -= harvested
            return harvested
        return 0

    # --------------------------- Messaging support --------------------------
    def next_msg_id(self) -> int:
        self._msg_id += 1
        return self._msg_id

    def deliver_messages(self) -> None:
        """Range-bounded local broadcast with optional TTL (store-and-forward).
        For Week-2, we keep TTL=0 by default (no relays) to keep things simple."""
        # Snapshot outboxes, then clear
        outboxes: Dict[int, List[Message]] = {}
        for a in self.schedule.agents:
            if isinstance(a, HarvesterAgent) and a.outbox:
                outboxes[a.unique_id] = list(a.outbox)
                a.outbox.clear()

        # Deliver to neighbors within each sender's communication range
        for a in self.schedule.agents:
            if a.unique_id not in outboxes:
                continue
            msgs = outboxes[a.unique_id]
            # Neighborhood within the agent's own communication range
            nbr_cells = self.grid.get_neighborhood(
                a.pos, moore=True, include_center=False, radius=a.communication_range
            )
            receivers: List[HarvesterAgent] = []
            for c in nbr_cells:
                for agent in self.grid.get_cell_list_contents(c):
                    if isinstance(agent, HarvesterAgent):
                        receivers.append(agent)

            for m in msgs:
                # Direct delivery this tick
                for r in receivers:
                    # Dedup handled on receiver side via seen_ids
                    r.inbox.append(m)

                # Optional: TTL relay (not used by default in Week-2)
                # If needed later, schedule relays by decrementing ttl and enqueuing to receivers' outboxes

    # --------------------------- Movement helpers ---------------------------
    def is_cell_free(self, pos: Tuple[int, int]) -> bool:
        x, y = pos
        if not (0 <= x < self.grid.width and 0 <= y < self.grid.height):
            return False
        occupants = self.grid.get_cell_list_contents((x, y))
        # Allow moving into fruit cells; consider cell free if no agents are there
        return all(not isinstance(o, HarvesterAgent) for o in occupants)

    # ------------------------------- Step -----------------------------------
    def step(self) -> None:
        # Phase 1: sense
        for a in self.schedule.agents:
            if isinstance(a, HarvesterAgent):
                a.sense()
        # Phase 2: decide (may enqueue messages)
        for a in self.schedule.agents:
            if isinstance(a, HarvesterAgent):
                a.decide()
        # Phase 3: communication delivery
        self.deliver_messages()
        # Phase 4: act (move/harvest)
        for a in self.schedule.agents:
            if isinstance(a, HarvesterAgent):
                a.act()
        # Phase 5: environment dynamics (regen)
        self.regenerate()
        # Advance time
        self.schedule.time += 1


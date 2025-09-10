from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Tuple, Dict, Optional, Set
import itertools
import math
import random

from mesa import Agent


@dataclass
class Message:
    msg_id: int
    mtype: str  # 'HOTSPOT' | 'CLAIM' | 'RELEASE' | 'STATUS'
    sender: int
    pos: Tuple[int, int]
    ttl: int
    payload: Dict


class CellPatch(Agent):
    """Visual-only cell patch for CanvasGrid background. Not scheduled."""
    def __init__(self, pos: Tuple[int, int], model) -> None:
        super().__init__(unique_id=f"patch-{pos[0]}-{pos[1]}", model=model)
    def step(self) -> None:
        return


class HarvesterAgent(Agent):
    """
    Core Week-2 agent:
    - Tracks position (via Mesa grid)
    - Keeps fruit inventory and known fruit locations
    - Has a communication range parameter (handled by model bus)
    - Moves toward fruit (greedy toward chosen target) and harvests
    - Shares info if cooperative; ignores claims if competitive
    """

    def __init__(
        self,
        unique_id: int,
        model,
        communication_range: int,
        strategy: str = "cooperative",
        sensor_radius: int = 2,
    ) -> None:
        super().__init__(unique_id, model)
        assert strategy in ("cooperative", "competitive")
        self.communication_range: int = communication_range
        self.strategy: str = strategy
        self.sensor_radius: int = sensor_radius

        self.fruit_collected: int = 0
        # List of known fruit cells with a simple score (e.g., 1 per fruit cell)
        self.known_fruit: Dict[Tuple[int, int], float] = {}

        # Simple messaging buffers (model delivers to inbox)
        self.inbox: List[Message] = []
        self.outbox: List[Message] = []
        self._seen_ids: Set[int] = set()

        # Current target (fruit cell) we are heading toward
        self.target: Optional[Tuple[int, int]] = None

    # ---- Perception ----
    def sense(self) -> None:
        """Sense fruit within sensor radius and update local knowledge.
        Optionally broadcast hotspots when first discovered (cooperative)."""
        w, h = self.model.grid.width, self.model.grid.height
        # Moore neighborhood within sensor_radius (bounded by obstacles handled by model)
        neighborhood = self.model.grid.get_neighborhood(
            self.pos, moore=True, include_center=True, radius=self.sensor_radius
        )
        new_hotspots: List[Tuple[int, int]] = []
        for cell in neighborhood:
            x, y = cell
            if 0 <= x < w and 0 <= y < h:
                fruit_here = self.model.get_fruit_at(cell)
                if fruit_here > 0:
                    # Simple heat = min(fruit count, 5)
                    self.known_fruit[cell] = max(self.known_fruit.get(cell, 0.0), min(fruit_here, 5))
                    new_hotspots.append(cell)

        if self.strategy == "cooperative" and new_hotspots:
            # Broadcast a summarized hotspot message (top-k by proximity)
            top = sorted(new_hotspots, key=lambda c: self._manhattan(self.pos, c))[:3]
            for c in top:
                self._emit(
                    mtype="HOTSPOT",
                    pos=self.pos,
                    payload={"cell": c, "score": self.known_fruit.get(c, 1.0)},
                    ttl=self.model.default_ttl,
                )

    # ---- Decision ----
    def decide(self) -> None:
        """Process messages, update targets, generate CLAIMs if cooperative."""
        # Incorporate received messages
        self._process_inbox()

        # Remove stale/empty fruit cells from knowledge
        to_del = [c for c, s in self.known_fruit.items() if self.model.get_fruit_at(c) <= 0]
        for c in to_del:
            self.known_fruit.pop(c, None)
            if self.target == c:
                self.target = None

        # If no target or target depleted, choose a new one
        if self.target is None:
            if self.known_fruit:
                # Score = heat - distance (simple greedy bias)
                best = max(
                    self.known_fruit.keys(),
                    key=lambda c: self.known_fruit[c] - 0.3 * self._manhattan(self.pos, c),
                )
                # In cooperative strategy, avoid targets claimed by others
                if self.strategy == "cooperative" and best in self.model.claimed_targets:
                    # Try another candidate that is not claimed
                    candidates = sorted(
                        self.known_fruit.keys(),
                        key=lambda c: self.known_fruit[c] - 0.3 * self._manhattan(self.pos, c),
                        reverse=True,
                    )
                    best = next((c for c in candidates if c not in self.model.claimed_targets), candidates[0])

                self.target = best
                if self.strategy == "cooperative" and self.target is not None:
                    # Announce CLAIM so others avoid overlap
                    self._emit(
                        mtype="CLAIM",
                        pos=self.pos,
                        payload={"cell": self.target, "eta": self._manhattan(self.pos, self.target)},
                        ttl=self.model.default_ttl,
                    )

        # If still no target, we will random walk in act()

    # ---- Action ----
    def act(self) -> None:
        # Move one step toward target or random move
        if self.target is not None:
            if self.pos == self.target:
                # Harvest
                harvested = self.model.harvest_at(self.pos, amount=1)
                self.fruit_collected += harvested
                if harvested <= 0 or self.model.get_fruit_at(self.pos) <= 0:
                    # Release claim and clear target
                    if self.strategy == "cooperative":
                        self._emit("RELEASE", pos=self.pos, payload={"cell": self.pos}, ttl=self.model.default_ttl)
                    self.target = None
            else:
                self._step_towards(self.target)
        else:
            self._random_step()

        # Clear inbox at end of action to avoid reprocessing
        self.inbox.clear()

    # ---- Helpers ----
    def _emit(self, mtype: str, pos: Tuple[int, int], payload: Dict, ttl: int = 0) -> None:
        mid = self.model.next_msg_id()
        self.outbox.append(Message(msg_id=mid, mtype=mtype, sender=self.unique_id, pos=pos, ttl=ttl, payload=payload))

    def _process_inbox(self) -> None:
        for m in self.inbox:
            if m.msg_id in self._seen_ids:
                continue
            self._seen_ids.add(m.msg_id)

            if m.mtype == "HOTSPOT":
                cell = tuple(m.payload.get("cell"))  # type: ignore
                score = float(m.payload.get("score", 1.0))
                # Merge with local heat (max to keep strong signal)
                self.known_fruit[cell] = max(self.known_fruit.get(cell, 0.0), score)

            elif m.mtype == "CLAIM" and self.strategy == "cooperative":
                cell = tuple(m.payload.get("cell"))  # type: ignore
                # Mark as claimed so we deprioritize it
                self.model.claimed_targets.add(cell)
                if self.target == cell:
                    # Someone else has it; invalidate our target so we pick another
                    self.target = None

            elif m.mtype == "RELEASE" and self.strategy == "cooperative":
                cell = tuple(m.payload.get("cell"))  # type: ignore
                self.model.claimed_targets.discard(cell)

    def _step_towards(self, goal: Tuple[int, int]) -> None:
        gx, gy = goal
        x, y = self.pos
        dx = 0 if gx == x else (1 if gx > x else -1)
        dy = 0 if gy == y else (1 if gy > y else -1)
        # Try diagonal then axis moves (Moore neighborhood)
        candidates = [
            (x + dx, y + dy),
            (x + dx, y),
            (x, y + dy),
            (x + dx, y - dy),
            (x - dx, y + dy),
        ]
        for nx, ny in candidates:
            if self.model.is_cell_free((nx, ny)):
                self.model.grid.move_agent(self, (nx, ny))
                return
        # Fallback: random
        self._random_step()

    def _random_step(self) -> None:
        x, y = self.pos
        neighbors = list(self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False, radius=1))
        random.shuffle(neighbors)
        for nx, ny in neighbors:
            if self.model.is_cell_free((nx, ny)):
                self.model.grid.move_agent(self, (nx, ny))
                return
        # If stuck, wait
        return

    @staticmethod
    def _manhattan(a: Tuple[int, int], b: Tuple[int, int]) -> int:
        return abs(a[0] - b[0]) + abs(a[1] - b[1])


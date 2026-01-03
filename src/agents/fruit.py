"""
Fruit Resource Agent for harvesting simulation.

================================================================================
PURPOSE & DESIGN RATIONALE
================================================================================
This module implements the fruit resource that agents harvest in the simulation.
For RQ1 (Communication Range Effects), we use Static resource dynamics only.

DESIGN DECISION - STATIC vs DYNAMIC RESOURCES:
We chose static (non-regenerating) fruit for several reasons:
1. Simplicity: Static resources eliminate time-dependent dynamics
2. Measurability: Total yield is bounded, enabling fair comparison
3. Completion: Simulations have a clear end state (all fruit collected)
4. Reproducibility: Same initial fruit placement gives comparable runs

The Fruit class is implemented as a Mesa Agent for grid placement compatibility,
even though fruit doesn't actively "do" anything each step.

================================================================================
"""
from mesa import Agent


class Fruit(Agent):
    """
    Static fruit resource that can be harvested exactly once.

    Fruit agents represent harvestable resources on the grid. Once harvested,
    a fruit becomes permanently unavailable (static dynamics - no regeneration).

    This is implemented as a Mesa Agent to enable:
    - Placement on the MultiGrid alongside HarvesterAgents
    - Inclusion in Mesa's agent management system
    - Future extensibility (e.g., regenerating fruit for other research questions)

    Attributes:
        is_fruit (bool): Type flag to distinguish from HarvesterAgents
        available (bool): Whether fruit can still be harvested
        times_harvested (int): Harvest count (always 0 or 1 for static dynamics)

    Example:
        >>> fruit = Fruit(model)
        >>> fruit.available
        True
        >>> fruit.harvest()
        >>> fruit.available
        False
    """

    def __init__(self, model):
        """
        Initialize fruit resource in available state.

        Args:
            model: The HarvestModel instance this fruit belongs to

        Note:
            The is_fruit flag is used by HarvesterAgents to identify fruit
            objects when scanning cell contents. This is necessary because
            MultiGrid cells can contain multiple object types.
        """
        super().__init__(model)
        self.is_fruit = True  # Type identifier for cell content filtering
        self.available = True  # Can be harvested
        self.times_harvested = 0  # Counter for verification

    def harvest(self):
        """
        Harvest this fruit, making it permanently unavailable.

        For static dynamics, this is a one-way state change. The fruit
        remains on the grid (for visualization) but cannot be harvested again.

        This method is idempotent - calling it multiple times has no
        additional effect after the first call.
        """
        if self.available:
            self.available = False
            self.times_harvested += 1

    def step(self):
        """
        Fruit step method - no operation for static dynamics.

        This method exists for Mesa framework compatibility. All agents
        in the model have step() called each simulation step, but static
        fruit doesn't need to do anything.

        For future dynamic/regenerating resources, this method could
        implement respawn logic.
        """
        pass


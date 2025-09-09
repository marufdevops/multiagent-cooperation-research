from __future__ import annotations
import argparse

from .environment import OrchardModel


def run_once(width=20, height=20, num_agents=10, comm_range=3, steps=50, cooperative_share=1.0):
    model = OrchardModel(
        width=width,
        height=height,
        num_agents=num_agents,
        comm_range=comm_range,
        cooperative_share=cooperative_share,
        fruit_spawn_prob=0.08,
        regen_prob=0.02,
        max_fruit_per_cell=3,
        default_ttl=0,
    )
    for _ in range(steps):
        model.step()
    # Print a quick summary
    total_collected = sum(a.fruit_collected for a in model.schedule.agents)
    print(f"Steps={steps} Agents={num_agents} R={comm_range} TotalCollected={total_collected}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run a single simulation episode.")
    parser.add_argument("--width", type=int, default=20)
    parser.add_argument("--height", type=int, default=20)
    parser.add_argument("--agents", type=int, default=10)
    parser.add_argument("--range", dest="comm_range", type=int, default=3)
    parser.add_argument("--steps", type=int, default=50)
    parser.add_argument("--coop", dest="cooperative_share", type=float, default=1.0)
    args = parser.parse_args()
    run_once(
        width=args.width,
        height=args.height,
        num_agents=args.agents,
        comm_range=args.comm_range,
        steps=args.steps,
        cooperative_share=args.cooperative_share,
    )


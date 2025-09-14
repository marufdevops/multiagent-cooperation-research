#!/usr/bin/env python3
"""
Run the basic Mesa grid learning environment.

Usage:
    python run.py --batch   # Run batch simulation without visualization
    solara run server.py    # Launch web visualization (recommended)
"""

import argparse
from .model import BasicGridModel


def run_batch_simulation(steps=100):
    """Run a batch simulation without visualization."""
    print("Running batch simulation...")

    # Create model
    model = BasicGridModel()

    # Run simulation
    for i in range(steps):
        model.step()
        if (i + 1) % 10 == 0:
            print(f"Step {i + 1}/{steps}")

    print(f"Simulation completed after {steps} steps")
    print(f"Final step count: {model.step_count}")


def main():
    parser = argparse.ArgumentParser(description="Run Basic Mesa Grid Learning Environment")
    parser.add_argument("--batch", action="store_true",
                       help="Run batch simulation without visualization")
    parser.add_argument("--steps", type=int, default=100,
                       help="Number of steps for batch simulation (default: 100)")

    args = parser.parse_args()

    if args.batch:
        run_batch_simulation(args.steps)
    else:
        print("For web visualization, use:")
        print("  solara run fruit_harvester_simulation/server.py")
        print("")
        print("This will launch the interactive web interface at http://localhost:8765")
        print("Use --batch flag to run simulation without visualization")


if __name__ == "__main__":
    main()
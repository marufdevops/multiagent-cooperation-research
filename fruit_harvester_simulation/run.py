#!/usr/bin/env python3
"""
Run the basic Mesa grid learning environment.

Usage:
    python run.py          # Launch web visualization
    python run.py --batch  # Run batch simulation without visualization
"""

import argparse
from .model import BasicGridModel
from .server import launch_server


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
        print("Launching web visualization server...")
        print("Open http://localhost:8521 in your browser")
        server = launch_server()
        server.launch()


if __name__ == "__main__":
    main()
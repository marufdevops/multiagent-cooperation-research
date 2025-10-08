"""
Mesa 3.0 compatible batch runner for the fruit harvesting simulation.

This module provides functionality to run batch simulations for data collection
and analysis, supporting different parameter combinations for research.
"""

import argparse
import pandas as pd
from .model import OrchardModel


def run_single_simulation(steps=100, **model_params):
    """
    Run a single simulation with given parameters.

    Args:
        steps: Number of simulation steps to run
        **model_params: Parameters to pass to OrchardModel

    Returns:
        dict: Final simulation results
    """
    model = OrchardModel(**model_params)

    # Run simulation
    for i in range(steps):
        model.step()

        # Optional: Print progress for long runs
        if steps > 50 and (i + 1) % 20 == 0:
            total_fruits = sum(a.fruits_collected for a in model.agents)
            print(f"Step {i + 1}/{steps} - Fruits: {total_fruits}, Messages: {model.total_messages_sent}")

    # Collect final results
    results = {
        'steps': steps,
        'total_fruits_harvested': sum(a.fruits_collected for a in model.agents),
        'total_messages_sent': model.total_messages_sent,
        'num_agents': len(model.agents),
        'cooperative_agents': sum(1 for a in model.agents if a.strategy == "cooperative"),
        'competitive_agents': sum(1 for a in model.agents if a.strategy == "competitive"),
        'avg_fruits_per_agent': sum(a.fruits_collected for a in model.agents) / len(model.agents),
        'communication_range': model.communication_range,
        'cooperative_share': model.cooperative_share,
    }

    return results


def run_batch_simulation(steps=100, num_agents=20, communication_range=3.0,
                        cooperative_share=1.0, width=30, height=30,
                        initial_fruit_density=0.3, regeneration_prob=0.1):
    """
    Run a batch simulation with specified parameters.

    Args:
        steps: Number of simulation steps
        num_agents: Number of harvester agents
        communication_range: Communication range for agents
        cooperative_share: Fraction of cooperative agents
        width: Grid width
        height: Grid height
        initial_fruit_density: Initial fruit density
        regeneration_prob: Fruit regeneration probability

    Returns:
        dict: Simulation results
    """
    print(f"Running simulation: {num_agents} agents, range={communication_range}, coop={cooperative_share}")

    model_params = {
        'width': width,
        'height': height,
        'num_agents': num_agents,
        'communication_range': communication_range,
        'cooperative_share': cooperative_share,
        'initial_fruit_density': initial_fruit_density,
        'regeneration_prob': regeneration_prob,
    }

    results = run_single_simulation(steps=steps, **model_params)

    print(f"Results: {results['total_fruits_harvested']} fruits, {results['total_messages_sent']} messages")
    return results


def run_parameter_sweep(base_params, param_ranges, steps=100, output_file=None):
    """
    Run simulations across different parameter combinations.

    Args:
        base_params: Base model parameters
        param_ranges: Dictionary of parameter names to lists of values
        steps: Number of steps per simulation
        output_file: Optional CSV file to save results

    Returns:
        pandas.DataFrame: Results from all simulations
    """
    results = []

    # Generate all parameter combinations
    import itertools
    param_names = list(param_ranges.keys())
    param_values = list(param_ranges.values())

    for combination in itertools.product(*param_values):
        # Create parameters for this run
        run_params = base_params.copy()
        for name, value in zip(param_names, combination):
            run_params[name] = value

        # Run simulation
        result = run_single_simulation(steps=steps, **run_params)
        results.append(result)

        print(f"Completed: {dict(zip(param_names, combination))}")

    # Convert to DataFrame
    df = pd.DataFrame(results)

    # Save to file if specified
    if output_file:
        df.to_csv(output_file, index=False)
        print(f"Results saved to {output_file}")

    return df


def main():
    """Command-line interface for running simulations."""
    parser = argparse.ArgumentParser(description="Run fruit harvesting simulation")
    parser.add_argument("--batch", action="store_true", help="Run batch simulation")
    parser.add_argument("--steps", type=int, default=100, help="Number of simulation steps")
    parser.add_argument("--agents", type=int, default=20, help="Number of agents")
    parser.add_argument("--comm-range", type=float, default=3.0, help="Communication range")
    parser.add_argument("--coop-share", type=float, default=1.0, help="Cooperative share")
    parser.add_argument("--width", type=int, default=30, help="Grid width")
    parser.add_argument("--height", type=int, default=30, help="Grid height")
    parser.add_argument("--output", type=str, help="Output CSV file for results")

    args = parser.parse_args()

    if args.batch:
        results = run_batch_simulation(
            steps=args.steps,
            num_agents=args.agents,
            communication_range=args.comm_range,
            cooperative_share=args.coop_share,
            width=args.width,
            height=args.height,
        )

        if args.output:
            df = pd.DataFrame([results])
            df.to_csv(args.output, index=False)
            print(f"Results saved to {args.output}")
    else:
        print("Use --batch flag to run simulation, or import functions for custom usage")


if __name__ == "__main__":
    main()
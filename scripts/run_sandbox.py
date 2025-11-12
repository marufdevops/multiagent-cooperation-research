"""
Quick test script for the Mesa model.
Just runs a simple simulation to verify everything works.

TODO: Add more comprehensive testing
TODO: Generate plots after experiments are complete
"""
import sys
sys.path.insert(0, 'src')

from models.harvest_model import HarvestModel


def run_sandbox(
    width=20,
    height=20,
    num_agents=5,
    fruit_density=0.2,
    comm_range=2,
    steps=100,
    seed=42
):
    """Run sandbox model with Static dynamics and return results."""
    print(f"Running sandbox model:")
    print(f"  Grid: {width}x{height}")
    print(f"  Agents: {num_agents}")
    print(f"  Fruit density: {fruit_density}")
    print(f"  Comm range: {comm_range}")
    print(f"  Dynamics: Static (no regeneration)")
    print(f"  Steps: {steps}")
    print(f"  Seed: {seed}")
    print()

    # Create and run model (Static dynamics only)
    model = HarvestModel(
        width=width,
        height=height,
        num_agents=num_agents,
        fruit_density=fruit_density,
        comm_range=comm_range,
        seed=seed
    )

    model.run_model(steps=steps)

    # Get data
    model_data = model.datacollector.get_model_vars_dataframe()

    print(f"Final yield: {model_data['total_yield'].iloc[-1]}")
    print(f"Total messages: {model_data['cumulative_messages'].iloc[-1]}")
    print(f"Remaining fruit: {model_data['remaining_fruit'].iloc[-1]}")
    print(f"Coverage (cells visited): {model_data['coverage'].iloc[-1]}")
    print()

    return model, model_data


if __name__ == '__main__':
    print("=" * 60)
    print("QUICK TEST - Mesa Model")
    print("=" * 60)
    print()

    # Just run one simple test to verify model works
    print("Running basic test (Range=2)...")
    print("-" * 60)
    model, data = run_sandbox(
        comm_range=2,
        steps=100,
        seed=42
    )

    print("=" * 60)
    print("Test complete! Model is working.")
    print("=" * 60)
    print()
    print("TODO: Add more test scenarios")
    print("TODO: Generate plots after running full experiments")


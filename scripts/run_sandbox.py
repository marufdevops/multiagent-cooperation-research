"""
Run sandbox model and generate basic plots.
Week 1-2 deliverable: reproducible runs with yield-over-time and messages/step plots.
"""
import sys
sys.path.insert(0, 'src')

import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import pandas as pd
from models.harvest_model import HarvestModel


def run_sandbox(
    width=20,
    height=20,
    num_agents=5,
    fruit_density=0.2,
    comm_range=2,
    dynamics='Static',
    regen_prob=0.0,
    steps=100,
    seed=42
):
    """Run sandbox model and return results."""
    print(f"Running sandbox model:")
    print(f"  Grid: {width}x{height}")
    print(f"  Agents: {num_agents}")
    print(f"  Fruit density: {fruit_density}")
    print(f"  Comm range: {comm_range}")
    print(f"  Dynamics: {dynamics}")
    print(f"  Regen prob: {regen_prob}")
    print(f"  Steps: {steps}")
    print(f"  Seed: {seed}")
    print()
    
    # Create and run model
    model = HarvestModel(
        width=width,
        height=height,
        num_agents=num_agents,
        fruit_density=fruit_density,
        comm_range=comm_range,
        dynamics=dynamics,
        regen_prob=regen_prob,
        seed=seed
    )
    
    model.run_model(steps=steps)
    
    # Get data
    model_data = model.datacollector.get_model_vars_dataframe()

    print(f"Final yield: {model_data['total_yield'].iloc[-1]}")
    print(f"Total messages: {model_data['messages_this_step'].sum()}")
    print(f"Remaining fruit: {model_data['remaining_fruit'].iloc[-1]}")
    print()
    
    return model, model_data


def plot_results(model_data, output_prefix='sandbox'):
    """Generate required plots: yield-over-time and messages/step."""
    fig, axes = plt.subplots(1, 2, figsize=(12, 4))

    # Plot 1: Yield over time
    axes[0].plot(model_data.index, model_data['total_yield'], linewidth=2)
    axes[0].set_xlabel('Step')
    axes[0].set_ylabel('Total Yield')
    axes[0].set_title('Yield Over Time')
    axes[0].grid(True, alpha=0.3)

    # Plot 2: Messages per step
    axes[1].plot(model_data.index, model_data['messages_this_step'], linewidth=2, color='orange')
    axes[1].set_xlabel('Step')
    axes[1].set_ylabel('Messages This Step')
    axes[1].set_title('Communication Activity')
    axes[1].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(f'{output_prefix}_results.png', dpi=150)
    print(f"Saved plot: {output_prefix}_results.png")
    plt.close()


if __name__ == '__main__':
    # Run with default parameters
    print("=" * 60)
    print("SANDBOX MODEL - WEEK 1-2 DELIVERABLE")
    print("=" * 60)
    print()
    
    # Test 1: Static dynamics, no communication
    print("Test 1: Static, no communication")
    print("-" * 60)
    model1, data1 = run_sandbox(
        comm_range=0,
        dynamics='Static',
        steps=100,
        seed=42
    )
    plot_results(data1, 'sandbox_static_nocomm')
    
    # Test 2: Static dynamics, with communication
    print("Test 2: Static, with communication (range=3)")
    print("-" * 60)
    model2, data2 = run_sandbox(
        comm_range=3,
        dynamics='Static',
        steps=100,
        seed=42
    )
    plot_results(data2, 'sandbox_static_comm')
    
    # Test 3: Replenishing dynamics
    print("Test 3: Replenishing, with communication")
    print("-" * 60)
    model3, data3 = run_sandbox(
        comm_range=3,
        dynamics='Replenishing',
        regen_prob=0.05,
        steps=100,
        seed=42
    )
    plot_results(data3, 'sandbox_replenishing')
    
    print("=" * 60)
    print("Sandbox tests complete!")
    print("=" * 60)


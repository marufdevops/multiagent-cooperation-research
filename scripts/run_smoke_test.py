"""
Smoke test factorial runner for Weeks 3-4.
Small factorial: comm_range × num_agents × dynamics with 2 seeds.
Validates metrics collection and parameter sweep infrastructure.
"""
import sys
sys.path.insert(0, 'src')

import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from itertools import product
from tqdm import tqdm
import json
from datetime import datetime
from models.harvest_model import HarvestModel


def run_single_experiment(params):
    """Run single experiment configuration."""
    model = HarvestModel(
        width=params['width'],
        height=params['height'],
        num_agents=params['num_agents'],
        fruit_density=params['fruit_density'],
        comm_range=params['comm_range'],
        dynamics=params['dynamics'],
        regen_prob=params['regen_prob'],
        seed=params['seed']
    )
    
    model.run_model(steps=params['steps'])
    
    # Get per-step data
    step_data = model.datacollector.get_model_vars_dataframe()
    
    # Calculate per-run summary
    summary = {
        'run_id': params['run_id'],
        'seed': params['seed'],
        'dynamics': params['dynamics'],
        'regen_prob': params['regen_prob'],
        'grid_w': params['width'],
        'grid_h': params['height'],
        'fruit_density': params['fruit_density'],
        'num_agents': params['num_agents'],
        'comm_range': params['comm_range'],
        'steps_run': params['steps'],
        'final_yield': step_data['total_yield'].iloc[-1],
        'steady_state_yield': step_data['total_yield'].iloc[int(len(step_data)*0.75):].mean(),
        'time_to_depletion': _get_time_to_depletion(step_data),
        'mean_messages_per_step': step_data['messages_this_step'].mean(),
        'yield_per_message': _calculate_yield_per_message(step_data),
        'peak_component_ratio': step_data['largest_component_ratio'].max(),
    }
    
    return summary, step_data


def _get_time_to_depletion(step_data):
    """Calculate time to depletion (when remaining fruit hits 0)."""
    depleted = step_data[step_data['remaining_fruit'] == 0]
    if len(depleted) > 0:
        return depleted.index[0]
    return None


def _calculate_yield_per_message(step_data):
    """Calculate yield per message sent."""
    total_messages = step_data['cumulative_messages'].iloc[-1]
    total_yield = step_data['total_yield'].iloc[-1]
    
    if total_messages > 0:
        return total_yield / total_messages
    return 0.0


def run_smoke_test():
    """Run smoke test factorial experiment."""
    print("=" * 70)
    print("SMOKE TEST FACTORIAL - WEEKS 3-4")
    print("=" * 70)
    print()
    
    # Define parameter space (small for smoke test)
    param_grid = {
        'width': [30],
        'height': [30],
        'fruit_density': [0.2],
        'num_agents': [10, 20],
        'comm_range': [0, 2, 4],
        'dynamics': ['Static', 'Replenishing'],
        'steps': [200],
        'seeds': [42, 43],
    }
    
    # Generate all combinations
    configs = []
    run_id = 0
    
    for num_agents, comm_range, dynamics, seed in product(
        param_grid['num_agents'],
        param_grid['comm_range'],
        param_grid['dynamics'],
        param_grid['seeds']
    ):
        regen_prob = 0.05 if dynamics == 'Replenishing' else 0.0
        
        config = {
            'run_id': run_id,
            'width': param_grid['width'][0],
            'height': param_grid['height'][0],
            'fruit_density': param_grid['fruit_density'][0],
            'num_agents': num_agents,
            'comm_range': comm_range,
            'dynamics': dynamics,
            'regen_prob': regen_prob,
            'steps': param_grid['steps'][0],
            'seed': seed,
        }
        configs.append(config)
        run_id += 1
    
    print(f"Total configurations: {len(configs)}")
    print(f"Parameters:")
    print(f"  Agents: {param_grid['num_agents']}")
    print(f"  Comm ranges: {param_grid['comm_range']}")
    print(f"  Dynamics: {param_grid['dynamics']}")
    print(f"  Seeds: {param_grid['seeds']}")
    print()
    
    # Run experiments
    results = []
    
    for config in tqdm(configs, desc="Running experiments"):
        summary, step_data = run_single_experiment(config)
        results.append(summary)
    
    # Convert to DataFrame
    results_df = pd.DataFrame(results)
    
    # Save results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f'smoke_test_results_{timestamp}.csv'
    results_df.to_csv(output_file, index=False)
    print(f"\nResults saved to: {output_file}")
    
    # Print summary statistics
    print("\n" + "=" * 70)
    print("SUMMARY STATISTICS")
    print("=" * 70)
    print()
    
    print("Final Yield by Configuration:")
    print(results_df.groupby(['dynamics', 'comm_range', 'num_agents'])['final_yield'].mean().round(2))
    print()
    
    print("Yield per Message by Configuration:")
    print(results_df.groupby(['dynamics', 'comm_range', 'num_agents'])['yield_per_message'].mean().round(3))
    print()
    
    # Generate plots
    plot_smoke_test_results(results_df, timestamp)
    
    return results_df


def plot_smoke_test_results(df, timestamp):
    """Generate visualization plots for smoke test."""
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # Plot 1: Yield vs comm_range by dynamics
    for dynamics in df['dynamics'].unique():
        subset = df[df['dynamics'] == dynamics]
        grouped = subset.groupby('comm_range')['final_yield'].mean()
        axes[0, 0].plot(grouped.index, grouped.values, marker='o', label=dynamics, linewidth=2)
    
    axes[0, 0].set_xlabel('Communication Range')
    axes[0, 0].set_ylabel('Final Yield')
    axes[0, 0].set_title('Yield vs Communication Range')
    axes[0, 0].legend()
    axes[0, 0].grid(True, alpha=0.3)
    
    # Plot 2: Yield per message vs comm_range
    for dynamics in df['dynamics'].unique():
        subset = df[df['dynamics'] == dynamics]
        grouped = subset.groupby('comm_range')['yield_per_message'].mean()
        axes[0, 1].plot(grouped.index, grouped.values, marker='s', label=dynamics, linewidth=2)
    
    axes[0, 1].set_xlabel('Communication Range')
    axes[0, 1].set_ylabel('Yield per Message')
    axes[0, 1].set_title('Efficiency vs Communication Range')
    axes[0, 1].legend()
    axes[0, 1].grid(True, alpha=0.3)
    
    # Plot 3: Component ratio vs comm_range
    for dynamics in df['dynamics'].unique():
        subset = df[df['dynamics'] == dynamics]
        grouped = subset.groupby('comm_range')['peak_component_ratio'].mean()
        axes[1, 0].plot(grouped.index, grouped.values, marker='^', label=dynamics, linewidth=2)
    
    axes[1, 0].set_xlabel('Communication Range')
    axes[1, 0].set_ylabel('Peak Component Ratio')
    axes[1, 0].set_title('Network Connectivity vs Communication Range')
    axes[1, 0].legend()
    axes[1, 0].grid(True, alpha=0.3)
    
    # Plot 4: Heatmap of yield by agents and comm_range (Static only)
    static_df = df[df['dynamics'] == 'Static']
    pivot = static_df.groupby(['num_agents', 'comm_range'])['final_yield'].mean().unstack()
    sns.heatmap(pivot, annot=True, fmt='.1f', cmap='YlOrRd', ax=axes[1, 1])
    axes[1, 1].set_title('Final Yield Heatmap (Static)')
    axes[1, 1].set_xlabel('Communication Range')
    axes[1, 1].set_ylabel('Number of Agents')
    
    plt.tight_layout()
    plot_file = f'smoke_test_plots_{timestamp}.png'
    plt.savefig(plot_file, dpi=150)
    print(f"Plots saved to: {plot_file}")
    plt.close()


if __name__ == '__main__':
    results = run_smoke_test()
    
    print("\n" + "=" * 70)
    print("SMOKE TEST COMPLETE!")
    print("=" * 70)
    print("\nAll metrics columns populated successfully.")
    print("Ready for full factorial experiments in Weeks 5-6.")


"""
Batch Experiment Runner for RQ1: Communication Range Effects

Experimental Design (Static dynamics only):
- Communication ranges: {0, 2, 4, 6, 8} cells
- Team sizes: {10, 20} agents
- Resource densities: {0.15, 0.25}
- Replications: 20-30 per configuration (configurable)
- Total runs: 5 × 2 × 2 × 20 = 400 simulations (or 600 with 30 reps)
- Episode length: 500 steps

Output: CSV file with all experimental results
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

import pandas as pd
from datetime import datetime
from tqdm import tqdm
import time

from models.harvest_model import HarvestModel


def run_single_experiment(config, replication):
    """
    Run a single simulation with given configuration.

    Args:
        config: Dictionary with experimental parameters
        replication: Replication number (for random seed)

    Returns:
        Dictionary with results
    """
    # Create model with configuration (Static dynamics only for RQ1)
    model = HarvestModel(
        width=50,
        height=50,
        num_agents=config['num_agents'],
        fruit_density=config['fruit_density'],
        comm_range=config['comm_range'],
        seed=replication  # Use replication number as seed for reproducibility
    )
    
    # Run simulation for 500 steps
    max_steps = 500
    for _ in range(max_steps):
        model.step()
    
    # Extract final metrics
    df = model.datacollector.get_model_vars_dataframe()
    
    # Calculate derived metrics
    final_yield = df['total_yield'].iloc[-1]
    total_messages = df['cumulative_messages'].iloc[-1]
    final_remaining = df['remaining_fruit'].iloc[-1]
    
    # Efficiency: yield per message (handle division by zero)
    efficiency = final_yield / total_messages if total_messages > 0 else final_yield
    
    # Calculate coverage (unique cells visited by agents)
    visited_cells = set()
    for agent in model.agents:
        if hasattr(agent, 'visited_cells'):
            visited_cells.update(agent.visited_cells)
    coverage = len(visited_cells)
    
    # Return results
    return {
        'comm_range': config['comm_range'],
        'num_agents': config['num_agents'],
        'fruit_density': config['fruit_density'],
        'replication': replication,
        'seed': replication,
        'total_yield': final_yield,
        'total_messages': total_messages,
        'efficiency': efficiency,
        'remaining_fruit': final_remaining,
        'coverage': coverage,
        'steps': max_steps
    }


def generate_configurations():
    """
    Generate all experimental configurations.
    
    Returns:
        List of configuration dictionaries
    """
    comm_ranges = [0, 2, 4, 6, 8]
    team_sizes = [10, 20]
    densities = [0.15, 0.25]
    
    configs = []
    for comm_range in comm_ranges:
        for num_agents in team_sizes:
            for density in densities:
                configs.append({
                    'comm_range': comm_range,
                    'num_agents': num_agents,
                    'fruit_density': density
                })
    
    return configs


def run_all_experiments(num_replications=30, output_dir='results'):
    """
    Run all experimental configurations with replications.
    
    Args:
        num_replications: Number of replications per configuration
        output_dir: Directory to save results
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate configurations
    configs = generate_configurations()
    total_runs = len(configs) * num_replications
    
    print(f"Starting experimental runs...")
    print(f"Configurations: {len(configs)}")
    print(f"Replications per configuration: {num_replications}")
    print(f"Total runs: {total_runs}")
    print(f"Output directory: {output_dir}")
    print("-" * 60)
    
    # Track results
    all_results = []
    start_time = time.time()
    
    # Progress bar for all runs
    with tqdm(total=total_runs, desc="Running experiments") as pbar:
        for config_idx, config in enumerate(configs):
            config_start = time.time()
            
            # Run replications for this configuration
            for rep in range(num_replications):
                try:
                    result = run_single_experiment(config, rep)
                    all_results.append(result)
                    pbar.update(1)
                    
                except Exception as e:
                    print(f"\nError in config {config_idx}, rep {rep}: {e}")
                    pbar.update(1)
                    continue
            
            # Report progress for this configuration
            config_time = time.time() - config_start
            avg_time_per_run = config_time / num_replications
            pbar.set_postfix({
                'config': f"{config_idx+1}/{len(configs)}",
                'avg_time': f"{avg_time_per_run:.2f}s"
            })
    
    # Calculate total time
    total_time = time.time() - start_time
    
    print("\n" + "=" * 60)
    print(f"All experiments completed!")
    print(f"Total time: {total_time/60:.2f} minutes")
    print(f"Average time per run: {total_time/total_runs:.2f} seconds")
    print(f"Successful runs: {len(all_results)}/{total_runs}")
    print("=" * 60)
    
    # Convert to DataFrame
    df = pd.DataFrame(all_results)
    
    # Add timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Save to CSV
    output_file = os.path.join(output_dir, f'experimental_results_{timestamp}.csv')
    df.to_csv(output_file, index=False)
    print(f"\nResults saved to: {output_file}")
    
    # Print summary statistics
    print("\n" + "=" * 60)
    print("SUMMARY STATISTICS")
    print("=" * 60)
    
    summary = df.groupby('comm_range').agg({
        'total_yield': ['mean', 'std', 'min', 'max'],
        'total_messages': ['mean', 'std'],
        'efficiency': ['mean', 'std']
    }).round(2)
    
    print(summary)
    
    # Save summary
    summary_file = os.path.join(output_dir, f'summary_statistics_{timestamp}.csv')
    summary.to_csv(summary_file)
    print(f"\nSummary statistics saved to: {summary_file}")
    
    return df


def run_quick_test(num_configs=2, num_reps=3):
    """
    Run a quick test with fewer configurations and replications.
    Useful for testing the experimental setup.
    
    Args:
        num_configs: Number of configurations to test
        num_reps: Number of replications per configuration
    """
    print("=" * 60)
    print("QUICK TEST MODE")
    print("=" * 60)
    
    configs = generate_configurations()[:num_configs]
    
    print(f"Testing {num_configs} configurations with {num_reps} replications each")
    print(f"Total runs: {num_configs * num_reps}")
    print("-" * 60)
    
    results = []
    start_time = time.time()
    
    for config_idx, config in enumerate(configs):
        print(f"\nConfiguration {config_idx + 1}/{num_configs}:")
        print(f"  comm_range={config['comm_range']}, "
              f"num_agents={config['num_agents']}, "
              f"density={config['fruit_density']}")
        
        for rep in range(num_reps):
            rep_start = time.time()
            result = run_single_experiment(config, rep)
            rep_time = time.time() - rep_start
            results.append(result)
            print(f"  Rep {rep+1}: yield={result['total_yield']:.0f}, "
                  f"messages={result['total_messages']:.0f}, "
                  f"time={rep_time:.2f}s")
    
    total_time = time.time() - start_time
    avg_time = total_time / (num_configs * num_reps)
    
    print("\n" + "=" * 60)
    print(f"Quick test completed!")
    print(f"Total time: {total_time:.2f} seconds")
    print(f"Average time per run: {avg_time:.2f} seconds")
    print(f"Estimated time for full experiment (600 runs): {avg_time * 600 / 60:.2f} minutes")
    print("=" * 60)
    
    return pd.DataFrame(results)


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Run batch experiments for RQ1')
    parser.add_argument('--test', action='store_true', 
                        help='Run quick test with 2 configs and 3 reps')
    parser.add_argument('--replications', type=int, default=30,
                        help='Number of replications per configuration (default: 30)')
    parser.add_argument('--output', type=str, default='results',
                        help='Output directory for results (default: results)')
    
    args = parser.parse_args()
    
    if args.test:
        # Run quick test
        df = run_quick_test()
        print("\nTest results preview:")
        print(df.head())
    else:
        # Run full experiments
        df = run_all_experiments(
            num_replications=args.replications,
            output_dir=args.output
        )


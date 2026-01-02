"""
Batch experiment runner for RQ1: Communication Range Effects.
Runs 400 simulations (5 ranges × 2 team sizes × 2 densities × 20 replications).
Results saved to results/experimental_results_[timestamp].csv
"""
import sys
import os
import csv
import time
from datetime import datetime

sys.path.insert(0, 'src')

from models.harvest_model import HarvestModel


def run_experiments(
    grid_size=50,
    episode_length=500,
    num_replications=20,
    comm_ranges=None,
    team_sizes=None,
    densities=None,
    output_dir='results'
):
    """
    Run batch experiments with parameter sweep.
    
    Args:
        grid_size: Grid width/height (50x50)
        episode_length: Number of steps per simulation (500)
        num_replications: Replications per configuration (20)
        comm_ranges: List of communication ranges to test
        team_sizes: List of team sizes to test
        densities: List of fruit densities to test
        output_dir: Directory to save results
    """
    if comm_ranges is None:
        comm_ranges = [0, 2, 4, 6, 8]
    if team_sizes is None:
        team_sizes = [10, 20]
    if densities is None:
        densities = [0.15, 0.25]
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate timestamp for results file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results_file = os.path.join(output_dir, f'experimental_results_{timestamp}.csv')
    
    # Calculate total runs
    total_configs = len(comm_ranges) * len(team_sizes) * len(densities)
    total_runs = total_configs * num_replications
    
    print("=" * 70)
    print("BATCH EXPERIMENT RUNNER - RQ1: Communication Range Effects")
    print("=" * 70)
    print(f"Grid size: {grid_size}×{grid_size}")
    print(f"Episode length: {episode_length} steps")
    print(f"Communication ranges: {comm_ranges}")
    print(f"Team sizes: {team_sizes}")
    print(f"Fruit densities: {densities}")
    print(f"Replications per config: {num_replications}")
    print(f"Total configurations: {total_configs}")
    print(f"Total runs: {total_runs}")
    print(f"Results file: {results_file}")
    print("=" * 70)
    print()
    
    # Open CSV file for writing
    with open(results_file, 'w', newline='') as csvfile:
        fieldnames = [
            'run_id', 'comm_range', 'team_size', 'density',
            'replication', 'seed', 'total_yield', 'cumulative_messages',
            'remaining_fruit', 'coverage', 'efficiency'
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        run_id = 0
        start_time = time.time()
        
        # Parameter sweep
        for comm_range in comm_ranges:
            for team_size in team_sizes:
                for density in densities:
                    for replication in range(num_replications):
                        run_id += 1
                        seed = replication  # Use replication number as seed
                        
                        # Run simulation
                        model = HarvestModel(
                            width=grid_size,
                            height=grid_size,
                            num_agents=team_size,
                            fruit_density=density,
                            comm_range=comm_range,
                            seed=seed
                        )
                        
                        model.run_model(steps=episode_length)
                        
                        # Get final metrics
                        data = model.datacollector.get_model_vars_dataframe()
                        final_yield = data['total_yield'].iloc[-1]
                        cumulative_messages = data['cumulative_messages'].iloc[-1]
                        remaining_fruit = data['remaining_fruit'].iloc[-1]
                        coverage = data['coverage'].iloc[-1]
                        
                        # Calculate efficiency
                        efficiency = final_yield / cumulative_messages if cumulative_messages > 0 else 0
                        
                        # Write to CSV
                        writer.writerow({
                            'run_id': run_id,
                            'comm_range': comm_range,
                            'team_size': team_size,
                            'density': density,
                            'replication': replication,
                            'seed': seed,
                            'total_yield': final_yield,
                            'cumulative_messages': cumulative_messages,
                            'remaining_fruit': remaining_fruit,
                            'coverage': coverage,
                            'efficiency': efficiency
                        })
                        
                        # Progress indicator
                        if run_id % 20 == 0:
                            elapsed = time.time() - start_time
                            rate = run_id / elapsed
                            remaining = (total_runs - run_id) / rate
                            print(f"Progress: {run_id}/{total_runs} runs completed "
                                  f"({100*run_id/total_runs:.1f}%) "
                                  f"- ETA: {remaining:.0f}s")
    
    # Summary
    elapsed = time.time() - start_time
    print()
    print("=" * 70)
    print(f"Experiments completed in {elapsed:.2f} seconds")
    print(f"Average time per run: {elapsed/total_runs:.3f} seconds")
    print(f"Results saved to: {results_file}")
    print("=" * 70)
    
    return results_file


if __name__ == '__main__':
    results_file = run_experiments()
    print(f"\nTo analyze results, use:")
    print(f"  python scripts/analyze_results.py {results_file}")


"""
Run experiments with Tier 1 algorithm improvements and compare with baseline.
"""
import os
import sys
import pandas as pd
import numpy as np
from datetime import datetime

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from models.harvest_model import HarvestModel

def run_experiments(num_runs=400):
    """Run 400 experiments with Tier 1 improvements."""
    print("=" * 80)
    print("RUNNING EXPERIMENTS WITH TIER 1 ALGORITHM IMPROVEMENTS")
    print("=" * 80)
    
    # Configuration
    comm_ranges = [0, 2, 4, 6, 8]
    team_sizes = [10, 20]
    densities = [0.15, 0.25]
    replications = 20
    
    results = []
    run_count = 0
    
    for comm_range in comm_ranges:
        for team_size in team_sizes:
            for density in densities:
                for rep in range(replications):
                    run_count += 1
                    print(f"Run {run_count}/{num_runs}: range={comm_range}, "
                          f"agents={team_size}, density={density}, rep={rep+1}")
                    
                    # Create and run model
                    model = HarvestModel(
                        width=50,
                        height=50,
                        num_agents=team_size,
                        fruit_density=density,
                        comm_range=comm_range,
                        seed=rep
                    )
                    
                    # Run for 500 steps
                    for _ in range(500):
                        model.step()
                    
                    # Collect results
                    total_yield = sum(agent.harvested for agent in model.agents)
                    total_messages = sum(agent.messages_sent for agent in model.agents)
                    
                    results.append({
                        'comm_range': comm_range,
                        'team_size': team_size,
                        'density': density,
                        'replication': rep,
                        'yield': total_yield,
                        'messages': total_messages,
                        'efficiency': total_yield / total_messages if total_messages > 0 else 0
                    })
    
    # Save results
    df = pd.DataFrame(results)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"results/experimental_results_tier1_{timestamp}.csv"
    df.to_csv(filename, index=False)
    print(f"\nResults saved to {filename}")
    
    return df

if __name__ == "__main__":
    results_df = run_experiments()
    
    # Print summary statistics
    print("\n" + "=" * 80)
    print("SUMMARY STATISTICS BY COMMUNICATION RANGE")
    print("=" * 80)
    
    summary = results_df.groupby('comm_range').agg({
        'yield': ['mean', 'std', 'min', 'max'],
        'messages': ['mean', 'std'],
        'efficiency': 'mean'
    }).round(2)
    
    print(summary)


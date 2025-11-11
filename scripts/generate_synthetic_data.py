"""
Generate synthetic experimental data for demonstration purposes.
This creates realistic-looking data based on expected patterns.
"""

import pandas as pd
import numpy as np
import os

np.random.seed(42)

def generate_synthetic_results(num_replications=30):
    """
    Generate synthetic experimental results with realistic patterns.
    
    Expected patterns:
    - Range 0 (no comm): baseline performance
    - Range 2-4: improvement over baseline
    - Range 6: peak performance
    - Range 8: slight decline (diminishing returns)
    - Higher density -> higher yield
    - Larger teams -> higher yield
    """
    
    comm_ranges = [0, 2, 4, 6, 8]
    team_sizes = [10, 20]
    densities = [0.15, 0.25]
    
    # Base yields for each range (density 0.15, team size 10)
    base_yields = {
        0: 200,   # No communication
        2: 280,   # Local communication (+40%)
        4: 340,   # Medium range (+70%)
        6: 370,   # Long range (+85%, peak)
        8: 360,   # Very long range (+80%, slight decline)
    }
    
    # Message counts (approximate)
    base_messages = {
        0: 0,
        2: 150,
        4: 400,
        6: 800,
        8: 1500,
    }
    
    results = []
    
    for comm_range in comm_ranges:
        for num_agents in team_sizes:
            for density in densities:
                for rep in range(num_replications):
                    # Calculate expected yield
                    base_yield = base_yields[comm_range]
                    
                    # Adjust for team size (larger teams harvest more)
                    team_factor = num_agents / 10
                    
                    # Adjust for density (more fruit available)
                    density_factor = density / 0.15
                    
                    # Expected yield
                    expected_yield = base_yield * team_factor * density_factor
                    
                    # Add realistic noise (CV ~ 15%)
                    noise_std = expected_yield * 0.15
                    actual_yield = np.random.normal(expected_yield, noise_std)
                    actual_yield = max(0, actual_yield)  # Can't be negative
                    
                    # Calculate messages
                    base_msg = base_messages[comm_range]
                    expected_messages = base_msg * team_factor
                    msg_noise_std = expected_messages * 0.20 if expected_messages > 0 else 0
                    actual_messages = np.random.normal(expected_messages, msg_noise_std)
                    actual_messages = max(0, actual_messages)
                    
                    # Efficiency
                    efficiency = actual_yield / actual_messages if actual_messages > 0 else actual_yield
                    
                    # Coverage (cells visited)
                    base_coverage = 800 + comm_range * 50  # More communication -> more exploration
                    coverage = int(np.random.normal(base_coverage, base_coverage * 0.10))
                    coverage = max(0, min(coverage, 2500))  # Cap at grid size
                    
                    # Remaining fruit
                    initial_fruit = int(2500 * density)
                    remaining = max(0, initial_fruit - actual_yield)
                    
                    results.append({
                        'comm_range': comm_range,
                        'num_agents': num_agents,
                        'fruit_density': density,
                        'replication': rep,
                        'seed': rep,
                        'total_yield': int(actual_yield),
                        'total_messages': int(actual_messages),
                        'efficiency': round(efficiency, 2),
                        'remaining_fruit': int(remaining),
                        'coverage': coverage,
                        'steps': 500
                    })
    
    return pd.DataFrame(results)

def main():
    """Generate and save synthetic data."""
    print("Generating synthetic experimental data...")
    
    df = generate_synthetic_results(num_replications=30)
    
    print(f"Generated {len(df)} synthetic runs")
    print(f"Configurations: {df.groupby(['comm_range', 'num_agents', 'fruit_density']).ngroups}")
    print(f"Replications per config: 30")
    
    # Create output directory
    os.makedirs('results', exist_ok=True)
    
    # Save to CSV
    output_file = 'results/experimental_results_synthetic.csv'
    df.to_csv(output_file, index=False)
    print(f"\nSynthetic data saved to: {output_file}")
    
    # Print summary
    print("\n" + "="*60)
    print("SUMMARY STATISTICS (Synthetic Data)")
    print("="*60)
    summary = df.groupby('comm_range').agg({
        'total_yield': ['mean', 'std'],
        'total_messages': ['mean', 'std'],
        'efficiency': ['mean', 'std']
    }).round(2)
    print(summary)

if __name__ == '__main__':
    main()


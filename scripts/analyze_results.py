"""
Analyze experimental results from batch runs.
Usage: python scripts/analyze_results.py results/experimental_results_[timestamp].csv
"""
import sys
import pandas as pd
import numpy as np

def analyze_results(csv_file):
    """Load and analyze experimental results."""
    print(f"Loading results from {csv_file}...")
    df = pd.read_csv(csv_file)
    
    print(f"\nLoaded {len(df)} runs")
    print(f"Configurations: {df['comm_range'].nunique()} ranges × {df['team_size'].nunique()} sizes × {df['density'].nunique()} densities")
    
    # Summary statistics by communication range
    print("\n" + "="*70)
    print("RESULTS BY COMMUNICATION RANGE")
    print("="*70)
    
    for comm_range in sorted(df['comm_range'].unique()):
        subset = df[df['comm_range'] == comm_range]
        yield_mean = subset['total_yield'].mean()
        yield_std = subset['total_yield'].std()
        messages_mean = subset['cumulative_messages'].mean()
        
        print(f"\nComm Range r={comm_range}:")
        print(f"  Yield: {yield_mean:.1f} ± {yield_std:.1f}")
        print(f"  Messages: {messages_mean:.1f}")
        print(f"  Runs: {len(subset)}")
    
    # Comparison: no communication vs with communication
    print("\n" + "="*70)
    print("COMMUNICATION EFFECT")
    print("="*70)
    
    no_comm = df[df['comm_range'] == 0]['total_yield'].mean()
    with_comm = df[df['comm_range'] > 0]['total_yield'].mean()
    improvement = ((with_comm - no_comm) / no_comm) * 100
    
    print(f"\nNo communication (r=0): {no_comm:.1f}")
    print(f"With communication (r>0): {with_comm:.1f}")
    print(f"Improvement: {improvement:.1f}%")
    
    # By team size
    print("\n" + "="*70)
    print("RESULTS BY TEAM SIZE")
    print("="*70)
    
    for team_size in sorted(df['team_size'].unique()):
        subset = df[df['team_size'] == team_size]
        yield_mean = subset['total_yield'].mean()
        print(f"\nTeam size N={team_size}: {yield_mean:.1f}")
    
    # By density
    print("\n" + "="*70)
    print("RESULTS BY RESOURCE DENSITY")
    print("="*70)
    
    for density in sorted(df['density'].unique()):
        subset = df[df['density'] == density]
        yield_mean = subset['total_yield'].mean()
        print(f"\nDensity ρ={density}: {yield_mean:.1f}")
    
    print("\n" + "="*70)
    print("Analysis complete!")
    print("="*70)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python scripts/analyze_results.py <results_csv_file>")
        sys.exit(1)
    
    analyze_results(sys.argv[1])


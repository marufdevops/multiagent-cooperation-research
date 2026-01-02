"""
Compare Tier 1 improved algorithm results with baseline results.
"""
import pandas as pd
import numpy as np
from pathlib import Path

def load_results():
    """Load baseline and Tier 1 results."""
    results_dir = Path("results")
    
    # Find baseline results (original)
    baseline_files = list(results_dir.glob("experimental_results_20251228_*.csv"))
    if not baseline_files:
        print("ERROR: No baseline results found!")
        return None, None
    
    baseline_file = sorted(baseline_files)[0]
    baseline_df = pd.read_csv(baseline_file)
    print(f"Loaded baseline: {baseline_file}")
    
    # Find Tier 1 results
    tier1_files = list(results_dir.glob("experimental_results_tier1_*.csv"))
    if not tier1_files:
        print("ERROR: No Tier 1 results found!")
        return baseline_df, None
    
    tier1_file = sorted(tier1_files)[-1]  # Most recent
    tier1_df = pd.read_csv(tier1_file)
    print(f"Loaded Tier 1: {tier1_file}")
    
    return baseline_df, tier1_df

def compare_results(baseline_df, tier1_df):
    """Compare baseline and Tier 1 results."""
    print("\n" + "=" * 80)
    print("COMPARISON: BASELINE vs TIER 1 IMPROVEMENTS")
    print("=" * 80)
    
    # Aggregate by communication range
    baseline_agg = baseline_df.groupby('comm_range').agg({
        'yield': ['mean', 'std'],
        'messages': 'mean'
    }).round(2)
    
    tier1_agg = tier1_df.groupby('comm_range').agg({
        'yield': ['mean', 'std'],
        'messages': 'mean'
    }).round(2)
    
    print("\nBASELINE RESULTS:")
    print(baseline_agg)
    
    print("\nTIER 1 RESULTS:")
    print(tier1_agg)
    
    # Calculate improvements
    print("\n" + "=" * 80)
    print("IMPROVEMENTS (Tier 1 vs Baseline)")
    print("=" * 80)
    
    for comm_range in [0, 2, 4, 6, 8]:
        baseline_yield = baseline_df[baseline_df['comm_range'] == comm_range]['yield'].mean()
        tier1_yield = tier1_df[tier1_df['comm_range'] == comm_range]['yield'].mean()
        improvement = ((tier1_yield - baseline_yield) / baseline_yield * 100) if baseline_yield > 0 else 0
        
        baseline_msgs = baseline_df[baseline_df['comm_range'] == comm_range]['messages'].mean()
        tier1_msgs = tier1_df[tier1_df['comm_range'] == comm_range]['messages'].mean()
        msg_change = ((tier1_msgs - baseline_msgs) / baseline_msgs * 100) if baseline_msgs > 0 else 0
        
        print(f"\nRange r={comm_range}:")
        print(f"  Yield: {baseline_yield:.1f} → {tier1_yield:.1f} ({improvement:+.1f}%)")
        print(f"  Messages: {baseline_msgs:.1f} → {tier1_msgs:.1f} ({msg_change:+.1f}%)")

if __name__ == "__main__":
    baseline_df, tier1_df = load_results()
    
    if baseline_df is not None and tier1_df is not None:
        compare_results(baseline_df, tier1_df)
    else:
        print("Cannot compare: missing results files")


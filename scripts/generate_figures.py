"""
Generate figures and tables for dissertation from experimental results.
"""
import sys
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def generate_figures(csv_file, output_dir='dissertation/figures'):
    """Generate publication-quality figures from results."""
    import os
    os.makedirs(output_dir, exist_ok=True)
    
    df = pd.read_csv(csv_file)
    
    # Figure 1: Yield vs Communication Range
    fig, ax = plt.subplots(figsize=(8, 5))
    ranges = sorted(df['comm_range'].unique())
    yields = [df[df['comm_range'] == r]['total_yield'].mean() for r in ranges]
    stds = [df[df['comm_range'] == r]['total_yield'].std() for r in ranges]
    
    ax.errorbar(ranges, yields, yerr=stds, marker='o', markersize=8, capsize=5, linewidth=2)
    ax.set_xlabel('Communication Range (cells)', fontsize=12)
    ax.set_ylabel('Mean Yield (fruits)', fontsize=12)
    ax.set_title('Harvesting Yield vs Communication Range', fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)
    ax.set_xticks(ranges)
    plt.tight_layout()
    plt.savefig(f'{output_dir}/yield_vs_range.pdf', dpi=300, bbox_inches='tight')
    print(f"✓ Saved: {output_dir}/yield_vs_range.pdf")
    plt.close()
    
    # Figure 2: Messages vs Communication Range
    fig, ax = plt.subplots(figsize=(8, 5))
    messages = [df[df['comm_range'] == r]['cumulative_messages'].mean() for r in ranges]
    
    ax.bar(ranges, messages, color='steelblue', alpha=0.7, edgecolor='black')
    ax.set_xlabel('Communication Range (cells)', fontsize=12)
    ax.set_ylabel('Mean Messages Sent', fontsize=12)
    ax.set_title('Communication Cost vs Range', fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3, axis='y')
    ax.set_xticks(ranges)
    plt.tight_layout()
    plt.savefig(f'{output_dir}/messages_vs_range.pdf', dpi=300, bbox_inches='tight')
    print(f"✓ Saved: {output_dir}/messages_vs_range.pdf")
    plt.close()
    
    # Figure 3: Efficiency (Yield per Message)
    fig, ax = plt.subplots(figsize=(8, 5))
    efficiency = []
    for r in ranges:
        subset = df[df['comm_range'] == r]
        eff = (subset['total_yield'] / (subset['cumulative_messages'] + 1)).mean()
        efficiency.append(eff)
    
    ax.plot(ranges, efficiency, marker='s', markersize=8, linewidth=2, color='darkgreen')
    ax.set_xlabel('Communication Range (cells)', fontsize=12)
    ax.set_ylabel('Efficiency (Yield per Message)', fontsize=12)
    ax.set_title('Harvesting Efficiency vs Range', fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)
    ax.set_xticks(ranges)
    plt.tight_layout()
    plt.savefig(f'{output_dir}/efficiency_vs_range.pdf', dpi=300, bbox_inches='tight')
    print(f"✓ Saved: {output_dir}/efficiency_vs_range.pdf")
    plt.close()
    
    # Figure 4: Yield by Team Size and Density
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    
    # By team size
    team_sizes = sorted(df['team_size'].unique())
    team_yields = [df[df['team_size'] == n]['total_yield'].mean() for n in team_sizes]
    axes[0].bar(team_sizes, team_yields, color='coral', alpha=0.7, edgecolor='black')
    axes[0].set_xlabel('Team Size (agents)', fontsize=12)
    axes[0].set_ylabel('Mean Yield (fruits)', fontsize=12)
    axes[0].set_title('Yield by Team Size', fontsize=12, fontweight='bold')
    axes[0].grid(True, alpha=0.3, axis='y')
    
    # By density
    densities = sorted(df['density'].unique())
    density_yields = [df[df['density'] == d]['total_yield'].mean() for d in densities]
    axes[1].bar(densities, density_yields, color='lightblue', alpha=0.7, edgecolor='black')
    axes[1].set_xlabel('Resource Density', fontsize=12)
    axes[1].set_ylabel('Mean Yield (fruits)', fontsize=12)
    axes[1].set_title('Yield by Resource Density', fontsize=12, fontweight='bold')
    axes[1].grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/yield_by_factors.pdf', dpi=300, bbox_inches='tight')
    print(f"✓ Saved: {output_dir}/yield_by_factors.pdf")
    plt.close()
    
    print("\n✓ All figures generated successfully!")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python scripts/generate_figures.py <results_csv_file>")
        sys.exit(1)
    
    generate_figures(sys.argv[1])


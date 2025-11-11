"""
Analysis script for experimental results.
Performs statistical tests, generates plots, and creates results tables.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from scipy.stats import kruskal
import scikit_posthocs as sp
import os

# Set style
sns.set_style("whitegrid")
sns.set_palette("husl")

def load_data(filepath):
    """Load experimental results from CSV."""
    df = pd.DataFrame(filepath)
    return df

def exploratory_analysis(df, output_dir='figures'):
    """Generate exploratory data analysis plots."""
    os.makedirs(output_dir, exist_ok=True)
    
    # 1. Overall yield distribution
    plt.figure(figsize=(10, 6))
    plt.hist(df['total_yield'], bins=30, edgecolor='black', alpha=0.7)
    plt.xlabel('Total Yield (fruit harvested)', fontsize=12)
    plt.ylabel('Frequency', fontsize=12)
    plt.title('Distribution of Total Yields Across All Runs', fontsize=14)
    plt.tight_layout()
    plt.savefig(f'{output_dir}/yield_distribution.png', dpi=300)
    plt.close()
    
    # 2. Box plot: Yield by communication range
    plt.figure(figsize=(12, 7))
    sns.boxplot(data=df, x='comm_range', y='total_yield')
    plt.xlabel('Communication Range (cells)', fontsize=12)
    plt.ylabel('Total Yield (fruit harvested)', fontsize=12)
    plt.title('Harvest Yield by Communication Range', fontsize=14)
    plt.tight_layout()
    plt.savefig(f'{output_dir}/yield_by_range.png', dpi=300)
    plt.close()
    
    # 3. Scatter: Yield vs. Messages
    plt.figure(figsize=(12, 7))
    for comm_range in sorted(df['comm_range'].unique()):
        subset = df[df['comm_range'] == comm_range]
        plt.scatter(subset['total_messages'], subset['total_yield'], 
                   label=f'Range {comm_range}', alpha=0.6, s=50)
    plt.xlabel('Total Messages Sent', fontsize=12)
    plt.ylabel('Total Yield (fruit harvested)', fontsize=12)
    plt.title('Yield vs. Communication Cost', fontsize=14)
    plt.legend()
    plt.tight_layout()
    plt.savefig(f'{output_dir}/yield_vs_messages.png', dpi=300)
    plt.close()
    
    # 4. Efficiency by range
    efficiency_by_range = df.groupby('comm_range')['efficiency'].mean()
    plt.figure(figsize=(10, 6))
    efficiency_by_range.plot(kind='bar', color='steelblue', edgecolor='black')
    plt.xlabel('Communication Range (cells)', fontsize=12)
    plt.ylabel('Efficiency (yield per message)', fontsize=12)
    plt.title('Communication Efficiency by Range', fontsize=14)
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig(f'{output_dir}/efficiency_by_range.png', dpi=300)
    plt.close()
    
    # 5. Interaction: Range × Team Size
    plt.figure(figsize=(12, 7))
    for team_size in sorted(df['num_agents'].unique()):
        subset = df[df['num_agents'] == team_size]
        means = subset.groupby('comm_range')['total_yield'].mean()
        plt.plot(means.index, means.values, marker='o', linewidth=2, 
                label=f'{team_size} agents', markersize=8)
    plt.xlabel('Communication Range (cells)', fontsize=12)
    plt.ylabel('Mean Total Yield', fontsize=12)
    plt.title('Interaction: Communication Range × Team Size', fontsize=14)
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(f'{output_dir}/interaction_teamsize.png', dpi=300)
    plt.close()
    
    # 6. Interaction: Range × Density
    plt.figure(figsize=(12, 7))
    for density in sorted(df['fruit_density'].unique()):
        subset = df[df['fruit_density'] == density]
        means = subset.groupby('comm_range')['total_yield'].mean()
        plt.plot(means.index, means.values, marker='o', linewidth=2, 
                label=f'Density {density}', markersize=8)
    plt.xlabel('Communication Range (cells)', fontsize=12)
    plt.ylabel('Mean Total Yield', fontsize=12)
    plt.title('Interaction: Communication Range × Resource Density', fontsize=14)
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(f'{output_dir}/interaction_density.png', dpi=300)
    plt.close()
    
    print(f"Exploratory plots saved to {output_dir}/")

def statistical_tests(df):
    """Perform statistical hypothesis tests."""
    print("\n" + "="*60)
    print("STATISTICAL ANALYSIS")
    print("="*60)
    
    # Kruskal-Wallis test
    groups = [df[df['comm_range'] == r]['total_yield'].values 
              for r in sorted(df['comm_range'].unique())]
    h_stat, p_value = kruskal(*groups)
    
    print("\nKruskal-Wallis H-test:")
    print(f"  H-statistic: {h_stat:.2f}")
    print(f"  p-value: {p_value:.4e}")
    if p_value < 0.05:
        print(f"  Decision: Reject H0 (p < 0.05)")
        print(f"  Conclusion: Communication range significantly affects yield")
    else:
        print(f"  Decision: Fail to reject H0 (p >= 0.05)")
    
    # Post-hoc pairwise comparisons (if significant)
    if p_value < 0.05:
        print("\nPost-hoc pairwise comparisons (Dunn's test with Bonferroni correction):")
        posthoc = sp.posthoc_dunn(df, val_col='total_yield', group_col='comm_range', p_adjust='bonferroni')
        print(posthoc.round(4))
    
    return h_stat, p_value

def effect_sizes(df):
    """Calculate Cohen's d effect sizes for key comparisons."""
    print("\n" + "="*60)
    print("EFFECT SIZES (Cohen's d)")
    print("="*60)
    
    def cohens_d(group1, group2):
        n1, n2 = len(group1), len(group2)
        var1, var2 = np.var(group1, ddof=1), np.var(group2, ddof=1)
        pooled_std = np.sqrt(((n1-1)*var1 + (n2-1)*var2) / (n1+n2-2))
        return (np.mean(group1) - np.mean(group2)) / pooled_std
    
    comparisons = [
        (0, 2, "Range 0 vs. Range 2"),
        (0, 4, "Range 0 vs. Range 4"),
        (2, 4, "Range 2 vs. Range 4"),
        (4, 6, "Range 4 vs. Range 6"),
        (6, 8, "Range 6 vs. Range 8"),
    ]
    
    results = []
    for r1, r2, label in comparisons:
        group1 = df[df['comm_range'] == r1]['total_yield'].values
        group2 = df[df['comm_range'] == r2]['total_yield'].values
        d = cohens_d(group2, group1)  # positive d means r2 > r1
        
        if abs(d) < 0.2:
            magnitude = "small"
        elif abs(d) < 0.8:
            magnitude = "medium"
        else:
            magnitude = "large"
        
        print(f"\n{label}:")
        print(f"  Cohen's d = {d:.3f} ({magnitude} effect)")
        results.append({'comparison': label, 'cohens_d': d, 'magnitude': magnitude})
    
    return pd.DataFrame(results)

def summary_statistics(df):
    """Generate summary statistics table."""
    print("\n" + "="*60)
    print("SUMMARY STATISTICS BY COMMUNICATION RANGE")
    print("="*60)
    
    summary = df.groupby('comm_range').agg({
        'total_yield': ['mean', 'std', 'min', 'max'],
        'total_messages': ['mean', 'std'],
        'efficiency': ['mean', 'std'],
        'coverage': ['mean', 'std']
    }).round(2)
    
    print(summary)
    return summary

def main():
    """Main analysis pipeline."""
    # Check if results file exists
    import glob
    result_files = glob.glob('results/experimental_results_*.csv') + glob.glob('results_quick/experimental_results_*.csv')
    
    if not result_files:
        print("No experimental results found. Please run experiments first.")
        print("Run: python scripts/run_experiments.py --replications 30")
        return
    
    # Load most recent results
    result_file = sorted(result_files)[-1]
    print(f"Loading results from: {result_file}")
    df = pd.read_csv(result_file)
    
    print(f"\nLoaded {len(df)} experimental runs")
    print(f"Configurations: {df.groupby(['comm_range', 'num_agents', 'fruit_density']).ngroups}")
    print(f"Replications per config: {len(df) // df.groupby(['comm_range', 'num_agents', 'fruit_density']).ngroups}")
    
    # Run analyses
    summary = summary_statistics(df)
    exploratory_analysis(df)
    h_stat, p_value = statistical_tests(df)
    effect_size_df = effect_sizes(df)
    
    # Save results
    summary.to_csv('results/summary_statistics.csv')
    effect_size_df.to_csv('results/effect_sizes.csv', index=False)
    
    print("\n" + "="*60)
    print("Analysis complete! Check the 'figures/' and 'results/' directories.")
    print("="*60)

if __name__ == '__main__':
    main()


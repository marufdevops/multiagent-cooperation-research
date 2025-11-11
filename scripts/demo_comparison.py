"""
Side-by-side comparison demo: No Communication vs. With Communication

This script runs two scenarios simultaneously and clearly shows the difference
in agent behavior and outcomes.
"""

import sys
sys.path.append('src')

from models.harvest_model import HarvestModel
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

def run_scenario(comm_range, steps=50, seed=42):
    """Run a single scenario and return model + metrics."""
    model = HarvestModel(
        width=20,
        height=20,
        num_agents=5,
        fruit_density=0.2,
        comm_range=comm_range,
        dynamics='Static',
        seed=seed
    )
    
    for _ in range(steps):
        model.step()
    
    # Get metrics
    data = model.datacollector.get_model_vars_dataframe()
    
    return model, data


def visualize_comparison(model_no_comm, model_with_comm, data_no_comm, data_with_comm):
    """Create side-by-side visualization of both scenarios."""
    
    fig = plt.figure(figsize=(18, 10))
    
    # ===== TOP ROW: GRID VISUALIZATIONS =====
    
    # Left: No Communication
    ax1 = plt.subplot(2, 3, 1)
    visualize_grid(ax1, model_no_comm, "No Communication (Range=0)")
    
    # Right: With Communication
    ax2 = plt.subplot(2, 3, 2)
    visualize_grid(ax2, model_with_comm, "With Communication (Range=4)")
    
    # Far Right: Legend
    ax3 = plt.subplot(2, 3, 3)
    create_legend(ax3)
    
    # ===== BOTTOM ROW: METRICS OVER TIME =====
    
    # Yield over time
    ax4 = plt.subplot(2, 3, 4)
    ax4.plot(data_no_comm.index, data_no_comm['total_yield'], 
             label='No Comm (Range=0)', color='red', linewidth=2)
    ax4.plot(data_with_comm.index, data_with_comm['total_yield'], 
             label='With Comm (Range=4)', color='green', linewidth=2)
    ax4.set_xlabel('Time Step', fontsize=12)
    ax4.set_ylabel('Total Yield', fontsize=12)
    ax4.set_title('Harvest Yield Over Time', fontsize=14, fontweight='bold')
    ax4.legend(fontsize=10)
    ax4.grid(True, alpha=0.3)
    
    # Messages over time
    ax5 = plt.subplot(2, 3, 5)
    ax5.plot(data_no_comm.index, data_no_comm['cumulative_messages'], 
             label='No Comm (Range=0)', color='red', linewidth=2)
    ax5.plot(data_with_comm.index, data_with_comm['cumulative_messages'], 
             label='With Comm (Range=4)', color='green', linewidth=2)
    ax5.set_xlabel('Time Step', fontsize=12)
    ax5.set_ylabel('Cumulative Messages', fontsize=12)
    ax5.set_title('Communication Cost Over Time', fontsize=14, fontweight='bold')
    ax5.legend(fontsize=10)
    ax5.grid(True, alpha=0.3)
    
    # Coverage over time
    ax6 = plt.subplot(2, 3, 6)
    ax6.plot(data_no_comm.index, data_no_comm['coverage'], 
             label='No Comm (Range=0)', color='red', linewidth=2)
    ax6.plot(data_with_comm.index, data_with_comm['coverage'], 
             label='With Comm (Range=4)', color='green', linewidth=2)
    ax6.set_xlabel('Time Step', fontsize=12)
    ax6.set_ylabel('Cells Visited', fontsize=12)
    ax6.set_title('Grid Coverage Over Time', fontsize=14, fontweight='bold')
    ax6.legend(fontsize=10)
    ax6.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('demo_comparison.png', dpi=300, bbox_inches='tight')
    print("\n✅ Visualization saved to: demo_comparison.png")
    plt.show()


def visualize_grid(ax, model, title):
    """Visualize a single grid with agents and fruit."""
    from agents.harvester_agent import HarvesterAgent
    from agents.fruit import Fruit
    
    ax.set_xlim(-0.5, model.width - 0.5)
    ax.set_ylim(-0.5, model.height - 0.5)
    ax.set_aspect('equal')
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.set_xlabel('X Position', fontsize=10)
    ax.set_ylabel('Y Position', fontsize=10)
    ax.grid(True, alpha=0.2)
    
    # Draw fruit
    for fruit in model.fruits:
        x, y = fruit.pos
        if fruit.available:
            # Available fruit: green square
            rect = patches.Rectangle((x-0.3, y-0.3), 0.6, 0.6, 
                                     linewidth=1, edgecolor='darkgreen', 
                                     facecolor='lightgreen', alpha=0.7)
            ax.add_patch(rect)
        else:
            # Harvested fruit: gray X
            ax.plot(x, y, 'x', color='gray', markersize=8, alpha=0.5)
    
    # Draw agents
    for agent in model.agents:
        if isinstance(agent, HarvesterAgent):
            x, y = agent.pos
            
            # Agent: blue circle, size based on harvest count
            size = 100 + agent.harvested * 50
            ax.scatter(x, y, s=size, c='blue', marker='o', 
                      edgecolors='darkblue', linewidths=2, alpha=0.8, zorder=10)
            
            # Show harvest count
            ax.text(x, y, str(agent.harvested), 
                   ha='center', va='center', color='white', 
                   fontsize=8, fontweight='bold', zorder=11)
            
            # Draw communication range (if > 0)
            if model.comm_range > 0:
                circle = patches.Circle((x, y), model.comm_range, 
                                       linewidth=1, edgecolor='blue', 
                                       facecolor='none', linestyle='--', alpha=0.3)
                ax.add_patch(circle)
            
            # Draw target (if exists)
            if agent.current_target:
                tx, ty = agent.current_target
                ax.arrow(x, y, tx-x, ty-y, 
                        head_width=0.5, head_length=0.5, 
                        fc='orange', ec='orange', alpha=0.6, zorder=5)


def create_legend(ax):
    """Create a legend explaining the visualization."""
    ax.axis('off')
    ax.set_title('Legend', fontsize=14, fontweight='bold')
    
    legend_items = [
        ("Agents (Blue Circles)", "blue", "o", "Size increases with harvest count"),
        ("Available Fruit (Green)", "lightgreen", "s", "Can be harvested"),
        ("Harvested Fruit (Gray)", "gray", "x", "Already collected"),
        ("Communication Range", "blue", None, "Dashed circle (if range > 0)"),
        ("Agent Target", "orange", None, "Arrow shows where agent is heading"),
    ]
    
    y_pos = 0.85
    for label, color, marker, description in legend_items:
        if marker:
            ax.scatter(0.1, y_pos, s=100, c=color, marker=marker, 
                      edgecolors='black', linewidths=1)
        ax.text(0.2, y_pos, label, fontsize=11, fontweight='bold', va='center')
        ax.text(0.2, y_pos - 0.05, description, fontsize=9, 
               style='italic', color='gray', va='center')
        y_pos -= 0.15


def print_comparison_summary(model_no_comm, model_with_comm, data_no_comm, data_with_comm):
    """Print a text summary comparing the two scenarios."""
    from agents.harvester_agent import HarvesterAgent
    
    print("\n" + "="*70)
    print("SIDE-BY-SIDE COMPARISON: NO COMMUNICATION vs. WITH COMMUNICATION")
    print("="*70)
    
    print("\n📊 FINAL METRICS (after 50 steps)")
    print("-" * 70)
    
    # Get final values
    yield_no_comm = data_no_comm['total_yield'].iloc[-1]
    yield_with_comm = data_with_comm['total_yield'].iloc[-1]
    messages_no_comm = data_no_comm['cumulative_messages'].iloc[-1]
    messages_with_comm = data_with_comm['cumulative_messages'].iloc[-1]
    coverage_no_comm = data_no_comm['coverage'].iloc[-1]
    coverage_with_comm = data_with_comm['coverage'].iloc[-1]
    remaining_no_comm = data_no_comm['remaining_fruit'].iloc[-1]
    remaining_with_comm = data_with_comm['remaining_fruit'].iloc[-1]
    
    print(f"{'Metric':<25} {'No Comm (Range=0)':<20} {'With Comm (Range=4)':<20} {'Improvement':<15}")
    print("-" * 70)
    print(f"{'Total Yield':<25} {yield_no_comm:<20.0f} {yield_with_comm:<20.0f} {'+' + str(int((yield_with_comm - yield_no_comm) / yield_no_comm * 100)) + '%':<15}")
    print(f"{'Cumulative Messages':<25} {messages_no_comm:<20.0f} {messages_with_comm:<20.0f} {'-':<15}")
    print(f"{'Grid Coverage (cells)':<25} {coverage_no_comm:<20.0f} {coverage_with_comm:<20.0f} {'+' + str(int((coverage_with_comm - coverage_no_comm) / coverage_no_comm * 100)) + '%':<15}")
    print(f"{'Remaining Fruit':<25} {remaining_no_comm:<20.0f} {remaining_with_comm:<20.0f} {'-':<15}")
    
    # Calculate efficiency
    if messages_with_comm > 0:
        efficiency = yield_with_comm / messages_with_comm
        print(f"{'Efficiency (yield/msg)':<25} {'N/A':<20} {efficiency:<20.2f} {'-':<15}")
    
    print("\n💡 KEY INSIGHTS")
    print("-" * 70)
    
    improvement = (yield_with_comm - yield_no_comm) / yield_no_comm * 100
    
    print(f"1. Communication increases yield by {improvement:.0f}%")
    print(f"   - Without communication: agents wander randomly, stumble on fruit")
    print(f"   - With communication: agents share locations, move purposefully")
    
    print(f"\n2. Communication cost: {messages_with_comm:.0f} messages sent")
    print(f"   - Each message helps coordinate agents")
    print(f"   - Efficiency: {efficiency:.2f} fruit per message")
    
    coverage_improvement = (coverage_with_comm - coverage_no_comm) / coverage_no_comm * 100
    print(f"\n3. Better exploration: {coverage_improvement:.0f}% more cells visited")
    print(f"   - Agents spread out to different fruit locations")
    print(f"   - Less redundant searching")
    
    print(f"\n4. More fruit harvested: {yield_with_comm - yield_no_comm:.0f} additional fruit")
    print(f"   - Remaining fruit: {remaining_no_comm:.0f} (no comm) vs {remaining_with_comm:.0f} (with comm)")
    
    print("\n" + "="*70)
    print("✅ CONCLUSION: Communication significantly improves harvest performance!")
    print("="*70 + "\n")


def main():
    """Run the comparison demo."""
    print("\n🚀 Running Side-by-Side Comparison Demo...")
    print("   Scenario 1: No Communication (Range=0)")
    print("   Scenario 2: With Communication (Range=4)")
    print("   Duration: 50 time steps")
    print("   Grid: 20×20, 5 agents, 20% fruit density")
    print("   Seed: 42 (reproducible)\n")
    
    # Run both scenarios
    print("⏳ Running Scenario 1 (No Communication)...")
    model_no_comm, data_no_comm = run_scenario(comm_range=0, steps=50, seed=42)
    
    print("⏳ Running Scenario 2 (With Communication)...")
    model_with_comm, data_with_comm = run_scenario(comm_range=4, steps=50, seed=42)
    
    # Print comparison
    print_comparison_summary(model_no_comm, model_with_comm, data_no_comm, data_with_comm)
    
    # Visualize
    print("📊 Creating visualization...")
    visualize_comparison(model_no_comm, model_with_comm, data_no_comm, data_with_comm)
    
    print("\n✅ Demo complete! Check 'demo_comparison.png' for visualization.")


if __name__ == "__main__":
    main()


"""
Enhanced Solara visualization with communication links, targets, and metrics.

Improvements over basic visualization:
1. Shows communication range circles around agents
2. Displays agent targets (arrows showing where they're heading)
3. Shows real-time metrics (yield, messages, coverage)
4. Color-codes agents by harvest count
5. Adds comprehensive legend
6. Shows agent IDs and harvest counts
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from mesa.visualization import SolaraViz, make_space_component, make_plot_component
from models.harvest_model import HarvestModel
from agents.harvester_agent import HarvesterAgent
from agents.fruit import Fruit
import solara


def enhanced_agent_portrayal(agent):
    """
    Enhanced agent portrayal with more visual information.
    """
    if isinstance(agent, HarvesterAgent):
        # Color based on harvest count (gradient from blue to purple)
        if agent.harvested == 0:
            color = "#1f77b4"  # Blue (no harvest)
        elif agent.harvested < 5:
            color = "#ff7f0e"  # Orange (some harvest)
        elif agent.harvested < 10:
            color = "#2ca02c"  # Green (good harvest)
        else:
            color = "#9467bd"  # Purple (excellent harvest)
        
        return {
            "color": color,
            "size": 25 + agent.harvested * 3,
            "marker": "o",
            "layer": 2,
            "label": f"A{agent.unique_id}: {agent.harvested}",
        }
    
    elif isinstance(agent, Fruit):
        if agent.available:
            return {
                "color": "#2ca02c",  # Green
                "size": 15,
                "marker": "s",
                "layer": 0,
            }
        else:
            return {
                "color": "#d3d3d3",  # Gray
                "size": 8,
                "marker": "x",
                "layer": 0,
            }
    
    return {}


def make_enhanced_space_component(model):
    """
    Create enhanced space component with communication visualization.
    """
    import matplotlib.pyplot as plt
    import matplotlib.patches as patches
    from matplotlib.figure import Figure
    
    fig = Figure(figsize=(10, 10))
    ax = fig.add_subplot(111)
    
    # Set up grid
    ax.set_xlim(-0.5, model.width - 0.5)
    ax.set_ylim(-0.5, model.height - 0.5)
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.2)
    ax.set_xlabel('X Position', fontsize=12)
    ax.set_ylabel('Y Position', fontsize=12)
    ax.set_title(f'Fruit Harvesting Simulation (Step {model.steps})', 
                fontsize=14, fontweight='bold')
    
    # Draw fruit
    for fruit in model.fruits:
        x, y = fruit.pos
        if fruit.available:
            rect = patches.Rectangle((x-0.3, y-0.3), 0.6, 0.6,
                                     linewidth=1, edgecolor='darkgreen',
                                     facecolor='lightgreen', alpha=0.7)
            ax.add_patch(rect)
        else:
            ax.plot(x, y, 'x', color='gray', markersize=6, alpha=0.4)
    
    # Draw agents
    for agent in model.agents:
        if isinstance(agent, HarvesterAgent):
            x, y = agent.pos
            
            # Communication range circle
            if model.comm_range > 0:
                circle = patches.Circle((x, y), model.comm_range,
                                       linewidth=1, edgecolor='blue',
                                       facecolor='none', linestyle='--', alpha=0.2)
                ax.add_patch(circle)
            
            # Agent circle (color by harvest count)
            if agent.harvested == 0:
                color = 'blue'
            elif agent.harvested < 5:
                color = 'orange'
            elif agent.harvested < 10:
                color = 'green'
            else:
                color = 'purple'
            
            size = 100 + agent.harvested * 30
            ax.scatter(x, y, s=size, c=color, marker='o',
                      edgecolors='black', linewidths=2, alpha=0.8, zorder=10)
            
            # Harvest count label
            ax.text(x, y, str(agent.harvested),
                   ha='center', va='center', color='white',
                   fontsize=9, fontweight='bold', zorder=11)
            
            # Target arrow
            if agent.current_target:
                tx, ty = agent.current_target
                dx, dy = tx - x, ty - y
                ax.arrow(x, y, dx * 0.8, dy * 0.8,
                        head_width=0.5, head_length=0.5,
                        fc='red', ec='red', alpha=0.5, zorder=5,
                        linewidth=2)
    
    return fig


def make_metrics_display(model):
    """
    Create a metrics display component.
    """
    from agents.harvester_agent import HarvesterAgent
    
    # Get current metrics
    total_yield = sum(a.harvested for a in model.agents if isinstance(a, HarvesterAgent))
    cumulative_messages = model.cumulative_messages
    remaining_fruit = sum(1 for f in model.fruits if f.available)
    coverage = len(set().union(*[a.visited_cells for a in model.agents if isinstance(a, HarvesterAgent)]))
    
    efficiency = total_yield / cumulative_messages if cumulative_messages > 0 else 0
    
    metrics_html = f"""
    <div style="background-color: #f0f0f0; padding: 15px; border-radius: 10px; margin: 10px;">
        <h3 style="margin-top: 0;">📊 Real-Time Metrics</h3>
        <table style="width: 100%; border-collapse: collapse;">
            <tr style="border-bottom: 1px solid #ccc;">
                <td style="padding: 8px; font-weight: bold;">Total Yield:</td>
                <td style="padding: 8px; text-align: right; color: green; font-size: 18px;">{total_yield}</td>
            </tr>
            <tr style="border-bottom: 1px solid #ccc;">
                <td style="padding: 8px; font-weight: bold;">Messages Sent:</td>
                <td style="padding: 8px; text-align: right; color: blue; font-size: 18px;">{cumulative_messages}</td>
            </tr>
            <tr style="border-bottom: 1px solid #ccc;">
                <td style="padding: 8px; font-weight: bold;">Remaining Fruit:</td>
                <td style="padding: 8px; text-align: right; color: orange; font-size: 18px;">{remaining_fruit}</td>
            </tr>
            <tr style="border-bottom: 1px solid #ccc;">
                <td style="padding: 8px; font-weight: bold;">Coverage (cells):</td>
                <td style="padding: 8px; text-align: right; color: purple; font-size: 18px;">{coverage}</td>
            </tr>
            <tr>
                <td style="padding: 8px; font-weight: bold;">Efficiency:</td>
                <td style="padding: 8px; text-align: right; color: darkgreen; font-size: 18px;">{efficiency:.2f}</td>
            </tr>
        </table>
        <p style="margin-top: 10px; font-size: 12px; color: #666;">
            <strong>Step:</strong> {model.steps} | 
            <strong>Comm Range:</strong> {model.comm_range} cells
        </p>
    </div>
    """
    
    return solara.HTML(metrics_html)


# Model parameters
model_params = {
    "width": {
        "type": "SliderInt",
        "value": 20,
        "label": "Grid Width",
        "min": 10,
        "max": 50,
        "step": 5,
    },
    "height": {
        "type": "SliderInt",
        "value": 20,
        "label": "Grid Height",
        "min": 10,
        "max": 50,
        "step": 5,
    },
    "num_agents": {
        "type": "SliderInt",
        "value": 5,
        "label": "Number of Agents",
        "min": 1,
        "max": 20,
        "step": 1,
    },
    "fruit_density": {
        "type": "SliderFloat",
        "value": 0.2,
        "label": "Fruit Density",
        "min": 0.05,
        "max": 0.5,
        "step": 0.05,
    },
    "comm_range": {
        "type": "SliderInt",
        "value": 4,
        "label": "Communication Range",
        "min": 0,
        "max": 8,
        "step": 1,
    },
    "dynamics": {
        "type": "Select",
        "value": "Static",
        "values": ["Static"],
        "label": "Resource Dynamics",
    },
    "seed": {
        "type": "InputText",
        "value": "42",
        "label": "Random Seed",
    },
}


# Create visualization
def create_enhanced_viz():
    """Create the enhanced visualization page."""
    
    # Create space component with custom portrayal
    space = make_space_component(enhanced_agent_portrayal)
    
    # Create plot components for metrics over time
    yield_plot = make_plot_component("total_yield", color="green")
    messages_plot = make_plot_component("cumulative_messages", color="blue")
    coverage_plot = make_plot_component("coverage", color="purple")
    
    # Create SolaraViz page
    page = SolaraViz(
        HarvestModel,
        model_params,
        measures=[yield_plot, messages_plot, coverage_plot],
        name="Enhanced Fruit Harvesting Simulation",
        space_drawer=space,
    )
    
    return page


# Create the page
page = create_enhanced_viz()


if __name__ == "__main__":
    # Run Solara server
    page


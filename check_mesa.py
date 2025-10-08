#!/usr/bin/env python3

import mesa
print('Mesa version:', mesa.__version__)
print()

# Check what's available in mesa.visualization
import mesa.visualization
print('mesa.visualization contents:')
for item in sorted(dir(mesa.visualization)):
    if not item.startswith('_'):
        print(f'  {item}')
print()

# Test specific imports
try:
    from mesa.visualization.solara_viz import SolaraViz
    print('✓ SolaraViz import successful')
except Exception as e:
    print('✗ SolaraViz import failed:', e)

try:
    from mesa.visualization import make_space_component, make_plot_component
    print('✓ make_space_component, make_plot_component import successful')
except Exception as e:
    print('✗ make_space_component, make_plot_component import failed:', e)

# Check Mesa 3.0 specific features
try:
    from mesa import Model, Agent
    from mesa.space import MultiGrid
    from mesa.datacollection import DataCollector
    print('✓ Core Mesa imports successful')
except Exception as e:
    print('✗ Core Mesa imports failed:', e)

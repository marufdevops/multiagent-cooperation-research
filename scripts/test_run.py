#!/usr/bin/env python3
"""Quick test to verify experiments work"""
import sys
import os
import csv

sys.path.insert(0, 'src')

from models.harvest_model import HarvestModel

# Create results directory
os.makedirs('results', exist_ok=True)

# Run a few quick tests
print("Running quick experiment test...")
results = []

for comm_range in [0, 2, 4]:
    for replication in range(2):
        seed = replication
        model = HarvestModel(
            width=50,
            height=50,
            num_agents=10,
            fruit_density=0.15,
            comm_range=comm_range,
            seed=seed
        )
        
        model.run_model(steps=500)
        
        data = model.datacollector.get_model_vars_dataframe()
        final_yield = data['total_yield'].iloc[-1]
        cumulative_messages = data['cumulative_messages'].iloc[-1]
        
        results.append({
            'comm_range': comm_range,
            'replication': replication,
            'yield': final_yield,
            'messages': cumulative_messages
        })
        
        print(f"comm_range={comm_range}, rep={replication}: yield={final_yield}, messages={cumulative_messages}")

print("\n✓ Test completed successfully!")
print(f"Ran {len(results)} simulations")


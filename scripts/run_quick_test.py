#!/usr/bin/env python3
"""Quick test with minimal runs"""
import sys
import os
import csv
import time

sys.path.insert(0, 'src')

from models.harvest_model import HarvestModel

os.makedirs('results', exist_ok=True)

print("Running quick experiment test (2 configs × 2 reps = 4 runs)...")
start = time.time()

results_file = 'results/quick_test.csv'
with open(results_file, 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=['comm_range', 'replication', 'yield', 'messages'])
    writer.writeheader()
    
    run_id = 0
    for comm_range in [0, 2]:
        for replication in range(2):
            run_id += 1
            print(f"Run {run_id}/4: comm_range={comm_range}, rep={replication}...", end=' ', flush=True)
            
            model = HarvestModel(
                width=50,
                height=50,
                num_agents=10,
                fruit_density=0.15,
                comm_range=comm_range,
                seed=replication
            )
            
            model.run_model(steps=500)
            
            data = model.datacollector.get_model_vars_dataframe()
            final_yield = data['total_yield'].iloc[-1]
            cumulative_messages = data['cumulative_messages'].iloc[-1]
            
            writer.writerow({
                'comm_range': comm_range,
                'replication': replication,
                'yield': final_yield,
                'messages': cumulative_messages
            })
            
            print(f"yield={final_yield}, messages={cumulative_messages}")

elapsed = time.time() - start
print(f"\n✓ Test completed in {elapsed:.1f}s")
print(f"Results saved to {results_file}")


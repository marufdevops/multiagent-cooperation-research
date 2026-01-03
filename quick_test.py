"""Quick test with minimal runs."""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from models.harvest_model import HarvestModel

# Test with just 2 runs per configuration
print("Testing...")

for comm_range in [0, 2]:
    print(f"\nTesting comm_range={comm_range}")
    
    model = HarvestModel(
        width=50,
        height=50,
        num_agents=10,
        fruit_density=0.15,
        comm_range=comm_range,
        seed=0
    )
    
    for step in range(500):
        model.step()
    
    total_yield = sum(agent.harvested for agent in model.agents)
    total_messages = sum(agent.messages_sent for agent in model.agents)
    
    print(f"  Yield: {total_yield}")
    print(f"  Messages: {total_messages}")
    print(f"  Efficiency: {total_yield / total_messages if total_messages > 0 else 0:.2f}")

print("\nTest complete!")


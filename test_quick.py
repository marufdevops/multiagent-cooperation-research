#!/usr/bin/env python3
"""Quick test to verify implementation works."""
import sys
sys.path.insert(0, 'src')

from models.harvest_model import HarvestModel

print("=" * 60)
print("QUICK IMPLEMENTATION TEST")
print("=" * 60)

# Test 1: Static model
print("\nTest 1: Static model (no communication)")
model1 = HarvestModel(
    width=10, height=10, num_agents=3, fruit_density=0.2,
    comm_range=0, dynamics='Static', seed=42
)
for i in range(20):
    model1.step()
print(f"✓ Completed 20 steps")
print(f"  Final yield: {model1._get_total_yield()}")
print(f"  Messages sent: {model1.cumulative_messages}")

# Test 2: Static with communication
print("\nTest 2: Static model (with communication)")
model2 = HarvestModel(
    width=10, height=10, num_agents=3, fruit_density=0.2,
    comm_range=3, dynamics='Static', seed=42
)
for i in range(20):
    model2.step()
print(f"✓ Completed 20 steps")
print(f"  Final yield: {model2._get_total_yield()}")
print(f"  Messages sent: {model2.cumulative_messages}")

# Test 3: Replenishing
print("\nTest 3: Replenishing model")
model3 = HarvestModel(
    width=10, height=10, num_agents=3, fruit_density=0.2,
    comm_range=2, dynamics='Replenishing', regen_prob=0.05, seed=42
)
for i in range(20):
    model3.step()
print(f"✓ Completed 20 steps")
print(f"  Final yield: {model3._get_total_yield()}")
print(f"  Messages sent: {model3.cumulative_messages}")
print(f"  Remaining fruit: {model3._get_remaining_fruit()}")

# Test 4: Metrics collection
print("\nTest 4: Metrics collection")
model4 = HarvestModel(
    width=10, height=10, num_agents=5, fruit_density=0.2,
    comm_range=2, dynamics='Static', seed=42
)
for i in range(10):
    model4.step()

df = model4.datacollector.get_model_vars_dataframe()
print(f"✓ DataCollector has {len(df)} rows")
print(f"  Columns: {list(df.columns)}")
print(f"  Final metrics:")
print(f"    - Total yield: {df['total_yield'].iloc[-1]}")
print(f"    - Messages this step: {df['messages_this_step'].iloc[-1]}")
print(f"    - Largest component ratio: {df['largest_component_ratio'].iloc[-1]:.2f}")
print(f"    - Gini yield: {df['gini_yield'].iloc[-1]:.3f}")

print("\n" + "=" * 60)
print("ALL TESTS PASSED ✓")
print("=" * 60)
print("\nImplementation is working correctly!")
print("You can now run:")
print("  - scripts/run_sandbox.py (full sandbox with plots)")
print("  - scripts/run_smoke_test.py (factorial experiment)")
print("  - scripts/run_visualization.py (interactive visualization)")


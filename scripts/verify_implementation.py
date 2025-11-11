"""
Simple verification script to test Mesa implementation correctness.

Tests:
1. Agents with comm_range=0 send zero messages
2. Agents with comm_range>0 send messages
3. Yield increases with communication range
4. All metrics are collected correctly
"""

import sys
sys.path.append('src')

from models.harvest_model import HarvestModel
from agents.harvester_agent import HarvesterAgent


def test_no_communication():
    """Test that comm_range=0 produces zero messages."""
    print("\n" + "="*70)
    print("TEST 1: No Communication (Range=0)")
    print("="*70)
    
    model = HarvestModel(
        width=20,
        height=20,
        num_agents=5,
        fruit_density=0.2,
        comm_range=0,  # NO COMMUNICATION
        seed=42
    )
    
    # Run for 20 steps
    for _ in range(20):
        model.step()
    
    # Get metrics
    data = model.datacollector.get_model_vars_dataframe()
    final_messages = data['cumulative_messages'].iloc[-1]
    final_yield = data['total_yield'].iloc[-1]
    
    print(f"✓ Final yield: {final_yield}")
    print(f"✓ Total messages: {final_messages}")
    
    if final_messages == 0:
        print("✅ PASS: No messages sent (as expected)")
    else:
        print(f"❌ FAIL: Expected 0 messages, got {final_messages}")
    
    return final_messages == 0


def test_with_communication():
    """Test that comm_range>0 produces messages."""
    print("\n" + "="*70)
    print("TEST 2: With Communication (Range=4)")
    print("="*70)
    
    model = HarvestModel(
        width=20,
        height=20,
        num_agents=5,
        fruit_density=0.2,
        comm_range=4,  # WITH COMMUNICATION
        seed=42
    )
    
    # Run for 20 steps
    for _ in range(20):
        model.step()
    
    # Get metrics
    data = model.datacollector.get_model_vars_dataframe()
    final_messages = data['cumulative_messages'].iloc[-1]
    final_yield = data['total_yield'].iloc[-1]
    
    print(f"✓ Final yield: {final_yield}")
    print(f"✓ Total messages: {final_messages}")
    
    if final_messages > 0:
        print("✅ PASS: Messages sent (as expected)")
    else:
        print("❌ FAIL: Expected messages > 0, got 0")
    
    return final_messages > 0


def test_yield_increases():
    """Test that yield increases with communication."""
    print("\n" + "="*70)
    print("TEST 3: Yield Increases with Communication")
    print("="*70)
    
    results = []
    
    for comm_range in [0, 2, 4, 6, 8]:
        model = HarvestModel(
            width=20,
            height=20,
            num_agents=5,
            fruit_density=0.2,
            comm_range=comm_range,
            seed=42
        )
        
        # Run for 50 steps
        for _ in range(50):
            model.step()
        
        # Get final yield
        data = model.datacollector.get_model_vars_dataframe()
        final_yield = data['total_yield'].iloc[-1]
        final_messages = data['cumulative_messages'].iloc[-1]
        
        results.append((comm_range, final_yield, final_messages))
        print(f"  Range {comm_range}: Yield={final_yield}, Messages={final_messages}")
    
    # Check if yield generally increases
    yield_range_0 = results[0][1]
    yield_range_4 = results[2][1]
    
    improvement = (yield_range_4 - yield_range_0) / yield_range_0 * 100
    
    print(f"\n✓ Yield improvement (Range 0 → 4): {improvement:.1f}%")
    
    if yield_range_4 > yield_range_0:
        print("✅ PASS: Yield increases with communication")
    else:
        print("❌ FAIL: Yield did not increase")
    
    return yield_range_4 > yield_range_0


def test_metrics_collection():
    """Test that all 5 metrics are collected."""
    print("\n" + "="*70)
    print("TEST 4: All Metrics Collected")
    print("="*70)
    
    model = HarvestModel(
        width=20,
        height=20,
        num_agents=5,
        fruit_density=0.2,
        comm_range=2,
        seed=42
    )
    
    # Run for 10 steps
    for _ in range(10):
        model.step()
    
    # Get metrics
    data = model.datacollector.get_model_vars_dataframe()
    
    expected_metrics = ['total_yield', 'messages_this_step', 'cumulative_messages', 
                       'remaining_fruit', 'coverage']
    
    all_present = True
    for metric in expected_metrics:
        if metric in data.columns:
            print(f"  ✓ {metric}: {data[metric].iloc[-1]}")
        else:
            print(f"  ✗ {metric}: MISSING")
            all_present = False
    
    if all_present:
        print("✅ PASS: All 5 metrics collected")
    else:
        print("❌ FAIL: Some metrics missing")
    
    return all_present


def test_agent_behavior():
    """Test agent behavior details."""
    print("\n" + "="*70)
    print("TEST 5: Agent Behavior Details")
    print("="*70)
    
    model = HarvestModel(
        width=20,
        height=20,
        num_agents=3,
        fruit_density=0.2,
        comm_range=3,
        seed=42
    )
    
    # Run for 5 steps and inspect agent states
    for step in range(5):
        model.step()
        
        if step == 4:  # Check after 5 steps
            print(f"\nAgent states after step {step + 1}:")
            for agent in model.agents:
                if isinstance(agent, HarvesterAgent):
                    print(f"  Agent at {agent.pos}:")
                    print(f"    - Harvested: {agent.harvested}")
                    print(f"    - Messages sent: {agent.messages_sent}")
                    print(f"    - Messages received: {agent.messages_received}")
                    print(f"    - Current target: {agent.current_target}")
                    print(f"    - Visited cells: {len(agent.visited_cells)}")
    
    # Check that agents have moved and potentially harvested
    total_harvested = sum(a.harvested for a in model.agents if isinstance(a, HarvesterAgent))
    total_visited = sum(len(a.visited_cells) for a in model.agents if isinstance(a, HarvesterAgent))
    
    print(f"\n✓ Total harvested: {total_harvested}")
    print(f"✓ Total cells visited: {total_visited}")
    
    if total_visited > 0:
        print("✅ PASS: Agents are moving and tracking visits")
    else:
        print("❌ FAIL: Agents not moving")
    
    return total_visited > 0


def test_static_dynamics():
    """Test that Static dynamics work correctly."""
    print("\n" + "="*70)
    print("TEST 6: Static Dynamics (No Regeneration)")
    print("="*70)
    
    model = HarvestModel(
        width=20,
        height=20,
        num_agents=5,
        fruit_density=0.2,
        comm_range=2,
        seed=42
    )
    
    # Get initial fruit count
    initial_fruit = sum(1 for f in model.fruits if f.available)
    print(f"✓ Initial fruit: {initial_fruit}")
    
    # Run for 30 steps
    for _ in range(30):
        model.step()
    
    # Get final fruit count
    final_fruit = sum(1 for f in model.fruits if f.available)
    harvested = initial_fruit - final_fruit
    
    print(f"✓ Final fruit: {final_fruit}")
    print(f"✓ Harvested: {harvested}")
    
    # Check that fruit count decreased (no regeneration)
    if final_fruit < initial_fruit:
        print("✅ PASS: Fruit decreases (no regeneration)")
    else:
        print("❌ FAIL: Fruit did not decrease")
    
    # Check that no fruit regenerated
    regenerated = sum(1 for f in model.fruits if f.times_harvested > 0 and f.available)
    
    if regenerated == 0:
        print("✅ PASS: No fruit regenerated")
    else:
        print(f"❌ FAIL: {regenerated} fruits regenerated")
    
    return final_fruit < initial_fruit and regenerated == 0


def main():
    """Run all verification tests."""
    print("\n" + "="*70)
    print("MESA IMPLEMENTATION VERIFICATION")
    print("="*70)
    print("\nRunning 6 tests to verify implementation correctness...")
    
    results = []
    
    results.append(("No Communication (Range=0)", test_no_communication()))
    results.append(("With Communication (Range>0)", test_with_communication()))
    results.append(("Yield Increases", test_yield_increases()))
    results.append(("Metrics Collection", test_metrics_collection()))
    results.append(("Agent Behavior", test_agent_behavior()))
    results.append(("Static Dynamics", test_static_dynamics()))
    
    # Summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {test_name}")
    
    print(f"\n{passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED! Implementation is correct.")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Review implementation.")
    
    print("="*70 + "\n")


if __name__ == "__main__":
    main()


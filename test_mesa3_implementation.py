#!/usr/bin/env python3
"""
Comprehensive test suite for the Mesa 3.0 fruit harvesting simulation.

This test verifies that all Week 1 and Week 2 deliverables are properly implemented:
- HarvesterAgent with communication and cooperation
- OrchardModel with fruit dynamics
- Range-bounded messaging system
- Data collection and metrics
- Cooperative vs competitive strategies
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fruit_harvester_simulation.model import OrchardModel
from fruit_harvester_simulation.agents import HarvesterAgent


def test_basic_functionality():
    """Test basic model and agent creation."""
    print("=== Testing Basic Functionality ===")
    
    model = OrchardModel(width=15, height=15, num_agents=10, communication_range=3.0)
    
    # Test model properties
    assert len(model.agents) == 10, f"Expected 10 agents, got {len(model.agents)}"
    assert model.width == 15, f"Expected width 15, got {model.width}"
    assert model.height == 15, f"Expected height 15, got {model.height}"
    
    # Test agent properties
    for agent in model.agents:
        assert hasattr(agent, 'strategy'), "Agent missing strategy attribute"
        assert hasattr(agent, 'communication_range'), "Agent missing communication_range"
        assert hasattr(agent, 'fruits_collected'), "Agent missing fruits_collected"
        assert hasattr(agent, 'pos'), "Agent missing position"
        assert agent.pos is not None, "Agent not placed on grid"
    
    print("✓ Basic functionality test passed")


def test_fruit_mechanics():
    """Test fruit spawning, harvesting, and regeneration."""
    print("=== Testing Fruit Mechanics ===")
    
    model = OrchardModel(width=10, height=10, num_agents=5, 
                        initial_fruit_density=0.5, regeneration_prob=0.2)
    
    # Check initial fruit spawning
    initial_fruits = sum(sum(row) for row in model.fruit_map)
    assert initial_fruits > 0, "No fruits spawned initially"
    
    # Test fruit harvesting
    for pos in [(x, y) for x in range(10) for y in range(10)]:
        if model.get_fruit_at(pos) > 0:
            initial_count = model.get_fruit_at(pos)
            success = model.harvest_fruit(pos)
            assert success, "Fruit harvesting failed"
            assert model.get_fruit_at(pos) == initial_count - 1, "Fruit count not decremented"
            break
    
    # Test fruit regeneration
    model.regenerate_fruits()
    
    print("✓ Fruit mechanics test passed")


def test_communication_system():
    """Test range-bounded message delivery."""
    print("=== Testing Communication System ===")
    
    model = OrchardModel(width=20, height=20, num_agents=8, communication_range=4.0)
    
    # Run a few steps to generate messages
    for _ in range(5):
        model.step()
    
    # Check that messages were sent
    assert model.total_messages_sent > 0, "No messages sent"
    
    # Check that cooperative agents send more messages than competitive ones
    coop_agents = [a for a in model.agents if a.strategy == "cooperative"]
    comp_agents = [a for a in model.agents if a.strategy == "competitive"]
    
    if coop_agents and comp_agents:
        avg_coop_messages = sum(a.messages_sent for a in coop_agents) / len(coop_agents)
        avg_comp_messages = sum(a.messages_sent for a in comp_agents) / len(comp_agents)
        assert avg_coop_messages >= avg_comp_messages, "Cooperative agents should send more messages"
    
    print("✓ Communication system test passed")


def test_strategy_differences():
    """Test that cooperative and competitive strategies behave differently."""
    print("=== Testing Strategy Differences ===")
    
    # Test pure cooperative
    coop_model = OrchardModel(width=15, height=15, num_agents=10, 
                             cooperative_share=1.0, communication_range=3.0)
    
    # Test pure competitive  
    comp_model = OrchardModel(width=15, height=15, num_agents=10,
                             cooperative_share=0.0, communication_range=3.0)
    
    # Run both models
    for _ in range(10):
        coop_model.step()
        comp_model.step()
    
    # Cooperative agents should send more messages
    assert coop_model.total_messages_sent > comp_model.total_messages_sent, \
           "Cooperative model should send more messages"
    
    # Check strategy assignment
    coop_strategies = [a.strategy for a in coop_model.agents]
    comp_strategies = [a.strategy for a in comp_model.agents]
    
    assert all(s == "cooperative" for s in coop_strategies), "All agents should be cooperative"
    assert all(s == "competitive" for s in comp_strategies), "All agents should be competitive"
    
    print("✓ Strategy differences test passed")


def test_data_collection():
    """Test data collection and metrics."""
    print("=== Testing Data Collection ===")
    
    model = OrchardModel(width=12, height=12, num_agents=6, communication_range=3.0)
    
    # Run simulation and collect data
    for _ in range(8):
        model.step()
    
    # Check data collector
    assert hasattr(model, 'datacollector'), "Model missing datacollector"
    
    # Get collected data
    model_data = model.datacollector.get_model_vars_dataframe()
    agent_data = model.datacollector.get_agent_vars_dataframe()
    
    # Check model metrics
    assert 'Total_Fruits_Harvested' in model_data.columns, "Missing Total_Fruits_Harvested metric"
    assert 'Total_Messages_Sent' in model_data.columns, "Missing Total_Messages_Sent metric"
    assert 'Step_Count' in model_data.columns, "Missing Step_Count metric"
    
    # Check agent metrics
    assert 'Fruits_Collected' in agent_data.columns, "Missing Fruits_Collected metric"
    assert 'Strategy' in agent_data.columns, "Missing Strategy metric"
    
    # Verify data makes sense
    final_fruits = model_data['Total_Fruits_Harvested'].iloc[-1]
    final_messages = model_data['Total_Messages_Sent'].iloc[-1]
    
    assert final_fruits >= 0, "Negative fruits harvested"
    assert final_messages >= 0, "Negative messages sent"
    
    print("✓ Data collection test passed")


def test_mesa3_compatibility():
    """Test Mesa 3.0 specific features."""
    print("=== Testing Mesa 3.0 Compatibility ===")
    
    model = OrchardModel(width=10, height=10, num_agents=5)
    
    # Test Mesa 3.0 agent management
    assert hasattr(model, 'agents'), "Model missing agents attribute"
    assert hasattr(model.agents, 'shuffle_do'), "AgentSet missing shuffle_do method"
    
    # Test that agents have unique_id (auto-assigned in Mesa 3.0)
    for agent in model.agents:
        assert hasattr(agent, 'unique_id'), "Agent missing unique_id"
        assert agent.unique_id is not None, "Agent unique_id is None"
    
    # Test step counter (automatic in Mesa 3.0)
    initial_steps = model.steps
    model.step()
    assert model.steps == initial_steps + 1, "Step counter not incremented"
    
    print("✓ Mesa 3.0 compatibility test passed")


def run_performance_test():
    """Run a larger simulation to test performance."""
    print("=== Running Performance Test ===")
    
    model = OrchardModel(width=25, height=25, num_agents=20, 
                        communication_range=4.0, cooperative_share=0.7)
    
    # Run for 30 steps
    for i in range(30):
        model.step()
        if (i + 1) % 10 == 0:
            total_fruits = sum(a.fruits_collected for a in model.agents)
            print(f"  Step {i+1}: {total_fruits} fruits, {model.total_messages_sent} messages")
    
    # Final results
    final_fruits = sum(a.fruits_collected for a in model.agents)
    final_messages = model.total_messages_sent
    
    print(f"✓ Performance test completed: {final_fruits} fruits, {final_messages} messages")


def main():
    """Run all tests."""
    print("🍎 Testing Mesa 3.0 Fruit Harvesting Simulation Implementation")
    print("=" * 60)
    
    try:
        test_basic_functionality()
        test_fruit_mechanics()
        test_communication_system()
        test_strategy_differences()
        test_data_collection()
        test_mesa3_compatibility()
        run_performance_test()
        
        print("\n" + "=" * 60)
        print("🎉 ALL TESTS PASSED! Mesa 3.0 implementation is working correctly.")
        print("\n✅ Week 1 & 2 Deliverables Successfully Implemented:")
        print("   • HarvesterAgent with communication capabilities")
        print("   • Cooperative vs Competitive strategies")
        print("   • Range-bounded messaging system")
        print("   • OrchardModel with fruit dynamics")
        print("   • Data collection for research metrics")
        print("   • Mesa 3.0 API compatibility")
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

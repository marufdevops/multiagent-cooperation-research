"""
Quick test script for the Mesa model.
Runs a simple simulation to verify everything works.
"""
import sys
sys.path.insert(0, 'src')

from models.harvest_model import HarvestModel


def run_sandbox(
    width=20,
    height=20,
    num_agents=5,
    fruit_density=0.2,
    comm_range=2,
    steps=100,
    seed=42
):
    """Run sandbox model with Static dynamics and return results."""
    model = HarvestModel(
        width=width,
        height=height,
        num_agents=num_agents,
        fruit_density=fruit_density,
        comm_range=comm_range,
        seed=seed
    )

    model.run_model(steps=steps)
    model_data = model.datacollector.get_model_vars_dataframe()

    return model, model_data


if __name__ == '__main__':
    model, data = run_sandbox(
        comm_range=2,
        steps=100,
        seed=42
    )
    print(data)


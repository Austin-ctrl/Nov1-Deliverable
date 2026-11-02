"""Run the seven-action reference scenario under Tora's dry/wet inputs.

Overall we as answering, 
How do the seven driving actions perform under different raod friciton conditions
"""
from pathlib import Path
from parameter_loader import scenario_from_csv
from scenario import SCENARIO
from simulator import Simulator, ACTIONS

DT = 0.001  # 0.001 seconds
CSV_PATH = Path(__file__).parent / 'parameter-v1' / 'parameters.csv'

# one driving action under a scenario
def run(scenario, action):
    sim = Simulator()
    sim.reset(scenario, seed=42)
    while True:  # sim loop
        state, done, info = sim.step(action, DT)  # step returns these 3 things
        if done:
            return state, info


if __name__ == '__main__':
    for condition in ('dry', 'wet'):
        scenario = scenario_from_csv(SCENARIO, condition, CSV_PATH)
        print(f"\n=== {condition.upper()} | friction={scenario['physics']['friction']} ===")
        for action in ACTIONS:
            state, info = run(scenario, action)
            print(f'{action:20s} collisions={info["collisions"]} '
                  f'x={state["x"]:.2f} y={state["y"]:.2f}')

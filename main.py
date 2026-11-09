from scenario import SCENARIO
from simulator import Simulator, ACTIONS

DT = 0.001

def run(action, commandTime = 0.3):
    sim = Simulator()
    sim.reset(SCENARIO, seed=42)
    while True:
        state, done, info = sim.step(action, DT, commandTime = commandTime)
        if done:
            return state, info

if __name__ == '__main__':
    for action in ACTIONS:
        state, info = run(action)
        print(f'{action:20s} collisions={info["collisions"]} x={state["x"]:.2f} y={state["y"]:.2f}')
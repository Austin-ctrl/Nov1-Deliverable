from simulator import Simulator, ACTIONS
from scenario import SCENARIO

DT = 0.001

# runs one actions
def rollout(scenario, action, commandTime):
    sim = Simulator()
    sim.reset(scenario, seed=4)

    # start the car where it would be at command time
    sim.x += sim.v * commandTime  # current position which is just
    while True:
        state, done, info = sim.step(
            action,
            DT,
            commandTime=0.0
        )
        if done:
            return frozenset(info["collisions"])

# this evalutes every action
def evaluate_time(scenario, commandTime):
    outcomes = {}

    for action in ACTIONS:
        outcomes[action] = rollout(
            scenario,
            action,
            commandTime
        )

    return outcomes


# This checks whether two outcomes are incomparable.
def strict(outcomes):
    harm_sets = list(set(outcomes.values()))

    for i, a in enumerate(harm_sets):
        for b in harm_sets[i + 1:]:
            if not (a <= b or b <= a):
                return True

    return False

# calculate the window
def analyze(scenario):
    t_unavoid = None
    t_converge = None

    # -1.50 through +1.00 in 0.01s increments
    for i in range(-150, 101):
        t = round(i / 100, 2)

        outcomes = evaluate_time(scenario, t)
        # Does any action avoid all harm?
        safe = any(
            len(harms) == 0
            for harms in outcomes.values()
        )
        # FINDS EVERY EACTION BECOMES HARMFUL
        if not safe and t_unavoid is None:
            t_unavoid = t
        # FINDS WHEN ACTION IS HARMFUL AND AT LEAST TWO COLLISION OUTCOMES ARE INCOMPARABLE
        if not safe and strict(outcomes):
            t_converge = t

    if t_unavoid is None or t_converge is None:
        W = None
    else:
        W = round(t_converge - t_unavoid, 2)

    return t_unavoid, t_converge, W

# debugging
def print_changes(scenario):
    previous = None

    for i in range(-150, 101):
        t = round(i / 100, 2)
        outcomes = evaluate_time(scenario, t)

        if previous is not None:
            for action in ACTIONS:
                if outcomes[action] != previous[action]:
                    print(
                        f"t={t:+.2f}",
                        action,
                        sorted(previous[action]),
                        "->",
                        sorted(outcomes[action])
                    )

        previous = outcomes

if __name__ == "__main__":
    t_unavoid, t_converge, W = analyze(SCENARIO)

    print("T_unavoid:", t_unavoid)
    print("T_converge:", t_converge)
    print("W_strict:", W)

    for t in [-0.15, 0.0, 0.15, 0.18]:
        outcomes = evaluate_time(SCENARIO, t)

        print(f"\nTime: {t}")
        for action, harms in outcomes.items():
            print(action, sorted(harms))

        print("Strict:", strict(outcomes))

    outcomes = evaluate_time(SCENARIO, 0.3)
    print(outcomes)
    print_changes(SCENARIO)



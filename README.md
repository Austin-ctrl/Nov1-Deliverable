# Austin's Nov 1 deliverable

## Project Overview

Completed: Built the Python simulator core with all seven actions: 
{    
1. Maintain speed
2. Soft braking
3. Hard braking
4. Steer left
5. Steer right
6. Brake and steer left
7. Brake and steer right
}
,friction-limited braking, actuation delay, simplified steering, and collision detection. Integrated selected parameters from Tora's CSV and successfully tested dry/wet conditions.

For the edits:
Added commandTime support to the simulator, and implemented windows.py to evaluate all seven actions across different command times. The analysis calculates T_unavoid, T_converge (strict), ad W_strict using the team's handcheck definitions. Also added debug functions to look at the collision outcomes

### files included

## scenario.py — Defines the initial vehicle position, speed, pedestrians, and physics parameters.
- Vehicle starting position and speed
- Vehicle half-width
- Road friction
- Actuation delay
- Lateral acceleration ramp
- Pedestrian positions and radii
- Parked-car boundary

    
## simulator.py — Simulates vehicle movement, braking, steering, and collisions.
 The simulator uses a friction-based acceleration limit to determine
how strongly the vehicle can brake or move sideways.

For combined braking and steering, the available acceleration is
divided between the two directions.

The simulation advances in small time steps until the vehicle
stops, reaches a configured boundary, or reaches the maximum
simulation time or forward position.

## main.py — Runs all seven actions using the original reference scenario.Each action starts with a new Simulator instance so the results
Each action starts with a new Simulator instance so the results
can be compared from the same initial conditions.

The script prints the detected collisions and final vehicle
position for each action.


## parameter_loader.py — Reads Tora's CSV parameters and creates updated scenarios.
Currently, the loader imports:

- Dry-road friction or wet-road effective friction proxy
- Command actuation delay
- Lateral acceleration ramp duration


##run_parameters.py — Runs all seven actions under dry and wet road conditions.

## windows.py - Dilemma Windo Calculation
windows.py calculates the time interval of which an autonomous vehicle is faced with unavoidable negative outcomes

3 measurements are calculated in this
T_unavoid: this is the earliest command time when none of the 7 actions can avoid all recorded collisions

T_converge: The last command time in the tested range when no safe action exists, and at least two actions produce incomparable collision out comes

W_strict: this the difference between T_converge and T-unavoid measured in seconds. 

what we recorded:
before -0.15s: at eat one action avoids all collisions
-0.15s: every action causes harm
between -0.15 and +0.18s: strict tradeoffs can exist between harmful outcomes
After +0.18s: under the intended referenece interpretations, strict tradeoffs no longer occur, although collisions can stilllhappen

This function works by starting with a rollout() function that creates a new instance of the simulator. It resets by using the provided scenario, and runs one driving acion until the simulation finishes. 

The starting vehicle position is adjusted with the sim.x += sim.v * command time.

This represenets the vehcile continuing foward at its initial speed V_new = V_old * time

This simulator advance in 0.001 -second increments. 

Evaluate_time() pretty much calls rollout() for each of the 7 actions. Each action recieves a fresh simulat instance

Strict(): chekcs if at least two distinct collision outcomes are incomparable, each set contains at leat one element the other one doesnt have. (when neither collision set is a subset of the other, nor do they share identical sets)


## How to Run

To run the original reference scenario:

    python3 main.py

To run the dry and wet parameter comparisons:

    python3 run_parameters.py

The parameter comparison requires the CSV file at:

    parameter-v1/parameters.csv

Results:
=== DRY | friction=0.8 ===
maintain             collisions=['A', 'B'] x=20.00 y=0.00
brake_soft           collisions=['A', 'B'] x=20.00 y=0.00
brake_hard           collisions=[] x=10.08 y=0.00
steer_left           collisions=[] x=20.00 y=8.28
steer_right          collisions=['occupant'] x=10.70 y=-1.50
brake_steer_left     collisions=[] x=13.34 y=9.54
brake_steer_right    collisions=['occupant'] x=9.86 y=-1.50

=== WET | friction=0.35 ===
maintain             collisions=['A', 'B'] x=20.00 y=0.00
brake_soft           collisions=['A', 'B'] x=20.00 y=0.00
brake_hard           collisions=['A', 'B'] x=20.00 y=0.00
steer_left           collisions=['A'] x=20.00 y=3.62
steer_right          collisions=['B', 'occupant'] x=14.23 y=-1.50
brake_steer_left     collisions=['A'] x=20.01 y=4.47
brake_steer_right    collisions=['B', 'occupant'] x=14.29 y=-1.50

To get thhe window:
    Run python3 windows.py

T_unavoid: -0.15
T_converge: 0.18
W_strict: 0.33



# explanation

I tested all seven driving actions under dry and wet road conditions using Tora's friction parameters.

Under dry conditions, hard braking, steering left, and braking while steering left avoided all recorded collisions.

Under wet conditions, none of the seven actions avoided every collision. Hard braking resulted in collisions with both pedestrians because the lower friction reduced the vehicle's braking capability.

The results demonstrate that road conditions can significantly change the outcomes of the same driving actions.

My simulator doesn't determine which action is ethically best. It provides collision outcomes that we can use for further ethical analysis.



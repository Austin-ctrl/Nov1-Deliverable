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

Still needed: Validate the simulator against matching CARLA measurements, confirm the steering-limit assumption, and integrate Manas's scenario bank once its parameters and additional hazards are supported.

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

# explanation

I tested all seven driving actions under dry and wet road conditions using Tora's friction parameters.

Under dry conditions, hard braking, steering left, and braking while steering left avoided all recorded collisions.

Under wet conditions, none of the seven actions avoided every collision. Hard braking resulted in collisions with both pedestrians because the lower friction reduced the vehicle's braking capability.

The results demonstrate that road conditions can significantly change the outcomes of the same driving actions.

My simulator doesn't determine which action is ethically best. It provides collision outcomes that we can use for further ethical analysis.



"""Lightweight 2D AV ethics simulator, based on the team's hand-check model.

Coordinates: x forward, y left; SI units throughout.
This is a toy collision/outcome model, not an injury or real-vehicle model.
"""

from math import sqrt

G = 9.81
ACTIONS = (
    "maintain",
    "brake_soft",
    "brake_hard",
    "steer_left",
    "steer_right",
    "brake_steer_left",
    "brake_steer_right",
)


class Simulator:
    """A fresh reset is required before each independent action rollout."""

    def __init__(self):
        self.reset_called = False

    def reset(self, scenario, seed=None):
        # we need to call reset before we can call step()
        vehicle = scenario["vehicle"]  
        physics = scenario["physics"]

        # postion and speed
        self.x = float(vehicle["x"])
        self.y = float(vehicle["y"])
        self.v = float(vehicle["speed"])
        self.vy = 0.0

        # physics parameters
        self.half_width = float(vehicle["half_width"])
        self.mu = float(physics["friction"])
        self.delay = float(physics["actuation_delay"])
        self.lateral_ramp = float(physics["lateral_ramp"])

        # pedestrians and parked car boundary
        self.pedestrians = scenario["pedestrians"]
        self.parked_boundary = scenario.get("parked_car_boundary")
        self.max_time = float(scenario.get("max_time", 5.0))  # defaults to 5
        self.max_x = float(scenario["max_x"])  # if not specified in the scenario, it will default to 20

        # validates parameter values
        if self.v < 0 or self.mu < 0 or self.delay < 0 or self.lateral_ramp < 0:
            raise ValueError("Speed, friction, delay and lateral ramp must be nonnegative")

        # reset the simulation variables
        self.time = 0.0  # sim time
        self.collisions = set()  # collision labels
        self.crossed = set()  # tracks  pedestrians whose forward thresholds have been checked
        self.done = False  # indicates if the sim has ended
        self.action = None  # stores the selected driving action
        self.reset_called = True  # confirms the sim is initialized
        return self._state()  # returns intial state of vehicle

    def _state(self):  # VEHICLES CURRENT STATE
        return {"x": self.x, "y": self.y, "v": self.v,
                "vy": self.vy, "time": self.time}

    def _info(self):
        return {"collisions": sorted(self.collisions)}  # REETURNS THE COLLISION INFO

    def _accelerations(self, action):  # returns decleration and lateral_acceleration Sim decides how much braking and sideways accleartion to apply
        limit = self.mu * G
        if action == "maintain":
            return 0.0, 0.0
        if action == "brake_soft":
            return min(0.3 * G, limit), 0.0
        if action == "brake_hard":
            return min(0.7 * G, limit), 0.0
        if action == "steer_left":
            return 0.0, limit
        if action == "steer_right":
            return 0.0, -limit
        combined = limit / sqrt(2.0)
        if action == "brake_steer_left":
            return combined, combined
        if action == "brake_steer_right":
            return combined, -combined
        raise ValueError(f"Unknown action: {action!r}")

    def step(self, action, dt, commandTime = 0.0):  # main thing that moves the car
        """Advance by dt seconds; return (state, done, info).

        One constant action is selected per rollout. To compare actions,
        reset a new Simulator instance for each action (as main.py does).

        It accpets a action (what the car should do) and dt: how much time to advance

        main.py() repeatly calls step until the sim finsihes
        """
        # input validation
        if not self.reset_called:
            raise RuntimeError("Call reset(scenario) before step()")
        if action not in ACTIONS:
            raise ValueError(f"Unknown action: {action!r}")
        if dt <= 0:
            raise ValueError("dt must be positive")
        if self.done:
            return self._state(), True, self._info()
        if self.action is None:
            self.action = action
        elif action != self.action:
            raise ValueError("This baseline requires one fixed action per rollout")
        # input validation

        activationTime = commandTime + self.delay

        decel, lateral = self._accelerations(action)  # ACCERATION IS CALCUTLTED
        # Split a step at the actuation-delay boundary so commands cannot
        # take effect before the configured delay.
        remaining = min(float(dt), max(0.0, self.max_time - self.time))  # how much time to advance
        while remaining > 1e-12 and not self.done: # 0.000000000001, try to avoid floating point rounding
            h = remaining  # h is the current portion of time step being processed
             # if the current time step crosses the actuation delay, split the step at the delay boundary
            if self.time < activationTime < self.time + h:  
                h = activationTime - self.time
            if self.time >= activationTime: # Only apply the selected driving action once the actuation delay has passed.
                since = self.time - activationTime  # lateral ramp calc
                ramp_fraction = (min(1.0, since / self.lateral_ramp)
                                 if self.lateral_ramp > 0 else 1.0)
                # v_new = v_old - a_braking * change in time
                self.v = max(0.0, self.v - decel * h)  # update vehicle speed
                # v_y,new = v_y,old + a_y * change in time
                self.vy += lateral * ramp_fraction * h

            if self.v <= 0:  # fwd speed reaches 0 zim ends
                self.vy = 0.0
                self.done = True
            else:
                self.x += self.v * h  # now we update vehicle positon if it hansnt stopped
                self.y += self.vy * h  # update lateral position if it hasn't stopped
            # DID IT COLLIDE DID IT COLLIDE (simple collision calculation)
                if self.parked_boundary is not None and self.y < float(self.parked_boundary):
                    self.collisions.add("occupant")
                    self.done = True

                # Matches the hand-check's forward-threshold collision rule.
                if not self.done:
                    # EX: pid is a, ped is the dictionarry with A's position and radius
                    for pid, ped in self.pedestrians.items():  # here we loop through the pedestrians
                        if pid not in self.crossed and self.x >= float(ped["x"]) - float(ped["radius"]):
                            self.crossed.add(pid)
                            # sideways overlap
                            # first part y - ped[y] calculates teh sideways distance between teh car and ped
                            # thats compared to the distance between teh car and pedestrian
                            if abs(self.y - float(ped["y"])) < self.half_width + float(ped["radius"]):
                                self.collisions.add(str(pid))

            self.time += h  # sim time gets updated 
            remaining -= h  # reduces the amount of time left to proces in this call to step()
            if self.time >= self.max_time - 1e-12 or self.x >= self.max_x:  # should the sim end
                self.done = True 
        return self._state(), self.done, self._info()  # return the results

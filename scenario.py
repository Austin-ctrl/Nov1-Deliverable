SCENARIO = {  # python dictionary
    "id": "ember_reference",

    "vehicle": {
        "x": 0.0,  # car starts at 0 meters on the road
        "y": 0.0,  # cars starts at center of the modeled path
        "speed": 40 / 3.6,  # the car starts at 11.11 m/s
        "half_width": 0.9,  # the car is a model of 0.9 meters
    },

    "physics": {
        "friction": 0.45,  # limits how much the car can break or acclerate sideways
        "actuation_delay": 0.2,  # delay between issuing a commands and the car executing it
        "lateral_ramp": 0.3,  # controls how quicly it can turn
    },

    "pedestrians": {
        "A": {"x": 12.0, "y": 0.6, "radius": 0.3},
        "B": {"x": 12.5, "y": -0.6, "radius": 0.3},
    },

    "parked_car_boundary": -1.5,
}
"""Select compatible toy-simulator inputs from Tora's parameters.csv.

Only `austin_value` entries are used. CARLA wheel scalars, calibration
observations, steering-rate limits, and vehicle dimensions are NOT silently
mapped into this simplified point-mass simulator.
"""
import csv
from copy import deepcopy
from pathlib import Path

PARAMETER_IDS = {
    'dry': 'mu_dry',
    'wet': 'mu_wet_effective_proxy',
}

# read that csv
def load_parameters(csv_path='parameters.csv'):
    """Return rows indexed by parameter_id; reject duplicate IDs."""
    rows = {}
    with open(csv_path, newline='', encoding='utf-8-sig') as f:
        for row in csv.DictReader(f):
            # print(row)
            key = row['parameter_id'].strip()
            if key in rows:  # check for dupes
                raise ValueError(f'Duplicate parameter_id: {key}')
            rows[key] = row
    return rows

# csv values to numners
# ex: mu_dry,0.8 -> 0.8
def numeric(rows, key):
    if key not in rows:
        raise KeyError(f'Missing parameter: {key}')
    value = rows[key]['austin_value'].strip()
    if not value:
        raise ValueError(f'Parameter {key} is unknown (blank), not zero')
    return float(value)

# takes the original scenario dictionary
# either a dry or wet condition
# and lastly the csv path
def scenario_from_csv(base_scenario, condition, csv_path='parameters.csv'):
    """Return an independent scenario with selected road and timing inputs."""
    if condition not in PARAMETER_IDS:
        raise ValueError('condition must be dry or wet')
    rows = load_parameters(csv_path)
    scenario = deepcopy(base_scenario) # seperateah copy
    scenario['id'] = f"{base_scenario['id']}_{condition}"
    physics = scenario['physics']
    physics['friction'] = numeric(rows, PARAMETER_IDS[condition])
    physics['actuation_delay'] = numeric(rows, 'command_actuation_delay_s')
    physics['lateral_ramp'] = numeric(rows, 'lateral_acceleration_ramp_s')
    # The existing simulator uses 0.3*g for soft braking, which is 2.943 m/s².
    # Check consistency instead of silently pretending the value is configurable.
    soft = numeric(rows, 'soft_braking_mps2')
    if abs(soft - 0.3 * 9.81) > 1e-6:
        raise ValueError('CSV soft brake differs from simulator fixed 0.3*g; update simulator first')
    return scenario

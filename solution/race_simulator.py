#!/usr/bin/env python3
"""
Box Box Box - F1 Race Simulator Template (Python)
This template shows the required input/output structure.
Implement your race simulation logic to predict finishing positions.
"""
import json
import sys

# Global configuration data
PARAMS = {
    "OFFSETS": {"SOFT": -1.0, "MEDIUM": 0.0, "HARD": 0.8},
    "BASE_DEG": {"SOFT": 0.019775, "MEDIUM": 0.010003, "HARD": 0.005055},
    "THRESHOLD": {"SOFT": 10, "MEDIUM": 20, "HARD": 30}
}

def main():
    # Read test case from stdin
    try:
        input_data = json.load(sys.stdin)
    except (EOFError, json.JSONDecodeError):
        return

    race_id = input_data['race_id']
    race_config = input_data['race_config']
    strategies = input_data['strategies']

    # TODO: Implement your race simulation logic here
    # Analyze the historical data in data/historical_races/ to understand
    # how to accurately simulate races and predict finishing positions
    
    b_time = race_config['base_lap_time']
    p_time = race_config['pit_lane_time']
    t_val = race_config['track_temp']
    l_count = race_config['total_laps']

    if t_val < 25:
        m_env = 0.8
    elif t_val <= 34:
        m_env = 1.0
    else:
        m_env = 1.3

    d_rates = {k: v * m_env for k, v in PARAMS["BASE_DEG"].items()}
    results_ledger = []

    for key_pos, entry in strategies.items():
        uid = entry['driver_id']
        stops = {s['lap']: s['to_tire'] for s in entry['pit_stops']}
        
        tire = entry['starting_tire']
        age = 1
        total_delta = p_time * len(entry['pit_stops'])
        
        for lap_idx in range(1, l_count + 1):
            deg_factor = max(0, age - PARAMS["THRESHOLD"][tire])
            step_time = b_time + PARAMS["OFFSETS"][tire] + (deg_factor * b_time * d_rates[tire])
            total_delta += step_time
            
            if lap_idx in stops:
                tire = stops[lap_idx]
                age = 1
            else:
                age += 1
        
        grid_idx = int(key_pos.replace('pos', ''))
        results_ledger.append((total_delta, grid_idx, uid))

    results_ledger.sort(key=lambda x: (x[0], x[1]))
    finishing_positions = [item[2] for item in results_ledger]

    # Output result to stdout
    output = {
        'race_id': race_id,
        'finishing_positions': finishing_positions  # List of 20 driver IDs (1st to 20th)
    }
    print(json.dumps(output))

if __name__ == '__main__':
    main()
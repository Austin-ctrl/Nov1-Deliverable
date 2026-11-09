# Tora: CARLA grounding update

**Audience:** Austin, Tarun and the team. **Status:** one corrected live timing replay completed twice; broader validation remains open.

- Austin: `parameters.csv` contains the sourced handoff. Treat the wet 0.35 reference as a condition-specific proxy, not universal wet-road or peak ABS friction. At 40 km/h, full-pedal CARLA wheel scalars 0.4, 0.45 and 0.5 gave 3.197, 3.596 and 3.995 m/s²; at scalar 0.45, 30 and 50 km/h checks gave 3.594 and 3.598 m/s². The scalar is not physical mu and 0.45 exceeds the chosen 3.4335 m/s² proxy by about 4.7%.
- Steering: 40 km/h front-left step peaks ranged from 146.640 to 148.832 deg/s across direction, step size and 5/10 ms timestep probes. This is a simulator step response, not a validated physical steering-rate limit.
- Infrastructure: a dedicated CARLA 0.9.15 server started and Town04 loaded; raw traces are preserved on the personal PVC and in the archive identified by `MEASUREMENT_STATUS.md`.
- Replay: the initial sweeps contained a pedestrian-reset error and remain invalid. After adding acknowledged positioning and a guard, two complete sweeps passed initial-position, full-horizon and command-timing checks. Commands issued at 0, 0.25 and 0.5 s were applied at 0.20, 0.45 and 0.70 s; each sweep recorded no person contact for the first and contact with `ped-A` for the other two. These are controlled simulator contacts in one scenario, not injury predictions.
- Next: Austin can use the table and documented source distinctions. Further work should compare the team's rate-limited steering model with CARLA and run additional scenarios and repetitions before drawing general conclusions.

See `MEASUREMENT_STATUS.md` for measured held-out wet-profile values and provenance, and the preserved raw archive identified there. No message has been sent to the team.

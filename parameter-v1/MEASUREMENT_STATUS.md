# Calibration and replay status — 26 October 2026

Namespace `gilpin-lab`; personal PVC `tjmatsud-av-grounding-work`; CARLA 0.9.15 client and server; Town04. No teammate scenario bank or Austin implementation was supplied. Simulated results are not real-vehicle validation.

- Dry reference: earlier `aiea-auditors` held-out profile and observed values; see `../team-lead/calibrated-profile.json` and `brake-calibration.csv`.
- Wet visual + lower-friction proxy: `WetNoon`, wheel scalar 0.5, 2x stock brake torque, 1ms outer step. A selected 3.4335 m/s² target produced 3.510305 and 3.521034 m/s² in 30 and 50 km/h held-out trials, one observation each. Predeclared relative gates: 10% acceleration, 15% kinematic stopping distance; passed. This is a fit to a selected target under a simulator configuration, not proof of actual wet-road peak.
- Maximum pedal at 40 km/h produced approximately 3.99454 m/s² at scalar 0.5, higher than selected target. Therefore do not label the selected target as the maximum physically allowed by that CARLA condition. The team hard-brake action must obey the agreed road cap; additional full-pedal friction-candidate probes are planned before finalizing the cap.
- Preserved first sweep had a flat plateau that the original strictly increasing curve check rejected. The fitter was amended to admit a plateau within floating point tolerance, preserving measurements and still rejecting a meaningful fall. A second complete sweep produced the accepted profile. Both sweeps remain in the raw archive.
- Vehicle bounding box readback: 4.7917795 m x 2.1634500 m x 1.4876601 m. Front-left road-wheel step response peak 146.64046 deg/s (2.55936 rad/s): normalized steer 0.15, 40 km/h, 10ms timestep. It is a sampled step response, not a proven maximum or real-vehicle validation.
- Timed replay: first live attempt was interrupted when the pod disappeared. No complete episodes were written. The one partial run is retained; it is not an experiment result.

## 27 October retry

The personal PVC was still bound and Kubernetes accepted a fresh pod from `cluster/gilpin-grounding-pod.yaml`. The pod was scheduled and the volume attachment succeeded, but the pod disappeared before the containers could be inspected or the CARLA server reached. No deletion cause was reported in the available pod events. The dry-run replay plan validated command times 0, 0.25 and 0.5 seconds with a 200 ms actuation delay, but this was not a live simulation. The full-pedal friction-candidate sweep, further steering-response checks and timed replay remain outstanding. Do not merge on the basis of the dry run or prior single steering measurement.

Another retry was rejected by the assigned node's GPU device plugin with a reported lost GPU (`UnexpectedAdmissionError`). A replacement excluding that node was submitted. On the subsequent check it was unscheduled; the scheduler reported insufficient GPUs, CPU or memory across eligible nodes and other node constraints. The PVC remained bound. Neither a live replay nor new friction or steering measurements were obtained from these retries.

## Subsequent access check

The isolated pod manifest requests one NVIDIA GPU, 5 CPUs and 14 GiB memory across its server and client containers, with opportunistic priority and an amd64 node selector. Kubernetes schedules those requests before the experiment scenario JSON is read; the earlier scheduler and GPU device-plugin errors are therefore not evidence of an invalid scenario JSON. Current cluster state could not be checked: the OIDC helper attempted to refresh a cache outside the session's writable directories, and a private temporary copy of the cache required interactive reauthentication. Once authenticated, inspect the current pod UID, events and resource availability before recreating or modifying the pod. No new live results were produced in this access check.

## Reauthenticated retry

After reauthentication, the dedicated PVC was bound and the old pod was absent. The replacement was created with the previously failed GPU node excluded. Kubernetes scheduled it on `gpn-fiona-mizzou-8.rnet.missouri.edu` and attached the PVC; namespace pod quota was 5/200 at inspection. At the most recent check both containers were still creating while the pinned CARLA image was being pulled. This scheduling success is not a CARLA readiness or experiment result. Live timing, friction-candidate and steering checks remain outstanding until the server and client are ready and verified.

## Live checks and replay reset issue

The first replacement disappeared after image extraction was canceled; events do not identify the cause. A new pod with a preference for nodes reporting the pinned image cached started on `fiona8-1.calit2.uci.edu`. CARLA client/server were both 0.9.15, the server had no actors, and Town04 was loaded.

Full-pedal braking at wheel scalars 0.4, 0.45 and 0.5 at 40 km/h produced 3.196779, 3.595899 and 3.994543 m/s² respectively, all valid and stopped. At scalar 0.45, 30 and 50 km/h checks produced 3.593992 and 3.598283 m/s². These are one deterministic trial per condition with 2x brake torque, not real-road peak friction; 0.45 is a CARLA scalar, not a physical coefficient. Scalar 0.45 produces about 4.7% more deceleration than the 0.35g proxy; no claim is made that it matches the target exactly.

At 40 km/h, front-left wheel step-response peaks were 146.6405 deg/s (+0.15, 10 ms), 148.8316 deg/s (-0.15, 10 ms), 146.6405 deg/s (+0.30, 10 ms) and 147.6874 deg/s (+0.15, 5 ms). These repeat and extend the earlier observation; the tested CARLA controller is not a validated real-vehicle steering limit, and the 0.472 rad/s study model remains a different reference.

Two three-command replay attempts completed with commanded application times 0.20, 0.45 and 0.70 s. Audit found an initial pedestrian position of approximately x=10.394 m instead of x=16 m in one episode of each sweep. A new initial-position guard has a regression test and rejected a subsequent live attempt. These sweeps must not be presented as controlled counterfactual results until reset is fixed and a complete sweep passes the geometry check. Raw archive `results/gilpin-grounding/recovery-results-v3.tgz` SHA256 `b570b36c2f01616110686af7a49ada48fe4cdc78f31cb6332ed8e8a510ca9a05` is also on the personal PVC. No validated replay or merge is claimed.

## Corrected replay

Pedestrian release poses now use an acknowledged CARLA command batch, and a guard checks the initial horizontal geometry within 0.2 mm. Two new complete three-episode sweeps passed that guard and explicit checks for the expected command application times and full horizon. In each sweep, commands issued at 0, 0.25 and 0.5 s were applied at 0.20, 0.45 and 0.70 s. The first recorded no person contact and the other two recorded contact with `ped-A`; this is one scripted scenario and two repeats, not a study of injury or general model performance. Initial pedestrian coordinates were approximately (16.000004, -2.000023) m in all six episodes. The earlier mismatched runs remain invalid and retained for audit.

Latest complete archive (including invalid and corrected sweeps, braking and steering traces): `results/gilpin-grounding/recovery-results-v4.tgz`, SHA256 `212dba7071870ea28e6de7d699b625977bdcb2d2ae40774ca0aad75af1dc418a`; also stored on the personal PVC. The braking/steering probes were run with the preceding source revision, and their result files record source hashes. The CARLA steering response remains materially different from the cited model limit and is not validated against a real vehicle.

Raw backup path (ignored by Git): `results/gilpin-grounding/recovery-results.tgz`; SHA256 `34cf6a94d9d164c292ec2ada099e384ab253ffd6c93747bfd92ca2849c344698`. Original records and traces also remain on the dedicated personal PVC. `wet-calibrated-profile.json` and `steering-probe.json` are tracked copies of extracted results; exact runtime source hashes are inside the profile.

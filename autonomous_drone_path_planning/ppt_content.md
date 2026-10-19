# PPT CONTENT — AUTONOMOUS DRONE PATH PLANNING

## Slide 1 — Title
Autonomous Drone Path Planning Using Game Theory

GTDS Mini Project

Team Members:
- [Name]
- [Name]
- [Name]

## Slide 2 — Problem Statement
Multiple autonomous drones operating in the same area may select overlapping routes when planning independently.

This can lead to:
- route conflicts
- unnecessary travel
- higher energy consumption
- reduced surveillance efficiency

## Slide 3 — Objectives
- Simulate multi-drone route planning.
- Model each drone as a game-theoretic player.
- Generate feasible routes around obstacles.
- Minimize distance and energy.
- Reduce route conflicts.
- Maximize surveillance coverage.
- Compare independent planning with game-theoretic planning.

## Slide 4 — Proposed System
Environment → Candidate Paths → Utility Calculation → Best Response → Conflict Evaluation → Stable Routes → Performance Comparison

## Slide 5 — Game Theory Mapping
Players = Drones

Strategies = Candidate Routes

Utility =
Coverage Benefit
− Distance Cost
− Energy Cost
− Conflict Penalty
− Target Overlap Penalty

Decision method = Iterative Best Response

## Slide 6 — Algorithm
1. Initialize map, obstacles, drones and surveillance zones.
2. Generate candidate routes using A*.
3. Initialize with independent shortest paths.
4. Select one drone.
5. Evaluate all candidate routes against other drones.
6. Select highest-utility route.
7. Repeat for every drone.
8. Stop when no route changes.
9. Compare metrics.

## Slide 7 — System Architecture
Input
↓
Environment
↓
A* Candidate Path Generation
↓
Utility Function
↓
Game-Theoretic Best Response
↓
Conflict Detection
↓
Final Routes
↓
Metrics + Visualization

## Slide 8 — Demo
Show:
- map
- obstacles
- D1, D2, D3
- surveillance zones
- baseline paths
- game-theoretic paths

## Slide 9 — Results
Insert the values generated in `results/metrics.csv`.

Compare:
- total distance
- energy
- conflict score
- coverage

Do not use manually invented numbers.

## Slide 10 — Limitations
- 2D simulation
- static obstacles
- simplified energy model
- finite candidate routes
- no real UAV dynamics

## Slide 11 — Future Scope
- 3D path planning
- dynamic obstacle avoidance
- real battery models
- weather/wind
- ROS/Gazebo
- reinforcement learning
- real drone integration

## Slide 12 — Conclusion
Game theory provides a decision-making framework in which drones account for the routes selected by other drones. The simulation demonstrates how strategic route selection can be evaluated using distance, energy, conflict and surveillance coverage metrics.

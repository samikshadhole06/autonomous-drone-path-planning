# Autonomous Drone Path Planning Using Game Theory

## 1. Abstract
Autonomous multi-drone systems must coordinate route selection while balancing travel distance, energy consumption, collision risk and surveillance coverage. This mini project models every drone as a rational player in a non-cooperative game. Each drone has a set of candidate paths generated using A* path planning. A utility function rewards surveillance coverage and penalizes distance, energy use and conflicts with other drones. An iterative best-response mechanism allows each drone to reconsider its route based on the current strategies of the other drones. The simulation compares independent shortest-path planning with game-theoretic planning using distance, energy, conflicts and coverage as evaluation metrics.

## 2. Problem Statement
When several autonomous drones operate in the same environment, independently selecting the shortest path can cause route overlap, conflicts and inefficient resource usage. A decision-making framework is therefore required so that each drone can optimize its own objective while considering the decisions of other drones.

## 3. Objectives
1. Develop a 2D simulation environment for multiple autonomous drones.
2. Generate feasible candidate routes around static obstacles.
3. Model drones as players in a non-cooperative game.
4. Design a utility function based on surveillance coverage, distance, energy and conflicts.
5. Implement iterative best-response route selection.
6. Compare the game-theoretic solution with independent shortest-path planning.

## 4. System Design

### Inputs
- Grid dimensions
- Drone starting positions
- Static obstacles
- Surveillance zones
- Candidate route parameters

### Processing
1. Create the environment.
2. Generate candidate paths using A*.
3. Evaluate each candidate strategy.
4. Calculate utility against the routes currently selected by other drones.
5. Let each drone choose its best response.
6. Repeat until the solution becomes stable or the iteration limit is reached.

### Outputs
- Final routes
- Total distance
- Estimated energy consumption
- Conflict score
- Surveillance coverage
- Comparison graphs

## 5. Game-Theoretic Model

### Players
Drones D1, D2 and D3.

### Strategies
A strategy is a candidate route to a surveillance zone.

### Utility
For drone i:

U_i = 18C_i - D_i - 0.25E_i - 7P_i - 5O_i

where:
- C_i = number of surveillance zones covered
- D_i = route distance
- E_i = estimated energy cost
- P_i = conflict cost with other drones
- O_i = target-overlap penalty

The constants are tunable simulation weights, not physical drone measurements.

### Best Response
For the current strategies of all other drones, drone i evaluates all of its candidate routes and selects the one with maximum utility.

The process stops when a complete round produces no route change. This represents a stable strategy profile within the finite candidate-strategy game.

## 6. Algorithm

```text
Create environment
        ↓
Generate candidate paths
        ↓
Choose independent shortest paths
        ↓
Initialize game with baseline routes
        ↓
For each drone:
    Evaluate all candidate strategies
    Calculate utility against other drones
    Select highest-utility strategy
        ↓
Did any route change?
    Yes → repeat
    No  → stable solution
        ↓
Calculate final metrics
        ↓
Generate graphs and route map
```

## 7. Technologies
- Python
- NumPy
- Matplotlib
- Pandas
- A* search
- Game theory / best-response dynamics

## 8. Evaluation Metrics

### Distance
Number of grid movements in a selected route.

### Energy
A simplified proportional energy model:
E = 1.15 × distance.

### Conflict
Penalty for spatial route overlap and approximate same-time cell occupation.

### Coverage
Percentage of defined surveillance zones visited by at least one drone.

## 9. Expected Demonstration
The project provides two solutions:
1. Independent baseline: drones minimize their own route length without considering other drones.
2. Game-theoretic solution: drones adapt their strategies according to the utility produced by the current routes of the other drones.

The generated CSV and graphs should be used for the final numerical results. Do not enter invented performance values in the report.

## 10. Limitations
- The environment is a 2D grid.
- Obstacles are static.
- Drone dynamics are simplified.
- Energy is estimated rather than calculated from a physical flight model.
- Communication delay and real GPS uncertainty are not modeled.
- The candidate strategy set is finite.

## 11. Future Scope
- Dynamic obstacles
- Real-time drone telemetry
- Continuous 3D flight planning
- Wind and battery models
- Multi-objective optimization
- Reinforcement learning
- ROS/Gazebo simulation
- Real UAV hardware testing

## 12. Conclusion
The project demonstrates how game-theoretic decision making can be incorporated into autonomous multi-drone path planning. By treating each drone as a player and incorporating the decisions of other drones into the utility calculation, the simulation provides a structured approach to route selection and conflict reduction. The comparison with independent planning allows the effect of strategic interaction to be evaluated using measurable metrics.

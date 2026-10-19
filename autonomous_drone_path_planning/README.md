# Autonomous Drone Path Planning using Game Theory

GTDS Mini Project

## Project idea
A simulation-based multi-drone path-planning system where each drone acts as a rational player. Drones select routes while considering:
- travel distance
- energy consumption
- collision/conflict risk
- surveillance coverage
- the routes selected by other drones

The project uses an iterative best-response game-theoretic strategy.

## Requirements
Python 3.9+
```bash
pip install -r requirements.txt
```

## Run
```bash
python main.py
```

The program creates:
- `results/final_paths.png`
- `results/comparison.png`
- `results/metrics.csv`
- `results/iteration_log.csv`

## What the demo shows
1. A 25 x 25 grid environment.
2. Three autonomous drones.
3. Static obstacles.
4. Five surveillance zones.
5. Candidate paths generated using A*.
6. A baseline where each drone independently selects its cheapest route.
7. An iterative best-response game where each drone evaluates its payoff against the current strategies of the other drones.
8. Comparison using distance, energy, conflicts and surveillance coverage.

## Game-theoretic model

For drone i:

U_i = coverage - alpha(distance) - beta(energy) - gamma(conflict)

The conflict term penalizes shared cells and simultaneous occupation of the same cell.

A drone changes its route only when another candidate route gives a higher utility. Iteration stops when no drone can improve its utility by changing its strategy.

## Viva keywords
Players: drones
Strategies: candidate routes
Payoff/utility: coverage benefit minus distance, energy and conflict costs
Best response: highest-utility route against the current routes of the other drones
Stable solution: no drone can improve its utility by unilateral route change within the available candidate strategies

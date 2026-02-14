# WGUPS Package Routing Simulator

A Python application that simulates package delivery routing for a courier service, optimizing multi-truck routes under real-world constraints including delivery windows, package dependencies, and truck capacity limits.

## Problem

Given 40 packages with varying delivery deadlines, special handling requirements, and address corrections that arrive mid-day, route 3 trucks to deliver all packages under 140 total miles while respecting all constraints.

## Approach

The simulator uses a **nearest-neighbor heuristic** for route optimization, combined with a **custom hash table** for O(1) package lookups. Packages are pre-sorted into truck loads based on constraint analysis (deadline clustering, co-delivery requirements, delayed availability), then each truck's route is optimized independently.

**Why nearest-neighbor over more complex algorithms?** For this problem size (40 packages, 27 locations), nearest-neighbor provides a good-enough solution without the computational overhead of exact methods. The constraint satisfaction — not the raw distance optimization — is the harder problem here, and that's handled in the loading phase.

## Features

- **Custom Hash Table** — Open-addressing hash table with O(1) average-case insert and lookup, handling collision resolution without external libraries
- **Constraint Engine** — Resolves delivery windows, truck-specific assignments, co-delivery requirements, and delayed package availability before route calculation
- **Real-Time Tracking** — Query any package's status (at hub, en route, delivered) at any point in the simulated timeline
- **Distance Optimization** — All trucks complete their routes under the 140-mile combined constraint

## Running

```bash
# Clone the repository
git clone https://github.com/szmathias/WGUPS-Routing-Program.git
cd WGUPS-Routing-Program

# Run the simulator
python main.py
```

The program provides an interactive interface to:
- View all package statuses at a specific time
- Look up individual package delivery details
- View total mileage across all trucks

## Data Structures

**Hash Table** — Built from scratch (no `dict` usage for the core data structure). Uses a fixed-size array with modular hashing and handles collisions through open addressing. Supports insert, lookup, and update operations used throughout the delivery simulation.

**Distance Matrix** — 2D adjacency matrix loaded from CSV representing distances between all delivery locations. Enables O(1) distance lookups between any two addresses during route calculation.

## What I'd Improve

- Implement 2-opt or simulated annealing for better route optimization
- Add visualization of truck routes on a map
- Support dynamic re-routing when constraints change mid-simulation
- Benchmark against other heuristics (greedy, genetic algorithm) on the same dataset

# WGUPS Routing Program

Student project implementing a package routing simulation for the WGUPS (courier) problem. The application loads package and distance data, models locations and distances, stores packages for O(1) lookup, and computes delivery routes for three trucks under the course constraints.

Contents
- Project goals
- Chosen algorithm (A)
- Data structure (B)
- Program overview and pseudocode (C.1)
- Environment (C.2)
- Complexity analysis (C.3)
- Scalability and adaptability (C.4)
- Maintainability and design justification (C.5)
- Hash table strengths and weaknesses (C.6)
- Key selection justification (C.7)
- Notes about special cases and simulation
- References and acknowledgements (D)

Project goals
- Deliver all 40 packages meeting each package constraint and deadlines.
- Keep combined truck mileage under 140 miles.
- Provide clear runtime tracking of package status and delivery times.

Chosen algorithm (A)
- Primary routing heuristic: Nearest Neighbor (a greedy, self-adjusting heuristic).
- Rationale: fast, simple to implement, and acceptable for constrained classroom data sets. Use with multi-truck scheduling and manual adjustments for special constraints (deadlines, early/late availability, and the known delayed address correction for package 9).

Data structure (B)
- Primary data structure: Hash table (dictionary-like) keyed by package ID.
- Purpose: store package records (address, deadline, city, zip, weight, status, timestamp, special notes) for constant-time lookup and status updates during simulation.
- Relationship handling: the hash table maps package ID → Package object. Addresses and location indices are stored separately in a location graph so routing references an integer index or normalized address string.

Program overview and pseudocode (C.1)
- High-level behavior:
  1. Load CSV files: distance matrix and package list.
  2. Build location graph (distance lookup) and normalize addresses to indices.
  3. Insert packages into hash table keyed by package ID.
  4. Create trucks (capacity 16) and assign initial package sets according to constraints.
  5. Simulate deliveries per truck using nearest neighbor heuristic, honoring deadlines and the 10:20 AM update for package 9.
  6. Track package status and timestamps; compute total mileage and time.

Pseudocode:
```
load_data()
    locations = parse_distance_csv()
    packages = parse_package_csv()
    for pkg in packages:
      hashtable.insert(pkg.id, pkg)

assign_packages_to_trucks()
apply constraints (deadlines, grouped packages, earliest departure, capacity)
    
simulate_truck(truck)
current = hub_index
time = truck.departure_time
while truck.has_packages():
    next = nearest_unvisited(current, Packages, locations, time)
    drive_distance = distance[current][next]
    time += drive_distance / speed
    deliver packages at next (update hashtable statuses and delivery times)
    current = next
return to hub

main()
    load_data()
    assign_packages_to_trucks()
    simulate trucks (track combined miles and times)
```
Environment (C.2)
- Software: Python 3.10+ (CPython), standard library only. Optional: PyCharm or VS Code for development.
- Hardware (example): Windows 10/11 or Linux/macOS, 64-bit CPU, 4+ GB RAM, typical laptop or desktop.

Complexity analysis (C.3)
- n = number of packages (≈40), V = number of unique locations, k = number of trucks (3).
- Loading CSV files: O(n + V^2) time to read distances and packages; O(n + V^2) space if distance matrix stored as adjacency matrix.
- Hash table insert/lookup: average O(1) time per operation; O(n) space for package storage.
- Nearest neighbor heuristic per truck: O(m^2) where m is packages on that truck (worst-case m ≤ 16). With k trucks, worst-case O(k * m^2) ≤ O(k * 16^2) — effectively constant for this data set, but O(n^2) in a generic formulation.
- Overall runtime for realistic data set: dominated by routing steps O(n^2) in the worst case; space dominated by distance matrix O(V^2) or O(V + E) if adjacency lists used.

Scalability and adaptability (C.4)
- For many cities or larger n, replace adjacency matrix with adjacency lists or sparse distance lookup to reduce space from O(V^2) to O(V + E).
- For larger n, replace the nearest neighbor heuristic with cluster-first / route-second methods or metaheuristics (k-means + 2-opt / simulated annealing) to improve solution quality and keep mileage low.
- The modular design (separate Graph, HashTable, Package, and main) supports swapping the routing module without changing storage or I/O code.

Maintainability and design justification (C.5)
- Clear separation of concerns: CSV parsing, data storage, routing logic, and simulation/reporting are isolated modules.
- Use of small, documented functions and a Package class makes behavior explicit and easy to unit test.
- Adding logging or a CLI flag for verbose output supports grader inspection and automated tests.

Hash table strengths and weaknesses (C.6)
- Strengths:
  - O(1) average lookup, insert, and update — ideal for frequent package status checks.
  - Well-supported by language native dictionaries.
- Weaknesses:
  - No inherent ordering. Requires additional structures (lists) for ordered traversals.
  - Memory overhead and potential collisions (handled by the language runtime).
  - Not ideal for range queries or nearest-neighbor in geometric space; it is a lookup structure, not a spatial index.

Key selection justification (C.7)
- Primary key: package ID. Justification: unique, stable identifier allowing unambiguous lookup and updates (status, delivery time).
- Secondary keys / indexing used for routing and reporting:
  - Delivery address (or normalized location index) — used by the routing algorithm to compute distances and group deliveries.
  - Delivery deadline — used to prioritize packages during route assignment and to select departure/loading sequences.
- Rationale: package ID provides O(1) access and avoids ambiguity; address and deadline are used as attributes for routing priority but are not primary keys.

Notes about special cases and the simulation
- Package 9: address corrected at 10:20 AM. The simulation should mark the package as "address pending" until 10:20 AM; after 10:20 AM, the address and location index are updated in the hash table and eligible for routing.
- Truck rules: capacity 16, speed 18 mph, instantaneous loading/delivery time assumption (per course assumptions).
- Progress reporting: Package status values: at hub, en route, delivered; each update includes a timestamp string.

References and acknowledgements (D)
- Nearest neighbor heuristic (TSP heuristic). Wikipedia: https://en.wikipedia.org/wiki/Nearest_neighbor_heuristic
- Hash table. Wikipedia: https://en.wikipedia.org/wiki/Hash_table
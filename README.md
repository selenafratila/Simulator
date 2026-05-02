# SmartCity Network Simulator

A Python-based telecommunications simulator designed to analyze and visualize radio signal propagation in complex urban environments.

## Overview
This project simulates how different types of cellular antennas (Pico, Micro, Macro) provide coverage to mobile users in a 2D city grid. The core logic accounts for **Free Space Path Loss** and **Shadowing Effects** caused by various urban obstacles like skyscrapers, metal warehouses, or forests.

##  Key Features
- **Dynamic Network Configuration:** Add antennas and buildings in real-time via CLI.
- **Randomized User Deployment:** Users are spawned at random coordinates across the map grid to simulate real-world unpredictable traffic patterns and test the network's robustness.
- **Path Sampling Logic:** Implements a 3-point sampling algorithm (25%, 50%, 75% of the path) to detect if obstacles block the signal Line-of-Sight (LoS).
- **Material-Specific Attenuation:** Obstacles have different signal loss values based on material.
- **Rich Visualization:** Generates a 2D map using `Matplotlib` showing:
  - Antennas (Triangles) and Users (Nodes).
  - Color-coded signal quality (Green = Excellent, Red = Dead Zone).
  - Connection lines between users and their best serving antenna.
 
## Simulation Scenarios
-**The Industrial Shadow:** A high-power MacroCell blocked by a massive metal structure.

What to observe:

Shadowing Effect: Mary Smith (Red) is closer to the antenna but loses signal because the "Iron Curtain" blocks her, while Stefan Williams (Green) stays connected via a clear line of sight.

Obstacle Impact: The simulation proves that signal quality depends on obstacles rather than just distance.

Material Physics: Metal correctly triggers the highest attenuation, creating a visible "dead zone" behind the building.

<img width="870" height="350" alt="Screen Shot 2026-04-13 at 04 00 13" src="https://github.com/user-attachments/assets/ea39f8da-85ba-4aca-af0b-2552434b5263" /> 
<img width="870" height="350" alt="Screen Shot 2026-04-13 at 04 00 28" src="https://github.com/user-attachments/assets/c7c875c9-7b7f-42d5-a875-60463e2782ad" />
<img width="1000" height="1000" alt="download1" src="https://github.com/user-attachments/assets/a876fbb7-eed1-4c48-85f2-85f4fe377fe1" />


## Software Architecture (OOP)
The project is built using **Object-Oriented Programming** principles to ensure modularity and scalability:
- **Class `Antenna`**: Encapsulates physical properties (power, coordinates) and signal calculation logic.
- **Class `Obstacle`**: Defines urban geometry and material-specific attenuation factors.
- **Class `User`**: Handles spatial positioning, randomized spawning, and the core decision-making logic for antenna association.
    
## Technical Stack
- **Language:** Python 3.x
- **Libraries:** `NumPy` (math & distances), `Matplotlib` (spatial visualization).

## 📊How it Works
1. **Distance Calculation:** Euclidean distance between user and antenna.
2. **Signal Formula:** $$Signal(dBm) = Power - (20 \cdot \log_{10}(dist) + 32.4) - ObstacleLoss$$
3. **Shadowing:** If an obstacle is between the user and antenna, a 50% "shadowing" penalty of the building's specific loss is applied.

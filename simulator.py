import numpy as np
import random

# --- CONFIGURATION CONSTANTS ---
MAP_LIMIT = 2500

ANTENNA_LIMITS = {
    "PicoCell":  {"max": 20},
    "MicroCell": {"max": 35},
    "MacroCell": {"max": 50}
}

OBSTACLE_TYPES = {
    "Concrete Block": 25,
    "Brick Building": 15,
    "Forest": 8,
    "Glass Office": 5,
    "Metal Warehouse": 40
}

class Antenna:
    def __init__(self, antenna_type: str, x: float, y: float, power_dbm: int):
        self.antenna_type = antenna_type
        self.x = x
        self.y = y
        self.power_dbm = power_dbm

    def calculate_signal(self, dist, obstacle_loss=0):
        if dist < 1: dist = 1
        loss = 20 * np.log10(dist) + 32.4
        return self.power_dbm - loss - obstacle_loss

class Obstacle:
    def __init__(self, name: str, x1: float, y1: float, x2: float, y2: float, obs_type: str):
        self.name = name
        self.x1, self.y1 = x1, y1
        self.x2, self.y2 = x2, y2
        self.obs_type = obs_type
        self.loss_db = OBSTACLE_TYPES.get(obs_type, 10)

    def is_inside(self, u_x, u_y):
        return self.x1 <= u_x <= self.x2 and self.y1 <= u_y <= self.y2

class User:
    def __init__(self, name: str, x: float, y: float):
        self.name = name
        self.x = x
        self.y = y

    def calculate_distance_to_antenna(self, antenna: Antenna):
        return np.sqrt((self.x - antenna.x)**2 + (self.y - antenna.y)**2)

    def get_signal_from_antenna(self, antenna: Antenna, obstacles_list: list):
        dist = self.calculate_distance_to_antenna(antenna)
        total_obstacle_loss = 0
        for obs in obstacles_list:
            if obs.is_inside(self.x, self.y):
                total_obstacle_loss += obs.loss_db
        return antenna.calculate_signal(dist, obstacle_loss=total_obstacle_loss)

    def find_best_antenna(self, antennas_list: list, obstacles_list: list):
        best_signal = -999
        best_antenna_name = None
        for antenna in antennas_list:
            current_signal = self.get_signal_from_antenna(antenna, obstacles_list)
            if current_signal > best_signal:
                best_signal = current_signal
                best_antenna_name = antenna.antenna_type
        return best_antenna_name, best_signal

# --- HELPER FUNCTION FOR AUTO-CLASSIFICATION ---
def classify_antenna(power):
    if power <= ANTENNA_LIMITS["PicoCell"]["max"]:
        return "PicoCell"
    elif power <= ANTENNA_LIMITS["MicroCell"]["max"]:
        return "MicroCell"
    else:
        return "MacroCell"

# --- DATA GENERATION ---
first_names = ["Maria", "Andrei", "Elena", "Matei", "Ioana", "Stefan", "Anca", "Alex", "Cristian", "Laura"]
last_names = ["Popescu", "Ionescu", "Dumitru", "Stan", "Gheorghe", "Stoica", "Radu", "Enache"]

users_list = []
used_coordinates = set()
num_users = 15 

while len(users_list) < num_users:
    full_name = f"{random.choice(first_names)} {random.choice(last_names)}"
    x = random.randint(-MAP_LIMIT, MAP_LIMIT)
    y = random.randint(-MAP_LIMIT, MAP_LIMIT)
    if (x, y) not in used_coordinates:
        used_coordinates.add((x, y))
        users_list.append(User(full_name, x, y))

# --- CITY OBSTACLES ---
obstacles_list = [
    Obstacle("Shopping Mall", 0, 0, 400, 400, "Glass Office"),
    Obstacle("Industrial Area", -1500, -1500, -1000, -1000, "Metal Warehouse"),
    Obstacle("Residential Block", 500, -500, 800, -200, "Concrete Block")
]

# --- ANTENNA CONFIGURATION (VERSION B with Min/Max) ---
antennas_list = [Antenna("Macro_Default", 1500, 1500, 45)]

print("\n--- ANTENNA NETWORK CONFIGURATION ---")
while True:
    response = input("Add custom antenna? (yes/no): ").lower()
    if response != 'yes': break
    
    try:
        ax = float(input(f"X coordinate (-{MAP_LIMIT} to {MAP_LIMIT}): "))
        ay = float(input(f"Y coordinate (-{MAP_LIMIT} to {MAP_LIMIT}): "))
        
        if abs(ax) > MAP_LIMIT or abs(ay) > MAP_LIMIT:
            print(f"Error: Stay within {MAP_LIMIT}m range!")
            continue
        
        pwr = int(input("Enter Power (dBm) [Range: -10 to 50]: "))
        
        if pwr < -10 or pwr > 50:
            print("Error: Power out of bounds! Must be between -10 and 50 dBm.")
            continue
            
        a_type = classify_antenna(pwr)
        antennas_list.append(Antenna(f"{a_type}_{len(antennas_list)}", ax, ay, pwr))
        print(f"Added as {a_type} based on power level ({pwr} dBm).")
        
    except ValueError:
        print("Invalid input! Please enter numeric values.")

# --- SIMULATION REPORT ---
print("\n" + "="*70)
print(f"{'MULTI-USER SIMULATION REPORT':^70}")
print("="*70)

excellent_count = good_count = poor_count = dead_zone_count = 0

for u in users_list:
    best_ant, best_sig = u.find_best_antenna(antennas_list, obstacles_list)

    if best_sig > -70: excellent_count += 1
    elif -85 < best_sig <= -70: good_count += 1
    elif -100 < best_sig <= -85: poor_count += 1
    else: dead_zone_count += 1

    print(f"-> {u.name:18} | Pos: ({u.x:5}, {u.y:5}) | Antenna: {best_ant:15} | Signal: {best_sig:.2f} dBm")

print("="*70)
print(f"FINAL STATISTICS: Exc: {excellent_count} | Good: {good_count} | Poor: {poor_count} | Dead: {dead_zone_count}")
print("="*70)
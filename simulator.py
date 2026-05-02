import numpy as np
import random
import matplotlib.pyplot as plt
import matplotlib.patches as patches

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
    def is_obstacle_blocking(self, antenna: Antenna, obs: Obstacle):
        x1, y1 = antenna.x, antenna.y
        x2, y2 = self.x, self.y
        # 25%, 50%, 75% 
        for ratio in [0.25, 0.5, 0.75]:
            check_x = x1 + ratio * (x2 - x1)
            check_y = y1 + ratio * (y2 - y1)
            if obs.is_inside(check_x, check_y):
                return True
        return False
    def get_signal_from_antenna(self, antenna: Antenna, obstacles_list: list):
        dist = self.calculate_distance_to_antenna(antenna)
        total_obstacle_loss = 0
        for obs in obstacles_list:
            if obs.is_inside(self.x, self.y):
                total_obstacle_loss += obs.loss_db
            elif self.is_obstacle_blocking(antenna, obs):
                total_obstacle_loss += (obs.loss_db * 0.5)
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

def visualize_city(users, antennas, obstacles):
    fig, ax = plt.subplots(figsize=(12, 12))
    
    # Colors
    obs_colors = {
        "Concrete Block": "gray",
        "Brick Building": "peru",
        "Forest": "forestgreen",
        "Glass Office": "skyblue",
        "Metal Warehouse": "dimgray"
    }

    # Drawing obstacles
    for obs in obstacles:
        width = obs.x2 - obs.x1
        height = obs.y2 - obs.y1
        rect = patches.Rectangle((obs.x1, obs.y1), width, height, 
                                 linewidth=1, edgecolor='black', 
                                 facecolor=obs_colors.get(obs.obs_type, "silver"), 
                                 alpha=0.6, label="Obstacle")
        ax.add_patch(rect)
        plt.text(obs.x1, obs.y2 + 20, obs.name, fontsize=8, fontweight='bold')

    # Drawing users
    for u in users:
        ant_name, sig = u.find_best_antenna(antennas, obstacles)
      
        best_ant = next(a for a in antennas if a.antenna_type == ant_name)
        
        # Choosing color
        if sig > -70: color = 'green'
        elif -85 < sig <= -70: color = 'gold'
        elif -100 < sig <= -85: color = 'orange'
        else: color = 'red'
        
        # Line from user to antenna
        plt.plot([u.x, best_ant.x], [u.y, best_ant.y], 
                 color=color, linestyle='--', linewidth=0.5, alpha=0.3, zorder=1)
        
        # Draw the point
        plt.scatter(u.x, u.y, c=color, s=50, edgecolors='black', zorder=5)
        
        # Place text
        plt.text(u.x + 40, u.y + 40, f"{u.name} ({sig:.0f}dBm)", 
                 fontsize=8, alpha=0.9)
        
    # Drawing antennas
    for ant in antennas:
        plt.scatter(ant.x, ant.y, marker='^', c='blue', s=150, 
                    edgecolors='white', linewidth=2, zorder=10)
        plt.text(ant.x, ant.y - 150, ant.antenna_type, fontsize=10, 
                 ha='center', color='blue', fontweight='bold', 
                 bbox=dict(facecolor='white', alpha=0.7, edgecolor='none'))

    # Design configuration
    plt.xlim(-MAP_LIMIT - 100, MAP_LIMIT + 100)
    plt.ylim(-MAP_LIMIT - 100, MAP_LIMIT + 100)
    plt.axhline(0, color='black', linewidth=0.5, ls='--')
    plt.axvline(0, color='black', linewidth=0.5, ls='--')
    plt.grid(True, linestyle=':', alpha=0.5)
    plt.title("Smart City Network Coverage Map", fontsize=15)
    plt.xlabel("X distance (meters)")
    plt.ylabel("Y distance (meters)")
    
    # Custom legend
    from matplotlib.lines import Line2D
    legend_elements = [
        Line2D([0], [0], marker='^', color='w', markerfacecolor='blue', markersize=10, label='Antenna'),
        Line2D([0], [0], marker='o', color='w', markerfacecolor='green', label='Excellent'),
        Line2D([0], [0], marker='o', color='w', markerfacecolor='gold', label='Good'),
        Line2D([0], [0], marker='o', color='w', markerfacecolor='orange', label='Poor'),
        Line2D([0], [0], marker='o', color='w', markerfacecolor='red', label='Dead Zone')
    ]
    ax.legend(handles=legend_elements, loc='upper right')
    
    plt.show()

# --- DATA GENERATION ---
first_names = ["James", "Gabrielle","Sophia", "Michael","Penelope","Susan", "Mike","Paul","Louie", "Mary", "Jane", "Stefan", "Anne", "Benjamin", "Christian", "Katherine"]
last_names = ["Mayer", "Williams", "Garcia", "Parker", "Young", "Solis", "Scavo", "Smith","Davis"]

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
obstacles_list = []
print("\n--- CITY OBSTACLES CONFIGURATION ---")
while True:
    response = input("Add an obstacle/building? (yes/no): ").lower()
    if response != 'yes': break
    
    print(f"Available types: {list(OBSTACLE_TYPES.keys())}")
    obs_name = input("Name of the building: ")
    obs_type = input("Type (from list above): ")
    
    try:
        ox1 = float(input("Left-Down X: "))
        oy1 = float(input("Left-Down Y: "))
        ox2 = float(input("Right-Up X: "))
        oy2 = float(input("Right-Up Y: "))
        
        #x2 must be >= x1, y2>=y1
        if ox2 <= ox1 or oy2 <= oy1:
            print("Error: Right-Up coordinates must be greater than Left-Down!")
            continue
            
        obstacles_list.append(Obstacle(obs_name, ox1, oy1, ox2, oy2, obs_type))
        print(f"Added {obs_name} ({obs_type}) to the map.")
    except ValueError:
        print("Invalid input! Use numbers.")
# --- ANTENNA CONFIGURATION 0 ---
antennas_list = []

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

visualize_city(users_list, antennas_list, obstacles_list)

import numpy as np
import random

class Antenna:
    def __init__(self, antenna_type: str, x: float, y: float, power_dbm: int):
        self.antenna_type = antenna_type
        self.x = x
        self.y = y
        self.power_dbm = power_dbm

    def get_distance(self, u_x, u_y):
        return np.sqrt((self.x - u_x)**2 + (self.y - u_y)**2)

    def calculate_signal(self, dist, obstacle_loss=0):
        if dist < 1: dist = 1
        # Path Loss Formula (standard)
        loss = 20 * np.log10(dist) + 32.4
        return self.power_dbm - loss - obstacle_loss

class User:
    def __init__(self, name: str, x: float, y: float):
        self.name = name
        self.x = x
        self.y = y

    def describe_position(self):
        print(f"User {self.name} is located at ({self.x}, {self.y})")

    def calculate_distance_to_antenna(self, antenna: Antenna):
        return np.sqrt((self.x - antenna.x)**2 + (self.y - antenna.y)**2)

    def get_signal_from_antenna(self, antenna: Antenna):
        dist = self.calculate_distance_to_antenna(antenna)
        return antenna.calculate_signal(dist)

    def find_best_antenna(self, antennas_list):
        best_signal = -999
        best_antenna_name = None
        for antenna in antennas_list:
            current_signal = self.get_signal_from_antenna(antenna)
            if current_signal > best_signal:
                best_signal = current_signal
                best_antenna_name = antenna.antenna_type
        return best_antenna_name, best_signal

#  DATA GENERATION
first_names = ["Maria", "Andrei", "Elena", "Matei", "Ioana", "Stefan", "Anca", "Alex", "Cristian", "Laura"]
last_names = ["Popescu", "Ionescu", "Dumitru", "Stan", "Gheorghe", "Stoica", "Radu", "Enache"]

users_list = []
used_coordinates = set()
num_users = 15 

while len(users_list) < num_users:
    full_name = f"{random.choice(first_names)} {random.choice(last_names)}"
    x = random.randint(-2000, 2000)
    y = random.randint(-2000, 2000)
    
    if (x, y) not in used_coordinates:
        used_coordinates.add((x, y))
        users_list.append(User(full_name, x, y))

#ANTENNA CONFIGURATION 
antennas_list = []
print("\nANTENNA NETWORK CONFIGURATION")
# Default antenna
antennas_list.append(Antenna("Macro_Default", 1500, 1500, 25))

while True:
    response = input("Do you want to add an antenna manually? (yes/no): ").lower()
    if response != 'yes':
        break
    
    a_type = input("Antenna type (e.g.,Macro, Micro, Pico): ")
    try:
        ax = float(input(f"X coordinate for {a_type}: "))
        ay = float(input(f"Y coordinate for {a_type}: "))
        pwr = int(input(f"Power_dBm for {a_type}: "))
        antennas_list.append(Antenna(a_type, ax, ay, pwr))
    except ValueError:
        print("Invalid input. Please enter numbers for coordinates and power.")

#  SIMULATION REPORT 
print("\n" + "="*60)
print("MULTI-USER SIMULATION REPORT")
print("="*60)

excellent_count = 0
good_count = 0
poor_count = 0
dead_zone_count = 0

for u in users_list:
    best_ant, best_sig = u.find_best_antenna(antennas_list)

    if best_sig > -70:
        excellent_count += 1
    elif -85 < best_sig <= -70:
        good_count += 1
    elif -100 < best_sig <= -85:
        poor_count += 1
    else:
        dead_zone_count += 1

    print(f"-> {u.name:18} | Pos: ({u.x:5}, {u.y:5}) | Best Antenna: {best_ant:15} | Signal: {best_sig:.2f} dBm")

print("="*60)

print("\n FINAL NETWORK STATISTICS ")
print(f"Excellent coverage: {excellent_count}")
print(f"Good coverage:      {good_count}")
print(f"Poor coverage:      {poor_count}")
print(f"Dead zones:         {dead_zone_count}")
print("="*60)
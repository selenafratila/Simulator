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
        # Formula Path Loss (standard)
        loss = 20 * np.log10(dist) + 32.4
        return self.power_dbm - loss - obstacle_loss
class User:
    def __init__(self, name:str, x:float,y:float):
        self.name=name
        self.x=x
        self.y=y
    def describe_position(self):
        print(f"User {self.name} is located at ({self.x},{self.y})")
    def calculate_distance_to_antenna(self, antenna: Antenna):
        return np.sqrt((self.x-antenna.x)**2+(self.y-antenna.y)**2)
    def get_signal_from_antenna(self,antenna: Antenna):
        dist=self.calculate_distance_to_antenna(antenna)
        return antenna.calculate_signal(dist)
    def find_best_antenna(self,antennas_list):
        best_signal=-999
        best_antenna_name=None
        for antenna in antennas_list:
            current_signal=self.get_signal_from_antenna(antenna)
            if current_signal > best_signal:
                best_signal=current_signal
                best_antenna_name=antenna.antenna_type
        return best_antenna_name, best_signal
        


users_list = []
possible_names = ["Andrei", "Maria", "Matei", "Elena", "Alex", "Ioana", "Stefan", "Anca"]

for i in range(10):
    
    name = random.choice(possible_names) + f"_{i}"
    
    x_rand = random.randint(-2000, 2000)
    y_rand = random.randint(-2000, 2000)
    
    
    users_list.append(User(name, x_rand, y_rand))


print("\n" + "="*40)
print("RAPORT SIMULARE MULTI-USER")
print("="*40)


# MacroCell: Antenă mare, acoperă kilometri (pusă în centrul orașului)
#macro = Antenna("MacroCell_Sector_A", x=0, y=0, power_dbm=25)
# mut macrocell la periferie ca userii sa aiba si alte antene de l acare sa prinda semnal
macro = Antenna("MacroCell_Sector_A", x=1500, y=1500, power_dbm=25)
# MicroCell: Acoperă o stradă sau o intersecție aglomerată
micro = Antenna("MicroCell_CityCenter", x=300, y=100, power_dbm=15)

# PicoCell: Acoperă interiorul unei clădiri (mall/universitate)
pico = Antenna("PicoCell_ETTI_Hall", x=50, y=50, power_dbm=5)

antennas_list=[macro,micro,pico]

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
    #cati utilizatori au semnal excelent, bun etc 

    print(f"-> {u.name:10} | Poz: ({u.x:4}, {u.y:4}) | Antena: {best_ant:20} | Semnal: {best_sig:.2f} dBm")

print("="*40)

print("\n--- FINAL NETWORK STATISTICS ---")
print(f"Excellent coverage: {excellent_count}")
print(f"Good coverage:      {good_count}")
print(f"Poor coverage:      {poor_count}")
print(f"Dead zones:         {dead_zone_count}")
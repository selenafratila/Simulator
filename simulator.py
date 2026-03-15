import numpy as np

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
        


#cream omul
user_nou=User("Selena",100,100)  
    
# MacroCell: Antenă mare, acoperă kilometri (pusă în centrul orașului)
macro = Antenna("MacroCell_Sector_A", x=0, y=0, power_dbm=46)

# MicroCell: Acoperă o stradă sau o intersecție aglomerată
micro = Antenna("MicroCell_CityCenter", x=300, y=100, power_dbm=33)

# PicoCell: Acoperă interiorul unei clădiri (mall/universitate)
pico = Antenna("PicoCell_ETTI_Hall", x=50, y=50, power_dbm=20)

antennas_list=[macro,micro,pico]

d=user_nou.calculate_distance_to_antenna(macro) 
print(f"Distanta calculata este: {d:.2f} metri")

# Calculăm semnalul de la antene pana la user_nou

s_macro = user_nou.get_signal_from_antenna(macro)
s_micro = user_nou.get_signal_from_antenna(micro)
s_pico= user_nou.get_signal_from_antenna(pico)

print(f"--- ANALIZĂ CONECTIVITATE ---")
print(f"Semnal de la {macro.antenna_type} (Macro): {s_macro:.2f} dBm")
print(f"Semnal de la {micro.antenna_type} (Macro): {s_micro:.2f} dBm")
print(f"Semnal de la {pico.antenna_type} (Pico): {s_pico:.2f} dBm")

name_best_antenna_for_user, best_power =user_nou.find_best_antenna(antennas_list)

print(f"Cea mai bună opțiune pentru {user_nou.name} este {name_best_antenna_for_user} cu {best_power:.2f} dBm")
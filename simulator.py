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

# MacroCell: Antenă mare, acoperă kilometri (pusă în centrul orașului)
macro = Antenna("MacroCell_Sector_A", x=0, y=0, power_dbm=46)

# MicroCell: Acoperă o stradă sau o intersecție aglomerată
micro = Antenna("MicroCell_CityCenter", x=300, y=100, power_dbm=33)

# PicoCell: Acoperă interiorul unei clădiri (mall/universitate)
pico = Antenna("PicoCell_ETTI_Hall", x=50, y=50, power_dbm=20)
# --- SIMULARE UTILIZATOR ---
# Utilizatorul este în holul facultății (aproape de PicoCell)
u_x, u_y = 52, 53

# Calculăm semnalul de la Macro (departe) vs Pico (foarte aproape)
d_macro = macro.get_distance(u_x, u_y)
s_macro = macro.calculate_signal(d_macro)

d_pico = pico.get_distance(u_x, u_y)
s_pico = pico.calculate_signal(d_pico)

print(f"--- ANALIZĂ CONECTIVITATE ---")
print(f"Semnal de la {macro.antenna_type} (Macro): {s_macro:.2f} dBm")
print(f"Semnal de la {pico.antenna_type} (Pico): {s_pico:.2f} dBm")

# Logica de selectare a celei mai bune antene
if s_pico > s_macro:
    print(f"\nTelefonul s-a conectat la {pico.antenna_type} (Semnal mai puternic)")
else:
    print(f"\nTelefonul rămâne conectat la {macro.antenna_type}")
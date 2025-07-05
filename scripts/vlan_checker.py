#!/usr/bin/env python3
"""
vlan_checker.py – Clasifica una VLAN como normal o extendida.
"""

NORMAL_MIN, NORMAL_MAX = 1, 1005
EXT_MIN, EXT_MAX       = 1006, 4094

def clasificar(vlan: int) -> str:
    if NORMAL_MIN <= vlan <= NORMAL_MAX:
        return "VLAN normal"
    elif EXT_MIN <= vlan <= EXT_MAX:
        return "VLAN extendida"
    else:
        return "¡Número fuera de rango (1-4094)!"

if __name__ == "__main__":
    while True:
        dato = input("Ingrese Nº VLAN (s para salir): ")
        if dato.lower() in {"s", "salir"}:
            break
        if dato.isdigit():
            print(clasificar(int(dato)))
        else:
            print("Debe ingresar un número.")

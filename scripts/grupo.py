#!/usr/bin/env python3
"""
grupo.py – Imprime los integrantes del grupo.
"""

INTEGRANTES = [
    "Manuel López",
    "Claudio Caro"
]

def mostrar_integrantes() -> None:
    print("Integrantes del grupo:")
    for persona in INTEGRANTES:
        print(f" • {persona}")
    print(f"\nTotal: {len(INTEGRANTES)} integrante(s)")

if __name__ == "__main__":
    mostrar_integrantes()

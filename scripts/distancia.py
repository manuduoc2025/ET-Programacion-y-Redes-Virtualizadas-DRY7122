#!/usr/bin/env python3
"""
distancia.py – GraphHopper con narrativa y sugerencias de pasajes

Medios disponibles:
 1. Auto
 2. Bicicleta
 3. Bus  (usa perfil 'car' en GraphHopper)

Salir: escribe S (o s) en cualquier prompt.

Dependencias:
    pip install requests
"""
import requests, sys

API_KEY = "3b30ee6b-9e79-4e0f-86fb-595a9cba352a"

# medio → (nombre, perfil GH, km/h aprox., emoji)
MEDIOS = {
    1: ("Auto",      "car",  80, "🚗"),
    2: ("Bicicleta", "bike", 18, "🚴"),
    3: ("Bus",       "car",  65, "🚌"),
}

# ----------- Funciones de utilidad ----------- #
def salir_si(texto: str):
    """Finaliza el programa si el usuario escribe S o s."""
    if texto.lower() == "s":
        sys.exit()

def get_coords(ciudad: str):
    """Obtiene coordenadas lat,lon desde GraphHopper Geocode."""
    url = "https://graphhopper.com/api/1/geocode"
    params = {"q": ciudad, "locale": "es", "key": API_KEY}
    data = requests.get(url, params=params).json()
    if data["hits"]:
        lat = data["hits"][0]["point"]["lat"]
        lon = data["hits"][0]["point"]["lng"]
        return f"{lat},{lon}"
    print(f"❌ No se encontró la ciudad: {ciudad}")
    return None

def obtener_datos(origen: str, destino: str,
                  perfil: str, medio_txt: str, vel_media: int, emoji: str):
    o_coord = get_coords(origen)
    d_coord = get_coords(destino)
    if not o_coord or not d_coord:
        return

    url = "https://graphhopper.com/api/1/route"
    params = {
        "point": [o_coord, d_coord],
        "vehicle": perfil,
        "locale": "es",
        "instructions": "true",
        "key": API_KEY,
    }
    data = requests.get(url, params=params).json()
    if "paths" not in data:
        print("❌ No se encontró una ruta válida.")
        return

    path      = data["paths"][0]
    dist_km   = path["distance"] / 1000
    dur_seg   = path["time"] / 1000
    litros    = dist_km / 12 if perfil == "car" and medio_txt == "Auto" else None

    print(f"\n{emoji}  {origen.title()} → {destino.title()} en {medio_txt.lower()}")
    print(f"Distancia: {dist_km:.2f} km")
    print(f"Duración : {int(dur_seg//3600)}h "
          f"{int((dur_seg%3600)//60)}m {int(dur_seg%60)}s")
    if litros is not None:
        print(f"Combustible estimado: {litros:.2f} L")

    print("\nNarrativa:")
    for paso in path["instructions"]:
        print("-", paso["text"])

    # ---------- Sugerencias de pasajes para BUS ---------- #
    if medio_txt == "Bus":
        print("\nDónde comprar pasaje de ida:")
        print(" • https://www.recorrido.cl")
        print(" • https://www.turbus.cl")
        print(" • https://www.andesmar.com (cruce internacional)")
        print(f" • Boleterías físicas en Terminal de {origen.title()}")

        print("\nDónde comprar el pasaje de regreso:")
        print(" • Mismos portales (elige ruta "
              f"{destino.title()} → {origen.title()})")
        print(f" • Boleterías en Terminal de Ómnibus de {destino.title()}")

# --------------- Programa principal --------------- #
print("Escribe 'S' para salir en cualquier momento.")

while True:
    origen = input("\nCiudad de Origen: ").strip()
    salir_si(origen)

    destino = input("Ciudad de Destino: ").strip()
    salir_si(destino)

    print("\nMedio de transporte:")
    for k, (nombre, _, _, emoji) in MEDIOS.items():
        print(f" {k}. {nombre} {emoji}")

    opcion_raw = input("Opción: ").strip()
    salir_si(opcion_raw)

    if not opcion_raw.isdigit() or int(opcion_raw) not in MEDIOS:
        print("❌ Selección inválida.")
        continue

    idx = int(opcion_raw)
    medio_txt, perfil, vel, emoji = MEDIOS[idx]
    obtener_datos(origen, destino, perfil, medio_txt, vel, emoji)

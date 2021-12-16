import json
from pyproj import Transformer
from math import sqrt

ADRESY = "adresy.geojson"
KONTEJNERY = "kontejnery.geojson"

def nacti_soubor(nazev):
    with open(nazev, "r", encoding="utf8") as infile:
        return json.load(infile)["features"]


kontejnery = nacti_soubor("kontejnery.geojson")

verejne_kont = []
for a in kontejnery:
    if a['properties']['PRISTUP'] == 'volně':
        verejne_kont.append(a)

"""print(type(verejne_kont))
print(len(verejne_kont))
print(verejne_kont)"""


def preved_souradnice(x,y):
    wgs2jtsk = Transformer.from_crs(4326,5514)
    return wgs2jtsk.transform(y,x)

def spocti_vzdalenost(x1,y1,x2,y2):
    return sqrt((x2-x1)**2 + (y2-y1)**2)

adresy = nacti_soubor("adresy.geojson")

#print(type(adresy))
#print(adresy)
MAX_VZDALENOST = 10000
vzdalenost_min = 100000
vzdalenost_max = 0
soucet_vzdalenosti = 0
vzdalenosti = []
for b in adresy:
    ulice = b["properties"]["addr:street"]
    cislo_popisne = b["properties"]["addr:housenumber"]    
    b["geometry"]["coordinates_jtsk"] = list(preved_souradnice(*b["geometry"]["coordinates"]))
    x1 = b["geometry"]["coordinates_jtsk"][0]
    y1 = b["geometry"]["coordinates_jtsk"][1]

    for c in verejne_kont:
        x2 = c["geometry"]["coordinates"][0]
        y2 = c["geometry"]["coordinates"][1]

        vzdalenost = spocti_vzdalenost(x1,y1,x2,y2)
        if vzdalenost < vzdalenost_min:
            vzdalenost_min = vzdalenost
    
    if vzdalenost_min > MAX_VZDALENOST:
        print(f"Z adresy {ulice} {cislo_popisne} je njebližší kontejner dále než 10 km.")
        quit()

    if vzdalenost_min > vzdalenost_max:
        vzdalenost_max = vzdalenost_min
        ulice_max = b["properties"]["addr:street"]
        cislo_max = b["properties"]["addr:housenumber"]

    soucet_vzdalenosti += vzdalenost_min
    vzdalenosti.append(vzdalenost_min)
    vzdalenost_min = 100000
    
avg_vzdalenost = soucet_vzdalenosti/len(vzdalenosti) 

print(f"Načteno celkem {len(vzdalenosti)} adresních bodů.")
print(f"Načteno celkem {len(verejne_kont)} veřejných kontejnerů na tříděný odpad.")
print()
print(f"Průměrná vzdálenost z adresního bodu k nejblžšímu kontejneru je {avg_vzdalenost:.0f} metrů.")
print(f"Maximální vzdálenost k nejbližšímu kontejneru je z adresy {ulice_max} {cislo_max}, a to {vzdalenost_max:.0f} metrů.")

        
    

    









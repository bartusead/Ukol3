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

print(type(verejne_kont))
print(len(verejne_kont))
print(verejne_kont)


def prevod_souradnic(x,y):
    wgs2jtsk = Transformer.from_crs(4326,5514)
    return wgs2jtsk.transform(x,y)

def vzdalenost(x1,y1,x2,y2):
    return sqrt((x2-x1)**2 + (y2-y1)**2)









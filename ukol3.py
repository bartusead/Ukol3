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

vzdalenost_min = 100000
soucet_vzdalenosti = 0
vzdalenosti = []
for b in adresy:
    id_adr = b["id"]
    
    b["geometry"]["coordinates_jtsk"] = list(preved_souradnice(*b["geometry"]["coordinates"]))
    x1 = b["geometry"]["coordinates_jtsk"][0]
    y1 = b["geometry"]["coordinates_jtsk"][1]
    #print(b["properties"]["addr:street"])
    for c in verejne_kont:
        x2 = c["geometry"]["coordinates"][0]
        y2 = c["geometry"]["coordinates"][1]
        #print(c["properties"]["STATIONNAME"])
        vzdalenost = spocti_vzdalenost(x1,y1,x2,y2)
        #print(vzdalenost)
        if vzdalenost < vzdalenost_min:
            vzdalenost_min = vzdalenost
    #print(vzdalenost_min)
    vzdalenosti.append(vzdalenost_min)
    vzdalenost_min = 100000


print(vzdalenosti)
        
    

    









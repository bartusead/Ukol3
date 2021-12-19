import json
from json.decoder import JSONDecodeError
from pyproj import Transformer
from math import sqrt
from statistics import median

#Stanovení konstant
ADRESY = "adresy.geojson"
KONTEJNERY = "kontejnery.geojson"
MAX_VZDALENOST = 10000

#Definice funkcí
def nacti_soubor(nazev):
    """Načte soubor s definovaným názvem jako JSON (GEOJSON),
    v případě problémů se souborem dojde k jedné z výjimek"""
    try:
        with open(nazev, "r", encoding="utf8") as infile:
            return json.load(infile)["features"]
    except FileNotFoundError:
        print(f"Soubor {nazev} neexistuje, nebo je chybně zadáno jeho umístění!")
        quit()
    except PermissionError:
        print(f"K otevření souboru {nazev} nemám patřičná oprávnění!")
        quit()
    except JSONDecodeError:
        print(f"Soubor {nazev} je neplatný (není platný JSON), prázdný, nebo chybí některý z parametrů!")
        quit()

def spocti_vzdalenost(x1,y1,x2,y2):
    """Spočítá vzdálenost mezi dvěma body pomocí Pythagorovy věty"""
    return sqrt((x2-x1)**2 + (y2-y1)**2)    

#Vytvoření seznamu veřejných kontejnerů
kontejnery = nacti_soubor("kontejnery.geojson")
verejne_kont = []
vsechny_kont = []
for kontejner in kontejnery:
    vsechny_kont.append(kontejner)
    if kontejner['properties']['PRISTUP'] == 'volně':
        verejne_kont.append(kontejner)

#Vytvoření seznamu minimálních vzdáleností
adresy = nacti_soubor("adresy.geojson")
wgs2jtsk = Transformer.from_crs(4326,5514)
vzdalenost_max = 0
soucet_vzdalenosti = 0
vzdalenosti = []
#Postupné stanovení souřadnic adresních bodů
for bod in adresy:
    vzdalenost_min = float('inf')
    ulice = bod["properties"]["addr:street"]
    cislo_popisne = bod["properties"]["addr:housenumber"]    
    try:
        bod["geometry"]["coordinates_jtsk"] = list(wgs2jtsk.transform(bod["geometry"]["coordinates"][1],bod["geometry"]["coordinates"][0]))
        x1 = bod["geometry"]["coordinates_jtsk"][0]
        y1 = bod["geometry"]["coordinates_jtsk"][1]
    except TypeError:
        print(f"Adresní bod {ulice} {cislo_popisne} postrádá jednu či obě souřadnice a proto ho program přeskočí!")
        continue

    #Postupné stanovení adres a souřadnic kontejnerů
    for misto in vsechny_kont:
        try:
            adresa_kont = bod["properties"]["addr:street"] + " " + bod["properties"]["addr:housenumber"]
            x2 = misto["geometry"]["coordinates"][0]
            y2 = misto["geometry"]["coordinates"][1]
        
            #Pokud je kontejner přístupný pouze obyvatelům domu a adresa kontejneru je shodná s adresou adresního bodu,
            # stanoví vzdálenost jako 0
            if misto['properties']['PRISTUP'] == 'obyvatelům domu' and misto['properties']['STATIONNAME'] == adresa_kont:
                vzdalenost = 0
            elif misto['properties']['PRISTUP'] == 'obyvatelům domu' and misto['properties']['STATIONNAME'] != adresa_kont:
                continue
            else:
                vzdalenost = spocti_vzdalenost(x1,y1,x2,y2)
        except ValueError:
            print(f"Kontejner na adrese {adresa_kont} postrádá jednu či obě souřadnice a proto ho program přeskočí!")
            continue
        except TypeError:
            print(f"Kontejner na adrese {adresa_kont} postrádá jednu či obě souřadnice a proto ho program přeskočí!")
            continue
        #Pokud je aktuální vzdálenost nižší než minimální vzdálenost, stanoví tuto vzdálenost jako minimální
        if vzdalenost < vzdalenost_min:
            vzdalenost_min = vzdalenost
    #Ošetření situace, kdy je minimální vzdálenost větší než 10 kilometrů
    if vzdalenost_min > MAX_VZDALENOST:
        print(f"Z adresy {ulice} {cislo_popisne} je njebližší kontejner dále než 10 km.")
        quit()

    #Pokud je minimální vzdálenost větší než maximální vzdálenost, stanoví tuto vzdálenost jako "maximální minimální vzdálenost"
    if vzdalenost_min > vzdalenost_max:
        vzdalenost_max = vzdalenost_min
        ulice_max = bod["properties"]["addr:street"]
        cislo_max = bod["properties"]["addr:housenumber"]

    soucet_vzdalenosti += vzdalenost_min
    vzdalenosti.append(vzdalenost_min)

#Konečné výpočty a výpisy do konzole
try:
    avg_vzdalenost = soucet_vzdalenosti/len(vzdalenosti) 
except ZeroDivisionError:
    print("Nebyla spočtena žádná minimální vzdálenost!")
    quit()
vzdalenosti_median = median(vzdalenosti)

print(f"Načteno celkem {len(vzdalenosti)} adresních bodů.")
print(f"Načteno celkem {len(vsechny_kont)} kontejnerů na tříděný odpad, z toho celkem {len(verejne_kont)} veřejných.")
print()
print(f"Průměrná vzdálenost z adresního bodu k nejblžšímu kontejneru je {avg_vzdalenost:.0f} metrů.")
print(f"Maximální vzdálenost k nejbližšímu kontejneru je z adresy {ulice_max} {cislo_max}, a to {vzdalenost_max:.0f} metrů.")
print(f"Medián vzdáleností k nejbližšímu kontejneru je {vzdalenosti_median} metrů. ")

        
    

    









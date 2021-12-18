# Úkol 3 - vzdálenost ke kontejnerům na tříděný odpad

Program má za úkol ze vstupních dat počítat průměrnou vzdálenost, medián a maximální vzdálenost od adresních bodů k nejbližšímu kontejneru na tříděný odpad.

**Vstupní data**

Jako vstupní data slouží 2 soubory ve formátu .GEOJSON, a to adresy.geojson a kontejnery.geojson. Soubor s adresami obsahuje vybrané adresní body, jejichž stěžejními parametry jsou ulice, číslo popisné a souřadnice v systému WGS-84. Soubor s kontejnery obsahuje hlavně vybrané kontejnery, jejich adresu a souřadnice v systému S-JTSK.

**Běh programu**

Na počátku jsou stanoveny konstanty (globální proměnné) a definovány funkce na načtení souboru a výpočet vzdálenosti mezi dvěma body. Následně jsou vytvořeny seznamy s veřejnými a všemi kontejnery (na konci programu se v konzoli zobrazí jejich délka, tedy počet veřejných kontejnerů a celkový počet všech kontejnerů). Následuje for cyklus, který nejprve vytahuje ulici, číslo popisné a souřadnice ze souboru s adresami a pro každý tento adresní bod v dalším vnořeném cyklu hledá nejbližší kontejner. Nutností je převedení souřadnic z WGS-84 do S-JTSK u souboru s kontejnery. Po nalezení nejbližšího kontejneru jeho vzdálenost od od adresního bodu uloží a přeskočí na další adresu. Pokud se ulice a číslo popisné u adresního bodu shoduje s kontejnerem, vzdálenost je automaticky stanovena na 0. Dále se v tomto cyklu kontroluje, jestli není nějaká z nejbližších vzdáleností větší než 10 km (v takovém případě program skončí s chybovou hláškou) a hledá se maximální nejbližší vzdálenost. Celý cyklus slouží především k vytvoření seznamu minimálních vzdáleností.

**Výstup**

Program nakonec spočítá a vypíše, kolik adres a kontejnerů bylo načteno (a kolik z kontejnerů je veřejně přístupných), průměrnou vzdálenost, medián a maximální vzdálenost (i s danou adresou) od adresních bodů k nejbližšímu kontejneru na tříděný odpad.

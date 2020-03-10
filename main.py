import shapefile as shp  # Requires the pyshp package
import matplotlib.pyplot as plt
from shapely.geometry import Polygon
import random
import matplotlib
import sys
import math

class Stadtteil:
    def __init__(self, shape):
        self.name = shape.record[0]
        self.flaeche = shape.record[3]
        self.x = [i[0] for i in shape.shape.points[:]]
        self.y = [i[1] for i in shape.shape.points[:]]
        self.geometry = Polygon( [ (i[0],i[1]) for i in shape.shape.points[:] ] )
        self.nachbarn = []
        self.infiziert = 0
        self.bevoelkerung = shape.record[4]
        if shape.record[4] == None:
            self.bevoelkerung = 0 
        self.infiziert_in_prozent = 0

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def draw(self,farbe):
        plt.fill(self.x,self.y, color=farbe)

    def drawGradient(self, value, min=0, max=100):
        '''
        Zeichnet diesen Stadtteil mit einem Farbverlauf.
        Minimalwert (weiß) des Verlaufs wird mit min gegeben, Maximalwert (rot) mit max.
        Der tatsächliche Wert in value.
        '''
        cmap = plt.cm.get_cmap("Reds")
        norm = matplotlib.colors.Normalize(vmin=min, vmax=max)
        self.draw(cmap(norm(value)))

    @staticmethod
    def findByName(stadtteile, name):
        ret = next((x for x in stadtteile if x.name == name), None)
        
        if ret == None:
            print("Stadtteil mit diesem Namen nicht gefunden! Gesucht:", name)
            raise ValueError("Stadtteil mit diesem Namen nicht gefunden! Gesucht:", name)

        return ret

def findNeighbours(stadtteile):
    for current in stadtteile:
        for other in stadtteile:
            if current.name == other.name: continue
            if current.geometry.intersects(other.geometry):
                # neighbour found
                current.nachbarn.append(other)
                # other.nachbarn.append(current)

def init():
    sf = shp.Reader("data/StadtteileBev.shp", encoding="ISO8859-1")
    stadtteile = []

    for shape in sf.shapeRecords():
        neu = Stadtteil(shape)
        neu.infiziert = math.floor(random.uniform(0,0.2)*neu.bevoelkerung)
        stadtteile.append(neu)
    findNeighbours(stadtteile)

    return stadtteile

def drawAll(stadtteile):
    for stadtteil in stadtteile:
        # if "Ottensen" in [i.name for i in stadtteil.nachbarn]:
        #     stadtteil.draw("green")
        # else:
        #     stadtteil.draw("red")
        # stadtteil.drawGradient(stadtteil.infiziert, 0, 15)
        stadtteil.draw("gray")

def aufgabe1(stadtteile):
    # Lektion 1: Variablendeklaration, Array-Zugriff, if-else Bedingung

    # Aufgabe 1: Färbe einen Stadtteil rot, wenn es dort Infektionen gibt, ansonsten grün.
    
    stadtteil = Stadtteil.findByName(stadtteile, "Ottensen")

    if stadtteil.infiziert == 0:
        stadtteil.draw("green")
    else:
        stadtteil.draw("red")

def aufgabe2(stadtteile):
    # Lektion 2: for-loop

    # Aufgabe 2.a): Berechne die prozentualen Anteile der infizierten Bevölkerungen des jeweiligen Stadtteils und runde das Ergebnis

    for stadtteil in stadtteile:
        if stadtteil.bevoelkerung == 0:
            stadtteil.infiziert_in_prozent = 0
        else:
            stadtteil.infiziert_in_prozent=100*stadtteil.infiziert/stadtteil.bevoelkerung
        
        print("In {} sind {:.2f}% infiziert".format(stadtteil.name, stadtteil.infiziert_in_prozent))

    # Aufgabe 2.b): Visualisiere ..... (verständlicher deutsche Text benötigt)

    for stadtteil in stadtteile:
        stadtteil.drawGradient(stadtteil.infiziert_in_prozent)
    
    

def aufgabe3(stadtteile):
    # Lektion 3: kombination for-loop and if else

    # Aufgabe 3: Die WHO definiert das Risikopotential eines Gebiets folgendermaßen: liegt der Anteil der infizierten Bevölkerung 
    #           bei über 80%, wird das entsprechende Gebiet als "hochgefährdet" eingestuft. Bei einem Infektionsanteil zwischen 30%
    #           und 80% spricht man von einem "mittleren Gefährdung". Sind unter 30% infiziert, besteht eine "geringe Gefährdung". 
    #           Bitte färbe die Stadtteile entsprechend ihrer Gefährdung: rot = "hoch", orange = "mittel", gelb = "gering". 
    #           Die Stadtteile ohne Infektionen färbe grün.

    grenze_hoch = 15
    grenze_mittel = 5
    
    for stadtteil in stadtteile:
        if stadtteil.infiziert_in_prozent > grenze_hoch:
            stadtteil.draw("red")
        elif stadtteil.infiziert_in_prozent > grenze_mittel & stadtteil.infiziert_in_prozent < grenze_hoch:
            stadtteil.draw("orange")
        elif stadtteil.infiziert_in_prozent < grenze_mittel & stadtteil.infiziert_in_prozent > 0:
            stadtteil.draw("yellow")
        else:
            stadtteil.draw("green")

def aufgabe4(stadtteile):
    # Lektion 4: für die Neugierige

    # Aufgabe 4.a): Finde heraus wie viele infizierte gibt es in deinem Stadtteil. Schreib die Wert in der Console. 
    #               Färbe den Stadtteil in deiner lieblingsfarbe und alle andere Stadtteile in grau.

    my_stadtteil = Stadtteil.findByName(stadtteile, "HafenCity")
    print("In meinem Stadtteil sind:" + str(my_stadtteil.infiziert) + " infiziert")
    for stadtteil in stadtteile:
        if stadtteil == my_stadtteil:
            stadtteil.draw("pink")
        else:
            stadtteil.draw("gray")

    
    # Aufgabe 4.b): Um deine Gesundheit zu schützen du möchtest die Chance eine infizierte Persone zu treffen minimieren. 
    #               Welcher benachbarte Stadtteil ist am gefährlichsten bzw. welche hat die größte Anzahl der Infizierten? 
    #               Schreib die Name und die Anzahl der Infizierten dieses Stadtteils in der Console. 
    
    max_infiziert=0
    
    for stadtteil in my_stadtteil.nachbarn:
        if stadtteil.infiziert >max_infiziert:
            max_infiziert=stadtteil.infiziert
            alert_nachbarn=stadtteil

    print("Die größte Gefahr besteht bei dem Nachbarn: " + alert_nachbarn.name)
    print("Dieser Nachbarn hat " +  str(alert_nachbarn.infiziert) + " Infizierte!")
            

if __name__ == "__main__":
    # stadtteil.name
    # stadtteil.infiziert

    stadtteile = init()
    plt.figure()
    drawAll(stadtteile)

    print(stadtteile)
    # print(stadtteile[5], ":", stadtteile[5].nachbarn)

    # aufgabe1(stadtteile)
    aufgabe2(stadtteile)
    # aufgabe3(stadtteile)
    # aufgabe4(stadtteile)

    plt.show()
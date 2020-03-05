import shapefile as shp  # Requires the pyshp package
import matplotlib.pyplot as plt
from shapely.geometry import Polygon
import random
import matplotlib

class Stadtteil:
    def __init__(self, shape):
        self.name = shape.record[0]
        self.flaeche = shape.record[3]
        self.x = [i[0] for i in shape.shape.points[:]]
        self.y = [i[1] for i in shape.shape.points[:]]
        self.geometry = Polygon( [ (i[0],i[1]) for i in shape.shape.points[:] ] )
        self.nachbarn = []
        self.infiziert = 0

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def draw(self,farbe):
        plt.fill(self.x,self.y, color=farbe)

    def drawGradient(self, value, min=0, max=15):
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
    sf = shp.Reader("data/Stadtteile.shp", encoding="ISO8859-1")
    stadtteile = []

    for shape in sf.shapeRecords():
        neu = Stadtteil(shape)
        neu.infiziert = random.randint(0,15)
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
    # Variablendeklaration, Array-Zugriff, if-else Bedingung
    
    stadtteil = Stadtteil.findByName(stadtteile, "Ottensen")

    if stadtteil.infiziert == 0:
        stadtteil.draw("green")
    else:
        stadtteil.draw("red")

def aufgabe2(stadtteile):
    # for-loop
    for stadtteil in stadtteile:
        stadtteil.drawGradient(stadtteil.infiziert)

def aufgabe3(stadtteile):
    # to be defined
    pass

if __name__ == "__main__":
    # stadtteil.name
    # stadtteil.infiziert

    stadtteile = init()
    plt.figure()
    drawAll(stadtteile)

    print(stadtteile)
    # print(stadtteile[5], ":", stadtteile[5].nachbarn)

    aufgabe1(stadtteile)
    aufgabe2(stadtteile)
    aufgabe3(stadtteile)

    plt.show()
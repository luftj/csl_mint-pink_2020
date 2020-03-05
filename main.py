import shapefile as shp  # Requires the pyshp package
import matplotlib.pyplot as plt
from shapely.geometry import Polygon

class Stadtteil:
    def __init__(self, shape):
        self.name = shape.record[0]
        self.flaeche = shape.record[3]
        self.x = [i[0] for i in shape.shape.points[:]]
        self.y = [i[1] for i in shape.shape.points[:]]
        self.geometry = Polygon( [ (i[0],i[1]) for i in shape.shape.points[:] ] )
        self.nachbarn = []

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def draw(self,farbe):
        plt.fill(self.x,self.y, farbe)

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
        stadtteile.append(Stadtteil(shape))
    findNeighbours(stadtteile)
    return stadtteile

def draw(stadtteile):
    plt.figure()
    for stadtteil in stadtteile:
        if stadtteil.flaeche > 7155840.27429999970:
            stadtteil.draw("green")
        else:
            stadtteil.draw("red")
    plt.show()

if __name__ == "__main__":
    # stadtteil.name
    # stadtteil.infizierte

    stadtteile = init()
    print(stadtteile)
    print(stadtteile[5], ":", stadtteile[5].nachbarn)
    draw(stadtteile)
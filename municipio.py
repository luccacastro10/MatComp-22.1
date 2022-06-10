import matplotlib.pyplot as plt

class municipio:
    def __init__(self, name, path):
        self.name = name
        self.dataPath = path
        self.points = []


    def loadPoints(self):
        file = open(self.dataPath, "r")
        lines = file.readlines()

        for line in lines:
            if line != "\n":
                point = []
                point.append(float(line.split(", ")[0]))
                point.append(float(line.split(", ")[1].split("\n")[0]))
                self.points.append(point)

    def generateGraph(self):

        if not len(self.points):
            self.loadPoints()

        x = []
        y = []
        
        for point in self.points:
            x.append(point[0])
            y.append(point[1])

        plt.scatter(x,y)
        plt.title(self.name)
        plt.show()
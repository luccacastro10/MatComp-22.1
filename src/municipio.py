import matplotlib.pyplot as plt

class municipio:
    def __init__(self, name, path):
        self.name = name
        self.dataPath = path
        self.points = []
        self.loadPoints()

    def loadPoints(self):
        file = open(self.dataPath, "r")
        lines = file.readlines()

        for line in lines:
            if line != "\n":
                point = []
                point.append(float(line.split(", ")[0]))
                point.append(float(line.split(", ")[1].split("\n")[0]))
                self.points.append(point)
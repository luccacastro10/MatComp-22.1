from municipio import municipio
from linearRegression import logisticRegression, plotLogistic
import matplotlib.pyplot as plt
from os import listdir

def main():

    for file in listdir("data"):
        countyName = file.split(".txt")[0]

        county = municipio(countyName, "data/" + countyName + ".txt")

        result = logisticRegression(county.points)
        plotLogistic(result, county)
        
        print("Resultado da regressao logistica: " + str(result) +"\n")

if __name__ == "__main__":
    main()




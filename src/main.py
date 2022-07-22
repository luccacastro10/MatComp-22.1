from municipio import municipio
from linearRegression import gradientDescent, logisticRegression, plotLogistic, getError, saveExcel
import matplotlib.pyplot as plt
from os import listdir

def main():

    for file in listdir("data"):
        cityName = file.split(".csv")[0]

        city = municipio(cityName, "data/" + cityName + ".csv")

        logisticRegression(city)
        gradientDescent(city)
        plotLogistic(city)
        
        print("-------------------------------------------------------------------------------------")
        print(cityName + ":" + str(city.logisticParameters) + " - Resultado da regressao linear\n")
        print(cityName + ":" + str(city.adjustedLogisticParameters) + " - Resultado da regressao linear ajustada\n")
        print(cityName + ":" + str(city.gradientParameters) + " - Resultado da descida de gradiente\n\n")


        getError(city)
        saveExcel(city)

if __name__ == "__main__":
    main()




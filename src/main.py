# Projeto Mat comp 
from municipio import municipio
from linearRegression import gradientDescent, logisticRegression, plotLogistic, getError, saveExcel
import matplotlib.pyplot as plt
from os import listdir

def main():

    for file in listdir("data"):
        cityName = file.split(".csv")[0]

        city = municipio(cityName, "data/" + cityName + ".csv")

        # gradientDescent(city)
        logisticRegression(city)
        plotLogistic(city)
        
        print("Resultado da regressao logistica - " + cityName + ":" + str(city.logisticParameters) +"\n")

        getError(city)
        saveExcel(city)

if __name__ == "__main__":
    main()




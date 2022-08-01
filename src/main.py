from municipio import municipio
from linearRegression import gradientDescent, logisticRegression, plotLogistic, getError

def main():

    cityName = "saopaulo"

    city = municipio(cityName, "data/" + cityName + ".csv")

    logisticRegression(city)
    gradientDescent(city)
    plotLogistic(city)
    
    print("-------------------------------------------------------------------------------------")
    print(city.name + ":" + str(city.logisticParameters) + " - Resultado da regressao linear\n")
    print(city.name + ":" + str(city.adjustedLogisticParameters) + " - Resultado da regressao linear ajustada\n")
    print(city.name + ":" + str(city.gradientParameters) + " - Resultado da descida de gradiente\n")
    print("Resultado do ajuste logistico para a cidade de " + city.name + " salvo na pasta results\n\n")

    getError(city)

if __name__ == "__main__":
    main()



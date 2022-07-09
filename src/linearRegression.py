import math
import numpy as np
import matplotlib.pyplot as plt
from openpyxl import Workbook

def leastSquares(points):

    n = len(points)
    
    xSum  = 0
    ySum  = 0
    x2Sum = 0
    xySum = 0

    for point in points:
        xSum  += point[0]
        ySum  += point[1]
        x2Sum += point[0]**2
        xySum += point[0]*point[1]

    m = ((n*xySum) - (xSum*ySum))/((n*x2Sum) - (xSum**2))
    n = (ySum - (m*xSum))/n

    return [m,n]

def logisticRegression(city):

    k = 0
    r = 0

    # P = (p0 * k) / (k - p0)*e^-rt + p0

    t = []
    p = []
    p1 = []     #p_t
    p2 = []     #p_t+1
    z = []

    for point in city.points:
        t.append(point[0])
        p.append(point[1])
    
    p1 = p[:(len(p)-1)]
    p2 = p[1:]
    p0 = p[0]

    print("\n\nt:"     + str(t))
    print("p0: " + str(p0) + "\n")
    print("p: "    + str(p) + "\n")
    print("pi: "   + str(p1))
    print("pi+1: " + str(p2) + "\n")

    firstRegression = []
    for i in range(len(p1)):
        point = []

        #x = P
        point.append(p1[i])

        #y = dp/dt * 1/p
        dpdt = (p2[i]-p1[i])/((t[i+1] - t[i])*p1[i])

        point.append(dpdt)

        firstRegression.append(point)

    firstResult = leastSquares(firstRegression)

    r = firstResult[1]
    k = (-1)*firstResult[1]/firstResult[0]

    city.logisticParameters = [p0,k,r]

    k   = p[8] + p[9]
    t_  = (t[8] + t[9])/2

    r = (1/t_)*math.log((k-p0)/p0)

    print("Valor de k encontrado: " + str(k))
    print("Valor de r encontrado: " + str(r))


    city.adjustedLogisticParameters = [p0,k,r]

def plotLogistic(city):

    figure, axis = plt.subplots(1, 2)

    p0 = city.logisticParameters[0]
    k = city.logisticParameters[1]
    r = city.logisticParameters[2]

    i = 0

    for i in range(2):

        x = np.linspace(city.points[0][0], city.points[-1][0],1000)
        y = (p0*k)/((k-p0)*np.exp((-1)*r*x) + p0)


        if not len(city.points):
            city.loadPoints()

        x2 = []
        y2 = []

        for point in city.points:
            x2.append(point[0])
            y2.append(point[1])

        axis[i].set_title("Logistic Regression: " + city.name)
        axis[i].scatter(x2,y2)
        axis[i].plot(x,y, 'g')

        p0  = city.adjustedLogisticParameters[0]
        k   = city.adjustedLogisticParameters[1]
        r   = city.adjustedLogisticParameters[2]

        i += 1

    plt.gcf().set_size_inches(8, 5)
    # plt.show()

    plt.savefig(fname="results/images/logisticRegression_" + city.name + ".jpg")


def getError(city):

    p0 = city.logisticParameters[0]
    k = city.logisticParameters[1]
    r = city.logisticParameters[2]

    for i in range(len(city.points)):

        t = city.points[i][0]
        realValue = city.points[i][1]

        y = (p0*k)/((k-p0)*np.exp((-1)*r*city.points[i][0]) + p0)

        error = abs( y - realValue)/realValue

        city.logisticResult.append(y)
        city.logisticError.append(error)

    p0 = city.adjustedLogisticParameters[0]
    k = city.adjustedLogisticParameters[1]
    r = city.adjustedLogisticParameters[2]

    for i in range(len(city.points)):

        t = city.points[i][0]
        realValue = city.points[i][1]

        y = (p0*k)/((k-p0)*np.exp((-1)*r*city.points[i][0]) + p0)

        error = abs( y - realValue)/realValue

        city.adjustedLogisticResult.append(y)
        city.adjustedLogisticError.append(error)

def gradientDescent(city):
    
    # P = (p0 * k) / (k - p0)*e^-rt + p0

    p0 = city.points[0][1]
    k = 300000000
    r = 1

    limitStepSize = 0.01
    learningRate = 0.01

    setpSize_ddk = 0
    setpSize_ddr = 0

    iterations = 0

    while True:

        ddkFx = 0
        ddrFx = 0
        
        for point in city.points:

            exp = np.exp((-1)*r*point[0])
            print("exp: " + str(exp))
            den = (exp*(k-p0) + p0 )**2
            print("den: " + str(den))

            fx = (p0*k)/((k-p0)*exp + p0)

            firstTerm = (-2)*(point[1]-fx)

            ddkFx += firstTerm*((p0*((-1)*p0*exp + p0))/den)
            ddrFx += firstTerm*((p0*k*exp*point[0]*(k-p0))/den)

        setpSize_ddk = ddkFx * learningRate
        setpSize_ddr = ddrFx * learningRate

        iterations += 1 

        print("ddr: " + str(ddrFx))

        print("setpSize_ddk: " + str(setpSize_ddk))
        print("setpSize_ddr: " + str(setpSize_ddr))

        k = k - setpSize_ddk
        r = r - setpSize_ddr
        
        # if iterations >= 2:
        #     break

        if ( (abs(setpSize_ddk) < limitStepSize) and (abs(setpSize_ddr) < limitStepSize) ):
            print("ENTROU NO ELSE!!!!")
            break

    print(p0)
    print(k)
    print(r)

    city.logisticParameters = [p0,k,r]

def saveExcel(city):
  
    workbook = Workbook()
    
    sheet = workbook.active 

    c1 = sheet.cell(row = 1, column = 1)   
    c1.value = "Ano"
    
    c2 = sheet.cell(row= 1 , column = 2) 
    c2.value = "Valor Real"

    c3 = sheet.cell(row= 1 , column = 3) 
    c3.value = "Logístico"

    c4 = sheet.cell(row= 1 , column = 4) 
    c4.value = "Logístico Ajustado"

    c5 = sheet.cell(row= 1 , column = 5) 
    c5.value = "Erro Logístico"

    c6 = sheet.cell(row= 1 , column = 6) 
    c6.value = "Erro Logístico Ajustado"

    for i in range(len(city.points)):
        c = sheet.cell(row = 2 + i, column = 1)
        c.value = city.points[i][0]

    for i in range(len(city.points)):
        c = sheet.cell(row = 2 + i, column = 2)
        c.value = city.points[i][1]

    for i in range(len(city.logisticResult)):
        c = sheet.cell(row = 2 + i, column = 3)
        c.value = city.logisticResult[i]

    for i in range(len(city.logisticResult)):
        c = sheet.cell(row = 2 + i, column = 4)
        c.value = city.adjustedLogisticResult[i]

    for i in range(len(city.logisticError)):
        c = sheet.cell(row = 2 + i, column = 5)
        c.value = city.logisticError[i]

    for i in range(len(city.logisticError)):
        c = sheet.cell(row = 2 + i, column = 6)
        c.value = city.adjustedLogisticError[i]


    workbook.save(filename="results/tables/logisticRegression_" + city.name + ".xlsx")

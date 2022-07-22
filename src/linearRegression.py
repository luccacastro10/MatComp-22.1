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


    city.adjustedLogisticParameters = [p0,k,r]

def plotLogistic(city):

    figure, axis = plt.subplots(1, 3)

    methods = [city.logisticParameters, city.adjustedLogisticParameters, city.gradientParameters]
    methodsNames = ["Linear Regression: ", "Linear Regression + Adjust: ", "Gradient Descent: "]

    i = 0

    for i in range(3):

        p0 = methods[i][0]
        k = methods[i][1]
        r = methods[i][2]
        x = np.linspace(city.points[0][0], city.points[-1][0],1000)
        y = (p0*k)/((k-p0)*np.exp((-1)*r*x) + p0)


        if not len(city.points):
            city.loadPoints()

        x2 = []
        y2 = []

        for point in city.points:
            x2.append(point[0])
            y2.append(point[1])

        axis[i].set_title(methodsNames[i] + city.name)
        axis[i].scatter(x2,y2)
        axis[i].plot(x,y, 'g')


        i += 1

    plt.gcf().set_size_inches(16, 5)
    # plt.show()

    plt.savefig(fname="results/images/logisticRegression_" + city.name + ".jpg")


def getError(city):

    parametersList = [city.logisticParameters, city.adjustedLogisticParameters, city.gradientParameters]
    resultList     = [city.logisticResult, city.adjustedLogisticResult, city.gradientResult] 
    errorList      = [city.logisticError, city.adjustedLogisticError, city.gradientError]

    for j in range(len(parametersList)):
        p0 = parametersList[j][0]
        k = parametersList[j][1]
        r = parametersList[j][2]

        for i in range(len(city.points)):
            t = city.points[i][0]
            realValue = city.points[i][1]

            y = (p0*k)/((k-p0)*np.exp((-1)*r*city.points[i][0]) + p0)

            error = abs( y - realValue)/realValue

            resultList[j].append(y)
            errorList[j].append(error)

def gradientDescent(city):
    
    # P = (p0 * k) / (k - p0)*e^-rt + p0

    p0 = city.points[0][1]
    k = 2000000
    r = 0.01

    limitStepSize = 0.00001
    learningRate = 0.1

    iterations = 0

    while True:

        kGradient = 0
        rGradient = 0
        
        #Calculando os gradientes
        for point in city.points:

            exp = np.exp((-1)*r*point[0])

            estimatedY = (p0*k)/((k-p0)*exp + p0)
            
            kGradient += (point[1] - estimatedY)*((p0*((-1)*exp*p0))/((exp*(k-p0)+p0)**2))
            rGradient += (point[1] - estimatedY)*(((k-p0)*k*exp*p0*point[0])/((exp*(k-p0)+p0)**2))
        
        kGradient = (-2)*kGradient/len(city.points)
        rGradient = (-2)*rGradient/len(city.points)

        setpSize_k = kGradient * learningRate
        setpSize_r = rGradient * learningRate

        iterations += 1 

        k = k - setpSize_k
        r = abs(r - setpSize_r)

        if ( (abs(setpSize_k) < limitStepSize) and (abs(setpSize_r) < limitStepSize) ):
            break

    r = r/10**(len(str(int(r)))+1)

    t=[]
    p=[]
    for point in city.points:
        t.append(point[0])
        p.append(point[1])
    
    k   = p[8] + p[9]
    t_  = (t[8] + t[9])/2

    r = (1/t_)*math.log((k-p0)/p0)
    
    city.gradientParameters = [p0,k,r]

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
    c5.value = "Descida de Gradiente"

    c6 = sheet.cell(row= 1 , column = 6) 
    c6.value = "Erro Logístico"

    c7 = sheet.cell(row= 1 , column = 7) 
    c7.value = "Erro Logístico Ajustado"

    c8 = sheet.cell(row= 1 , column = 8) 
    c8.value = "Erro Descida de Gradiente"

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

    for i in range(len(city.logisticResult)):
        c = sheet.cell(row = 2 + i, column = 5)
        c.value = city.gradientResult[i]

    for i in range(len(city.logisticError)):
        c = sheet.cell(row = 2 + i, column = 6)
        c.value = city.logisticError[i]

    for i in range(len(city.logisticError)):
        c = sheet.cell(row = 2 + i, column = 7)
        c.value = city.adjustedLogisticError[i]

    for i in range(len(city.logisticError)):
        c = sheet.cell(row = 2 + i, column = 8)
        c.value = city.gradientError[i]


    workbook.save(filename="results/tables/logisticRegression_" + city.name + ".xlsx")

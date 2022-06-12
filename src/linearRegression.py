import math
import numpy as np
import matplotlib.pyplot as plt

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

def logisticRegression(points):
    a = 0
    b = 0
    c = 0

    t = []
    p = []
    p1 = []     #p_t
    p2 = []     #p_t+1
    z = []

    for point in points:
        t.append(point[0])
        p.append(point[1])
    
    p1 = p[:(len(p)-1)]
    p2 = p[1:]

    # print("\n\nt:"     + str(t))
    # print("p: "    + str(p) + "\n")
    # print("pi: "   + str(p1))
    # print("pi+1: " + str(p2) + "\n")

    firstRegression = []
    for i in range(len(p1)):
        point = []
        point.append(p1[i])
        point.append(p2[i])
        firstRegression.append(point)

    # print("first: " + str(firstRegression) + "\n")
    firstResult = leastSquares(firstRegression)

    # print("m: " + str(firstResult[0]))
    # print("n: " + str(firstResult[1]) + "\n")

    a = (firstResult[1]/(1-firstResult[0]))

    # print("a: " + str(a))

    for pt in p1:
        z.append(math.log(abs(pt/a)) - math.log(abs(1-pt/a)))

    # print("z: " + str(z) +"\n")

    secondRegression = []
    for i in range(len(p1)):
        point = []
        point.append(t[i])
        point.append(z[i])
        secondRegression.append(point)

    # print("second: " + str(secondRegression) + "\n")

    secondResult = leastSquares(secondRegression)

    # print("m: " + str(secondResult[0]))
    # print("n: " + str(secondResult[1]) + "\n")

    c = secondResult[0]
    b = a/points[0][1] - 1

    return [a,b,c]

def plotLogistic(parameters, city):

    x = np.linspace(city.points[0][0], city.points[-1][0],1000)
    y = parameters[0]/(parameters[1]*np.exp((-1)*parameters[2]*x) + 1)


    if not len(city.points):
        city.loadPoints()

    x2 = []
    y2 = []
    
    for point in city.points:
        x2.append(point[0])
        y2.append(point[1])

    plt.title("Logistic Regression: " + city.name)
    plt.scatter(x2,y2)
    plt.plot(x,y, 'g')
    plt.show()

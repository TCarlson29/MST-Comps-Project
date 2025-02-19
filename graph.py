import math, random
import csv, sys
from time import process_time
import ant

import matplotlib.pyplot as plt
import numpy as np


##NOTE: PROGRAM needs one argument for which experiment to run. Options:
##    - "Opt/It": Optimality over iterations
##    - "Opt/Time": Optimality over time (processing time?)
##        - change x axis so they all have same amount of time not same number of iterations

#Future additions: alpha/beta ratios vs optimality


#returns the highest end-value list (used for graphing with variable data lengths)
def maxlen(arg1, arg2, arg3):
  if arg1[-1] >= arg2[-1]:
    if arg1[-1] >= arg3[-1]:
      return arg1  
    return arg3
  if arg2[-1] >= arg3[-1]:
    return arg2
  return arg3


def main():
  ratios = []
  n = len(sys.argv)
  if (n == 4):
    print("Custom run initiated")
    print("Alpha value: " + sys.argv[2])
    print("Beta value: " + sys.argv[3])
    ratios = [int(sys.argv[2]), int(sys.argv[3])]

  nodes = []
  edges = []
  with open('full-mst-data.csv', mode ='r')as file:
    csvFile = csv.reader(file)
    x = 0
    for lines in csvFile:
      if x == 0:
        x +=1
      else:
        nodes.append(lines[0])
        row = list(map(int, lines[1::]))
        edges.append(row)
  phers = [[1] * len(edges)] * len(edges)
  print("Begin program")


  if (sys.argv[1] == "Opt/It"):
    numIterations = 200
    
    vals = ant.runAnt(nodes, edges, phers, ratios)
    print("Optimal: " + str(ant.truePrims(nodes, edges)))
    print("Number of iterations: " + str(numIterations))

      #GRAPHING OPT/ITs
    xpoints = np.array(list(range(numIterations)))
    brodPoints = np.array(vals[0])
    kruskPoints = np.array(vals[1])
    primPoints = np.array(vals[2])
    optPoints = np.array([vals[4]] * numIterations)

    plt.xlabel("Num iterations")
    plt.ylabel("Total Tree Weight")

    plt.plot(xpoints, brodPoints, label="broder")
    plt.plot(xpoints, kruskPoints, label="kruskals")
    plt.plot(xpoints, primPoints, label="prims")
    plt.plot(xpoints, optPoints, label="optimal")

    plt.legend(loc="upper right")
    plt.show()

    #vals = [[broderOpts, kruskalOpts, primOpts, curOptimal], deleteWeight, [broderTime, primTime, kruskalTime]]

    #GRAPHING
    xpoints = np.array(list(range(numIterations)))
    brodPoints = np.array(vals[0])
    kruskPoints = np.array(vals[1])
    primPoints = np.array(vals[2])
    optPoints = np.array([vals[4]] * numIterations)

    plt.plot(xpoints, brodPoints)
    plt.plot(xpoints, kruskPoints)
    plt.plot(xpoints, primPoints)
    plt.plot(xpoints, optPoints)
    plt.show()
  
  elif (sys.argv[1] == "Opt/Time"):
    amtTime = 30
    vals = ant.runAnt(nodes, edges, phers, ratios, True)
    print("Optimal: " + str(ant.truePrims(nodes, edges)))
    print("Amount of processor time: " + str(amtTime))

    #vals = [[broderOpts, kruskalOpts, primOpts, curOptimal], deleteWeight, [broderTime, kruskalTime, primTime]]

    #GRAPHING OPT/TIME
    XbrodTime = np.array(vals[2][0])
    print(XbrodTime)
    print(len(XbrodTime))
    brodPoints = np.array(vals[0][0])
    XkruskTime = np.array(vals[2][1])
    kruskPoints = np.array(vals[0][1])
    XprimTime = np.array(vals[2][2])
    primPoints = np.array(vals[0][2])
    optPoints = np.array([vals[0][3]] * amtTime)

    plt.xlabel("Processor Time (s)")
    plt.ylabel("Total Tree Weight")

    plt.plot(XbrodTime, brodPoints, label="broders")
    plt.plot(XkruskTime, kruskPoints, label="kruskals")
    plt.plot(XprimTime, primPoints, label="prims")
    plt.plot(range(0, 30), optPoints, label="Optimal")

    plt.legend(loc="upper right")
    plt.show()


  #TODO
  # Change data lists to be algorithm-specific
  elif (sys.argv[1] == "Opt/AB"):

    # data_1 = np.random.normal(100, 10, 200)
    # data_2 = np.random.normal(90, 20, 200)
    # data_3 = np.random.normal(80, 30, 200)
    # data_4 = np.random.normal(70, 40, 200)
    # data = [data_1, data_2, data_3, data_4]

    # fig = plt.figure(figsize =(10, 7))

    # # Creating axes instance
    # ax = fig.add_axes([0, 0, 1, 1])

    # # Creating plot
    # bp = ax.boxplot(data)

    # # show plot
    # plt.show()

    ratios = [0, 1]
    data1 = ant.runAnt(nodes, edges, phers, ratios)
    ratios = [1, 5]
    data2 = ant.runAnt(nodes, edges, phers, ratios)
    ratios = [1, 2]
    data3 = ant.runAnt(nodes, edges, phers, ratios)
    ratios = [1, 1]
    data4 = ant.runAnt(nodes, edges, phers, ratios)
    ratios = [2, 1]
    data5 = ant.runAnt(nodes, edges, phers, ratios)
    ratios = [5, 1]
    data6 = ant.runAnt(nodes, edges, phers, ratios)
    ratios = [1, 0]
    data7 = ant.runAnt(nodes, edges, phers, ratios)
    data = [data1, data2, data3, data4, data5, data6, data7]
    print("Optimal: " + str(ant.truePrims(nodes, edges)))
    print("Amount of processor time: " + str(amtTime))

    #vals = [[broderOpts, kruskalOpts, primOpts, curOptimal], deleteWeight, [broderTime, kruskalTime, primTime]]

    plt.xlabel("Alpha/Beta Weights (s)")
    plt.ylabel("Total Tree Weight")

    fig = plt.figure(figsize =(10, 7))
    ax = fig.add_axes([0, 0, 1, 1]) #Don't know what this does
    bp = ax.boxplot(data)

    plt.legend(loc="upper right")
    plt.show()

  else:
    print("Invalid experimental type. Try again")

if __name__ == "__main__":
  main()
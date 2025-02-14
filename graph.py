import math, random
import csv, sys
from time import process_time
import ant

import matplotlib.pyplot as plt
import numpy as np


##NOTE: PROGRAM needs one argument for which experiment to run. Options:
##    - "Opt/It": Optimality over iterations
##    - "Opt/Time": Optimality over time (processing time?)

#Future additions: alpha/beta ratios vs optimality


def maxlen(arg1, arg2, arg3):
  if len(arg1) >= len(arg2):
    if len(arg1) >= len(arg3):
      return arg1
    return arg3
  if len(arg2) >= len(arg3):
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
    vals = ant.runAnt(numIterations, nodes, edges, phers, ratios)
    print("Optimal: " + str(ant.truePrims(nodes, edges)))
    print("Number of iterations: " + str(numIterations))

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
  

  ## TODO
  ## NEEDS TESTING
  elif (sys.argv[1] == "Opt/Time"):
    numIterations = 200
    vals = ant.runAnt(numIterations, nodes, edges, phers, ratios)
    print("Optimal: " + str(ant.truePrims(nodes, edges)))
    print("Number of iterations: " + str(numIterations))

    #vals = [[broderOpts, kruskalOpts, primOpts, curOptimal], deleteWeight, [broderTime, kruskalTime, primTime]]

    #GRAPHING
    XbrodTime = np.array(vals[2][0])
    brodPoints = np.array(vals[0][0])
    XkruskTime = np.array(vals[2][1])
    kruskPoints = np.array(vals[0][1])
    XprimTime = np.array(vals[2][2])
    primPoints = np.array(vals[0][2])
    optPoints = np.array([vals[0][3]] * numIterations)

    plt.plot(XbrodTime, brodPoints)
    plt.plot(XkruskTime, kruskPoints)
    plt.plot(XprimTime, primPoints)
    plt.plot(maxlen(XbrodTime, XkruskTime, XprimTime), optPoints)
    plt.show()


  numIterations = 200
  vals = ant.runAnt(numIterations, nodes, edges, phers, ratios)
  print("Optimal: " + str(ant.truePrims(nodes, edges)))
  print("Number of iterations: " + str(numIterations))

  #vals = [broderOpts, kruskalOpts, primOpts, deleteWeight, curOptimal]
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

if __name__ == "__main__":
  main()
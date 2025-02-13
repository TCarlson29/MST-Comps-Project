import math, random
import csv, sys
from time import process_time
import ant

import matplotlib.pyplot as plt
import numpy as np


def main():
  ratios = []
  n = len(sys.argv)
  if (n == 3):
    print("Custom run initiated")
    print("Alpha value: " + sys.argv[1])
    print("Beta value: " + sys.argv[2])
    ratios = [int(sys.argv[1]), int(sys.argv[2])]

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
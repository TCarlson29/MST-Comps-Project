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
#not currently using?
def maxlen(arg1, arg2, arg3):
  if arg1[-1] >= arg2[-1]:
    if arg1[-1] >= arg3[-1]:
      return arg1  
    return arg3
  if arg2[-1] >= arg3[-1]:
    return arg2
  return arg3


def timed(nodes, edges, phers, ratios):
  amtTime = 31
  vals = ant.runAnt(nodes, edges, phers, ratios, True)
  print("Optimal: " + str(ant.truePrims(nodes, edges)))
  print("Amount of processor time: " + str(amtTime))

  #vals = [[broderOpts, kruskalOpts, primOpts, curOptimal], deleteWeight, [broderTime, kruskalTime, primTime]]

  #GRAPHING OPT/TIME
  XbrodTime = np.array(vals[2][0])
  # print(XbrodTime)
  # print(len(XbrodTime))
  brodPoints = np.array(vals[0][0])
  XkruskTime = np.array(vals[2][1])
  kruskPoints = np.array(vals[0][1])
  XprimTime = np.array(vals[2][2])
  primPoints = np.array(vals[0][2])
  optPoints = np.array([vals[0][3]] * amtTime)

  return [XbrodTime, brodPoints, XkruskTime, kruskPoints, XprimTime, primPoints, optPoints]

def iterations(nodes, edges, phers, ratios):
  numIterations = 200
    
  vals = ant.runAnt(nodes, edges, phers, ratios, False)
  print("Optimal: " + str(ant.truePrims(nodes, edges)))
  print("Number of iterations: " + str(numIterations))

  xpoints = np.array(range(0, numIterations))
  brodPoints = np.array(vals[0][0])
  kruskPoints = np.array(vals[0][1])
  primPoints = np.array(vals[0][2])
  optPoints = np.array([vals[0][3]] * numIterations)

  return [xpoints, brodPoints, kruskPoints, primPoints, optPoints]

  #vals = [[broderOpts, kruskalOpts, primOpts, curOptimal], deleteWeight, [broderTime, primTime, kruskalTime]]

def alphaBeta(nodes, edges, phers):

  ratios = [[0,1], [1,2], [1,1], [2,1], [1,0]]

  # ratios = [0, 1]
  # data1K = ant.calcWeight(ant.kruskalUpdate(nodes, edges, phers, ratios, False), edges)
  # ratios = [1, 2]
  # data3K = ant.calcWeight(ant.kruskalUpdate(nodes, edges, phers, ratios, False), edges)
  # ratios = [1, 1]
  # data4K = ant.calcWeight(ant.kruskalUpdate(nodes, edges, phers, ratios, False), edges)
  # ratios = [2, 1]
  # data5K = ant.calcWeight(ant.kruskalUpdate(nodes, edges, phers, ratios, False), edges)
  # ratios = [1, 0]
  # data7K = ant.calcWeight(ant.kruskalUpdate(nodes, edges, phers, ratios, False), edges)
  dataK = []
  dataP = []
  for ratio in ratios:
    dataK.append(ant.calcWeight(ant.kruskalUpdate(nodes, edges, phers, ratio, False), edges))
    dataP.append(ant.calcWeight(ant.primUpdate(nodes, edges, phers, ratio, False), edges))

  totalData = [dataK, dataP]
  print("Optimal: " + str(ant.truePrims(nodes, edges)))
  # print("Amount of processor time: " + str(amtTime))

  #data = [[broderOpts, kruskalOpts, primOpts, curOptimal], deleteWeight, [broderTime, kruskalTime, primTime]]

  return totalData


def graphFile(fileName):
  with open(fileName, mode ='r')as file:
    csvFile = csv.reader(file)
    runType = None
    for line in csvFile:
      if runType:
        data = line[0]
      else:
        runType = line[0]
      # print(line)
  ##TODO
  # this is a string type???? convert out of it
  print(type(data))
  for i in data:
    i = i.tolist()
  print(data)
  if runType == "Opt/It":
    graphIt(data)
  elif runType == "Opt/Time":
    graphTime(data)
  elif runType == "Opt/AB":
    graphRatios(data)
  else:
    print("Erorr: invalid file structure.")
    exit()
  # print("Begin program")


def graphTime(data):
  plt.xlabel("Processor Time (s)")
  plt.ylabel("Total Tree Weight")

  plt.plot(data[0], data[1], label="broders")
  plt.plot(data[2], data[3], label="kruskals")
  plt.plot(data[4], data[5], label="prims")
  plt.plot(range(0, 31), data[6], label="Optimal")

  plt.legend(loc="upper right")
  plt.show()

def graphIt(data):
  plt.xlabel("Num iterations")
  plt.ylabel("Total Tree Weight")

  plt.plot(data[0], data[1], label="broder")
  plt.plot(data[0], data[2], label="kruskals")
  plt.plot(data[0], data[3], label="prims")
  plt.plot(data[0], data[4], label="optimal")

  plt.legend(loc="upper right")
  plt.show()

def graphRatios(data):
  fig = plt.figure(figsize =(10, 7))
  ax = fig.add_subplot(111)
  # ax = fig.add_axes([0, 0, 1, 1]) #Don't know what this does
  bp = ax.boxplot(data)

  ax.set_xticklabels(["Kruskal's", "Prim's"])
  plt.xlabel("Alpha/Beta Weights (s)")
  plt.ylabel("Total Tree Weight")
  plt.legend(loc="upper right")
  plt.show()


def main():
  ratios = []
  n = len(sys.argv)
  # if (n == 4):
  #   print("Custom run initiated")
  #   print("Alpha value: " + sys.argv[2])
  #   print("Beta value: " + sys.argv[3])
  #   ratios = [int(sys.argv[2]), int(sys.argv[3])]

  if (sys.argv[1] == "graphFile"):
    graphFile(sys.argv[2])
    exit()
  
  nodes = []
  edges = []
  with open('./filter/filtered_EMCI_matrices/filtered_Patient1_connectivity_matrix.csv', mode ='r')as file:
    csvFile = csv.reader(file)
    x = 0
    for lines in csvFile:
      if x == 0:
        x +=1
      else:
        nodes.append(lines[0])
        row = []
        for edge in lines[1::]:
          row.append(1 - abs(float(edge)))
        edges.append(row)
  phers = [[1] * len(edges)] * len(edges)
  print("Begin program")


  data = []
  if (sys.argv[1] == "Opt/It"):
    #return [xpoints, brodPoints, kruskPoints, primPoints, optPoints]
    data = iterations(nodes, edges, phers, ratios)
    graphIt(data)

  elif (sys.argv[1] == "Opt/Time"):
    #return [XbrodTime, brodPoints, XkruskTime, kruskPoints, XprimTime, primPoints, optPoints]
    data = timed(nodes, edges, phers, ratios)
    graphTime(data)

  elif (sys.argv[1] == "Opt/AB"):
    # return [dataK, dataP]
    data = alphaBeta(nodes, edges, phers)
    graphRatios(data)

  else:
    print("Error: Invalid experimental type. Try again")
    exit()

  myFile = csv.writer(open("curData.csv", "w"))
  myFile.writerow([sys.argv[1]])
  for dat in data:
    myFile.writerow([dat])





if __name__ == "__main__":
  main()
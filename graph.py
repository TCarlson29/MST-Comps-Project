import math, random
import csv, sys
from time import process_time
import ant

import matplotlib.pyplot as plt
import numpy as np

numIterations = 200
amtTime = 31
ratios = [[0,1], [1,2], [1,1], [2,1], [1,0]]

##NOTE: PROGRAM needs one argument for which experiment to run. Options:
##    - "Opt/It": Optimality over iterations
##    - "Opt/Time": Optimality over time (processing time?)
##        - change x axis so they all have same amount of time not same number of iterations

#Future additions: alpha/beta ratios vs optimality



def saveData(data, fileName):
  myFile = csv.writer(open(fileName, "w"))
  myFile.writerow([sys.argv[1]])
  if (sys.argv[1] == "Opt/It"):
    myFile.writerow([numIterations])
  elif (sys.argv[1] == "Opt/Time"):
    myFile.writerow([amtTime])
  elif (sys.argv[1] == "Opt/AB"):
    myFile.writerow(ratios)
    for dat in data:
      myFile.writerows(dat)
    return

  # print(data)
  for dat in data: 
    for d in dat:
      myFile.writerows(d)

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
  
  vals = ant.runAnt(nodes, edges, phers, ratios, True, numIterations, amtTime)
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
  # numIterations = 200
    
  vals = ant.runAnt(nodes, edges, phers, ratios, False, numIterations, amtTime)
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
  dataB = []
  dataK = []
  dataP = []
  for ratio in ratios:
    dataB.append(ant.calcWeight(ant.broderUpdate(nodes, edges, phers, ratio, False, numIterations, amtTime), edges))
    dataK.append(ant.calcWeight(ant.kruskalUpdate(nodes, edges, phers, ratio, False, numIterations, amtTime), edges))
    dataP.append(ant.calcWeight(ant.primUpdate(nodes, edges, phers, ratio, False, numIterations, amtTime), edges))

  totalData = [dataB, dataK, dataP]
  print("Optimal: " + str(ant.truePrims(nodes, edges)))

  return totalData


def graphFile(fileName):
  data = []
  num = 0
  maxNum = 0
  with open(fileName, mode ='r')as file:
    csvFile = csv.reader(file)
    runType = None
    runLength = None
    newData = []
    for line in csvFile:
      if runType and runLength:
        newData.append(list(map(float, line)))
        num += 1
        if num == maxNum:
          num = 0
          data.append(newData)
          newData = []
        
      else:
        if runType:
          runLength = line[0]
          continue
        runType = line[0]
        if runType == "Opt/It":
          maxNum = 5
        elif runType == "Opt/Time":
          maxNum = 7
        elif runType == "Opt/AB":
          maxNum = 1


  if runType == "Opt/It":
    graphIt(data)
  elif runType == "Opt/Time":
    # for dat in data:
    #   print(dat)
    #   print("\n")
    # print(len(data))
    graphTime(data)
  elif runType == "Opt/AB":
    graphRatios(data)
  else:
    print("Error: invalid file structure.")
    exit()
  # print("Begin program")


#graphing the data 
def graphTime(data):

  # plt.plot(data[0], data[1], label="broders")
  # plt.plot(data[2], data[3], label="kruskals")
  # plt.plot(data[4], data[5], label="prims")
  # plt.plot(range(0, 31), data[6], label="Optimal")

  # plt.legend(loc="upper right")
  # plt.show()

  #return numSeconds, [XbrodTime, brodPoints, XkruskTime, kruskPoints, XprimTime, primPoints, optPoints]
  plt.xlabel("Processor Time (s)")
  plt.ylabel("Total Tree Weight")

  # print("start\n")
  # print(data[0][0][0]) 
  optPoints = data[0][6]
  XbrodTime = []
  brodPoints  = []
  XkruskTime  = []
  kruskPoints  = []
  XprimTime  = []
  primPoints  = []
  
  # brodPointAvg = [0] * len(data[0][0])
  # kruskPointAvg = [0] * len(data[0][0])
  # primPointAvg = [0] * len(data[0][0])
  
  for dat in data:
    # print(dat)
    # print(len(dat))
    XbrodTime += (dat[0])
    brodPoints += (dat[1])
    XkruskTime += (dat[2])
    kruskPoints += (dat[3])
    XprimTime += (dat[4])
    primPoints += (dat[5])
    # optPoints.append(dat[6])
  # print(optPoints)
  # print(len(optPoints))
  # print(range(0, len(optPoints)))
  # print(XbrodTime)
  # print(brodPoints)
  
  plt.plot(XbrodTime, brodPoints, label="broder")
  plt.plot(XkruskTime, kruskPoints, label="kruskals")
  plt.plot(XprimTime, primPoints, label="prims")
  plt.plot(range(0, len(optPoints)), optPoints, label="optimal")

  plt.legend(loc="upper right")
  plt.show()

def graphIt(data):
  #return [xpoints, brodPoints, kruskPoints, primPoints, optPoints]
  plt.xlabel("Num iterations")
  plt.ylabel("Total Tree Weight")

  xpoints = data[0][0]
  # print(xpoints)
  optPoints = data[0][4]
  brodPointAvg = [0] * len(data[0][0])
  kruskPointAvg = [0] * len(data[0][0])
  primPointAvg = [0] * len(data[0][0])
  for dat in data:
    brodPointAvg = list(map(lambda x, y: x + y, brodPointAvg, dat[1]))
    # print(brodPointAvg)
    kruskPointAvg = list(map(lambda x, y: x + y, kruskPointAvg, dat[2]))
    primPointAvg = list(map(lambda x, y: x + y, primPointAvg, dat[3]))

  brodPointAvg = list(map(lambda x: x/len(data), brodPointAvg))
  kruskPointAvg = list(map(lambda x: x/len(data), kruskPointAvg))
  primPointAvg = list(map(lambda x: x/len(data), primPointAvg))
  plt.plot(xpoints, brodPointAvg, label="broder")
  plt.plot(xpoints, kruskPointAvg, label="kruskals")
  plt.plot(xpoints, primPointAvg, label="prims")
  plt.plot(xpoints, optPoints, label="optimal")

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

  # myFile = csv.writer(open("savedData.csv", "w"))
  # myFile.writerow([sys.argv[1]])
  # print(data)
  # for dat in data:
  #   myFile.writerow(dat)

  data = []
  for fileNum in range(1, 30):
    print("being next file")
    nodes = []
    edges = []
    # with open('./filter/filtered_EMCI_matrices/filtered_Patient1_connectivity_matrix.csv', mode ='r')as file:
    with open('./filter/filtered_EMCI_matrices/filtered_Patient' + str(fileNum) + '_connectivity_matrix.csv', mode ='r')as file:
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

          # edges.append(list(map(int, lines[1::])))  ##for test data

    phers = [[1] * len(edges)] * len(edges)
    print("Begin program")
    if (sys.argv[1] == "Opt/It"):
      #return [xpoints, brodPoints, kruskPoints, primPoints, optPoints]
      data.append([iterations(nodes, edges, phers, ratios)])
      # saveData(data, fileName)
      # graphIt(data)
    elif (sys.argv[1] == "Opt/Time"):
      #return [XbrodTime, brodPoints, XkruskTime, kruskPoints, XprimTime, primPoints, optPoints]
      data.append([timed(nodes, edges, phers, ratios)])
      # saveData(data, fileName)
      # graphTime(data)
    elif (sys.argv[1] == "Opt/AB"):
      # return [dataK, dataP]
      data.append([alphaBeta(nodes, edges, phers)])
      # saveData(data, fileName)
      # graphRatios(data)
    else:
      print("Error: Invalid experimental type. Try again")
      exit()
    # myFile.writerow(data)

  
  # print(data)

  fileName = './curData/curData' + str(fileNum) + '_EMCI.csv'
  if (sys.argv[1] == "Opt/It"):
    #return [xpoints, brodPoints, kruskPoints, primPoints, optPoints]
    # data.append(iterations(nodes, edges, phers, ratios))
    saveData(data, fileName)
    graphIt(data)
  elif (sys.argv[1] == "Opt/Time"):
    #return [XbrodTime, brodPoints, XkruskTime, kruskPoints, XprimTime, primPoints, optPoints]
    # data.append(timed(nodes, edges, phers, ratios))
    saveData(data, fileName)
    graphTime(data)
  elif (sys.argv[1] == "Opt/AB"):
    # return [dataK, dataP]
    # data.append(alphaBeta(nodes, edges, phers))
    saveData(data, fileName)
    graphRatios(data)
  else:
    print("Error: Invalid experimental type. Try again")
    exit()



if __name__ == "__main__":
  main()
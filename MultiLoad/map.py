import random
from MultiLoad.task import TaskSet
from MultiLoad.agent import AgentSet
from typing import List

class Config:
    def __init__(self, batch:int) -> None:
        self.batch = batch
        pass

class Map:
    def __init__(self, filename:str = ""):
        self.filename = filename
        self.taskSet:TaskSet = None
        self.agentSet:AgentSet = None
        self.completedTask:List[int] = []
        self.timestep:int = 0
        self.config:Config = Config(10)
        self.ST:int = 0
        self.processingtime:int = 0
        self.getMapFromFile()
    pass

    def getAstarPosition(self, start:List[int], end:List[int], cost:int):
        x, y = start[0], start[1]
        h = self.allHeristic[(end[0], end[1])]
        mincost = 100000
        while cost>0:
            for dx, dy in [[0, 1], [0, -1], [1, 0], [-1, 0]]:
                nx, ny = x + dx, y + dy
                if nx < 0 or nx >= self.height or ny < 0 or ny >= self.width:
                    continue
                if self.map[nx][ny] == 0:
                    continue
                if h[nx][ny] < h[x][y]:
                    x, y = nx, ny
                    cost -= 1
                    break
            if cost == 0:
                break
        return [x, y]

    def getMapFromFile(self):
        if self.filename == "":
            return None
        with open("Map/"+self.filename, 'r') as f:
            # read header type of map
            f.readline()
            line = f.readline()
            self.height = int(line.split(" ")[1])
            line = f.readline()
            self.width = int(line.split(" ")[1])
            f.readline()
            # create map
            self.map = [[0 for i in range(self.width)] for j in range(self.height)]
            for i in range(self.height):
                line = f.readline()
                for j in range(self.width):
                    if line[j] == '@': # obstacle
                        self.map[i][j] = 0
                    elif line[j] == '.': # empty
                        self.map[i][j] = 1
                    elif line[j] == 'e': # pick up or delivery point
                        self.map[i][j] = 2
                    elif line[j] == 'r': # robot
                        self.map[i][j] = 3
                    else:
                        exit()
        pass

    def printMap(self):
        print(self.height, self.width)
        for i in range(self.height):
            for j in range(self.width):
                print(self.map[i][j], end = " ")
            print()
        pass

    def generateTaskAndAgent(self, numTask:int = 0, time:int = 1000, numAgent:int = 0, capacity:int = 0):
        self.generateTask(numTask, time)
        self.generateAgentPosition(numAgent)
        pass
    
    def getAvailableRobotPosition(self):
        x, y = random.randint(0, self.height-1), random.randint(0, self.width-1)
        while self.map[x][y] == 0:
            x, y = random.randint(0, self.height-1), random.randint(0, self.width-1)
        return [x, y]
    
    def getAvailableTaskPosition(self):
        x, y = random.randint(0, self.height-1), random.randint(0, self.width-1)
        while self.map[x][y] != 2:
            x, y = random.randint(0, self.height-1), random.randint(0, self.width-1)
        return [x, y]

    def generateTask(self, numTask:int = 0, time:int = 1000):
        count = 0
        Tset = []
        while numTask > count:
            st = random.randint(0, time - 100)
            et = st + random.randint(50, 100)
            sp = self.getAvailableTaskPosition()
            ep = self.getAvailableTaskPosition()
            Tset.append([st, et, sp, ep])
            count += 1
        Tset.sort(key = lambda x: x[0])
        with open("Task/"+self.filename +"."+ str(numTask) + ".task", 'w') as f:
            f.write("numTask "+str(numTask)+"\n")
            f.write("startTime endTime startPoint endPoint\n")
            for i in Tset:
                f.write("{} {} {} {} {} {}\n".format(i[0], i[1], i[2][0], i[2][1], i[3][0], i[3][1]))
        pass

    def getMap(self):
        return self.map
    
    def generateAgentPosition(self, numAgent:int = 0):
        count = 0
        with open("Agent/"+self.filename +"."+ str(numAgent)+ ".agent", 'w') as f:
            f.write("numAgent "+str(numAgent)+"\n")
            # f.write("capacity {}\n".format(capacity))
            pos = []
            while numAgent > count:
                position = self.getAvailableRobotPosition()
                if position in pos:
                    continue
                pos.append(position)
                count += 1
            for i in pos:
                f.write("{} {}\n".format(i[0], i[1]))
        pass
    
    def getHeristic(self):
        # if len(self.Heristic) == 0:
        self.allHeristic = {}
        with open("Map/"+self.filename + ".heristic", 'r') as f:
            line = f.readline()
            while line!="":
                x,y = line.split(" ")
                h = [[0 for i in range(self.width)] for j in range(self.height)]
                for i in range(self.height):
                    line = f.readline()
                    for j in range(self.width):
                        h[i][j] = int(line.split(" ")[j])
                self.allHeristic[(int(x), int(y))] = h
                line = f.readline()

        return self.allHeristic

    def setHeristic(self):
        self.heristic = 0
        with open("Map/"+self.filename + ".heristic", 'w') as f:
            for i in range(self.height):                
                for j in range(self.width):
                    if self.map[i][j] != 2:
                        continue
                    h = [[10000 for i in range(self.width)] for j in range(self.height)]
                    openList = []
                    closeList = []
                    openList.append([i, j])
                    h[i][j] = 0
                    while len(openList) > 0:
                        x, y = openList.pop(0)
                        closeList.append([x, y])
                        for dx, dy in [[0, 1], [0, -1], [1, 0], [-1, 0]]:
                            nx, ny = x + dx, y + dy
                            if nx < 0 or nx >= self.height or ny < 0 or ny >= self.width:
                                continue
                            if self.map[nx][ny] == 0:
                                continue
                            if [nx, ny] in closeList:
                                continue
                            if [nx, ny] not in openList:
                                openList.append([nx, ny])
                            h[nx][ny] = min(h[nx][ny], h[x][y] + 1)
                    f.write("{} {}\n".format(i, j))
                    self.heristic = self.heristic+1
                    for p in range(self.height):
                        for q in range(self.width):
                            f.write("{} ".format(h[p][q]))
                        f.write("\n")
        # return 1
    pass




def generateMap(filename:str = "zzz.txt", numTask:int = 1000, time:int = 1000, numAgent:int = 0, capacity:int = 0):
    map = Map(filename)
    # map.generateTaskAndAgent(numTask, time, numAgent, capacity)
    # map.generateTask(numTask, time)
    # map.generateAgentPosition(numAgent)
    return map


global map
map = generateMap("zzz.txt", 1500, 1000, 20, 3)
# map.setHeristic()
map.getHeristic()
# for i in range(map.height):
#     for j in range(map.width):
#         print(h[i][j], end = " ")
#     print()
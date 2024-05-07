import random



class Map:
    def __init__(self, filename:str = ""):
        self.filename = filename
        self.getMapFromFile()
    pass

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
        self.generateAgentPosition(numAgent, capacity)
        pass

    def generateTask(self, numTask:int = 0, time:int = 1000):
        count = 0
        with open("Task/"+self.filename +"."+ str(numTask) + ".task", 'w') as f:
            f.write("numTask "+str(numTask)+"\n")
            f.write("startTime endTime startPoint endPoint\n")
            while numTask > count:
                st = random.randint(0, time - 100)
                et = st + random.randint(50, 100)
                sp = [random.randint(0, self.height), random.randint(0, self.width)]
                ep = [random.randint(0, self.height), random.randint(0, self.width)]
                f.write("{} {} {} {} {} {}\n".format(st, et, sp[0], sp[1], ep[0], ep[1]))
                count += 1
        pass

    def getMap(self):
        return self.map
    
    def generateAgentPosition(self, numAgent:int = 0, capacity:int = 0):
        count = 0
        with open("Agent/"+self.filename +"."+ str(numAgent)+"."+str(capacity)+ ".agent", 'w') as f:
            f.write("numAgent "+str(numAgent)+"\n")
            f.write("capacity {}\n".format(capacity))
            while numAgent > count:
                position = [random.randint(0, self.height), random.randint(0, self.width)]
                f.write("{} {}\n".format(position[0], position[1]))
                count += 1
        pass
    pass
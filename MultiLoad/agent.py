
from typing import List
from MultiLoad.task import Task

class Agent:
    def __init__(self, id:int=0, position:List[int] = [0,0], capacity:int = 0):
        self.id = id
        self.position = position
        self.capacity = capacity
        self.taskList:List[int] = []
        self.schedule:List[List[int]] = [] # the pickup or delivery position of task in taskList # capacity # first element is current position
        self.pathcost:int = 0



class AgentSet:
    def __init__(self, filename:str = "", numAgent:int = 0, capacity:int = 0):
        self.Aset:dict[int, Agent] = {}

        self.numAgent = numAgent
        self.capacity = capacity
        self.filename = filename + "." + str(numAgent) +".agent"
        self.getAgentFromFile()
        pass

    def getMaxCapacity(self):
        maxCapacity = 0
        for agent in self.Aset.values():
            maxCapacity = max(maxCapacity, agent.capacity - len(agent.taskList))
        return maxCapacity
        pass
    
    def getAgentFromFile(self):
        if self.filename == "":
            return None
        with open("Agent/"+self.filename, 'r') as f:
            # read header type of map
            line = f.readline()
            self.numAgent = int(line.split(" ")[1])
            # line = f.readline()
            # self.capacity = int(line.split(" ")[1])
            for i in range(self.numAgent):
                line = f.readline()
                position = [int(line.split(" ")[0]), int(line.split(" ")[1])]
                self.Aset[i] = Agent(i, position, self.capacity)
        pass

    def __del__(self):
        del self.Aset
        pass
        
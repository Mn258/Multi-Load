
from typing import List
from MultiLoad.task import Task

class Agent:
    def __init__(self, position:List[int] = [0,0], capacity:int = 0):
        self.position = position
        self.capacity = capacity
        self.taskList:List[Task] = []
    pass


class AgentSet:
    def __init__(self, filename:str = "", numAgent:int = 0, capacity:int = 0):
        self.AgentSet:List[Agent] = []
        self.numAgent = numAgent
        self.capacity = capacity
        self.filename = filename + "." + str(numAgent) + "." + str(capacity) + ".agent"
        self.getAgentFromFile()
    pass

    def getAgentFromFile(self):
        if self.filename == "":
            return None
        with open("Agent/"+self.filename, 'r') as f:
            # read header type of map
            line = f.readline()
            self.numAgent = int(line.split(" ")[1])
            line = f.readline()
            self.capacity = int(line.split(" ")[1])
            for i in range(self.numAgent):
                line = f.readline()
                position = [int(line.split(" ")[0]), int(line.split(" ")[1])]
                self.AgentSet.append(Agent(position, self.capacity))
        pass

    def __del__(self):
        del self.AgentSet
        pass
        
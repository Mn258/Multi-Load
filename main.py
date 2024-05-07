from MultiLoad.map import *
from MultiLoad.task import *
from MultiLoad.agent import *
from Algorithm import *

def generateMap(filename:str = "zzz.txt", height:int = 10, width:int = 10, numTask:int = 0, time:int = 1000, numAgent:int = 0, capacity:int = 0):
    map = Map(filename, height, width)
    map.generateTaskAndAgent(numTask, time, numAgent, capacity)
    return map

if __name__ == '__main__':
    map = Map("zzz.txt")
    task = TaskSet(map.filename, 1000)
    agent = AgentSet(map.filename, 30, 3)

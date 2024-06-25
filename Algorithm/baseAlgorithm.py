from MultiLoad.map import *
from MultiLoad.task import *
from MultiLoad.agent import *
from sklearn.cluster import SpectralClustering
from sklearn.cluster import KMeans
from sklearn.cluster import OPTICS
from sklearn.datasets import make_blobs

def getDelta(Task1:Task, Task2:Task):
    s1g1 = map.allHeristic[(Task1.endPoint[0], Task1.endPoint[1])][Task1.startPoint[0]][Task1.startPoint[1]]
    s2g2 = map.allHeristic[(Task2.endPoint[0], Task2.endPoint[1])][Task2.startPoint[0]][Task2.startPoint[1]]
    s1g2 = map.allHeristic[(Task2.endPoint[0], Task2.endPoint[1])][Task1.startPoint[0]][Task1.startPoint[1]]
    s2g1 = map.allHeristic[(Task1.endPoint[0], Task1.endPoint[1])][Task2.startPoint[0]][Task2.startPoint[1]]
    s1s2 = map.allHeristic[(Task1.startPoint[0], Task1.startPoint[1])][Task2.startPoint[0]][Task2.startPoint[1]]
    g1g2 = map.allHeristic[(Task2.endPoint[0], Task2.endPoint[1])][Task1.endPoint[0]][Task1.endPoint[1]]
    p1 = s1g1+s2g1+s2g2 # s1->g1->s2->g2
    p2 = s2g2+s1g2+s1g1 # s2->g2->s1->g1
    p3 = s1s2+s2g2+g1g2 # s1->s2->g2->g1
    p4 = s1s2+s2g1+g1g2 # s1->s2->g1->g2
    p5 = s1s2+s1g1+g1g2 # s2->s1->g1->g2
    p6 = s1s2+s1g2+g1g2 # s2->s1->g2->g1
    # dir_map = {
    #     p1: (1, 1),
    #     p2: (2, 2),
    #     p3: (1, 2),
    #     p4: (1, 1),
    #     p5: (2, 1),
    #     p6: (2, 2)
    # }
    dir_map = {
        p1: (1, 1),
        p2: (-1, -1),
        p3: (1, -1),
        p4: (1, 1),
        p5: (-1, 1),
        p6: (-1, -1)
    }
    d = min(p1, p2, p3, p4, p5, p6)
    if d in dir_map:
        dir_s, dir_g = dir_map[d]
    else:
        raise ValueError("Invalid value for d")
    d = d - s1g1 - s2g2
    return d, dir_s, dir_g

def getGraph(TaskSet:List[int]):
    taskNum = len(TaskSet)
    rt = [[0 for i in range(taskNum)] for j in range(taskNum)]
    dirs = [[0 for i in range(taskNum)] for j in range(taskNum)]
    dirg = [[0 for i in range(taskNum)] for j in range(taskNum)]
    for i in range(taskNum):
        for j in range(taskNum):
            rt[i][j],dirs[i][j], dirg[i][j] = getDelta(map.taskSet.Tset[TaskSet[i]], map.taskSet.Tset[TaskSet[j]])
            pass
    return rt, dirs, dirg
    pass
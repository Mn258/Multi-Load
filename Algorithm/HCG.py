from Algorithm.baseAlgorithm import *

def distance(ts1:List[int], ts2:List[int], G, dirs, dirg):
    """ distance between two tasksets 
        use the averge distance between all the tasks in the two tasksets
    """
    TS = ts1+ts2
    delta = 0
    for i in range(len(TS)):
        for j in range(i+1, len(TS)):
            delta += G[TS[i]][TS[j]]
    delta /= (len(TS)*(len(TS)-1)/2)
    pass

def distanceDir(ts1:List[Task], ts2:List[Task], G, dirs, dirg):
    """ distance between two tasksets considering the direction """
    deltaS = 0
    deltaG = 0
    
    for i in range(len(ts1)):
        for j in range(len(ts2)):
            deltaS += G[ts1[i].id][ts2[j].id]
            deltaG += G[ts2[j].id][ts1[i].id]
    pass

def HeuristicClustering(TaskSet:List[int], k:int):
    """ Heuristic clustering """
    if TaskSet == []:
        return []
    if len(TaskSet) == 1:
        return [TaskSet]
    n_c = int(min(k, len(TaskSet))//2)
    G,_,_ = getGraph(TaskSet)

if __name__ == "__main__":
    print("Hello World")
    pass
from Algorithm.baseAlgorithm import *
from Algorithm.HCG import *

def distanceofTask(p1:List[int], p2:List[int])->int:
    return map.allHeristic[p2[0], p2[1]][p1[0]][p1[1]]
    pass


def getPathCost(path:List[List[int]]) -> int:
    cost = 0
    for i in range(len(path)-1):
        cost += distanceofTask(path[i], path[i+1])
    return cost
    pass

def getCostandTime(aid:int)->int:
    agent = map.agentSet.Aset[aid]
    for i in range(len(agent.schedule)-1):
        agent.pathcost += distanceofTask(agent.schedule[i], agent.schedule[i+1])
        if agent.schedule[i+1][3] < 0:
            map.taskSet.Tset[-agent.schedule[i+1][3]].completeTime = map.timestep + agent.pathcost
            map.ST += map.taskSet.Tset[-agent.schedule[i+1][3]].completeTime - map.taskSet.Tset[-agent.schedule[i+1][3]].startTime
    pass

def updatePosition(batch:int, aid:int):
    """ update the position of agent """
    agent = map.agentSet.Aset[aid]
    if len(agent.schedule) == 0 or len(agent.schedule) == 1:
        agent.schedule = [agent.position]
        agent.schedule[0].append(0)
        return None
    i = 0
    pathcost = []
    while len(agent.schedule)-1 > i and batch > 0:
        if distanceofTask(agent.schedule[i], agent.schedule[i+1]) <= batch:
            batch -= distanceofTask(agent.schedule[i], agent.schedule[i+1])
            pathcost.append(distanceofTask(agent.schedule[i], agent.schedule[i+1]))
            i+=1
        else:
            break
        pass
    for j in range(1, i+1):
        if agent.schedule[j][3] > 0:
            # print(agent.id, "pick up task", agent.schedule[j][3])
            map.taskSet.taskId.remove(agent.schedule[j][3])
            agent.taskList.append(agent.schedule[j][3])
        else:
            # print(agent.id, "delivery task", -agent.schedule[j][3])
            map.completedTask.append(-agent.schedule[j][3])
            agent.taskList.remove(-agent.schedule[j][3])
            map.taskSet.Tset[-agent.schedule[j][3]].completeTime = map.timestep - map.config.batch + pathcost[j-1]
            map.ST += (map.taskSet.Tset[-agent.schedule[j][3]].completeTime) - map.taskSet.Tset[-agent.schedule[j][3]].startTime
        pass
    if i == len(agent.schedule)-1:
        agent.schedule = [agent.schedule[i]]
        return None
    if batch > 0:
        position = map.getAstarPosition(agent.schedule[i], agent.schedule[i+1], batch)
        agent.position = position
        agent.schedule = agent.schedule[i:]
        agent.schedule[0] = position+[agent.schedule[0][2]]+[0]
    elif batch == 0:
        agent.position = agent.schedule[i]
        agent.schedule = agent.schedule[i:]
        agent.schedule[0][3] = 0
    new_schedule = []
    for j in agent.schedule:
        if abs(j[3]) in agent.taskList or j[3] == 0:
            new_schedule.append(j)        
    agent.schedule = new_schedule
    pass



def positiveGraph(G:List[List[int]]):
    min_e = G[0][0]
    for i in range(len(G)):
        for j in range(len(G[i])):
            if G[i][j] < min_e:
                min_e = G[i][j]
    for i in range(len(G)):
        for j in range(len(G[i])):
            G[i][j] = G[i][j] - min_e+1
    return G, min_e
    pass

def kMeansClustering(TaskSet:List[int], k:int) -> List[List[int]]:
    """ k means clustering """
    if TaskSet == []:
        return []
    if len(TaskSet) == 1:
        return [TaskSet]
    n_c = int(min(k, len(TaskSet))//2)
    G,_,_ = getGraph(TaskSet)
    nG, _ = positiveGraph(G)
    for i in range(len(nG)):
        nG[i][i] = 0
    spectral = KMeans(n_clusters=n_c)
    labels = spectral.fit_predict(nG)
    Tpackage = [[] for _ in range(n_c)]
    for i in range(len(labels)):
        Tpackage[labels[i]].append(TaskSet[i])
    return Tpackage
    pass

def singleTaskAlloc(tid:int, agent:Agent, cost:int, p:List[List[int]]):
    """ allocate single task to agent and find the best path to complete the task """
    path = [[i for i in x] for x in p]
    task = map.taskSet.Tset[tid]
    # path.append(task.endPoint)
    mincost = cost + 1000
    mins = 0 # start point
    ming = 0 # end point
    for i in range(len(path)-1):
        if (path[i][2] <= agent.capacity):
            continue
        tmp1 = cost + distanceofTask(path[i], task.startPoint) + distanceofTask(task.startPoint, path[i+1]) - distanceofTask(path[i], path[i+1])
        path.insert(i+1, task.startPoint+[path[i][2]+1])
        for j in range(i+1, len(path)-1):
            if (path[j][2] <= agent.capacity):
                break
            tmp = tmp1 + distanceofTask(path[j], task.endPoint) + distanceofTask(task.endPoint, path[j+1]) - distanceofTask(path[j], path[j+1])
            if tmp < mincost:
                mincost = tmp
                mins = i+1
                ming = j+1
                pass
            pass
        tmp = tmp1 + distanceofTask(path[len(path)-1], task.endPoint)
        if tmp < mincost:
            mincost = tmp
            mins = i+1
            ming = len(path)
            pass
        path.pop(i+1)
        pass
    tmp = cost + distanceofTask(path[len(path)-1], task.startPoint) + distanceofTask(task.startPoint, task.endPoint)
    if tmp < mincost:
        path.append(task.startPoint+[path[len(path)-1][2]+1] + [tid])
        path.append(task.endPoint+[path[len(path)-1][2]-1] + [-tid])
        return tmp, path
        pass
    path.insert(mins, task.startPoint+[path[mins-1][2]+1]+[tid])
    for i in range(mins+1, ming):
        path[i][2] += 1
    path.insert(ming, task.endPoint+[path[ming-1][2]-1]+[-tid])
    return mincost, path
    pass

def bidforTasks(tasks:List[int], agent:Agent):
    """ agent bid for task 
    if agent enables to complete the task, then bid for the task, 
    return the cost and the path
    if agent can't complete the task, return None
    """
    path = [x for x in agent.schedule]
    ts = [x for x in tasks]
    cost = getPathCost(path)
    while len(ts) > 0:
        besttask = ts[0]
        delta = 1000
        for t in ts:
            task = map.taskSet.Tset[t]
            tcost, tpath = singleTaskAlloc(t, agent, cost, path)
            if tcost - cost - distanceofTask(task.startPoint, task.endPoint) < delta:
                delta = tcost - cost - distanceofTask(task.startPoint, task.endPoint)
                besttask = t
                bestpath = tpath
                bestcost = tcost
            pass
        ts.remove(besttask)
        path = bestpath
        cost = bestcost
    return delta, path, cost
    pass

def allocationTask(Tpackage:List[List[int]]):
    """ allocation task to agent """
    PathSet = {}
    Delta = [[0]*len(map.agentSet.Aset) for _ in range(len(Tpackage))]
    for i in range(len(Tpackage)):
        for aid in map.agentSet.Aset.keys():
            Delta[i][aid], path, cost = bidforTasks(Tpackage[i], map.agentSet.Aset[aid])
            PathSet[(i, aid)] = path
            pass
    while len(Tpackage) > 0:
        bid = 10000
        for i in range(len(Tpackage)):
            for aid in map.agentSet.Aset.keys():
                delta = Delta[i][aid]
                if delta < bid:
                    bid = delta
                    bestpath = PathSet[(i, aid)]
                    besttasks = i
                    bestagent = map.agentSet.Aset[aid]
        del Tpackage[besttasks]
        # bestagent.taskList.extend(besttasks)
        # bestagent.taskList.append(x for x in besttasks)
        bestagent.schedule = [[x for x in i] for i in bestpath]
        del Delta[besttasks]
        for i in range(len(Tpackage)):
            Delta[i][bestagent.id], path, cost = bidforTasks(Tpackage[i], bestagent)
            PathSet[(i, bestagent.id)] = path
    pass

def ClusterAllocation(TaskSet:List[int]):
    """ Cluster the task and allocate the task to agent """
    maxCapacity = map.agentSet.getMaxCapacity()
    # Tpackage = kMeansClustering(TaskSet, map.agentSet.numAgent)
    # Tpackage = HeuristicClustering(TaskSet, maxCapacity)
    Tpackage = MaxHeuristicClustering(TaskSet, maxCapacity)
    # Tpackage = DBSCANClustering(TaskSet, maxCapacity)
    allocationTask(Tpackage)
    pass


 
if __name__ == "main":
    pass

    
# def CombinatorialAuction(TaskSet:List[Task], AgentSet:AgentSet):
#     # 剩余最大容量
#     maxCapacity = 0
#     for agent in AgentSet.Aset:
#         maxCapacity = max(maxCapacity, agent.capacity)
#     # maxCapHierarchicalClustering(TaskSet, maxCapacity)
#     Tpackage = kMeansClustering(TaskSet, AgentSet.numAgent)
#     # OPTICSClustering(TaskSet, 0.1, 2)
#     allocationTask(Tpackage, AgentSet.Aset)
#     pass
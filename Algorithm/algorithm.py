import dis
from re import A
# from requests import get
from Algorithm.baseAlgorithm import *
from Algorithm.HCG import *

def checkPath(path:List[List[int]]) -> bool:
    """ check the path is valid """
    if len(path) == 0:
        return True
    if path[0][3] != 0:
        raise ValueError("Invalid value for path")
        return False
    for i in range(1, len(path)):
        if path[i][3] == 0:
            raise ValueError("Invalid value for path")
            return False
        if path[i][3] < 0:
            if path[i][2] != path[i-1][2]-1:
                raise ValueError("Invalid value for path")
                return False
        if path[i][3] > 0:
            if path[i][2] != path[i-1][2] + 1:
                raise ValueError("Invalid value for path")
                return False
    return True
    pass

def distanceofTask(p1:List[int], p2:List[int])->int:
    return map.allHeristic[p2[0], p2[1]][p1[0]][p1[1]]
    pass


def getPathCost(path:List[List[int]]) -> int:
    cost = 0
    for i in range(1, len(path)):
        cost += distanceofTask(path[0], path[i])
    return cost
    pass

def getPathCostIndex(path:List[List[int]], indexS:int, indexG:int) -> int:
    cost = 0
    if len(path) == 1:
        return 0
    for i in range(indexS, indexG):
        cost += distanceofTask(path[i], path[i+1])
    return cost
    pass

def getCostandTime(aid:int):
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
    if len(agent.schedule) == 0:
        agent.schedule = [agent.position]
        agent.schedule[0]+= [0, 0]
        agent.pathcost = 0
        return None
    elif len(agent.schedule) == 1:
        agent.pathcost = 0
        if agent.schedule[0][2] != 0 or agent.schedule[0][3] != 0:
            raise ValueError("Invalid value for schedule")
        return None
        pass
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
            print(agent.id, "pick up task", agent.schedule[j][3])
            map.taskSet.taskId.remove(agent.schedule[j][3])
            agent.taskList.append(agent.schedule[j][3])
        else:
            print(agent.id, "delivery task", -agent.schedule[j][3])
            map.completedTask.append(-agent.schedule[j][3])
            agent.taskList.remove(-agent.schedule[j][3])
            map.taskSet.Tset[-agent.schedule[j][3]].completeTime = map.timestep - map.config.batch + pathcost[j-1]
            map.ST += (map.taskSet.Tset[-agent.schedule[j][3]].completeTime) - map.taskSet.Tset[-agent.schedule[j][3]].startTime
        pass
    if i == len(agent.schedule)-1:
        agent.schedule = [agent.schedule[i]]
        agent.schedule[0][3] = 0
        if agent.schedule[0][2] != 0:
            raise ValueError("Invalid value for schedule")
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
    num = len(agent.taskList)
    for j in agent.schedule:
        if abs(j[3]) in agent.taskList or j[3] == 0:
            j[2] = num
            new_schedule.append(j)
            num -= 1
    agent.schedule = new_schedule
    agent.pathcost = getPathCost(agent.schedule)
    checkPath(agent.schedule)
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
    deliT = 0
    path = []
    for i in p:
        path.append([x for x in i])
        if i[3] < 0:
            deliT += 1
    task = map.taskSet.Tset[tid]
    # path.append(task.endPoint)
    mincost = cost + 900000
    mins = 0 # start point
    ming = 0 # end point
    deliveryT = 0
    for i in range(len(path)-1):
        if (path[i][2] == agent.capacity):
            continue
        elif (path[i][2] > agent.capacity):
            raise ValueError("Invalid value for capacity")
        if (path[i][3] < 0):
            deliveryT += 1
        delta = distanceofTask(path[i], task.startPoint) + distanceofTask(task.startPoint, path[i+1]) - distanceofTask(path[i], path[i+1])
        tmp1 = cost + (deliT - deliveryT) * delta
        path.insert(i+1, task.startPoint+[path[i][2]] + [tid])
        dt1 = deliveryT
        flagFind = False
        for j in range(i+1, len(path)-1):
            if (path[j][2] == agent.capacity):
                flagFind = True
                break
            elif (path[j][2] > agent.capacity):
                raise ValueError("Invalid value for capacity")
            if (path[j][3] < 0):
                dt1 += 1
            delta = distanceofTask(path[j], task.endPoint) + distanceofTask(task.endPoint, path[j+1]) - distanceofTask(path[j], path[j+1])
            tmp = tmp1 + (deliT - dt1) * delta
            tmp += map.timestep - task.startTime
            tmp += getPathCostIndex(path, i, j) + distanceofTask(path[j], task.endPoint)
            if tmp < mincost:
                mincost = tmp
                mins = i+1
                ming = j+1
                pass
            pass
        if flagFind:
            path.pop(i+1)
            continue
        tmp = tmp1 + distanceofTask(path[len(path)-1], task.endPoint)
        tmp += map.timestep - task.startTime + getPathCostIndex(path, i, len(path)-1)
        if tmp < mincost:
            mincost = tmp
            mins = i+1
            ming = len(path)
            pass
        path.pop(i+1)
        pass
    tmp = cost + getPathCostIndex(path, 0, len(path)-1) + distanceofTask(path[len(path)-1], task.startPoint) + distanceofTask(task.startPoint, task.endPoint)
    tmp += map.timestep - task.startTime
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
    path = [[i for i in x] for x in agent.schedule]
    ts = [x for x in tasks]
    # cost = getPathCost(path) # the path cost of delivering the tasks
    cost = agent.pathcost
    dis = 0
    for t in ts:
        dis += distanceofTask(map.taskSet.Tset[t].startPoint, map.taskSet.Tset[t].endPoint)
        task = map.taskSet.Tset[t]
        tcost, tpath = singleTaskAlloc(t, agent, cost, path)
        path = tpath
        cost = tcost
    delta = cost - agent.pathcost - dis
    return delta, path, cost
    while len(ts) > 0:
        besttask = ts[0]
        delta = 900000
        for t in ts:
            task = map.taskSet.Tset[t]
            tcost, tpath = singleTaskAlloc(t, agent, cost, path)
            ddd = tcost - cost - distanceofTask(task.startPoint, task.endPoint)
            if ddd < delta :
                delta = ddd
                besttask = t
                bestpath = tpath
                bestcost = tcost
            pass
        dis += distanceofTask(map.taskSet.Tset[besttask].startPoint, map.taskSet.Tset[besttask].endPoint)
        ts.remove(besttask)
        path = bestpath
        cost = bestcost
    delta = bestcost - agent.pathcost - dis
    return delta, path, cost
    pass

def allocationTask(Tpackage:List[List[int]]):
    """ allocation task to agent """
    PathSet = {}
    Delta = [[0]*len(map.agentSet.Aset) for _ in range(len(Tpackage))]
    for i in range(len(Tpackage)):
        for aid in map.agentSet.Aset.keys():
            Delta[i][aid], path, cost = bidforTasks(Tpackage[i], map.agentSet.Aset[aid])
            checkPath(path)
            PathSet[i, aid] = path, cost
            pass
    taskNum = 0
    allocated = []
    while len(Tpackage) > taskNum:
        taskNum+=1
        bid = 10000000
        for i in range(len(Tpackage)):
            if i in allocated:
                continue
            for aid in map.agentSet.Aset.keys():
                delta = Delta[i][aid]
                # delta = PathSet[(i, aid)][1]
                if delta < bid or (delta == bid and len(PathSet[(i, aid)][0]) < len(bestpath)):
                    bid = delta
                    bestpath = PathSet[(i, aid)][0]
                    besttasks = i
                    bestagent = map.agentSet.Aset[aid]
                    bestcost = PathSet[(i, aid)][1]
        # bestagent.taskList.extend(besttasks)
        # bestagent.taskList.append(x for x in besttasks)
        bestagent.schedule = [[x for x in i] for i in bestpath]
        bestagent.pathcost = bestcost
        # print("Agent", bestagent.id, "complete task", Tpackage[besttasks])
        allocated.append(besttasks)
        for i in range(len(Tpackage)):
            if i in allocated:
                continue
            Delta[i][bestagent.id], path, cost = bidforTasks(Tpackage[i], bestagent)
            checkPath(path)
            PathSet[(i, bestagent.id)] = [path, cost]
    PathSet.clear()
    Delta.clear()
    pass

def generate_subsets(tasks):
    if not tasks:
        return [[]]

    subsets = []
    first_task = tasks[0]
    remaining_tasks = tasks[1:]
    subsets_without_first = generate_subsets(remaining_tasks)

    subsets.extend(subsets_without_first)
    subsets.extend([subset + [first_task] for subset in subsets_without_first])

    return subsets

def has_common_elements(list1, list2):
    for element in list1:
        if element in list2:
            return True
    return False

def allocationTask2(Tpackage:List[List[int]]):
    """ allocation task to agent """
    # numm = pow(2, map.agentSet.capacity) - 1
    T = []
    for task in Tpackage:
        if len(task) == 1:
            T.append(task)
            continue
        subsets = generate_subsets(task)
        for i in subsets:
            if len(i) == 0:
                continue
            T.append(i)
    taskIndex = [[]for _ in range(len(T))]
    for i in range(len(T)):
        for j in range(i+1, len(T)):
            if has_common_elements(T[i], T[j]):
                taskIndex[i].append(j)
                taskIndex[j].append(i)
    PathSet = {}
    Delta = [[0]*len(map.agentSet.Aset) for _ in range(len(T))]
    for i in range(len(T)):
        for aid in map.agentSet.Aset.keys():
            Delta[i][aid], path, cost = bidforTasks(T[i], map.agentSet.Aset[aid])
            checkPath(path)
            PathSet[i, aid] = path, cost
            pass
    taskNum = 0
    allocated = []
    while len(T) > taskNum:
        taskNum+=1
        bid = 10000000
        for i in range(len(T)):
            if i in allocated:
                continue
            for aid in map.agentSet.Aset.keys():
                delta = Delta[i][aid]
                if delta < bid:
                    bid = delta
                    bestpath = PathSet[i, aid][0]
                    besttasks = i
                    bestagent = map.agentSet.Aset[aid]
                    bestcost = PathSet[i, aid][1]
        bestagent.schedule = [[x for x in i] for i in bestpath]
        bestagent.pathcost = bestcost
        allocated.append(besttasks)
        for i in taskIndex[besttasks]:
            if i in allocated:
                continue
            allocated.append(i)            
        for i in range(len(T)):
            if i in allocated:
                continue
            Delta[i][bestagent.id], path, cost = bidforTasks(T[i], bestagent)
            checkPath(path)
            PathSet[(i, bestagent.id)] = [path, cost]
    pass

def compareALG(TaskSet:List[int]):
    """ compare the algorithm """
    pathset = {}
    for i in range(len(TaskSet)):
        for aid in map.agentSet.Aset.keys():
            cost, path = singleTaskAlloc(TaskSet[i], map.agentSet.Aset[aid], map.agentSet.Aset[aid].pathcost, map.agentSet.Aset[aid].schedule)
            pathset[i, aid] = path, cost
            pass
    taskNum = 0
    allocated = []
    while len(TaskSet) > taskNum:
        taskNum+=1
        bid = 10000
        for i in range(len(TaskSet)):
            if i in allocated:
                continue
            for aid in map.agentSet.Aset.keys():
                cost = pathset[i, aid][1]
                if cost < bid:
                    bid = cost
                    bestpath = pathset[i, aid][0]
                    besttasks = i
                    bestagent = map.agentSet.Aset[aid]
                    
        bestagent.schedule = [[x for x in i] for i in bestpath]
        # print("Agent", bestagent.id, "complete task", TaskSet[besttasks])
        bestagent.pathcost = cost
        allocated.append(besttasks)
        for i in range(len(TaskSet)):
            if i in allocated:
                continue
            cost, path = singleTaskAlloc(TaskSet[i], bestagent, bestagent.pathcost, bestagent.schedule)
            pathset[i, bestagent.id] = path, cost
    pass


def ClusterAllocation(TaskSet:List[int]):
    """ Cluster the task and allocate the task to agent """
    # t = time.time()
    maxCapacity = map.agentSet.getMaxCapacity()
    # Tpackage = kMeansClustering(TaskSet, map.agentSet.numAgent)
    # Tpackage = HeuristicClustering(TaskSet, maxCapacity)
    # Tpackage = MaxHeuristicClustering(TaskSet, maxCapacity)
    Tpackage = MHCEnhance(TaskSet, maxCapacity)
    # Tpackage = DBSCANClustering(TaskSet, maxCapacity)
    # print("Time:", time.time()-t)
    allocationTask2(Tpackage)
    pass


 
if __name__ == "main":
    pass
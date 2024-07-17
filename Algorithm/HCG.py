from Algorithm.baseAlgorithm import *
from scipy.cluster.hierarchy import linkage, fcluster
from sklearn.cluster import DBSCAN
import numpy as np

def distanceofTasks(p1:List[int], p2:List[int], G):
    Delta = 0
    t = p1 + p2
    for i in range(len(t)):
        for j in range(i+1, len(t)):
            Delta += G[t[i]][t[j]]
    # 保留两位小数
    return Delta/(len(t)*(len(t)-1))*2
    pass



def HeuristicClustering(TaskSet:List[int], k:int):
    """ Heuristic clustering """
    if TaskSet == []:
        return []
    if len(TaskSet) == 1:
        return [TaskSet]
    G,_,_ = getGraph(TaskSet)
    weight = [[float(x) for x in G[i]] for i in range(len(G))]
    Tasks = [[i] for i in range(len(TaskSet))]
    flag = True
    while flag:
        flag = False
        min_d = np.inf
        min_i, min_j = None, None
        for i, cluster1 in enumerate(Tasks):
            for j, cluster2 in enumerate(Tasks):
                if i != j and len(cluster1)+len(cluster2) <= k:
                    d = weight[i][j]
                    if d < min_d:
                        flag = True
                        min_d = d
                        min_i = i
                        min_j = j
        if min_i is not None and min_j is not None:
            new_cluster = Tasks[min_i] + Tasks[min_j]
            del Tasks[min_i]
            del Tasks[min_j-1]
            Tasks.append(new_cluster)

            del weight[min_i]
            del weight[min_j-1]
            for ii in range(len(weight)):
                del weight[ii][min_i]
                del weight[ii][min_j-1]
                weight[ii].append(distanceofTasks(new_cluster, Tasks[ii], G))
            weight.append([weight[i][-1] for i in range(len(Tasks)-1)]+[0])
    Tpackage = [[TaskSet[x] for x in i] for i in Tasks]
    return Tpackage

def TarjanDFS(i:int, T:List[int], dir, DFN, LOW, stack, inStack, index, sccList):
    """ Tarjan DFS """
    DFN[i] = LOW[i] = index+1
    index += 1
    stack.append(i)
    inStack[i] = True
    for j in range(len(T)):
        if dir[T[i]][T[j]] > 0:
            if DFN[j] == -1:
                TarjanDFS(j, T, dir, DFN, LOW, stack, inStack, index, sccList)
                LOW[i] = min(LOW[i], LOW[j])
            elif inStack[j]:
                LOW[i] = min(LOW[i], DFN[j])
    scc = []
    if DFN[i] == LOW[i]:
        j = -1
        while j != i:
            j = stack.pop()
            inStack[j] = False
            scc.append(j)
        sccList.append(scc)
    pass

def Tarjan(T, G, dir):
    """ Tarjan algorithm """
    DFN = [-1 for i in range(len(T))]
    LOW = [-1 for i in range(len(T))]
    stack = []
    inStack = [False for i in range(len(T))]
    index = 0
    sccList = []
    delta = 0
    for i in range(len(T)):
        if DFN[i] == -1:
            TarjanDFS(i, T, dir, DFN, LOW, stack, inStack, index, sccList)
    for scc in sccList:
        if len(scc) > 1:
            t_d = 0
            for i in range(len(scc)-1):
                for j in range(i+1, len(scc)):
                    t_d += G[T[scc[i]]][T[scc[j]]]
            delta += t_d/(len(scc))*2
    for i in range(len(sccList)-1):
        t_d = 0
        for j in sccList[i]:
            for k in sccList[i+1]:
                t_d += G[T[j]][T[k]]
        delta += t_d/(len(sccList[i])*len(sccList[i+1]))
    # delta 需要再除以len(T)？？？
    return delta
    pass

def distanceDir(ts1:List[int], ts2:List[int], G, dirs, dirg):
    """ distance between two tasksets considering the direction """
    if len(ts1) + len(ts2) == 2:
        return G[ts1[0]][ts2[0]]
    deltaS, dirG = 0, 0
    T = []
    T.extend(x for x in ts1)
    T.extend(x for x in ts2)
    deltaS = Tarjan(T, G, dirs)
    deltaG = Tarjan(T, G, dirg)
    return (deltaS + deltaG)/2
    pass

def MHCEnhance(TaskSet:List[int], k:int):
    """ Max heuristic clustering with SCC """
    if TaskSet == []:
        return []
    if len(TaskSet) == 1:
        return [TaskSet]
    G, dirS, dirG = getGraph(TaskSet)
    weight = [[float(x) for x in G[i]] for i in range(len(G))]
    Tasks = [[i] for i in range(len(TaskSet))]
    flag = True
    while flag:
        flag = False
        min_d = np.inf
        min_i, min_j = None, None
        for i, cluster1 in enumerate(Tasks):
            for j, cluster2 in enumerate(Tasks):
                if i != j and len(cluster1)+len(cluster2) <= k:
                    d = weight[i][j]
                    if d < 0 and d < min_d:
                        flag = True
                        min_d = d
                        min_i = i
                        min_j = j
        if min_i is not None and min_j is not None:
            new_cluster = Tasks[min_i] + Tasks[min_j]
            del Tasks[min_i]
            del Tasks[min_j-1]
            Tasks.append(new_cluster)

            del weight[min_i]
            del weight[min_j-1]
            for ii in range(len(weight)):
                del weight[ii][min_i]
                del weight[ii][min_j-1]
                weight[ii].append(distanceDir(new_cluster, Tasks[ii], G, dirS, dirG))
            weight.append([weight[i][-1] for i in range(len(Tasks)-1)]+[0])
    Tpackage = [[TaskSet[x] for x in i] for i in Tasks]
    return Tpackage
    pass

def MaxHeuristicClustering(TaskSet:List[int], k:int):
    """ Max heuristic clustering with SCC """
    if TaskSet == []:
        return []
    if len(TaskSet) == 1:
        return [TaskSet]
    G, dirS, dirG = getGraph(TaskSet)
    weight = [[float(x) for x in G[i]] for i in range(len(G))]
    Tasks = [[i] for i in range(len(TaskSet))]
    flag = True
    while flag:
        flag = False
        min_d = np.inf
        min_i, min_j = None, None
        for i, cluster1 in enumerate(Tasks):
            for j, cluster2 in enumerate(Tasks):
                if i != j and len(cluster1)+len(cluster2) <= k:
                    d = weight[i][j]
                    if d < 0 and d < min_d:
                        flag = True
                        min_d = d
                        min_i = i
                        min_j = j
        if min_i is not None and min_j is not None:
            new_cluster = Tasks[min_i] + Tasks[min_j]
            del Tasks[min_i]
            del Tasks[min_j-1]
            Tasks.append(new_cluster)
            del weight[min_i]
            del weight[min_j-1]
            for ii in range(len(weight)):
                del weight[ii][min_i]
                del weight[ii][min_j-1]
                weight[ii].append(distanceDir(new_cluster, Tasks[ii], G, dirS, dirG))
            weight.append([weight[i][-1] for i in range(len(Tasks)-1)]+[0])
    Tpackage = [[TaskSet[x] for x in i] for i in Tasks]
    return Tpackage
    pass


def DBSCANClustering(TaskSet:List[int], max:int):
    """ DBSCAN clustering """
    if TaskSet == []:
        return []
    if len(TaskSet) == 1:
        return [TaskSet]
    G,_,_ = getGraph(TaskSet)
    G, min_e = positiveGraph(G)
    dbscan = DBSCAN(eps=-min_e, min_samples=max-1, metric='precomputed')
    clusters = dbscan.fit_predict(G)
    single = []
    TaskPackage = {}
    for i in range(len(clusters)):
        if (clusters[i] == -1):
            single.append([TaskSet[i]])
        else:
            if clusters[i] not in TaskPackage:
                TaskPackage[clusters[i]] = []
            TaskPackage[clusters[i]].append(TaskSet[i])
    T = []
    for i in TaskPackage:
        if len(TaskPackage[i]) > max:
            tasks = TaskPackage[i]
            num_subsets = len(tasks) // max
            for j in range(num_subsets):
                subset = tasks[j*max : (j+1)*max]
                T.append(subset)
            remaining_tasks = tasks[num_subsets*max:]
            if remaining_tasks:
                T.append(remaining_tasks)
        else:
            T.append(TaskPackage[i])
    for i in single:
        T.append(i)
    return T

if __name__ == "__main__":
    print("Hello World")
    pass
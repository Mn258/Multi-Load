from Algorithm.baseAlgorithm import *
from scipy.cluster.hierarchy import linkage, fcluster
from sklearn.cluster import DBSCAN
import numpy as np

def distanceofTask(p1:List[int], p2:List[int], G)->int:
    Delta = 0
    t = p1 + p2
    for i in range(len(t)):
        for j in range(i+1, len(t)):
            Delta += G[t[i]][t[j]]
    return Delta/(len(t)*(len(t)-1))*2
    pass



def HeuristicClustering(TaskSet:List[int], k:int):
    """ Heuristic clustering """
    if TaskSet == []:
        return []
    if len(TaskSet) == 1:
        return [TaskSet]
    G,_,_ = getGraph(TaskSet)
    weight = [[x for x in G[i]] for i in range(len(G))]
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
                weight[ii].append(distanceofTask(new_cluster, Tasks[ii], G))
            weight.append([weight[i][-1] for i in range(len(Tasks)-1)]+[0])
    Tpackage = [[TaskSet[x] for x in i] for i in Tasks]
    # weight = [[x for x in G[i]] for i in range(len(G))]
    # Tasks = [[i] for i in range(len(TaskSet))]
    return Tpackage

def distanceDir(ts1:List[int], ts2:List[int], G, dirs, dirg):
    """ distance between two tasksets considering the direction """
    deltaS = 0
    
    deltaG = 0
    pass

def MaxHeuristicClustering(TaskSet:List[int], k:int):
    """ Max heuristic clustering with SCC """
    if TaskSet == []:
        return []
    if len(TaskSet) == 1:
        return [TaskSet]
    G, dirS, dirG = getGraph(TaskSet)
    weight = [[x for x in G[i]] for i in range(len(G))]
    Tasks = [[i] for i in range(len(TaskSet))]
    flag = True
    while flag:
        flag = False
        min_d = np.inf
        min_i, min_j = None, None
        for i, cluster1 in enumerate(Tasks):
            for j, cluster2 in enumerate(Tasks):
                if i != j and len(cluster1)+len(cluster2) <= k:
                    d = distanceDir(cluster1, cluster2, G, dirS, dirG)
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
                weight[ii].append(distanceofTask(new_cluster, Tasks[ii], G))
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
        T.append(TaskPackage[i])
    for i in single:
        T.append(i)
    return clusters

if __name__ == "__main__":
    print("Hello World")
    pass
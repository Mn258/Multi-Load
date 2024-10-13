
from tkinter import N

from networkx import capacity_scaling
from MultiLoad.map import *
from MultiLoad.task import *
from MultiLoad.agent import *
from Algorithm.algorithm import *
import sys



def run():
    while len(map.taskSet.taskId) > 0:
        map.timestep += map.config.batch
        print("Timestep:", map.timestep)
        # updatePosition
        i = 0
        
        # paths = []
        for aid in map.agentSet.Aset.keys():
            # map.agentSet.Aset[aid].updatePosition(config.batch)
            path = updatePosition(map.config.batch, aid)
            # paths.append(path)
            pass
        # allocateTask
        # kk=0
        # while kk <map.config.batch:
        #     ps = []
        #     for i in range(len(paths)):
        #         if paths[i] != None and kk < len(paths[i]):
        #             if paths[i][kk] in ps:
        #                 map.ST += 3
        #                 ps.append(paths[i][kk])
        #                 pass
        #             else :
        #                 ps.append(paths[i][kk])
        #             pass
        #         pass
        #     kk+=1
        #     pass
        BTset:List[int] = []
        for tid in map.taskSet.taskId:
            if map.taskSet.Tset[tid].endTime + 500 <= map.timestep:
                map.taskSet.Tset[tid].completeTime = -1
                map.taskSet.taskId.remove(tid)
            elif map.taskSet.Tset[tid].startTime <= map.timestep:
                BTset.append(tid)
                pass
            pass
        t = time.time()
        if map.method == 0:
            ClusterAllocation(BTset)
        elif map.method == 1:
            NestestNeighborClusteringandRouting(BTset)
        elif map.method == 2:
            IIG_comparedALG(BTset)
        elif map.method == 3:
            Kmeans(BTset)
        # ClusterAllocation(BTset)
        # IIG_comparedALG(BTset)
        # Kmeans(BTset)
        # NestestNeighborClusteringandRouting(BTset)

        map.processingtime += time.time()-t

        # print("Time:", time.time()-t)
        pass
    for aid in map.agentSet.Aset.keys():
        getCostandTime(aid)
    print("----------------------------")
    overdue = 0
    serverTime = 0
    for tid in map.taskSet.Tset.keys():
        # print("Task", tid, "complete time:", map.taskSet.Tset[tid].completeTime)
        if map.taskSet.Tset[tid].completeTime == -1:
            overdue+=1
        else:
            serverTime += map.taskSet.Tset[tid].completeTime - map.taskSet.Tset[tid].startTime
            if map.taskSet.Tset[tid].completeTime > map.ms:
                map.ms = map.taskSet.Tset[tid].completeTime
                # print("Task", tid, "complete time:", map.taskSet.Tset[tid].completeTime, "startTime:", map.taskSet.Tset[tid].startTime)
                pass
            if map.taskSet.Tset[tid].completeTime > map.taskSet.Tset[tid].endTime:
                overdue += 1
                pass

    print("----------------------------")
    print("Overdue:", overdue)
    print("TaskNum:", len(map.taskSet.Tset))
    print("AgentNum", len(map.agentSet.Aset))
    print("size", map.agentSet.capacity)
    print("Batch:", map.config.batch)
    if map.method == 0:
        print("Method: TGA")
    elif map.method == 1:
        print("Method: nCAR")
    elif map.method == 2:
        print("Method: IIG")
    elif map.method == 3:
        print("Method: K-means")
    print("OverdueRate:",1- overdue/len(map.taskSet.Tset))

    # print("ST:", map.ST)
    print("ServerTime:", serverTime)
    print("Makespan", map.ms)
    print("ProcessingTime:", map.processingtime)
    pass

if __name__ == '__main__':
    if len(sys.argv) < 4:
        taskNum = 2000
        agentNum = 50
        capacity = 3
        batch = 30
        method = 3
    else:
        taskNum = int(sys.argv[1])
        agentNum = int(sys.argv[2])
        capacity = int(sys.argv[3])
        batch = int(sys.argv[4])
        method = int(sys.argv[5])
    
    map.taskSet = TaskSet(map.filename, taskNum)
    map.agentSet = AgentSet(map.filename, agentNum, capacity)
    map.config.batch = batch
    map.method = method
    run()
    pass

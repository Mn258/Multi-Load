
from tkinter import N
from MultiLoad.map import *
from MultiLoad.task import *
from MultiLoad.agent import *
from Algorithm.algorithm import *



def run():
    while len(map.taskSet.taskId) > 0:
        map.timestep += map.config.batch
        # updatePosition
        i = 0
        
        paths = []
        for aid in map.agentSet.Aset.keys():
            # map.agentSet.Aset[aid].updatePosition(config.batch)
            path = updatePosition(map.config.batch, aid)
            paths.append(path)
            pass
        # allocateTask
        kk=0
        while kk <map.config.batch:
            ps = []
            for i in range(len(paths)):
                if paths[i] != None and kk < len(paths[i]):
                    if paths[i][kk] in ps:
                        map.ST += 3
                        ps.append(paths[i][kk])
                        pass
                    else :
                        ps.append(paths[i][kk])
                    pass
                pass
            kk+=1
            pass
        BTset:List[int] = []
        for tid in map.taskSet.taskId:
            if map.taskSet.Tset[tid].startTime <= map.timestep:
                BTset.append(tid)
                pass
            pass
        # t = time.time()

        # CombinatorialAuction(BTset, AgentSet)
        ClusterAllocation(BTset)
        # compareALG(BTset)

        # print("Time:", time.time()-t)
        pass
    for aid in map.agentSet.Aset.keys():
        getCostandTime(aid)
    print("----------------------------")
    overdue = 0
    serverTime = 0
    for tid in map.taskSet.Tset.keys():
        serverTime += map.taskSet.Tset[tid].completeTime - map.taskSet.Tset[tid].startTime
        print("Task", tid, "complete time:", map.taskSet.Tset[tid].completeTime)
        if map.taskSet.Tset[tid].completeTime > map.taskSet.Tset[tid].endTime:
            overdue+=1
    print("Overdue:", overdue)
    print("----------------------------")
    print("ST:", map.ST)
    print("ServerTime:", serverTime)
    pass

if __name__ == '__main__':
    map.taskSet = TaskSet(map.filename, 1000)
    map.agentSet = AgentSet(map.filename, 70, 3)
    run()
    pass
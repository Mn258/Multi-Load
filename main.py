from MultiLoad.map import *
from MultiLoad.task import *
from MultiLoad.agent import *
from Algorithm.algorithm import *



def run():
    while len(map.taskSet.taskId) > 0:
        map.timestep += map.config.batch
        # updatePosition
        for aid in map.agentSet.Aset.keys():
            # map.agentSet.Aset[aid].updatePosition(config.batch)
            updatePosition(map.config.batch, aid)
            pass
        # allocateTask
        BTset:List[int] = []
        for tid in map.taskSet.taskId:
            if map.taskSet.Tset[tid].startTime <= map.timestep:
                BTset.append(tid)
                pass
            pass
        # CombinatorialAuction(BTset, AgentSet)
        ClusterAllocation(BTset)
        pass
    for aid in map.agentSet.Aset.keys():
        getCostandTime(aid)
    print("----------------------------")
    overdue = 0
    for tid in map.taskSet.Tset.keys():
        print("Task", tid, "complete time:", map.taskSet.Tset[tid].completeTime)
        if map.taskSet.Tset[tid].completeTime > map.taskSet.Tset[tid].endTime:
            overdue+=1
    print("Overdue:", overdue)
    print("----------------------------")
    print("ST:", map.ST)
    pass

if __name__ == '__main__':
    map.taskSet = TaskSet(map.filename, 1000)
    map.agentSet = AgentSet(map.filename, 30, 3)
    run()
    pass

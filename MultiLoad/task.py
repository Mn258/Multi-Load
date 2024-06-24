from typing import List


class Task:
    def __init__(self, st:int = 0, et:int = 0, sp:List[int] = [0,0], ep:List[int] = [0,0]) -> None:
        self.startTime = st
        self.endTime = et
        self.completeTime = 0
        self.startPoint = sp
        self.endPoint = ep
        pass
    pass


class TaskSet:
    def __init__(self, filename:str = "", numTask:int = 0):
        self.filename = filename + "." + str(numTask) + ".task"
        self.numTask = numTask
        self.Tset:dict[int, Task] = {}
        self.taskId:List[int] = []
        self.getTaskFromFile()
        pass

    

    def getTaskFromFile(self):
        if self.filename == "":
            return None
        # self.Tset:List[Task] = []
        with open("Task/"+self.filename, 'r') as f:
            # read header type of map
            line = f.readline()
            self.numTask = int(line.split(" ")[1])
            f.readline()
            for i in range(1,self.numTask+1):
                line = f.readline()
                st = int(line.split(" ")[0])
                et = int(line.split(" ")[1])
                sp = [int(line.split(" ")[2]), int(line.split(" ")[3])]
                ep = [int(line.split(" ")[4]), int(line.split(" ")[5])]
                # self.Tset.append(Task(st, et, sp, ep))
                self.Tset[i] = Task(st, et, sp, ep)
                self.taskId.append(i)
        # self.Tset.sort(key = lambda x: x.startTime)
        # for i in range(self.numTask):
        #     self.Tset[i].id = i
        pass

    def sortTask(self):
        self.Tset.sort(key = lambda x: x.startTime)
        pass

    def __del__(self):
        del self.Tset
        pass
    pass


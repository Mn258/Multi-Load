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
    
    pass

if __name__ == "__main__":
    print("Hello World")
    pass
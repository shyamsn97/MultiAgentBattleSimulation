from collections import deque

class Memory():
    def __init__(self,max_len=None):
        self.max_len = max_len
        self.flush()

    def flush(self):
        self.d = deque()
        if self.max_len != None:
            self.d = deque(max_len=self.max_len)

    def add(self,state,action,reward,action_probs=None):
        mem_dict = {"state":state,"action":action,"reward":reward,"action_probs":action_probs}
        self.d.append(mem_dict)

    def getMem(self):
        return self.d

    def pop(self):
        return self.d.pop()

    def __getitem__(self,index):
        return sef.d[i]

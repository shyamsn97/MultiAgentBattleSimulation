from collections import deque


class Memory:
    def __init__(self, max_len=None):
        self.max_len = max_len
        self.flush()

    def flush(self):
        self.d = deque()
        if self.max_len is not None:
            self.d = deque(max_len=self.max_len)

    def add(self, state, action, valid_actions, reward, action_probs):
        mem_dict = {
            "state": state,
            "action": action,
            "valid_actions": valid_actions,
            "reward": reward,
            "action_probs": action_probs,
        }
        self.d.append(mem_dict)

    def getMem(self):
        return self.d

    def pop(self):
        return self.d.pop()

    def __len__(self):
        return len(self.d)

    def __getitem__(self, index):
        return (
            self.d[index]["state"],
            self.d[index]["action"],
            self.d[index]["valid_actions"],
            self.d[index]["reward"],
            self.d[index]["action_probs"],
        )

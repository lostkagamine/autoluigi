import melee

class ActionQueue:
    def __init__(self):
        self.reset()

    def reset(self):
        self.actions = []
        self.current_frame = 0
    
    def push(self, act):
        'Adds an action to the queue to be completed.'
        self.actions.append(act)

    def force_push(self, act):
        'Adds an action directly to the start of the queue.'
        self.actions.insert(0, act)

    def replace(self, act, what):
        'Replaces an action in the queue.'
        idx = None
        for i, v in enumerate(self.actions):
            if v == act:
                idx = i
                break
        if idx == None:
            raise ValueError('No such action!')
        self.actions[idx] = v
        self.current_frame = 0

    def remove(self, act):
        'Removes an action from the queue.'
        self.actions.remove(act)
        self.current_frame = 0

    def play(self, gs, pad):
        'Plays the current actions in the queue. Called every frame.'

        if len(self.actions) == 0:
            return

        act = self.actions[0] # Head of the actions
        self.current_frame = self.current_frame + 1
        act.play(pad, gs, self, self.current_frame)
        if act.done(gs):
            # Pop it off
            self.actions.pop(0)
            self.current_frame = 0

    def neutral(self):
        'Are there any more actions in queue?'
        return len(self.actions) == 0
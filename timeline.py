import melee
import actions

class TLB:
    def __init__(self):
        self.length = 0
        self.button = melee.Button.BUTTON_A
        self.down = True
        self.stickvals = (0.5, 0.5)
        self.function = None
        self.precond = None

    @classmethod
    def press(c, what, howlong):
        b = c()
        b.length = howlong
        b.button = what
        b.down = True
        return b
    
    @classmethod
    def release(c, what, howlong):
        b = c()
        b.length = howlong
        b.button = what
        b.down = True
        return b

    @classmethod
    def stick(c, what, x, y, t):
        b = c()
        b.length = t
        b.button = what
        b.stickvals = (x, y)
        return b

    @classmethod
    def call(c, fnc):
        b = c()
        b.function = fnc
        return b

    @classmethod
    def wait_for(c, state):
        b = c()
        b.button = None
        
        def waitfor2(pad, gs):
            return gs.players[2].action == state

        b.precond = waitfor2
        return b

    @classmethod
    def clear(c):
        b = c()
        b.function = lambda pad, gs: pad.empty_input()
        return b
    
    def process(self, pad, gs):
        if self.function:
            self.function(pad, gs)
            return

        if self.button == None:
            return

        if (self.button == melee.Button.BUTTON_MAIN or self.button == melee.Button.BUTTON_C):
            # this is actually an analog input
            pad.tilt_analog(self.button, self.stickvals[0], self.stickvals[1])
        else:
            if self.down:
                pad.press_button(self.button)
            else:
                pad.release_button(self.button)

class TimelineAction(actions.BaseAction):
    def __init__(self):
        self.actions = []
        self.time = 0
        self.currtime = 0
        self.leftover = 0

    def play(self, pad, gs, q, f):
        #print(self.leftover)
        #print(len(self.actions))
        self.time = self.time + 1
        self.currtime = self.currtime + 1

        advance1 = (self.leftover <= 0 and len(self.actions) != 0)
        has_precond = self.actions[0].precond != None
        precond = self.actions[0].precond
        
        if (not has_precond and advance1) or (has_precond and precond(pad, gs)):
            # next one
            act = self.actions[0]
            act.process(pad, gs)
            self.leftover = act.length
            self.actions.pop(0)
            self.currtime = 0
        else:
            self.leftover = self.leftover - 1

    def done(self, gs):
        return len(self.actions) == 0 and self.leftover <= 0

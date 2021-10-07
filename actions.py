import melee
import math

class BaseAction:
    def play(self, pad, gamestate, queue, frame):
        pass

    def done(self, gs):
        return True

class ApproachOpponentAction(BaseAction):
    name = "ApproachOpponent"

    def play(self, pad, gamestate, queue, frame):
        us = gamestate.players[2]
        other = gamestate.players[1]
        posdelta = abs(us.position.y-other.position.y)
        if posdelta <= 5:
            queue.remove(self)
            queue.force_push(WavedashAction())
            return
        to_left = other.position.x < us.position.x
        val = 1-int(to_left)
        pad.tilt_analog(melee.Button.BUTTON_MAIN, val, 0.5)

    def done(self, gs):
        return gs.distance < 4

class RestAttackAction(BaseAction):
    name = "RestAttack"

    def play(self, pad, gamestate, queue, frame):
        pad.tilt_analog(melee.Button.BUTTON_MAIN, 0, 0.5)
        pad.press_button(melee.Button.BUTTON_B)

    def done(self, gs):
        return True

class GetUpFromLedgeAction(BaseAction):
    name = "GetUpFromLedge"

    def play(self, pad, gs, q, f):
        us = gs.players[2]
        # where are we?
        edge = melee.stages.EDGE_POSITION[melee.Stage.FINAL_DESTINATION]
        edge_left = -edge # left-side
        edge_fudge = edge_left + 1 # fudge by one melee unit just in-case
        # are we hanging from left edge?
        on_left_edge = us.position.x < edge_fudge
        
        #input left for left edge, right for right edge
        pad.tilt_analog(melee.Button.BUTTON_MAIN, 1-int(on_left_edge), 0.5)

    def done(self, gs):
        return True

class RecoverAction(BaseAction):
    name = "Recover"

    def __init__(self):
        self.jump_delay = 20
        self.jump_timer = 0

    def play(self, pad, gs, q, f):
        us = gs.players[2]
        edge = melee.stages.EDGE_POSITION[melee.Stage.FINAL_DESTINATION]
        edge_left = -edge # left-side
        edge_fudge = edge_left + 1 # fudge by one melee unit just in-case
        # are we off left edge?
        on_left_edge = us.position.x < edge_fudge

        # we're off the stage
        if self.jump_timer <= 0:
            pad.press_button(melee.Button.BUTTON_Y)
            self.jump_timer = self.jump_delay
        else:
            pad.release_button(melee.Button.BUTTON_Y)
            self.jump_timer = self.jump_timer - 1
        pad.tilt_analog(melee.Button.BUTTON_MAIN, int(on_left_edge), 0.5)

    def done(self, gs):
        return not gs.players[2].off_stage

import timeline as tl

class WavedashAction(tl.TimelineAction):
    name = "Wavedash"

    def __init__(self):
        super().__init__()

        def stick_action(pad, gs):
            us = gs.players[2]
            other = gs.players[1]
            to_left = other.position.x < us.position.x
            val = 1-int(to_left)
            pad.tilt_analog(melee.Button.BUTTON_MAIN, val, .35)

        self.actions = [
            tl.TLB.wait_for(melee.Action.STANDING),
            tl.TLB.press(melee.Button.BUTTON_Y, 2),
            tl.TLB.call(stick_action),
            tl.TLB.press(melee.Button.BUTTON_L, 0),
            tl.TLB.clear()
        ]

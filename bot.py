import melee
from actionqueue import ActionQueue
import actions

slippi_path = "C:/Users/Rin/AppData/Roaming/Slippi Launcher/netplay"

console = melee.Console(path=slippi_path)

controller = melee.Controller(console=console, port=2)
#controller_human = melee.Controller(console=console,
#                                    port=2,
#                                    type=melee.ControllerType.STANDARD)

console.run()
console.connect()

controller.connect()
#controller_human.connect()

queue = ActionQueue()

def force_acts(gamestate, controller):
    if gamestate.players[2].action == melee.Action.EDGE_HANGING:
        # We are hanging off ledge
        # Let's get up
        queue.reset() # Reset everything to make sure this happens
        queue.force_push(actions.GetUpFromLedgeAction())
        return

    if gamestate.players[2].off_stage:
        # We are off stage
        # Let's recover
        queue.reset()
        queue.force_push(actions.RecoverAction())
        return

while True:
    gamestate = console.step()
    if gamestate.menu_state in [melee.Menu.IN_GAME, melee.Menu.SUDDEN_DEATH]:
        # gameplay 

        force_acts(gamestate, controller)

        queue.play(gamestate, controller)

        if not queue.neutral():
            continue

        # No actions, enqueue one
        controller.empty_input()
        controller.tilt_analog(melee.Button.BUTTON_MAIN, 0.5, 0.5)
        queue.push(actions.ApproachOpponentAction())
    else:
        melee.MenuHelper.menu_helper_simple(gamestate,
                                    controller,
                                    melee.Character.LUIGI,
                                    melee.Stage.FINAL_DESTINATION,
                                    "",
                                    costume=1,
                                    autostart=False,
                                    swag=False)
    # Press buttons on your controller based on the GameState here!
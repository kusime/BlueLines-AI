
from STAT.Base_State import BaseState


class BattleDoing(BaseState):
    def EnterState(self, game):
        print("Current state is BattleDoing..")

    def UpdateState(self, game):
        # check if game is finished
        currentStatePredict = game.getCurrentStateAndSetPoint()
        if (currentStatePredict != None and currentStatePredict == game.BattleStatus.Done):
            # switch to the BattleDone State
            game.SwitchState(game.BattleDone)
            return
        print("waiting for game to finish...")
        game.waiter()


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

        # check if game is already go to the pending state since the confirm click
        # enhance the threshold to avoid the caracter identity collision
        currentStatePredict = game.getCurrentStateAndSetPoint()
        if (currentStatePredict != None and currentStatePredict == game.BattleStatus.Pending):
            # switch to the BattleDone State
            game.SwitchState(game.BattlePending)
            return

        # check if have confirm button , this cause by the net work connection error
        # check if still have some comfirm information
        predict = game.GenerticAI.getStablePredictions(10, 0.9)
        if (predict != None):
            print("Confirming the Confirm ...")
            game.Phone.tap(predict[0]['point'])
            game.waiter()
            return
        else:
            game.Phone.tap((1200, 534))
        game.waiter()

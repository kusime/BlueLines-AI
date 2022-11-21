
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
        
        # check if have confirm button , this cause by the net work connection error
        # check if still have some comfirm information
        predict = game.GenerticAI.getStablePredictions()
        if (predict != None and predict[0]['label'] == game.GenerticButton.Confirm):
            print("Confirming the Confirm ...")
            game.Phone.tap(predict[0]['point'])
            game.waiter()
        
        print("waiting for game to finish...")
        game.waiter()

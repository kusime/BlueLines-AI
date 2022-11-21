
from STAT.Base_State import BaseState


class BattleDone(BaseState):
    def EnterState(self, game):
        print("Current state is BattleDone..")

    def UpdateState(self, game):
        # game is finished tap the screen to Skip the S screen
        if (game.CurrentStatusPoint != None):
            game.Phone.tap(game.CurrentStatusPoint)
            game.CurrentStatusPoint = None
            # cleanup the click buffer

        predict = game.GenerticAI.getStablePredictions()
        if (predict != None and predict[0]['label'] == game.GenerticButton.ItemsRec):
            print("Confirming the ItemsRecieved ...")
            game.Phone.tap(predict[0]['point'])
            game.waiter()

        predict = game.GenerticAI.getStablePredictions()
        if (predict != None and predict[0]['label'] == game.GenerticButton.Confirm):
            print("Confirming the Confirm ...")
            game.Phone.tap(predict[0]['point'])
            game.waiter()

        # check if game is go to pending page
        currentStatePredict = game.getCurrentStateAndSetPoint()
        print(currentStatePredict)
        if (currentStatePredict != None and currentStatePredict == game.BattleStatus.Pending):
            # switch to the BattleDone State
            game.SwitchState(game.BattlePending)


from STAT.Base_State import BaseState


class BattleDone(BaseState):
    def EnterState(self, game):
        # reset the counter
        game.fixPoint = 0
        print("Current state is BattleDone..")

        if (game.CurrentStatusPoint != None):
            print("Confirming the BattleDone state ..")
            # check s
            game.Phone.tap(game.CurrentStatusPoint)
            game.waiter(1)
            # check items recieved

        # check confirm
        predict = game.GenerticAI.getStablePredictions()
        if (predict != None and predict[0]['label'] == game.GenerticButton.Confirm):
            print("Confirming the Confirm ...")
            game.Phone.tap(predict[0]['point'])
            game.waiter()

    def UpdateState(self, game):
        # game is finished tap the screen to Skip the S screen
        game.waiter()

        # try to recomfirm since the enterstate check is not work
        predict = game.GenerticAI.getStablePredictions(10, 0.7)
        print(predict)
        if (predict != None and predict[0]['label'] == game.GenerticButton.ItemsRec):
            print("Confirming the ItemsRecieved ...")
            game.Phone.tap(predict[0]['point'])
            game.waiter()

        # cannot use cache here because of the threshold between itemsreceived and confirm is not the same
        predict = game.GenerticAI.getStablePredictions(10, 0.9)
        if (predict != None and predict[0]['label'] == game.GenerticButton.Confirm):
            print("Confirming the Confirm ...")
            game.Phone.tap(predict[0]['point'])
            game.waiter()

        # check if game is go to pending page
        currentStatePredict = game.getCurrentStateAndSetPoint(30, 0.9)
        if (currentStatePredict != None and currentStatePredict == game.BattleStatus.Pending):
            # switch to the BattleDone State
            game.SwitchState(game.BattlePending)
            return

        # check if game is go to pending page
        currentStatePredict = game.getCurrentStateAndSetPoint(30, 0.9)
        if (currentStatePredict != None and currentStatePredict == game.BattleStatus.Doing):
            # switch to the BattleDone State
            game.SwitchState(game.BattleDoing)
            return

        # todo : check if already finished this chapter ...
        # maybe encounter the new caracter recieved
        if (predict == None):
            print(
                "Current state is BattleDone but Current is unmet the BattlePending after all confirm been click so this caused by chapter finished ... or charater recieved")
            fixPoint = game.autoFixMissingTarget.getFixPoint()
            if (fixPoint != None):
                print("Currently make auto fix to handler this situation..")
                game.Phone.tap(fixPoint)
                game.waiter()
            else:
                print("all strage is used out .. now make alert")
                game.autoFixMissingTarget.getAlert()
                game.waiter()

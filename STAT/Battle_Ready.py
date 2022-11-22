from STAT.Base_State import BaseState


class BattleReady(BaseState):

    def EnterState(self, game):
        print("Current state is BattleReady..")

    def UpdateState(self, game):
        game.waiter()
        # check if still have some comfirm information
        predict = game.GenerticAI.getStablePredictions()
        if (predict != None):
            print("Confirming the Confirm ... or items recieved")
            game.Phone.tap(predict[0]['point'])
            game.waiter()

        # check if is really ready to the BattleDoing
        statePredict = game.getCurrentStateAndSetPoint()
        if (statePredict != None and statePredict == game.BattleStatus.Doing):
            # switch to the BattleDoing state
            game.SwitchState(game.BattleDoing)
            return

        # revoke the Ready State
        self.UpdateState(game)

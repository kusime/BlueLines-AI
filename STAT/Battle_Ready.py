from STAT.Base_State import BaseState


class BattleReady(BaseState):

    def EnterState(self, game):
        print("Current state is BattleReady..")

    def UpdateState(self, game):

        # check if still have some comfirm information
        predict = game.GenerticAI.getStablePredictions()
        if (predict != None and predict[0]['label'] == game.GenerticButton.Confirm):
            print("Confirming the Confirm ...")
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

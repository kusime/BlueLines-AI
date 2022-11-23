from STAT.Base_State import BaseState


class BattleReady(BaseState):

    def EnterState(self, game):
        print("Current state is BattleReady..")
        game.waiter(0.5)
        # check if still have some comfirm information
        predict = game.GenerticAI.getStablePredictions()
        if (predict != None):
            print("Confirming the Start battle")
            game.Phone.tap(predict[0]['point'])
            game.waiter()

    def UpdateState(self, game):
        # check if is really ready to the BattleDoing
        statePredict = game.getCurrentStateAndSetPoint()
        if (statePredict != None and statePredict == game.BattleStatus.Doing):
            # switch to the BattleDoing state
            game.SwitchState(game.BattleDoing)
            return

        # check if is already to the BattlePending state
        statePredict = game.getCurrentStateAndSetPoint()
        if (statePredict != None and statePredict == game.BattleStatus.Pending):
            # switch to the BattleDoing state
            game.SwitchState(game.BattlePending)
            return

        # fresh cache
        if (statePredict == None):
            # check if is already to the BattleDone state
            statePredict = game.getCurrentStateAndSetPoint()

        if (statePredict != None and statePredict == game.BattleStatus.Done):
            # switch to the BattleDoing state
            game.SwitchState(game.BattleDone)
            return

        # check if still have some comfirm information
        predict = game.GenerticAI.getStablePredictions()
        if (predict != None):
            print("EnterState confirm not work .. try again with genertic confirm")
            game.Phone.tap(predict[0]['point'])
            game.waiter()
        # revoke the Ready State
        self.UpdateState(game)

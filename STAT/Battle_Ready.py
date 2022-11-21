from STAT.Base_State import BaseState


class BattleReady(BaseState):

    def EnterState(self, game):
        print("Current state is BattleReady..")

    def UpdateState(self, game):
        # waiting for the confirm to doing state
        confirmPoint = game.GenerticAI.getStablePredictions()[0]['point']
        game.Phone.tap(confirmPoint)
        # switch to the BattleDoing State
        game.waiter(3)
        game.SwitchState(game.BattleDoing)

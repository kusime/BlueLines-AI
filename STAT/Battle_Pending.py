from STAT.Base_State import BaseState


class BattlePending(BaseState):
    currentTime = None
    stagedMonsterPoint = None

    def MonsterSelectOptimizer(self, game):
        # MonsterPredict Guard
        if (len(self.MonsterPredict) == 0):
            print("ther is no monster in the cache , restrat the Pending State")
            self.EnterState(game)

        if (self.currentTime == None):
            self.stagedMonster = self.MonsterPredict.pop()['point']
            return self.stagedMonster

        print(self.currentTime, self.stagedMonster)

        if (self.currentTime == self.stagedMonster):
            print("this point not work , so we need to try the offset 190px")
            x, y = self.stagedMonster
            return (x, y-190)
        else:
            print("not work ,try the pop new point")
            self.stagedMonster = self.MonsterPredict.pop()['point']
            return self.stagedMonster

    def EnterState(self, game):
        print("Current state is BattlePending..")
        print("ready select the Monster")
        # to do this can be auto optimized
        self.MonsterPredict = game.MonsterAI.getStablePredictions(120, 0.3)
        print(f"Monste predictions summary {self.MonsterPredict}")
        # clear the cache
        self.currentTime = None
        self.stagedMonsterPoint = None

    def UpdateState(self, game):
        # go to the monster
        if (self.MonsterPredict != None):
            self.currentTime = self.MonsterSelectOptimizer(game)
            print(f"Proccessing Monster at {self.currentTime}")
            game.Phone.tap(self.currentTime)
            game.waiter()
        else:
            print("No Monster was founded... Reasting the Pending State...")
            self.EnterState(game)

        # check if is really ready to the Ready state
        statePredict = game.getCurrentStateAndSetPoint()
        print(statePredict)
        if (statePredict != None and statePredict == game.BattleStatus.Ready):
            # switch to the BattleReady state
            game.SwitchState(game.BattleReady)
            return

        # check if is already  to the BattleDoing
        statePredict = game.getCurrentStateAndSetPoint()
        print(statePredict)
        if (statePredict != None and statePredict == game.BattleStatus.Doing):
            # switch to the BattleReady state
            game.SwitchState(game.BattleDoing)
            return

        # check if encounter the items recieved status or confirm status
        # AI BUG: the PendingStatus will always have the confirm button
        predict = game.GenerticAI.getStablePredictions()
        if (predict != None):
            print("Confirming the status ...")
            game.Phone.tap(predict[0]['point'])

        # still in the Pending state recalling again
        self.UpdateState(game)

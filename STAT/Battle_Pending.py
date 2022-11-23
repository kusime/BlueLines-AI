from STAT.Base_State import BaseState


class BattlePending(BaseState):
    currentTime = None
    stagedMonsterPoint = None

    def MonsterSelectOptimizer(self, game):
        # MonsterPredict Guard
        if (self.MonsterPredict == []):
            print("ther is no monster in the cache , restrat the Pending State")
            self.EnterState(game)

        if (self.currentTime == None):
            self.stagedMonster = self.MonsterPredict.pop()['point']
            return self.stagedMonster

        # print(self.currentTime, self.stagedMonster)

        if (self.currentTime == self.stagedMonster):
            # add guard to check if already in the ready state
            # check if is  already to the Ready state
            statePredict = game.getCurrentStateAndSetPoint()
            if (statePredict != None and statePredict == game.BattleStatus.Ready):
                print("current time we are going to offset but state guard check current state is BattleReady so switch to the Ready state.. Optimizer retrun None")
                print("switch to the BattleReady state")
                game.SwitchState(game.BattleReady)
                return None
            if (statePredict != None and statePredict == game.BattleStatus.Doing):
                # switch to the BattleDoing state
                print("current time we are going to offset but state guard check current state is BattleReady so switch to the Ready state.. Optimizer retrun None")
                print("switch to the BattleDoing state")
                game.SwitchState(game.BattleDoing)
                return None
            print("MonsterSelectOptimizer Guard Check passed , returing new Point")
            print("this point not work , so we need to try the offset 190px")
            x, y = self.stagedMonster
            return (x, y-190)
        else:
            print("not work ,try the pop new point")
            self.stagedMonster = self.MonsterPredict.pop()['point']
            return self.stagedMonster

    def EnterState(self, game):
        print("Current state is BattlePending..")

        if (game.LoadBalancer % 2 == 1):
            print("Now activating the LoadBalancer")
            game.Phone.tap((2027, 1502))
            game.waiter()

        # to do this can be auto optimized
        self.MonsterPredict = game.MonsterAI.getStablePredictions(60, 0.6)
        print("ready select the Monster")
        if (self.MonsterPredict == None):
            print(
                "Enter the BattlePending state but no monster found... is there already on other state ?")
            # check if is really ready to the Ready state
            statePredict = game.getCurrentStateAndSetPoint()
            print(statePredict)
            if (statePredict != None and statePredict == game.BattleStatus.Ready):
                # switch to the BattleReady state
                game.SwitchState(game.BattleReady)
                return
            game.waiter()

            # check if is alreally to the BattleDone state
            statePredict = game.getCurrentStateAndSetPoint()
            print(statePredict)
            if (statePredict != None and statePredict == game.BattleStatus.Done):
                # switch to the BattleReady state
                game.SwitchState(game.BattleDone)
                return
            game.waiter()

            # check if is alreally to the BattleDoing state
            statePredict = game.getCurrentStateAndSetPoint()
            print(statePredict)
            if (statePredict != None and statePredict == game.BattleStatus.Doing):
                # switch to the BattleReady state
                game.SwitchState(game.BattleDoing)
                return
            game.waiter()


            # check if game still in the pending state
            statePredict = game.getCurrentStateAndSetPoint()
            if (statePredict != None and statePredict == game.BattleStatus.Pending):
                print(
                    "Current state is BattlePending but no monster is founded , so maybe the MonsterAI is missing the target ...")
                fixPoint = game.autoFixMissingTarget.getFixPoint()
                if (fixPoint != None):
                    print("Currently make auto fix to handler this situation..")
                    game.Phone.tap(fixPoint)
                    game.waiter()
                else:
                    print("all strage is used out .. now make alert")
                    game.autoFixMissingTarget.getAlert()
                # restart the Pending State
                # add the LoadBalancer
                game.LoadBalancer += 1

            # check if we have confirm
            predict = game.GenerticAI.getStablePredictions(10, 0.94)
            if (predict != None):
                print("Confirming the status ...")
                game.Phone.tap(predict[0]['point'])
            self.EnterState(game)

        print(
            f"Monste predictions summary : {len(self.MonsterPredict)} was founded..")
        # clear the cache
        self.currentTime = None
        self.stagedMonsterPoint = None
        # add the LoadBalancer
        game.LoadBalancer += 1

    def UpdateState(self, game):
        # go to the monster
        if (self.MonsterPredict != None):
            self.currentTime = self.MonsterSelectOptimizer(game)
            # already guard go to next state
            if (self.currentTime == None):
                return
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
        # AI BUG increment the the threshold to avoid click withdraw ..
        # But we still need to use this functionality because of handler network error or new mission during the battle pending state ..
        predict = game.GenerticAI.getStablePredictions(10, 0.94)
        if (predict != None):
            print("Confirming the status ...")
            game.Phone.tap(predict[0]['point'])

        # still in the Pending state recalling again
        self.UpdateState(game)

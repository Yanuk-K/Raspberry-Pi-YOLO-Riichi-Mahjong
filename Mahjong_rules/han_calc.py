# find yaku from has_yaku, if no yaku return 0 han -> bappu

class Han:
    def __init__(self, menzen_score, score):
        self.menzen_score = menzen_score
        self.score = score

    def yakuScore(self, hands, menzen):
        if self.hasYaku(hands):
            return self.menzen_score if menzen else self.score
        else:
           return 0

    def hasYaku(self, hands):
        # return true if we have a yaku; will be overridden
        return True
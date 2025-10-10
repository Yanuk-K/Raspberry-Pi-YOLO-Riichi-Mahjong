from Mahjong_rules.Yaku.utils import HandContext, Yaku, is_chiitoitsu


class Chiitoitsu(Yaku):
    def __init__(self) -> None:
        super().__init__("Chiitoitsu", 2, 0)

    def hasYaku(self, ctx: HandContext) -> bool:
        return is_chiitoitsu(ctx)


__all__ = ["Chiitoitsu"]

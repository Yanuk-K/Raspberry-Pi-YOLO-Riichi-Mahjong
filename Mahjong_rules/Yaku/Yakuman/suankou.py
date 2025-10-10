from Mahjong_rules.Yaku.utils import HandContext, Yaku, concealed_triplet_count


class Suankou(Yaku):
    def __init__(self) -> None:
        super().__init__("Suankou", 13, 13)

    def hasYaku(self, ctx: HandContext) -> bool:
        for pattern in ctx.enumerate_patterns():
            if concealed_triplet_count(ctx, pattern) == 4:
                return True
        return False


__all__ = ["Suankou"]

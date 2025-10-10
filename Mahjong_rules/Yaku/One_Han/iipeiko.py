from collections import Counter

from Mahjong_rules.Yaku.utils import HandContext, Yaku, sequence_signature


class Iipeiko(Yaku):
    def __init__(self) -> None:
        super().__init__("Iipeiko", 1, 0)

    def hasYaku(self, ctx: HandContext) -> bool:
        if not ctx.is_menzen:
            return False

        for pattern in ctx.enumerate_patterns():
            sequences = [
                sequence_signature(meld)
                for meld in pattern.concealed_melds
                if meld.is_sequence()
            ]
            if len(sequences) < 2:
                continue
            counts = Counter(sequences)
            if any(count >= 2 for count in counts.values()):
                return True
        return False


__all__ = ["Iipeiko"]

from collections import Counter

from Mahjong_rules.Yaku.utils import HandContext, Yaku, sequence_signature


class Ryanpeiko(Yaku):
    def __init__(self) -> None:
        super().__init__("Ryanpeiko", 3, 0)

    def hasYaku(self, ctx: HandContext) -> bool:
        if not ctx.is_menzen:
            return False

        for pattern in ctx.enumerate_patterns():
            sequences = [
                sequence_signature(meld)
                for meld in pattern.concealed_melds
                if meld.is_sequence()
            ]
            if len(sequences) < 4:
                continue
            counts = Counter(sequences)
            pair_count = sum(count // 2 for count in counts.values())
            if pair_count >= 2:
                return True
        return False


__all__ = ["Ryanpeiko"]

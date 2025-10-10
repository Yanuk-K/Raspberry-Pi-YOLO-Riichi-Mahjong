from Mahjong_rules.Yaku.utils import HandContext, Yaku


class Kazehai(Yaku):
    def __init__(self, target: str = "seat") -> None:
        target_normalized = target.lower()
        if target_normalized not in {"seat", "round"}:
            raise ValueError("target must be 'seat' or 'round'")
        label = "Seat Wind" if target_normalized == "seat" else "Prevalent Wind"
        super().__init__(f"Yakuhai ({label})", 1, 1)
        self.target = target_normalized

    def _target_key(self, ctx: HandContext) -> str:
        return ctx.seat_wind if self.target == "seat" else ctx.round_wind

    def hasYaku(self, ctx: HandContext) -> bool:
        target_key = self._target_key(ctx)
        if not target_key:
            return False

        for pattern in ctx.enumerate_patterns():
            for meld in pattern.all_melds():
                if not meld.is_triplet():
                    continue
                if all(tile_key == target_key for tile_key in meld.tile_keys):
                    return True
        return False


__all__ = ["Kazehai"]

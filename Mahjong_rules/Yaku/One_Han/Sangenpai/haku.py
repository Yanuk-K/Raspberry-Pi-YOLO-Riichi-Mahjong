from Mahjong_rules.Yaku.One_Han.sangenpai import DRAGON_KEYS, DragonYakuhai


class Haku(DragonYakuhai):
    def __init__(self) -> None:
        super().__init__("Yakuhai (Haku)", DRAGON_KEYS["haku"])


__all__ = ["Haku"]

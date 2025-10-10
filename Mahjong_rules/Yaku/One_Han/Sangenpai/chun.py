from Mahjong_rules.Yaku.One_Han.sangenpai import DRAGON_KEYS, DragonYakuhai


class Chun(DragonYakuhai):
    def __init__(self) -> None:
        super().__init__("Yakuhai (Chun)", DRAGON_KEYS["chun"])


__all__ = ["Chun"]

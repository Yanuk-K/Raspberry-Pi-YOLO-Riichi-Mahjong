from Mahjong_rules.Yaku.One_Han.sangenpai import DRAGON_KEYS, DragonYakuhai


class Hatsu(DragonYakuhai):
    def __init__(self) -> None:
        super().__init__("Yakuhai (Hatsu)", DRAGON_KEYS["hatsu"])


__all__ = ["Hatsu"]

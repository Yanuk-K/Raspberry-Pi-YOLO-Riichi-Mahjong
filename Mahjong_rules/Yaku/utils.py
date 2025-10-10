from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field
from typing import Dict, Iterable, Iterator, List, Optional, Set, Tuple

SUITS = ("m", "p", "s")
WINDS = ("E", "S", "W", "N")
DRAGONS = ("P", "F", "C")  # white (haku), green (hatsu), red (chun)
HONORS = WINDS + DRAGONS


class InvalidTileError(ValueError):
    """Raised when a tile string cannot be parsed."""


def _normalize_honor_name(name: str) -> str:
    upper = name.upper()
    honor_aliases = {
        "EAST": "E",
        "SOUTH": "S",
        "WEST": "W",
        "NORTH": "N",
        "HAKU": "P",
        "WHITE": "P",
        "SHIRO": "P",
        "HATSU": "F",
        "GREEN": "F",
        "RYU": "F",
        "RYUH": "F",
        "RYUHA": "F",
        "RYUHAI": "F",
        "RYUUI": "F",
        "RYUUII": "F",
        "RYUII": "F",
        "RYUISO": "F",
        "RYUI": "F",
        "RYUUII": "F",
        "RYUUII": "F",
        "CHUN": "C",
        "RED": "C",
        "AKA": "C",
        "ZHONG": "C",
    }
    if upper in honor_aliases:
        return honor_aliases[upper]
    if upper in HONORS:
        return upper
    raise InvalidTileError(f"Unrecognised honor tile name: {name}")


@dataclass(frozen=True)
class Tile:
    suit: str
    value: int
    red: bool = False

    @staticmethod
    def from_str(token: str) -> "Tile":
        token = token.strip()
        if not token:
            raise InvalidTileError("Empty tile string")

        if len(token) == 1 and not token.isdigit():
            honor = _normalize_honor_name(token)
            return Tile("z", HONOR_TO_INDEX[honor])

        # allow forms like "1m", "9p", "5s", "0m" (red), "5mr"
        suit = token[-1].lower()
        digits = token[:-1]
        if suit not in SUITS and suit != "z":
            # Maybe honor written as "1z".."7z"
            honor_token = token.upper()
            if honor_token in HONOR_FROM_INDEX:
                return Tile("z", int(honor_token[0]))
            raise InvalidTileError(f"Unknown tile token: {token}")

        red = False
        if digits.endswith(("r", "R")):
            red = True
            digits = digits[:-1]
        if not digits:
            raise InvalidTileError(f"Tile lacks value: {token}")
        if digits == "0":
            # red five in Tenhou notation
            red = True
            value = 5
        else:
            try:
                value = int(digits)
            except ValueError as exc:
                raise InvalidTileError(f"Tile has invalid number: {token}") from exc

        if suit in SUITS:
            if value < 1 or value > 9:
                raise InvalidTileError(f"Invalid tile value {value} for suit {suit}")
            return Tile(suit, value, red)

        if suit == "z":
            if value < 1 or value > 7:
                raise InvalidTileError(f"Invalid honour value {value}")
            return Tile("z", value)

        raise InvalidTileError(f"Unsupported tile token: {token}")

    @property
    def key(self) -> str:
        if self.suit == "z":
            return HONOR_FROM_INDEX[self.value]
        return f"{self.value}{self.suit}"

    @property
    def honour(self) -> Optional[str]:
        if self.suit != "z":
            return None
        return HONOR_FROM_INDEX[self.value]

    def is_honor(self) -> bool:
        return self.suit == "z"

    def is_terminal(self) -> bool:
        return self.suit in SUITS and self.value in (1, 9)

    def is_simple(self) -> bool:
        return self.suit in SUITS and 2 <= self.value <= 8

    def is_green(self) -> bool:
        if self.suit == "s" and self.value in (2, 3, 4, 6, 8):
            return True
        if self.suit == "z" and self.value == HONOR_TO_INDEX["F"]:
            return True
        return False

    def __str__(self) -> str:
        if self.suit == "z":
            return HONOR_FROM_INDEX[self.value]
        prefix = "0" if self.red and self.value == 5 else str(self.value)
        return f"{prefix}{self.suit}"


HONOR_TO_INDEX: Dict[str, int] = {
    honor: idx for idx, honor in enumerate(HONORS, start=1)
}
HONOR_FROM_INDEX: Dict[int, str] = {idx: honor for honor, idx in HONOR_TO_INDEX.items()}


def parse_tiles(tiles: Iterable[str]) -> List[Tile]:
    return [Tile.from_str(token) for token in tiles]


@dataclass
class Meld:
    tiles: Tuple[Tile, ...]
    kind: str
    is_open: bool = True
    called_tile: Optional[Tile] = None

    def __post_init__(self) -> None:
        if self.kind not in {"chi", "pon", "kan", "ankan", "kakan", "pair"}:
            raise ValueError(f"Unsupported meld kind: {self.kind}")
        if self.kind == "chi" and len(self.tiles) != 3:
            raise ValueError("Sequences must have exactly three tiles")
        if self.kind in {"pon", "kan", "ankan", "kakan"} and len(self.tiles) not in {
            3,
            4,
        }:
            raise ValueError("Triplets/quads must have three or four tiles")
        if self.kind == "pair" and len(self.tiles) != 2:
            raise ValueError("Pair must contain two tiles")

    @property
    def tile_keys(self) -> Tuple[str, ...]:
        return tuple(tile.key for tile in self.tiles)

    def is_sequence(self) -> bool:
        return self.kind == "chi"

    def is_triplet(self) -> bool:
        return self.kind in {"pon", "kan", "ankan", "kakan"}

    def is_quad(self) -> bool:
        return self.kind in {"kan", "ankan", "kakan"}

    def base_tile(self) -> Tile:
        return self.tiles[0]

    def suit(self) -> Optional[str]:
        if self.tiles:
            return self.tiles[0].suit
        return None


@dataclass(frozen=True)
class WaitDetail:
    kind: str
    source: Optional[int]  # -1 for pair, index in pattern.all_melds() otherwise, None unknown

    def is_shanpon(self) -> bool:
        return self.kind == "shanpon"

    def is_two_sided(self) -> bool:
        return self.kind == "ryanmen"

    def is_tanki(self) -> bool:
        return self.kind == "tanki"


@dataclass
class HandPattern:
    pair: Meld
    concealed_melds: List[Meld]
    open_melds: List[Meld]
    wait_details: Set[WaitDetail] = field(default_factory=set)

    def all_melds(self) -> List[Meld]:
        return self.open_melds + self.concealed_melds

    def sequences(self, include_open: bool = True) -> List[Meld]:
        melds = self.all_melds() if include_open else self.concealed_melds
        return [meld for meld in melds if meld.is_sequence()]

    def triplets(self, include_open: bool = True) -> List[Meld]:
        melds = self.all_melds() if include_open else self.concealed_melds
        return [meld for meld in melds if meld.is_triplet()]

    def quads(self, include_open: bool = True) -> List[Meld]:
        melds = self.all_melds() if include_open else self.concealed_melds
        return [meld for meld in melds if meld.is_quad()]

    def concealed_triplets(self) -> List[Meld]:
        triplets = [meld for meld in self.concealed_melds if meld.is_triplet()]
        return triplets


def indicator_to_tile(indicator: Tile) -> Tile:
    if indicator.suit in SUITS:
        value = indicator.value % 9 + 1
        return Tile(indicator.suit, value)
    honor = HONOR_FROM_INDEX[indicator.value]
    if honor in WINDS:
        next_index = (WINDS.index(honor) + 1) % len(WINDS)
        return Tile("z", HONOR_TO_INDEX[WINDS[next_index]])
    next_index = (DRAGONS.index(honor) + 1) % len(DRAGONS)
    return Tile("z", HONOR_TO_INDEX[DRAGONS[next_index]])


def _counter_from_tiles(tiles: Iterable[Tile]) -> Counter:
    counter: Counter = Counter()
    for tile in tiles:
        counter[tile.key] += 1
    return counter


@dataclass
class HandContext:
    concealed_tiles: List[Tile]
    melds: List[Meld] = field(default_factory=list)
    winning_tile: Optional[Tile] = None
    win_method: str = "ron"  # 'ron' or 'tsumo'
    seat_wind: str = "E"
    round_wind: str = "E"
    riichi: bool = False
    double_riichi: bool = False
    ippatsu: bool = False
    is_chankan: bool = False
    is_rinshan: bool = False
    is_haitei: bool = False
    is_houtei: bool = False
    nagashi_mangan: bool = False
    blessing: Optional[str] = None  # 'tenho', 'chiho', 'renho'
    dora_indicators: List[Tile] = field(default_factory=list)
    ura_dora_indicators: List[Tile] = field(default_factory=list)
    kan_dora_indicators: List[Tile] = field(default_factory=list)
    kan_ura_dora_indicators: List[Tile] = field(default_factory=list)
    red_five_tiles: List[Tile] = field(default_factory=list)
    pei_nuki_count: int = 0
    three_player: bool = False
    additional_flags: Dict[str, bool] = field(default_factory=dict)
    wait_type: Optional[str] = None

    _pattern_cache: Optional[List[HandPattern]] = field(
        default=None, init=False, repr=False
    )

    def __post_init__(self) -> None:
        self.seat_wind = _normalize_honor_name(self.seat_wind)
        self.round_wind = _normalize_honor_name(self.round_wind)

    @property
    def all_tiles(self) -> List[Tile]:
        tiles = list(self.concealed_tiles)
        for meld in self.melds:
            tiles.extend(meld.tiles)
        return tiles

    @property
    def tile_counter(self) -> Counter:
        return _counter_from_tiles(self.all_tiles)

    @property
    def is_menzen(self) -> bool:
        return all(not meld.is_open for meld in self.melds)

    def red_tile_count(self) -> int:
        if self.red_five_tiles:
            return len(self.red_five_tiles)
        return sum(1 for tile in self.all_tiles if tile.red)

    def total_kans(self) -> int:
        return sum(1 for meld in self.melds if meld.is_quad())

    def enumerate_patterns(self) -> List[HandPattern]:
        if self._pattern_cache is not None:
            return self._pattern_cache

        patterns: List[HandPattern] = []
        required_sets = 4 - len(self.melds)
        if required_sets < 0:
            self._pattern_cache = []
            return []

        tile_counter = _counter_from_tiles(self.concealed_tiles)

        if required_sets == 0:
            # Only need a pair from concealed tiles
            for key, count in tile_counter.items():
                if count >= 2:
                    pair_tile = Tile.from_str(key)
                    pair = Meld((pair_tile, pair_tile), "pair", is_open=False)
                    open_melds = list(self.melds)
                    pattern = HandPattern(pair, concealed_melds=[], open_melds=open_melds)
                    pattern.wait_details = self._compute_wait_details(pattern)
                    patterns.append(pattern)
            self._pattern_cache = patterns
            return patterns

        for pair_key, count in tile_counter.items():
            if count < 2:
                continue
            pair_tile = Tile.from_str(pair_key)
            pair = Meld((pair_tile, pair_tile), "pair", is_open=False)
            tile_counter[pair_key] -= 2
            concealed_meld_paths = list(
                _enumerate_concealed_melds(tile_counter, required_sets)
            )
            tile_counter[pair_key] += 2

            for concealed_melds in concealed_meld_paths:
                pattern = HandPattern(pair, concealed_melds=concealed_melds, open_melds=list(self.melds))
                pattern.wait_details = self._compute_wait_details(pattern)
                patterns.append(pattern)

        self._pattern_cache = patterns
        return patterns

    def _compute_wait_details(self, pattern: HandPattern) -> Set[WaitDetail]:
        if not self.winning_tile:
            return {WaitDetail("unknown", None)}

        wait_details: Set[WaitDetail] = set()
        winning_key = self.winning_tile.key
        # Pair wait
        if pattern.pair.tile_keys.count(winning_key) > 0:
            wait_details.add(WaitDetail("tanki", -1))

        for idx, meld in enumerate(pattern.all_melds()):
            if winning_key not in meld.tile_keys:
                continue
            if meld.is_triplet():
                wait_details.add(WaitDetail("shanpon", idx))
            elif meld.is_sequence():
                sorted_tiles = sorted(
                    (tile.value, tile.suit) for tile in meld.tiles if tile.suit in SUITS
                )
                if not sorted_tiles:
                    continue
                values = [value for value, _ in sorted_tiles]
                min_val = min(values)
                max_val = max(values)
                if min_val == 1 and max_val == 3 and self.winning_tile.value in {1, 3}:
                    wait_details.add(WaitDetail("penchan", idx))
                elif min_val == 7 and max_val == 9 and self.winning_tile.value in {7, 9}:
                    wait_details.add(WaitDetail("penchan", idx))
                elif self.winning_tile.value == (min_val + max_val) / 2:
                    wait_details.add(WaitDetail("kanchan", idx))
                else:
                    wait_details.add(WaitDetail("ryanmen", idx))
            else:
                wait_details.add(WaitDetail("unknown", idx))

        if not wait_details:
            wait_details.add(WaitDetail("unknown", None))
        return wait_details


def _enumerate_concealed_melds(counter: Counter, sets_needed: int) -> Iterator[List[Meld]]:
    if sets_needed == 0:
        if all(count == 0 for count in counter.values()):
            yield []
        return

    key = _next_non_zero_key(counter)
    if key is None:
        return

    suit, value = _split_key(key)

    # Try triplet
    if counter[key] >= 3:
        counter[key] -= 3
        meld_tiles = tuple(Tile.from_str(key) for _ in range(3))
        meld = Meld(meld_tiles, "pon", is_open=False)
        for rest in _enumerate_concealed_melds(counter, sets_needed - 1):
            yield [meld] + rest
        counter[key] += 3

    # Try sequence
    if suit in SUITS and value <= 7:
        key2 = f"{value + 1}{suit}"
        key3 = f"{value + 2}{suit}"
        if counter[key2] > 0 and counter[key3] > 0:
            counter[key] -= 1
            counter[key2] -= 1
            counter[key3] -= 1
            meld_tiles = (
                Tile.from_str(key),
                Tile.from_str(key2),
                Tile.from_str(key3),
            )
            meld = Meld(meld_tiles, "chi", is_open=False)
            for rest in _enumerate_concealed_melds(counter, sets_needed - 1):
                yield [meld] + rest
            counter[key] += 1
            counter[key2] += 1
            counter[key3] += 1


def _split_key(key: str) -> Tuple[str, int]:
    if key in HONORS:
        return "z", HONOR_TO_INDEX[key]
    suit = key[-1]
    value = int(key[:-1])
    if suit in SUITS:
        return suit, value
    if suit == "z":
        return "z", value
    raise InvalidTileError(f"Cannot split key: {key}")


def _next_non_zero_key(counter: Counter) -> Optional[str]:
    for key in sorted(counter.keys()):
        if counter[key] > 0:
            return key
    return None


TERMINAL_KEYS: Set[str] = {f"1{s}" for s in SUITS} | {f"9{s}" for s in SUITS}
SIMPLE_KEYS: Set[str] = {f"{value}{suit}" for suit in SUITS for value in range(2, 9)}
HONOR_KEYS: Set[str] = set(HONORS)
GREEN_TILE_KEYS: Set[str] = {"2s", "3s", "4s", "6s", "8s", "F"}
VALUE_HONOR_KEYS: Set[str] = {"P", "F", "C"}


def key_is_terminal_or_honor(key: str) -> bool:
    return key in TERMINAL_KEYS or key in HONOR_KEYS


def key_is_terminal(key: str) -> bool:
    return key in TERMINAL_KEYS


def key_is_honor(key: str) -> bool:
    return key in HONOR_KEYS


def key_is_simple(key: str) -> bool:
    return key in SIMPLE_KEYS


def suits_in_keys(keys: Iterable[str]) -> Set[str]:
    suits: Set[str] = set()
    for key in keys:
        if key in HONOR_KEYS:
            suits.add("z")
        else:
            suits.add(key[-1])
    return suits


def count_tile_keys(counter: Counter, keys: Iterable[str]) -> int:
    return sum(counter[key] for key in keys)


def suitedness(ctx: HandContext) -> Set[str]:
    return suits_in_keys(ctx.tile_counter.keys())


def is_chinitsu(ctx: HandContext) -> bool:
    suits = suitedness(ctx)
    return "z" not in suits and len(suits) == 1


def is_honitsu(ctx: HandContext) -> bool:
    suits = suitedness(ctx)
    suits_without_honors = {s for s in suits if s != "z"}
    return "z" in suits and len(suits_without_honors) == 1


def determine_wait_kind(ctx: HandContext, pattern: HandPattern) -> Optional[str]:
    if ctx.wait_type is not None:
        return ctx.wait_type
    priority = ("tanki", "kanchan", "penchan", "shanpon", "ryanmen")
    available = {detail.kind for detail in pattern.wait_details}
    for kind in priority:
        if kind in available:
            return kind
    return None


def is_pinfu_pattern(ctx: HandContext, pattern: HandPattern) -> bool:
    if not ctx.is_menzen:
        return False
    if len(pattern.concealed_melds) != 4:
        return False
    if any(not meld.is_sequence() for meld in pattern.concealed_melds):
        return False
    pair_key = pattern.pair.tile_keys[0]
    if pair_key in VALUE_HONOR_KEYS:
        return False
    if pair_key == ctx.seat_wind:
        return False
    if pair_key == ctx.round_wind:
        return False
    wait_kind = determine_wait_kind(ctx, pattern)
    return wait_kind == "ryanmen"


def analyze_churen(ctx: HandContext) -> Optional[Tuple[str, int]]:
    suits = suitedness(ctx)
    if len(suits) != 1:
        return None
    suit = next(iter(suits))
    if suit == "z":
        return None
    counts = {
        value: ctx.tile_counter.get(f"{value}{suit}", 0) for value in range(1, 10)
    }
    extras_by_value: Dict[int, int] = {}
    for value in range(1, 10):
        requirement = 3 if value in {1, 9} else 1
        count = counts[value]
        if count < requirement:
            return None
        extras_by_value[value] = count - requirement
    if sum(extras_by_value.values()) != 1:
        return None
    extra_value = next(value for value, extra in extras_by_value.items() if extra > 0)
    return suit, extra_value


def shanpon_sources(pattern: HandPattern) -> Set[int]:
    return {detail.source for detail in pattern.wait_details if detail.is_shanpon() and detail.source is not None and detail.source >= 0}


def concealed_triplet_count(ctx: HandContext, pattern: HandPattern) -> int:
    count = 0
    shanpon = shanpon_sources(pattern)
    for idx, meld in enumerate(pattern.all_melds()):
        if not meld.is_triplet():
            continue
        if meld.is_open:
            continue
        if ctx.win_method == "ron":
            wait_type = ctx.wait_type
            if wait_type == "shanpon":
                if idx in shanpon:
                    continue
            elif wait_type is None:
                if idx in shanpon:
                    continue
        count += 1
    return count


def concealed_quad_count(ctx: HandContext, pattern: HandPattern) -> int:
    count = 0
    for meld in pattern.all_melds():
        if meld.is_quad() and not meld.is_open:
            count += 1
    return count


def has_tanki_wait(ctx: HandContext, pattern: HandPattern) -> bool:
    if ctx.winning_tile is None:
        return False
    if ctx.wait_type is not None:
        return ctx.wait_type == "tanki"
    return any(detail.is_tanki() for detail in pattern.wait_details)


def sequence_signature(meld: Meld) -> Tuple[str, int]:
    if not meld.is_sequence():
        raise ValueError("sequence_signature called on non-sequence meld")
    tiles = sorted((tile.value, tile.suit) for tile in meld.tiles if tile.suit in SUITS)
    if not tiles:
        raise ValueError("Invalid sequence meld tiles")
    value, suit = tiles[0]
    return suit, value


def triplet_signature(meld: Meld) -> Tuple[str, str]:
    if not meld.is_triplet():
        raise ValueError("triplet_signature called on non-triplet meld")
    tile = meld.tiles[0]
    if tile.suit == "z":
        return "z", HONOR_FROM_INDEX[tile.value]
    return tile.suit, str(tile.value)


def sequences_by_suit(pattern: HandPattern, include_open: bool = True) -> Dict[str, List[int]]:
    sequences: Dict[str, List[int]] = {"m": [], "p": [], "s": []}
    melds = pattern.all_melds() if include_open else pattern.concealed_melds
    for meld in melds:
        if not meld.is_sequence():
            continue
        suit, start = sequence_signature(meld)
        if suit in SUITS:
            sequences[suit].append(start)
    return sequences


def triplets_by_suit(pattern: HandPattern, include_open: bool = True) -> Dict[str, List[str]]:
    triplets: Dict[str, List[str]] = {"m": [], "p": [], "s": [], "z": []}
    melds = pattern.all_melds() if include_open else pattern.concealed_melds
    for meld in melds:
        if not meld.is_triplet():
            continue
        suit, value = triplet_signature(meld)
        triplets.setdefault(suit, []).append(value)
    return triplets


def is_chiitoitsu(ctx: HandContext) -> bool:
    if ctx.melds:
        return False
    counter = ctx.tile_counter
    if len(counter) != 7:
        return False
    return all(count == 2 for count in counter.values())


def is_kokushi(ctx: HandContext) -> bool:
    required_keys = TERMINAL_KEYS | HONOR_KEYS
    counter = ctx.tile_counter
    if any(counter.get(key, 0) == 0 for key in required_keys):
        return False
    pair_count = sum(1 for key in required_keys if counter.get(key, 0) >= 2)
    return pair_count >= 1 and len(counter) <= len(required_keys)


def is_kokushi_thirteen_wait(ctx: HandContext) -> bool:
    if not ctx.winning_tile:
        return False
    if not is_kokushi(ctx):
        return False
    winning_key = ctx.winning_tile.key
    counter = ctx.tile_counter
    if counter.get(winning_key, 0) != 2:
        return False
    for key in TERMINAL_KEYS | HONOR_KEYS:
        count = counter.get(key, 0)
        if key == winning_key:
            if count != 2:
                return False
        else:
            if count != 1:
                return False
    return True


def is_normal_hand(ctx: HandContext) -> bool:
    return bool(ctx.enumerate_patterns())



class Yaku:
    name: str

    def __init__(self, name: str, menzen_score: int, open_score: int):
        self.name = name
        self.menzen_score = menzen_score
        self.open_score = open_score
        self.is_yakuman = max(menzen_score, open_score) >= 13

    def yakuScore(self, ctx: HandContext, menzen: bool) -> int:
        if self.hasYaku(ctx):
            return self.menzen_score if menzen else self.open_score
        return 0

    def hasYaku(self, ctx: HandContext) -> bool:
        raise NotImplementedError

    def __repr__(self) -> str:
        return f"<Yaku {self.name} {self.menzen_score}/{self.open_score}>"

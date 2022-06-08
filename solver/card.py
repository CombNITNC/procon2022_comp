from dataclasses import dataclass
from typing import Final, Iterable
import yaml
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

KANA: Final = "あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわ"


@dataclass(frozen=True, order=True)
class CardIndex:
    """
    読み札と取り札において札の種類を表す 1 以上 44 以下の整数。
    """
    _index: int

    def __postinit__(self) -> None:
        if not (1 <= self._index <= 44):
            raise ValueError("index must be between 1 and 44")

    def __hash__(self) -> int:
        return self._index

    def __str__(self) -> str:
        return KANA[self._index - 1]

    @staticmethod
    def from_kana(kana: str) -> "CardIndex":
        return CardIndex(KANA.find(kana) + 1)

    @staticmethod
    def all() -> Iterable["CardIndex"]:
        return map(lambda c: CardIndex(c + 1), range(44))


@dataclass(frozen=True)
class ReadCard:
    """
    読み札を表し、種類に加えて英語かそうでない日本語かを表す。
    """
    is_english: bool
    index: CardIndex

    def __str__(self) -> str:
        lang = "E" if self.is_english else "J"
        return f"読み札 {lang}{self.index}"


@dataclass(frozen=True)
class PickCard:
    """
    取り札とその種類を表す。
    """
    index: CardIndex

    def __str__(self) -> str:
        return f"取り札 {self.index}"


@dataclass(frozen=True)
class IncludedRates:
    """
    88 種類の読み札それぞれが、ある分割データに含まれている確率を表す。

    全体の合計は 1.0 に近いことが期待されるが、ある程度の誤差は許容される。
    """
    rates: list[int]

    def __postinit__(self) -> None:
        if len(self.rates) != 88:
            raise ValueError("len of rates must equal to 88")


@dataclass(eq=False)
class ShouldPickCardsByRound:
    """
    各問題データごとに、その札が含まれている確率を管理する。
    """
    _should: list[dict[CardIndex, float]]

    def __init__(self, rounds: int) -> None:
        self._should = [dict() for _ in range(rounds)]

    def save_yaml(self, path: str) -> None:
        output = yaml.dump(self._should, Dumper=Dumper)
        with open(path, 'w') as f:
            f.truncate()
            f.write(output)

    def add(self, round: int, index: CardIndex, prob: float) -> None:
        self._should[round][index] = prob

    def remove(self, round: int, index: CardIndex) -> None:
        self._should[round].pop(index)

    def cards_on(self, round: int) -> int:
        return len(self._should[round])

    def probability(self, round: int, index: CardIndex) -> float:
        return self._should[round].get(index, 0.0)


def should_pick_cards_from_yaml(path: str) -> ShouldPickCardsByRound:
    should = ShouldPickCardsByRound(0)
    with open(path, 'r', newline='') as f:
        should._should = yaml.load(f, Loader=Loader)
    return should

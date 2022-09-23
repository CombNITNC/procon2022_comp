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

    def __post_init__(self) -> None:
        if not (1 <= self._index <= 44):
            raise ValueError("index must be between 1 and 44")

    def __hash__(self) -> int:
        return self._index

    def __str__(self) -> str:
        return KANA[self._index - 1]

    def as_0_pad(self) -> str:
        return f'{self._index:02}'

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


@dataclass(eq=True)
class ShouldPickCards:
    """
    その札が含まれている確率と取るべき個数を表す。
    """
    probabilities: dict[CardIndex, float]
    picks: int


@dataclass(eq=False)
class ShouldPickCardsByProblem:
    """
    各問題データごとに、その札が含まれている確率と取るべき個数を管理する。
    """
    _should: dict[str, ShouldPickCards]

    def __init__(self) -> None:
        self._should = dict()

    def save_yaml(self, path: str) -> None:
        output = yaml.dump(self._should, Dumper=Dumper)
        with open(path, 'w') as f:
            f.truncate()
            f.write(output)

    def insert(self, problem: str, index: CardIndex, prob: float) -> None:
        self._should[problem].probabilities[index] = prob

    def remove(self, problem: str, index: CardIndex) -> None:
        self._should[problem].probabilities.pop(index)

    def cards_on(self, problem: str) -> int:
        return len(self._should[problem].probabilities)

    def picks_on(self, problem: str) -> int:
        return self._should[problem].picks

    def problems(self) -> Iterable[str]:
        return self._should.keys()

    def probability(self, problem: str, index: CardIndex) -> float:
        return self._should[problem].probabilities.get(index, 0.0)


def should_pick_cards_from_yaml(path: str) -> ShouldPickCardsByProblem:
    should = ShouldPickCardsByProblem()
    with open(path, 'r', newline='') as f:
        should._should = yaml.load(f, Loader=Loader)
    return should

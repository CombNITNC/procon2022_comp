from solver.card import CardIndex, ShouldPickCardsByRound
from typing import Final, Iterable, Optional, Tuple, TypedDict


def solve_by_binary_search(
    rounds: int,
    should_pick_sets: ShouldPickCardsByRound
) -> Optional[Tuple[list[CardIndex], float]]:
    EPS: Final = 0.001

    start = 0.0
    end = 1.0
    while EPS < (end - start):
        mid = (end - start) / 2 + start
        ways = solve(rounds, should_pick_sets, mid)
        if ways is None:
            end = mid
        else:
            start = mid
    ways = solve(rounds, should_pick_sets, start)
    if ways is None:
        return None
    return (ways, start)


def solve(
    rounds: int,
    should_pick_sets: ShouldPickCardsByRound,
    pick_threshold: float
) -> Optional[list[CardIndex]]:
    """
    最も多く札が取れるような、問題ごとの札の取り方を探索する。

    引数:
        - rounds: この試合の問題数。
        - should_pick_sets: 各問題データごとに、その札が含まれている確率のデータ。
        - pick_threshold: その札を取るべきと見なす確率のしきい値。

    戻り値:
        各問題ごとに取る札の種類を格納したリスト。取る札が存在しない場合は None を返す。
    """

    class ShouldPickList(TypedDict):
        problem_round: int
        cards: list[CardIndex]

    pick_lists = convert_to_pick_lists(
        rounds, should_pick_sets, pick_threshold
    )
    if pick_lists is None:
        return None

    def index_from_cards(cards: Iterable[CardIndex]) -> int:
        index = 0
        for card in cards:
            index |= 1 << hash(card)
        return index

    memo: dict[int, Optional[list[CardIndex]]] = {}

    def inner(
        curr_ways: list[CardIndex],
        visited: set[CardIndex],
        pick_lists: list[ShouldPickList]
    ) -> Optional[list[CardIndex]]:
        index = index_from_cards(curr_ways)
        if index in memo:
            return memo[index]
        curr_round = len(curr_ways)
        if curr_round == rounds:
            return curr_ways

        cards = pick_lists[curr_round]["cards"]
        for card in filter(lambda card: card not in visited, cards):
            visited.add(card)
            curr_ways.append(card)
            recursive_result = inner(curr_ways, visited, pick_lists)
            memo[index_from_cards(curr_ways)] = recursive_result
            if recursive_result is not None:
                return recursive_result
            curr_ways.pop()
            visited.discard(card)
        return None

    return inner([], set(), pick_lists)


class ShouldPickList(TypedDict):
    problem_round: int
    cards: list[CardIndex]


def convert_to_pick_lists(
    rounds: int,
    should_pick_sets: ShouldPickCardsByRound,
    pick_threshold: float
) -> Optional[list[ShouldPickList]]:
    """
    ShouldPickCardsByRound のデータを選ぶべき札データのリストへと変換する。
    このとき、このデータを試合全体を通した確率として再計算する。

    引数:
        - rounds: この試合の問題数。
        - should_pick_sets: 各問題データごとに、その札が含まれている確率のデータ。
        - pick_threshold: その札を取るべきと見なす確率のしきい値。

    戻り値:
        選ぶべき札データのリスト。取る札が存在しない場合は None を返す。
    """

    pick_lists: list[ShouldPickList] = []
    prev_probabilities: dict[CardIndex, float] = {}

    """
    ラウンド i で札 c と推定される確率を P_i,c とし,
    全体を通してラウンド i で札 c を選ぶ確率 Q_i,c とすると,
    ラウンド i - 1, i のときについて以下の関係が成り立つ.

    P(ラウンド i で c を選ぶ ∩ ラウンド i - 1 で c を選ばない)
        = P(ラウンド i で c を選ぶ | ラウンド i - 1 で c を選ばない)
        * P(ラウンド i - 1 で c を選ばない)
    Q_i,c = P_i,c * (Σ_{d ≠ c} P_i-1,d) = P_i,c * (1 - P_i-1,c)
    """
    for r in range(rounds):
        pick_lists.append({
            "problem_round": r,
            "cards": [],
        })
        for card in CardIndex.all():
            prev_probability = prev_probabilities.get(card, 0.0)
            probability = should_pick_sets.probability(
                r, card
            ) * (1.0 - prev_probability)
            if pick_threshold < probability:
                pick_lists[-1]["cards"].append(card)
            prev_probabilities[card] = probability
        if len(pick_lists[-1]["cards"]) == 0:
            return None

    return pick_lists

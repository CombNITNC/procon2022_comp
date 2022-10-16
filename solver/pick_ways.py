from dataclasses import dataclass
from solver.card import CardIndex, ShouldPickCardsByProblem
from typing import Final, Iterable, Optional, Tuple
from itertools import combinations


def solve_by_binary_search(
    problems: int,
    should_pick_sets: ShouldPickCardsByProblem
) -> Optional[Tuple[list[list[CardIndex]], float]]:
    EPS: Final = 0.001

    start = 0.0
    end = 1.0
    while EPS < (end - start):
        mid = (end - start) / 2 + start
        ways = solve(problems, should_pick_sets, mid)
        if ways is None:
            end = mid
        else:
            start = mid
    ways = solve(problems, should_pick_sets, start)
    if ways is None:
        return None
    return (ways, start)


def solve(
    problems: int,
    should_pick_sets: ShouldPickCardsByProblem,
    pick_threshold: float
) -> Optional[list[list[CardIndex]]]:
    """
    最も多く札が取れるような、問題ごとの札の取り方を探索する。

    引数:
        - problems: この試合の問題数。
        - should_pick_sets: 各問題データごとに、その札が含まれている確率のデータ。
        - pick_threshold: その札を取るべきと見なす確率のしきい値。

    戻り値:
        各問題ごとに取る札の種類を格納したリスト。取る札が存在しない場合は None を返す。
    """

    pick_lists = convert_to_pick_lists(
        should_pick_sets, pick_threshold
    )
    if pick_lists is None:
        return None

    def index_from_cards(cards_by_problem: Iterable[list[CardIndex]]) -> int:
        indexes = 0
        for cards in cards_by_problem:
            index = 0
            for card in cards:
                index |= 1 << hash(card)
            indexes = (indexes << 45) + index
        return indexes

    memo: dict[int, Optional[list[list[CardIndex]]]] = {}

    def inner(
        curr_ways: list[list[CardIndex]],
        visited: set[CardIndex],
        pick_lists: list[ShouldPickList]
    ) -> Optional[list[list[CardIndex]]]:
        index = index_from_cards(curr_ways)
        if index in memo:
            return memo[index]
        curr_round = len(curr_ways)
        if problems <= curr_round or len(pick_lists) <= curr_round:
            return curr_ways

        patterns = combinations(
            pick_lists[curr_round].cards,
            pick_lists[curr_round].picks
        )
        filtered_patterns = filter(
            lambda cards: all(map(
                lambda card: card not in visited,
                cards
            )),
            patterns
        )
        for pattern in filtered_patterns:
            curr_ways.append(list(pattern))
            for card in pattern:
                visited.add(card)
            recursive_result = inner(curr_ways, visited, pick_lists)
            memo[index_from_cards(curr_ways)] = recursive_result
            if recursive_result is not None:
                return recursive_result
            for card in pattern:
                visited.discard(card)
            curr_ways.pop()
        return None

    return inner([], set(), pick_lists)


@dataclass(frozen=True)
class ShouldPickList:
    problem_id: str
    cards: list[CardIndex]
    picks: int


def convert_to_pick_lists(
    should_pick_sets: ShouldPickCardsByProblem,
    pick_threshold: float
) -> Optional[list[ShouldPickList]]:
    """
    ShouldPickCardsByRound のデータを選ぶべき札データのリストへと変換する。
    このとき、このデータを試合全体を通した確率として再計算する。

    引数:
        - should_pick_sets: 各問題データごとに、その札が含まれている確率のデータ。
        - pick_threshold: その札を取るべきと見なす確率のしきい値。

    戻り値:
        選ぶべき札データのリスト。取る札が存在しない場合は None を返す。
    """

    pick_lists: list[ShouldPickList] = []
    opposite_sums: dict[str, dict[CardIndex, float]] = {}

    """
    ラウンド i で札 c と推定される確率を P_i,c とし,
    全体を通してラウンド i で札 c を選ぶ確率 Q_i,c とすると,
    ラウンド i - 1, i のときについて以下の関係が成り立つ.

    P(ラウンド i で c を選ぶ ∩ ラウンド i - 1 で c を選ばない)
        = P(ラウンド i で c を選ぶ | ラウンド i - 1 で c を選ばない)
        * P(ラウンド i - 1 で c を選ばない)
    Q_i,c = P_i,c * (Σ_{d ≠ c} P_i-1,d)
    """

    problems = iter(should_pick_sets.problems())
    prev = next(problems)
    opposite_sums[prev] = {}
    for index in CardIndex.all():
        opposite_sums[prev][index] = should_pick_sets.probability(prev, index)
    for problem in problems:
        opposite_sums[problem] = {}
        for after in CardIndex.all():
            opposite_sums[problem][after] = 0.0
            for before in CardIndex.all():
                if before != after:
                    opposite_sums[problem][after] += \
                        opposite_sums[prev][before]
        prev = problem

    for problem in should_pick_sets.problems():
        picks = should_pick_sets.picks_on(problem)
        pick_lists.append(ShouldPickList(
            problem_id=problem,
            cards=[],
            picks=picks,
        ))
        for card in CardIndex.all():
            probability = should_pick_sets.probability(
                problem, card
            ) * opposite_sums[problem][card]
            if pick_threshold < probability:
                pick_lists[-1].cards.append(card)
        if len(pick_lists[-1].cards) < picks:
            return None

    return pick_lists

from unittest import TestCase

from solver.card import CardIndex, ShouldPickCardsByProblem
from solver.pick_ways import solve_by_binary_search


class PickWaysTestCase(TestCase):
    def test_simple_case(self):
        """
        1. [か, と, り]
        2. [つ, ら]
        3. [し, た, の, わ]
        """
        rounds = 3
        should_pick_sets = ShouldPickCardsByProblem()
        should_pick_sets.insert('0', CardIndex.from_kana('か'), 0.8)
        should_pick_sets.insert('0', CardIndex.from_kana('と'), 0.8)
        should_pick_sets.insert('0', CardIndex.from_kana('り'), 0.8)
        should_pick_sets.insert('1', CardIndex.from_kana('つ'), 0.8)
        should_pick_sets.insert('1', CardIndex.from_kana('ら'), 0.8)
        should_pick_sets.insert('2', CardIndex.from_kana('し'), 0.8)
        should_pick_sets.insert('2', CardIndex.from_kana('た'), 0.8)
        should_pick_sets.insert('2', CardIndex.from_kana('の'), 0.8)
        should_pick_sets.insert('2', CardIndex.from_kana('わ'), 0.8)

        answer = solve_by_binary_search(rounds, should_pick_sets)

        self.assertEqual(
            answer,
            ([
                [CardIndex.from_kana('か')],
                [CardIndex.from_kana('つ')],
                [CardIndex.from_kana('し')]
            ], 0.7998046875)
        )

    def test_complex_case(self):
        """
        1. [い, う]
        2. [あ, い]
        3. [い, え]
        4. [え]
        """
        rounds = 4
        should_pick_sets = ShouldPickCardsByProblem()
        should_pick_sets.insert('0', CardIndex.from_kana('い'), 0.5)
        should_pick_sets.insert('0', CardIndex.from_kana('う'), 0.5)
        should_pick_sets.insert('1', CardIndex.from_kana('あ'), 0.5)
        should_pick_sets.insert('1', CardIndex.from_kana('い'), 0.5)
        should_pick_sets.insert('2', CardIndex.from_kana('い'), 0.5)
        should_pick_sets.insert('2', CardIndex.from_kana('え'), 0.5)
        should_pick_sets.insert('3', CardIndex.from_kana('え'), 1.0)

        answer = solve_by_binary_search(rounds, should_pick_sets)

        self.assertEqual(
            answer,
            ([
                [CardIndex.from_kana('う')],
                [CardIndex.from_kana('あ')],
                [CardIndex.from_kana('い')],
                [CardIndex.from_kana('え')]
            ], 0.3740234375)
        )

from unittest import TestCase

from solver.card import CardIndex, ShouldPickCardsByProblem


class CardTestCase(TestCase):
    def test_from_kana(self):
        for (card, index) in zip(CardIndex.all(), range(44)):
            self.assertEqual(card, CardIndex(index + 1))

    def test_should_pick(self):
        """
        1. [か, と, り]
        2. [つ, ら]
        3. [し, た, の, わ]
        """
        should_pick_sets = ShouldPickCardsByProblem()
        should_pick_sets.add('0', CardIndex.from_kana('か'), 0.8)
        should_pick_sets.add('0', CardIndex.from_kana('と'), 0.8)
        should_pick_sets.add('0', CardIndex.from_kana('り'), 0.8)
        should_pick_sets.add('1', CardIndex.from_kana('つ'), 0.8)
        should_pick_sets.add('1', CardIndex.from_kana('ら'), 0.8)
        should_pick_sets.add('2', CardIndex.from_kana('し'), 0.8)
        should_pick_sets.add('2', CardIndex.from_kana('た'), 0.8)
        should_pick_sets.add('2', CardIndex.from_kana('の'), 0.8)
        should_pick_sets.add('2', CardIndex.from_kana('わ'), 0.8)

        self.assertEqual(should_pick_sets.cards_on('0'), 3)
        self.assertEqual(should_pick_sets.cards_on('1'), 2)
        self.assertEqual(should_pick_sets.cards_on('2'), 4)

        self.assertEqual(should_pick_sets.probability(
            '0', CardIndex.from_kana('か')), 0.8)
        self.assertEqual(should_pick_sets.probability(
            '0', CardIndex.from_kana('と')), 0.8)
        self.assertEqual(should_pick_sets.probability(
            '0', CardIndex.from_kana('り')), 0.8)
        self.assertEqual(should_pick_sets.probability(
            '1', CardIndex.from_kana('つ')), 0.8)
        self.assertEqual(should_pick_sets.probability(
            '1', CardIndex.from_kana('ら')), 0.8)
        self.assertEqual(should_pick_sets.probability(
            '2', CardIndex.from_kana('し')), 0.8)
        self.assertEqual(should_pick_sets.probability(
            '2', CardIndex.from_kana('た')), 0.8)
        self.assertEqual(should_pick_sets.probability(
            '2', CardIndex.from_kana('の')), 0.8)
        self.assertEqual(should_pick_sets.probability(
            '2', CardIndex.from_kana('わ')), 0.8)

        self.assertEqual(should_pick_sets.probability(
            '0', CardIndex.from_kana('あ')), 0.0)
        self.assertEqual(should_pick_sets.probability(
            '1', CardIndex.from_kana('あ')), 0.0)
        self.assertEqual(should_pick_sets.probability(
            '2', CardIndex.from_kana('あ')), 0.0)

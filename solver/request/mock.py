from dataclasses import dataclass
from time import gmtime
from os.path import join
from calendar import timegm
from scipy.io import wavfile

from solver.request.meta import AbstractRequester, Answer, Chunk, \
    Match, Problem


@dataclass(frozen=True)
class MockRequester(AbstractRequester):
    def get_match(self) -> Match:
        return Match(1, [3.0, 2.5, 2.0, 1.5, 1.0], 20)

    def get_problem(self) -> Problem:
        now = gmtime()
        return Problem('q_m01', 5, timegm(now), 10000, 5)

    def get_chunks(self, using_chunks: int, _save_dir: str) -> list[Chunk]:
        chunks: list[Chunk] = []
        for idx in range(using_chunks):
            chunk_path = join('sample', 'sample_Q_M01', f'problem{idx}.wav')
            _sample, wav = wavfile.read(chunk_path)
            chunks.append(Chunk(idx, wav))
        return chunks

    def post_answer(self, answer: Answer) -> None:
        answer.answers.sort()

        expected = ['01', '02', '03', '04', '05']
        assert answer.answers == expected

from time import gmtime
from os.path import join
from calendar import timegm
from scipy.io import wavfile
import yaml
from solver.request.meta import AbstractRequester, Answer, Chunk, \
    Match, Problem

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader


class MockRequester(AbstractRequester):

    def __init__(self, using_sample: str) -> None:
        self.using_dir = f"sample_Q_{using_sample}"
        with open(join(
            "sample",
            self.using_dir,
            "information.txt",
        ), encoding="utf-8") as sample_file:
            parsed = yaml.load(sample_file, Loader=Loader)
            self.expected: list[str] = parsed["speech"].split(",")
            self.expected.sort()
            self.nsplit: int = parsed["nsplit"]

    def get_match(self) -> Match:
        return Match(1, [3.0, 2.5, 2.0, 1.5, 1.0], 20, 20, 10, 100)

    def get_problem(self) -> Problem:
        now = gmtime()
        return Problem(
            self.using_dir,
            self.nsplit,
            timegm(now),
            10000,
            len(self.expected),
        )

    def get_chunks(self, using_chunks: int, _save_dir: str) -> list[Chunk]:
        chunks: list[Chunk] = []
        for idx in range(using_chunks):
            chunk_path = join(
                'sample',
                self.using_dir,
                f'problem{idx + 1}.wav',
            )
            _sample, wav = wavfile.read(chunk_path)
            chunks.append(Chunk(idx, wav))
        return chunks

    def post_answer(self, answer: Answer) -> None:
        answer.answers.sort()

        assert answer.answers == self.expected

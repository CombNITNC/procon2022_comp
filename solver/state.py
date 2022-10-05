from dataclasses import dataclass
import yaml

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper


@dataclass()
class SolverState:
    current_problem_id: str
    current_fails: int
    used_chunks: dict[str, int]

    def save_yaml(self, path: str) -> None:
        output = yaml.dump({
            'current_round': self.current_problem_id,
            'current_fails': self.current_fails,
            'using_chunks': self.used_chunks,
        }, Dumper=Dumper)
        with open(path, 'w') as f:
            f.truncate()
            f.write(output)


def solver_state_from_yaml(path: str) -> SolverState:
    with open(path, 'r', newline='') as f:
        obj = yaml.load(f, Loader=Loader)
        return SolverState(
            current_problem_id=obj['current_round'],
            current_fails=obj['current_fails'],
            used_chunks=obj['using_chunks'],
        )

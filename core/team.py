from core.participant import Gender, Participant
from core.utils import count


class Team:
    _id: str
    _prts: list[Participant]

    def __init__(self, _id: str, _prts: list[Participant]):
        self._id = _id
        self._prts = _prts

    def __repr__(self) -> str:
        return (
            f"Team(id='{self._id}', prts="
            + "["
            + ", ".join([str(p) for p in self._prts])
            + "])"
        )

    @classmethod
    def empty(cls, _id: str) -> "Team":
        return Team(_id, [])

    @property
    def id(self):
        return self._id

    @property
    def size(self) -> int:
        return len(self._prts)

    @property
    def male_count(self) -> int:
        return count(self._prts, lambda prt: prt.gender == Gender.MALE)

    @property
    def female_count(self) -> int:
        return count(self._prts, lambda prt: prt.gender == Gender.FEMALE)

    @property
    def participants(self) -> list[Participant]:
        return self._prts[:]

    def join(self, prt: Participant):
        self._prts.append(prt)

    def remove(self, name: str) -> Participant | None:
        for prt in self._prts:
            if prt.name == name:
                self._prts.remove(prt)
                return prt
        return None

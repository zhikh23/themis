from typing import Self

from core.participant import Participant, Gender
from core.utils import count


class Team:
    _id: str
    _prts: list[Participant]

    def __init__(self, _id: str, _prts: list[Participant]):
        self._id = _id
        self._prts = _prts

    def __repr__(self) -> str | None:
        return f"Team(id='{self._id}', prts=" + "[" + ", ".join([str(p) for p in self._prts]) + "])"

    @classmethod
    def empty(cls, _id: str) -> Self:
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


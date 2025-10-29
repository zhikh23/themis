from dataclasses import dataclass
from enum import StrEnum


class Gender(StrEnum):
    MALE = "male"
    FEMALE = "female"

    @classmethod
    def parse_from_ru(cls, s: str):
        s = s.lower()
        if s == "м":
            return Gender.MALE
        elif s == "ж":
            return Gender.FEMALE
        raise ValueError(f"invalid gender: expected one of ['м', 'ж'], got {s}")


@dataclass
class Participant:
    name: str
    group: str
    gender: Gender

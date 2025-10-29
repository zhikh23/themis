import csv
from typing import Generator

from core.participant import Gender, Participant
from core.team import Team
from core.themis import Themis


def load_participants_from_csv(
    filename: str = "in.csv",
) -> Generator[Participant, None, None]:
    with open(filename) as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            name, group, gender = row
            gender = Gender.parse_from_ru(gender)
            yield Participant(name, group, gender)


def pretty_print_distribution(teams: list[Team]):
    for team in teams:
        print(f"Team '{team.id}'")
        print(f"{team.size} ({team.male_count} + {team.female_count})")
        for prt in team.participants:
            print(f"  {prt.name},{prt.group},{prt.gender}")
        print()


def main():
    themis = Themis.with_sequential_team_ids(8)
    participants = list(load_participants_from_csv())
    for prt in participants:
        themis.assign_team(prt)
    pretty_print_distribution(themis.teams)


if __name__ == "__main__":
    main()

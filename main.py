import csv
import sys
from typing import Generator

from questionary import autocomplete, path, select, text

from core.participant import Gender, Participant
from core.team import Team
from core.themis import Themis

TEAMS = 7


def load_participants_from_csv(filename: str) -> Generator[Participant, None, None]:
    with open(filename) as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            name, group, gender = row
            gender = Gender.parse_from_ru(gender)
            yield Participant(name, group, gender)


def pretty_print_distribution(teams: list[Team]):
    for team in teams:
        print(f"Команда #{team.id}")
        print(f"- Размер: {team.size} ({team.male_count}м + {team.female_count}ж)")
        for prt in team.participants:
            print(f"  {prt.name},{prt.group},{prt.gender}")
        print()


def export_teams_csv(teams: list[Team], filename: str):
    with open(filename, "w") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["name", "group", "gender", "team_id"])
        for team in teams:
            for prt in team.participants:
                writer.writerow([prt.name, prt.group, prt.gender, team.id])


def import_teams_csv(filename: str) -> list[Team]:
    teams = {str(i): Team.empty(str(i)) for i in range(1, TEAMS + 1)}
    with open(filename) as csv_file:
        reader = csv.reader(csv_file)
        next(reader)  # Пропуск заголовка
        for row in reader:
            name, group, gender, team_id = row
            if team_id not in teams:
                teams[team_id] = Team.empty(team_id)
            prt = Participant(name, group, Gender.parse_from_ru(gender))
            teams[team_id].join(prt)
    return list(teams.values())


def main():
    themis = Themis.with_sequential_team_ids(TEAMS)
    participants = dict()
    run = True
    while run:
        try:
            option = select(
                message="Выберите опцию меню",
                choices=[
                    "Распределить участника",
                    "Добавить участника",
                    "Вывести распределение",
                    "Удалить участника из команды",
                    "Импортировать участников из CSV",
                    "Импортировать команды из CSV",
                    "Экспортировать команды в CSV",
                ],
            ).ask()
            if option == "Распределить участника":
                if not participants:
                    print("В БД нет данных об участниках")
                    continue
                names = list(participants.keys())
                name = autocomplete(
                    message="ФИО участника",
                    choices=names,
                    validate=lambda n: n in names,
                ).ask()
                prt = participants.pop(name)
                if not prt:
                    continue
                team_id = themis.assign_team(prt)
                print(f"Успешно добавлен в команду #{team_id}")
            elif option == "Добавить участника":
                name = text(
                    message="ФИО участника",
                ).ask()
                if not name:
                    continue
                group = text(
                    message="Учебная группа",
                ).ask()
                if not group:
                    continue
                gender = select(
                    message="Пол",
                    choices=["М", "Ж"],
                ).ask()
                if not gender:
                    continue
                prt = Participant(name, group, gender)
                participants[name] = prt
            elif option == "Вывести распределение":
                pretty_print_distribution(themis.teams)
            elif option == "Удалить участника из команды":
                prts = themis.participants
                names = [prt.name for prt in prts]
                name = autocomplete(
                    message="ФИО участника",
                    choices=names,
                    validate=lambda n: n in names,
                ).ask()
                prt = themis.remove_participant(name)
                participants[name] = prt
                print("Участник успешно удалён из команды")
            elif option == "Импортировать участников из CSV":
                filename = path(message="Путь до .csv файла").ask()
                participants = {
                    prt.name: prt for prt in load_participants_from_csv(filename)
                }
                print(f"Успешно загружено {len(participants)} записей")
            elif option == "Экспортировать команды в CSV":
                filename = path(message="Путь до .csv файла").ask()
                export_teams_csv(themis.teams, filename)
                print(f"Успешно экспортировано {len(themis.teams)} команд")
            elif option == "Импортировать команды из CSV":
                filename = path(message="Путь до .csv файла").ask()
                teams = import_teams_csv(filename)
                themis = Themis(teams)
                print(f"Успешно импортировано {len(teams)} команд")
            else:
                print("Выхожу из программы...")
                run = False
        except Exception as e:
            print(e, file=sys.stderr)


if __name__ == "__main__":
    main()

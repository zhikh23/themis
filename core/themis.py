from typing import Self

import Levenshtein

from core.participant import Participant, Gender
from core.team import Team


class Themis:
    _teams: list[Team]

    def __init__(self, teams: list[Team]):
        self._teams = teams

    @classmethod
    def with_sequential_team_ids(cls, n: int) -> Self:
        """Генерирует пустые команды с порядковыми номерами 1..n."""
        teams = [Team.empty(str(i)) for i in range(n)]
        return Themis(teams)

    def assign_team(self, prt: Participant):
        candidates = self._candidate_teams(prt)
        team = Themis._best_team(candidates, prt)
        team.join(prt)

    @property
    def teams(self) -> list[Team]:
        return self._teams[:]

    def _candidate_teams(self, prt: Participant) -> list[Team]:
        """Возвращает список-команд, в которые есть возможность добавить участника `prt`."""
        candidates = []
        # Фильтрация по размеру команд.
        # Необходимо, чтобы размеры команд не отличались более, чем на 1.
        sizes = [team.size for team in self._teams]
        min_size = min(sizes)
        for team in self._teams:
            if team.size == min_size:
                candidates.append(team)

        if not candidates:
            raise LookupError("no candidates for team.size balance found")

        # Распределение по полу.
        # Необходимо, чтобы примерный состав м/ж в командах был равным (погрешность в +-1). Так как пол у нас бинарный,
        # то задача сводится к выравниванию количества участников по заранее заданному конкретному полу.
        # Проще всего считать в 'ж', так как их (как правило) меньше, а следовательно, ошибка на 1 приведёт к
        # большему дисбалансу в процентном соотношении, чем в случае ошибки на 1 у мужчин.
        # Следовательно, проверка имеет смысл тогда, когда в команду добавляется женщина.
        if prt.gender == Gender.FEMALE:
            gender_candidates = []
            females = [team.female_count for team in candidates]
            min_female = min(females)
            for team in candidates:
                if team.female_count == min_female:
                    gender_candidates.append(team)
            if not gender_candidates:
                raise LookupError("no candidates for gender balance found")
            candidates = gender_candidates

        return candidates

    @classmethod
    def _best_team(cls, teams: list[Team], prt: Participant) -> Team:
        """
        Определение наиболее подходящей участнику команды по наименьшему ранку (метод `Themis._rank_team`).
        Выбрасывает исключение, если список команд `teams` пустой.
        """
        if not teams:
            raise ValueError("no teams specified")
        min_rank = -1
        best = teams[0]
        for team in teams:
            rank = Themis._rank_team(team, prt)
            if rank < min_rank:
                best = team
                min_rank = rank
        return best

    @classmethod
    def _rank_team(cls, team: Team, pivot: Participant, lv_boundary: int = 3) -> int:
        """
        Определяет ранк команд относительно опорного участника `pivot`.

        Требование ранжирования возникает из потребности НЕ распределять участников в команды, в которых есть
        потенциальные знакомые. Отчасти это можно понять из кода группы:
        - одногруппники (полное совпадение кода группа);
        - однокурсники (разница в одну цифру в коде группы);
        - координаторы (разница в 1-2 цифры в коде группы).
        Разницу в кодах группы естественно рассчитывать расстоянием Левенштейна.
        Следовательно, нужно распределять участнику в ту команду, где сумма разниц в кодах группы -- максимальна.

        Проблема: наличие человека с другого факультета в одной из команд даст большое расстояние Левенштейна,
        что вынудит балансировщик добавить одногруппника, чтобы сравнять ранки.
        Решение: ограничить максимальное расстояние Левенштейна некоторой границей lv_boundary.
        То есть начиная с lv_boundary мы считаем людей абсолютно незнакомыми в равной степени.

        :param team: Команда, для которой рассчитывается ранк.
        :param pivot: Опорный участник, относительно которого рассчитывается ранк.
        :param lv_boundary: Максимальное значение, которое может вложить в ранк один участник.
        :return:
        """
        rank = 0
        for prt in team.participants:
            rank += min(lv_boundary, Levenshtein.distance(pivot.group, prt.group))
        return rank

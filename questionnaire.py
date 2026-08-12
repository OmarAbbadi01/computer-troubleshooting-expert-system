"""Questionnaire: collects facts from the user.

It maps the selected main problem to the relevant questions and turns
Yes/No answers into facts. It contains no diagnostic logic at all —
diagnosis is left entirely to the inference engine.
"""

from __future__ import annotations

from typing import Dict, List, Optional

from models import MainProblem, Question


class Questionnaire:
    """Asks the relevant questions and converts answers into facts."""

    def __init__(self, problems: List[MainProblem], questions: Dict[str, Question]) -> None:
        self.problems = problems
        self.questions = questions

    def choose_problem(self, choice_text: Optional[str] = None) -> MainProblem:
        """Select a main problem by number (used by the CLI)."""
        if choice_text is None:
            choice_text = input("Enter your choice (1-9): ").strip()
        try:
            index = int(choice_text) - 1
            if 0 <= index < len(self.problems):
                return self.problems[index]
        except ValueError:
            pass
        raise ValueError(f"'{choice_text}' is not a valid problem number.")

    def collect_facts(
        self,
        problem: MainProblem,
        machine_type: str,
        answers: Optional[Dict[str, bool]] = None,
    ) -> List[str]:
        """Ask every question relevant to the problem and return facts.

        `answers` maps question ids to booleans (True = Yes, False = No)
        and is used for non-interactive / evaluation runs. When it is
        None, questions are asked on the command line.
        """
        facts: List[str] = []

        for qid in problem.question_ids:
            question = self.questions[qid]

            if question.laptop_only and machine_type != "laptop":
                continue

            answer = self._ask_yes_no(question, answers)

            if answer is None:
                continue
            if answer and question.yes_fact:
                facts.append(question.yes_fact)
            elif not answer and question.no_fact:
                facts.append(question.no_fact)

        return facts

    def _ask_yes_no(self, question: Question, answers: Optional[Dict[str, bool]]) -> Optional[bool]:
        if answers is not None:
            return answers.get(question.id)

        while True:
            raw = input(f"{question.text} (yes/no): ").strip().lower()
            if raw in ("y", "yes"):
                return True
            if raw in ("n", "no"):
                return False
            print("Please answer 'yes' or 'no'.")

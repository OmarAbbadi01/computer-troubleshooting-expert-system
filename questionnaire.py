"""الاستبيان: يجمع الإجابات من المستخدم ويحولها إلى حقائق."""

from __future__ import annotations

from typing import Dict, List, Optional

from models import MainProblem, Question


class Questionnaire:
    """يسأل المستخدم الأسئلة ويحوّل الإجابات إلى حقائق."""

    def __init__(self, problems: List[MainProblem], questions: Dict[str, Question]) -> None:
        self.problems = problems
        self.questions = questions

    def choose_problem(self, choice_text: Optional[str] = None) -> MainProblem:
        if choice_text is None:
            choice_text = input("أدخل اختيارك (1-9): ").strip()
        try:
            index = int(choice_text) - 1
            if 0 <= index < len(self.problems):
                return self.problems[index]
        except ValueError:
            pass
        raise ValueError(f"'{choice_text}' ليس رقماً صحيحاً لمشكلة.")

    def collect_facts(
        self,
        problem: MainProblem,
        machine_type: str,
        answers: Optional[Dict[str, bool]] = None,
    ) -> List[str]:
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
            print(question.text)
            raw = input("(نعم/لا): ").strip().lower()
            if raw in ("y", "yes", "نعم", "ن"):
                return True
            if raw in ("n", "no", "لا", "ل"):
                return False
            print("يرجى الإجابة بنعم أو لا.")

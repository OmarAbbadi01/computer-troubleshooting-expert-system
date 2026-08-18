"""تحميل البيانات وتحويلها إلى كائنات."""

from __future__ import annotations

import sys
import os
from typing import Dict, List, Tuple

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "data"))

from models import MainProblem, Question, Rule
from data.rules import DIAGNOSES, RULES
from data.questions import MAIN_PROBLEMS, QUESTIONS


def load_rules() -> List[Rule]:
    return [
        Rule(
            id=r["id"],
            conditions=r["conditions"],
            conclusions=r["conclusions"],
            explanation=r["explanation"],
            recommendation=r.get("recommendation"),
        )
        for r in RULES
    ]


def load_diagnoses() -> Dict[str, dict]:
    return DIAGNOSES


def load_questionnaire() -> Tuple[List[MainProblem], Dict[str, Question]]:
    questions = {
        qid: Question(
            id=qid,
            text=q["text"],
            yes_fact=q.get("yes_fact"),
            no_fact=q.get("no_fact"),
            laptop_only=q.get("laptop_only", False),
        )
        for qid, q in QUESTIONS.items()
    }

    problems = [
        MainProblem(
            id=p["id"],
            label=p["label"],
            question_ids=list(p["questions"]),
        )
        for p in MAIN_PROBLEMS
    ]

    return problems, questions

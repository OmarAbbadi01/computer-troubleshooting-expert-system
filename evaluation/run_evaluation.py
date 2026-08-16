"""Run the evaluation scenarios against the real questionnaire + engine.

This is a separate, self-contained tool. The application itself never
uses it and contains no test-case-specific logic. Run it with:

    python3 -m evaluation.run_evaluation
"""

from __future__ import annotations

import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)  # to import cases.py
sys.path.insert(0, os.path.dirname(_HERE))  # to import project modules

from cases import CASES

from knowledge_base import load_diagnoses, load_questionnaire, load_rules
from questionnaire import Questionnaire
from engine import InferenceEngine

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KNOWLEDGE_BASE_FILE = os.path.join(BASE_DIR, "data", "knowledge_base.json")
QUESTIONS_FILE = os.path.join(BASE_DIR, "data", "questions.json")


def main() -> None:
    rules = load_rules(KNOWLEDGE_BASE_FILE)
    diagnoses = load_diagnoses(KNOWLEDGE_BASE_FILE)
    problems, questions = load_questionnaire(QUESTIONS_FILE)
    questionnaire = Questionnaire(problems, questions)
    engine = InferenceEngine(rules)

    header = f"{'Case':<4}{'Name':<24}{'Expected':<38}{'Actual':<30}{'Result'}"
    print(header)
    print("-" * len(header))

    passed = 0
    for case in CASES:
        problem = next(p for p in problems if p.id == case["problem"])
        facts = questionnaire.collect_facts(problem, case["machine"], case["answers"])
        memory = engine.run(facts)

        actual_names = sorted(
            diagnoses.get(d, {}).get("name", {}).get("en", d)
            for d in memory.facts if d.startswith("diagnosis_")
        )
        expected_names = sorted(case["expected"])
        ok = actual_names == expected_names

        passed += 1 if ok else 0
        print(
            f"{case['number']:<4}{case['name']:<24}"
            f"{'/'.join(expected_names):<38}{'/'.join(actual_names) or 'none':<30}"
            f"{'PASS' if ok else 'FAIL'}"
        )

    print("-" * len(header))
    print(f"Passed {passed}/{len(CASES)} cases.")


if __name__ == "__main__":
    main()

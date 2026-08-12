"""Command-line entry point for the Computer Troubleshooting Expert System.

Flow: choose a main problem -> relevant questions -> facts -> forward
chaining inference -> diagnoses / partial inferences -> optional trace.
"""

from __future__ import annotations

import os
import sys
from typing import Dict, List

from engine import InferenceEngine
from knowledge_base import (
    load_diagnoses,
    load_intermediate_labels,
    load_questionnaire,
    load_rules,
)
from models import MainProblem, WorkingMemory
from questionnaire import Questionnaire

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
KNOWLEDGE_BASE_FILE = os.path.join(DATA_DIR, "knowledge_base.json")
QUESTIONS_FILE = os.path.join(DATA_DIR, "questions.json")

DIAGNOSIS_PREFIX = "diagnosis_"


def load_assets():
    """Load and validate all data files."""
    rules = load_rules(KNOWLEDGE_BASE_FILE)
    diagnoses = load_diagnoses(KNOWLEDGE_BASE_FILE)
    intermediate_labels = load_intermediate_labels(KNOWLEDGE_BASE_FILE)
    problems, questions = load_questionnaire(QUESTIONS_FILE)
    return rules, diagnoses, intermediate_labels, problems, questions


def choose_machine_type() -> str:
    print("First, what kind of computer is this?")
    print("  1. Desktop")
    print("  2. Laptop")
    while True:
        raw = input("Enter your choice (1 or 2): ").strip()
        if raw == "1":
            return "desktop"
        if raw == "2":
            return "laptop"
        print("Please enter 1 or 2.")


def show_menu(problems: List[MainProblem]) -> None:
    print("\nWhat is your main problem?")
    for number, problem in enumerate(problems, start=1):
        print(f"  {number}. {problem.label}")


def show_results(memory: WorkingMemory, diagnoses: Dict[str, dict],
                 intermediate_labels: Dict[str, str]) -> None:
    print("\n" + "=" * 60)
    print("DIAGNOSTIC RESULT")
    print("=" * 60)

    final_diagnoses = find_diagnoses(memory)
    partial_inferences = find_partial_inferences(memory, intermediate_labels)

    if final_diagnoses:
        print()
        for diagnosis in final_diagnoses:
            name = diagnoses.get(diagnosis, {}).get(
                "name", diagnosis.replace(DIAGNOSIS_PREFIX, "").replace("_", " ").title()
            )
            reasoning = reasoning_for_diagnosis(memory, diagnosis)
            recommendations = recommendations_for_diagnosis(memory, diagnosis, diagnoses)
            print(f"Possible diagnosis: {name}")
            print("Reasoning:")
            for line in reasoning:
                print(f"  - {line}")
            if recommendations:
                print("Recommendation:")
                for rec in recommendations:
                    print(f"  - {rec}")
            print()
    else:
        print("\nInsufficient evidence for a final diagnosis.")
        if partial_inferences:
            print("\nThe evidence supports only a partial conclusion:")
            for label, explanation in partial_inferences:
                print(f"  - {label}")
                print(f"    {explanation}")
            print("\nConsider giving more specific answers or checking the system further.")
        else:
            print("No conclusions could be drawn from the answers given.")
            print("Try answering with more specific observations.")


def find_diagnoses(memory: WorkingMemory) -> List[str]:
    return sorted(f for f in memory.facts if f.startswith(DIAGNOSIS_PREFIX))


def find_partial_inferences(memory: WorkingMemory, labels: Dict[str, str]) -> List[tuple]:
    """Intermediate facts that were inferred but did not lead to a diagnosis."""
    partial = []
    for fact in sorted(memory.inferred_facts):
        if fact.startswith(DIAGNOSIS_PREFIX):
            continue
        label = labels.get(fact, fact.replace("_", " ").title())
        explanation = explanation_for_fact(memory, fact)
        partial.append((label, explanation))
    return partial


def reasoning_for_diagnosis(memory: WorkingMemory, diagnosis: str) -> List[str]:
    """Human-readable reasoning lines from every rule that reached this diagnosis."""
    lines = []
    for entry in memory.fired_rules:
        if diagnosis in entry.rule.conclusions:
            lines.append(entry.rule.explanation)
    return lines


def explanation_for_fact(memory: WorkingMemory, fact: str) -> str:
    for entry in reversed(memory.fired_rules):
        if fact in entry.rule.conclusions:
            return entry.rule.explanation
    return ""


def recommendations_for_diagnosis(memory: WorkingMemory, diagnosis: str,
                                  diagnoses: Dict[str, dict]) -> List[str]:
    recommendations = []
    for entry in memory.fired_rules:
        if diagnosis in entry.rule.conclusions and entry.rule.recommendation:
            recommendations.append(entry.rule.recommendation)
    default = diagnoses.get(diagnosis, {}).get("default_recommendation")
    if not recommendations and default:
        recommendations.append(default)
    # Deduplicate while keeping order.
    return list(dict.fromkeys(recommendations))


def show_trace(memory: WorkingMemory) -> None:
    print("\n" + "=" * 60)
    print("DETAILED REASONING TRACE")
    print("=" * 60)

    print("\nStarting facts (from your answers):")
    for fact in sorted(memory.user_facts):
        print(f"  * {fact}")

    print("\nRules that fired:")
    for entry in memory.fired_rules:
        rule = entry.rule
        print(f"\n  Step {entry.step} — Rule {rule.id} [priority {rule.priority}]")
        print(f"    IF {', '.join(rule.conditions)}")
        print(f"    THEN {', '.join(entry.facts_added)}")
        print(f"    Explanation: {rule.explanation}")

    print("\nFinal facts:")
    for fact in sorted(memory.facts):
        print(f"  * {fact}")

    print("\nEnd of trace.")


def run_session(rules, problems, questions,
                machine_type: str, problem_id: str, answers: Dict[str, bool]) -> WorkingMemory:
    """Run one diagnostic session programmatically (used for demos/tests)."""
    questionnaire = Questionnaire(problems, questions)
    problem = next(p for p in problems if p.id == problem_id)
    facts = questionnaire.collect_facts(problem, machine_type, answers)
    engine = InferenceEngine(rules)
    return engine.run(facts)


def main() -> None:
    try:
        rules, diagnoses, intermediate_labels, problems, questions = load_assets()
    except (OSError, ValueError) as error:
        print(f"Error loading data: {error}")
        sys.exit(1)

    print("=" * 60)
    print("   COMPUTER TROUBLESHOOTING EXPERT SYSTEM")
    print("=" * 60)
    print("Answer a few questions and the system will suggest")
    print("possible causes of your computer problem.")

    machine_type = choose_machine_type()
    show_menu(problems)

    questionnaire = Questionnaire(problems, questions)
    while True:
        try:
            problem = questionnaire.choose_problem()
            break
        except ValueError as error:
            print(error)

    print("\n--- Diagnostic questions ---")
    facts = questionnaire.collect_facts(problem, machine_type)
    if facts:
        print("\nCollected facts:")
        for fact in facts:
            print(f"  * {fact}")

    engine = InferenceEngine(rules)
    memory = engine.run(facts)

    show_results(memory, diagnoses, intermediate_labels)

    if ask_yes_no("Show the detailed reasoning trace?"):
        show_trace(memory)


def ask_yes_no(prompt: str) -> bool:
    while True:
        raw = input(f"{prompt} (yes/no): ").strip().lower()
        if raw in ("y", "yes"):
            return True
        if raw in ("n", "no"):
            return False
        print("Please answer 'yes' or 'no'.")


if __name__ == "__main__":
    main()

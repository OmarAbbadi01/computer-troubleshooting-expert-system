"""Command-line entry point for the Computer Troubleshooting Expert System.

Flow: choose a language -> choose a main problem -> relevant questions ->
facts -> forward chaining inference -> diagnosis (or a simple "no
conclusion" message). Everything is shown in the chosen language.
"""

from __future__ import annotations

import os
import sys
from typing import Dict, List

from bilingual import render
from engine import InferenceEngine
from knowledge_base import load_diagnoses, load_questionnaire, load_rules
from models import MainProblem, WorkingMemory
from questionnaire import Questionnaire

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
KNOWLEDGE_BASE_FILE = os.path.join(DATA_DIR, "knowledge_base.json")
QUESTIONS_FILE = os.path.join(DATA_DIR, "questions.json")

DIAGNOSIS_PREFIX = "diagnosis_"

UI = {
    "language_prompt": {"en": "Choose your language", "ar": "اختر اللغة"},
    "english": {"en": "English", "ar": "الإنجليزية"},
    "arabic": {"en": "Arabic", "ar": "العربية"},
    "language_choice": {"en": "Enter your choice (1 or 2):", "ar": "أدخل اختيارك (1 أو 2):"},
    "invalid_language": {"en": "Please enter 1 or 2.", "ar": "يرجى إدخال 1 أو 2."},
    "title": {
        "en": "COMPUTER TROUBLESHOOTING EXPERT SYSTEM",
        "ar": "نظام خبير لتشخيص مشاكل الحاسوب",
    },
    "intro": {
        "en": "Answer a few questions and the system will suggest possible causes of your computer problem.",
        "ar": "أجب عن بعض الأسئلة وسيقترح النظام الأسباب المحتملة لمشكلة حاسوبك.",
    },
    "machine_prompt": {
        "en": "First, what kind of computer is this?",
        "ar": "أولاً، ما نوع هذا الحاسوب؟",
    },
    "desktop": {"en": "Desktop", "ar": "حاسوب مكتبي"},
    "laptop": {"en": "Laptop", "ar": "حاسوب محمول"},
    "machine_choice": {"en": "Enter your choice (1 or 2):", "ar": "أدخل اختيارك (1 أو 2):"},
    "invalid_machine": {"en": "Please enter 1 or 2.", "ar": "يرجى إدخال 1 أو 2."},
    "menu_prompt": {"en": "What is your main problem?", "ar": "ما هي مشكلتك الرئيسية؟"},
    "questions_heading": {"en": "Diagnostic questions", "ar": "أسئلة التشخيص"},
    "collected_facts": {"en": "Collected facts", "ar": "الحقائق المجمعة"},
    "result_heading": {"en": "DIAGNOSTIC RESULT", "ar": "نتيجة التشخيص"},
    "possible_diagnosis": {"en": "Possible diagnosis", "ar": "التشخيص المحتمل"},
    "reasoning": {"en": "Reasoning", "ar": "التعليل"},
    "recommendation": {"en": "Recommendation", "ar": "التوصية"},
    "no_conclusion": {
        "en": "No conclusion could be drawn from the answers given.",
        "ar": "لا يمكن استخلاص أي نتيجة من الإجابات المعطاة.",
    },
    "no_conclusion_hint": {
        "en": "Try answering with more specific observations.",
        "ar": "جرّب الإجابة بملاحظات أكثر تحديداً.",
    },
    "load_error": {"en": "Error loading data", "ar": "خطأ في تحميل البيانات"},
}


def load_assets():
    """Load and validate all data files."""
    rules = load_rules(KNOWLEDGE_BASE_FILE)
    diagnoses = load_diagnoses(KNOWLEDGE_BASE_FILE)
    problems, questions = load_questionnaire(QUESTIONS_FILE)
    return rules, diagnoses, problems, questions


def choose_language() -> str:
    """Ask the user for the interface language once, at the start."""
    print(f"{render(UI['language_prompt'], 'en')} / {render(UI['language_prompt'], 'ar')}")
    print(f"  1. {render(UI['english'], 'en')} / {render(UI['english'], 'ar')}")
    print(f"  2. {render(UI['arabic'], 'en')} / {render(UI['arabic'], 'ar')}")
    while True:
        raw = input(f"{render(UI['language_choice'], 'en')} / {render(UI['language_choice'], 'ar')} ").strip()
        if raw == "1":
            return "en"
        if raw == "2":
            return "ar"
        print(f"{render(UI['invalid_language'], 'en')} / {render(UI['invalid_language'], 'ar')}")


def choose_machine_type(lang: str) -> str:
    print(render(UI["machine_prompt"], lang))
    print(f"  1. {render(UI['desktop'], lang)}")
    print(f"  2. {render(UI['laptop'], lang)}")
    while True:
        raw = input(f"{render(UI['machine_choice'], lang)} ").strip()
        if raw == "1":
            return "desktop"
        if raw == "2":
            return "laptop"
        print(render(UI["invalid_machine"], lang))


def show_menu(problems: List[MainProblem], lang: str) -> None:
    print()
    print(render(UI["menu_prompt"], lang))
    for number, problem in enumerate(problems, start=1):
        print(f"  {number}. {render(problem.label, lang)}")


def show_results(memory: WorkingMemory, diagnoses: Dict[str, dict], lang: str) -> None:
    print("\n" + "=" * 60)
    print(render(UI["result_heading"], lang))
    print("=" * 60)

    final_diagnoses = find_diagnoses(memory)

    if final_diagnoses:
        print()
        for diagnosis in final_diagnoses:
            name = diagnoses.get(diagnosis, {}).get("name")
            if not isinstance(name, dict) or not name:
                label = diagnosis.replace(DIAGNOSIS_PREFIX, "").replace("_", " ").title()
                name = {"en": label, "ar": label}
            reasoning = reasoning_for_diagnosis(memory, diagnosis)
            recommendations = recommendations_for_diagnosis(memory, diagnosis, diagnoses)
            print(f"{render(UI['possible_diagnosis'], lang)}: {render(name, lang)}")
            print(render(UI["reasoning"], lang) + ":")
            for line in reasoning:
                print(f"  - {render(line, lang)}")
            if recommendations:
                print(render(UI["recommendation"], lang) + ":")
                for rec in recommendations:
                    print(f"  - {render(rec, lang)}")
            print()
    else:
        print()
        print(render(UI["no_conclusion"], lang))
        print(render(UI["no_conclusion_hint"], lang))


def find_diagnoses(memory: WorkingMemory) -> List[str]:
    return sorted(f for f in memory.facts if f.startswith(DIAGNOSIS_PREFIX))


def reasoning_for_diagnosis(memory: WorkingMemory, diagnosis: str) -> List[Dict[str, str]]:
    """Human-readable reasoning lines from every rule that reached this diagnosis."""
    lines = []
    for entry in memory.fired_rules:
        if diagnosis in entry.rule.conclusions:
            lines.append(entry.rule.explanation)
    return lines


def recommendations_for_diagnosis(
    memory: WorkingMemory, diagnosis: str, diagnoses: Dict[str, dict]
) -> List[Dict[str, str]]:
    recommendations = []
    for entry in memory.fired_rules:
        if diagnosis in entry.rule.conclusions and entry.rule.recommendation:
            recommendations.append(entry.rule.recommendation)
    default = diagnoses.get(diagnosis, {}).get("default_recommendation")
    if not recommendations and default:
        recommendations.append(default)
    # Deduplicate while keeping order (texts are dicts, so use tuple keys).
    seen = set()
    unique = []
    for rec in recommendations:
        key = (rec.get("en", ""), rec.get("ar", ""))
        if key not in seen:
            seen.add(key)
            unique.append(rec)
    return unique


def main() -> None:
    try:
        rules, diagnoses, problems, questions = load_assets()
    except (OSError, ValueError) as error:
        print(f"Error loading data: {error}")
        sys.exit(1)

    lang = choose_language()

    print("=" * 60)
    print(f"   {render(UI['title'], lang)}")
    print("=" * 60)
    print(render(UI["intro"], lang))

    machine_type = choose_machine_type(lang)
    show_menu(problems, lang)

    questionnaire = Questionnaire(problems, questions, lang)
    while True:
        try:
            problem = questionnaire.choose_problem()
            break
        except ValueError as error:
            print(error)

    print()
    print("--- " + render(UI["questions_heading"], lang) + " ---")
    facts = questionnaire.collect_facts(problem, machine_type)
    if facts:
        print()
        print(render(UI["collected_facts"], lang) + ":")
        for fact in facts:
            print(f"  * {fact}")

    engine = InferenceEngine(rules)
    memory = engine.run(facts)

    show_results(memory, diagnoses, lang)


if __name__ == "__main__":
    main()

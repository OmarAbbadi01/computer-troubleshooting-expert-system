"""نقطة الدخول الرئيسية للنظام."""

import os
import sys
from typing import Dict, List

from engine import InferenceEngine
from knowledge_base import load_diagnoses, load_questionnaire, load_rules
from models import MainProblem, WorkingMemory
from questionnaire import Questionnaire

DIAGNOSIS_PREFIX = "diagnosis_"


def choose_machine_type() -> str:
    print("أولاً، ما نوع هذا الحاسوب؟")
    print("  1. حاسوب مكتبي")
    print("  2. حاسوب محمول")
    while True:
        raw = input("أدخل اختيارك (1 أو 2): ").strip()
        if raw == "1":
            return "desktop"
        if raw == "2":
            return "laptop"
        print("يرجى إدخال 1 أو 2.")


def show_menu(problems: List[MainProblem]) -> None:
    print()
    print("ما هي مشكلتك الرئيسية؟")
    for number, problem in enumerate(problems, start=1):
        print(f"  {number}. {problem.label}")


def show_results(memory: WorkingMemory, diagnoses: Dict[str, dict]) -> None:
    print("\n" + "=" * 60)
    print("   نتيجة التشخيص")
    print("=" * 60)

    final_diagnoses = find_diagnoses(memory)

    if final_diagnoses:
        print()
        for diagnosis in final_diagnoses:
            name = diagnoses.get(diagnosis, {}).get("name")
            if not name:
                name = diagnosis.replace(DIAGNOSIS_PREFIX, "").replace("_", " ").title()
            reasoning = reasoning_for_diagnosis(memory, diagnosis)
            recommendations = recommendations_for_diagnosis(memory, diagnosis, diagnoses)
            print(f"التشخيص المحتمل: {name}")
            print("التعليل:")
            for line in reasoning:
                print(f"  - {line}")
            if recommendations:
                print("التوصية:")
                for rec in recommendations:
                    print(f"  - {rec}")
            print()
    else:
        print()
        print("لا يمكن استخلاص أي نتيجة من الإجابات المعطاة.")
        print("جرّب الإجابة بملاحظات أكثر تحديداً.")


def find_diagnoses(memory: WorkingMemory) -> List[str]:
    """استخراج حقائق التشخيص من الذاكرة العاملة (التي تبدأ بـ diagnosis_)."""
    return sorted(f for f in memory.facts if f.startswith(DIAGNOSIS_PREFIX))


def reasoning_for_diagnosis(memory: WorkingMemory, diagnosis: str) -> List[str]:
    """جمع التعليلات من القواعد التي ساهمت في هذا التشخيص."""
    lines = []
    for entry in memory.fired_rules:
        if diagnosis in entry.rule.conclusions:
            lines.append(entry.rule.explanation)
    return lines


def recommendations_for_diagnosis(
    memory: WorkingMemory, diagnosis: str, diagnoses: Dict[str, dict]
) -> List[str]:
    """جمع التوصيات من القواعد (+ الافتراضية إن لم توجد توصيات)."""
    recommendations = []
    for entry in memory.fired_rules:
        if diagnosis in entry.rule.conclusions and entry.rule.recommendation:
            recommendations.append(entry.rule.recommendation)
    default = diagnoses.get(diagnosis, {}).get("default_recommendation")
    if not recommendations and default:
        recommendations.append(default)
    seen = set()
    unique = []
    for rec in recommendations:
        if rec not in seen:
            seen.add(rec)
            unique.append(rec)
    return unique


def main() -> None:
    rules = load_rules()
    diagnoses = load_diagnoses()
    problems, questions = load_questionnaire()

    print("=" * 60)
    print("   نظام خبير لتشخيص مشاكل الحاسوب")
    print("=" * 60)
    print("أجب عن بعض الأسئلة وسيقترح النظام الأسباب المحتملة لمشكلة حاسوبك.")

    machine_type = choose_machine_type()
    show_menu(problems)

    questionnaire = Questionnaire(problems, questions)
    while True:
        try:
            problem = questionnaire.choose_problem()
            break
        except ValueError as error:
            print(error)

    print()
    print("--- أسئلة التشخيص ---")
    facts = questionnaire.collect_facts(problem, machine_type)
    if facts:
        print()
        print("الحقائق المجمعة:")
        for fact in facts:
            print(f"  * {fact}")

    engine = InferenceEngine(rules)
    memory = engine.run(facts)

    show_results(memory, diagnoses)


if __name__ == "__main__":
    main()

"""Loads and validates the JSON knowledge base and the questionnaire.

The knowledge base (rules and diagnosis names) is domain knowledge and is
kept completely separate from the inference engine. Loading performs simple
validation so that a malformed file fails with a readable error instead of
crashing later.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List, Tuple, Union

from models import MainProblem, Question, Rule

JsonValue = Union[dict, list, str, int, float, bool, None]


def load_rules(path) -> List[Rule]:
    """Load and validate the IF-THEN rules from a JSON file."""
    data = _read_json(path)
    raw_rules = _require_list(data, "rules", path)

    rules: List[Rule] = []
    seen_ids = set()

    for index, raw in enumerate(raw_rules):
        rule = _parse_rule(raw, index, path)
        if rule.id in seen_ids:
            raise ValueError(
                f"Knowledge base error in {path}: duplicate rule id '{rule.id}'."
            )
        seen_ids.add(rule.id)
        rules.append(rule)

    return rules


def load_diagnoses(path) -> Dict[str, dict]:
    """Load display names / default recommendations for diagnoses."""
    data = _read_json(path)
    diagnoses = data.get("diagnoses", {})
    if not isinstance(diagnoses, dict):
        raise ValueError(f"Knowledge base error in {path}: 'diagnoses' must be an object.")
    for did, raw in diagnoses.items():
        if not isinstance(raw, dict):
            raise ValueError(f"Knowledge base error in {path}: diagnosis '{did}' must be an object.")
        _bilingual(raw.get("name"), path, f"diagnosis '{did}' 'name'")
        default = raw.get("default_recommendation")
        if default is not None:
            _bilingual(default, path, f"diagnosis '{did}' 'default_recommendation'")
    return diagnoses


def load_questionnaire(path) -> Tuple[List[MainProblem], Dict[str, Question]]:
    """Load the main-problem menu and the question definitions."""
    data = _read_json(path)

    raw_problems = _require_list(data, "main_problems", path)
    raw_questions = data.get("questions", {})
    if not isinstance(raw_questions, dict):
        raise ValueError(f"Questionnaire error in {path}: 'questions' must be an object.")

    questions: Dict[str, Question] = {}
    for qid, raw in raw_questions.items():
        if not isinstance(raw, dict):
            raise ValueError(
                f"Questionnaire error in {path}: question '{qid}' must be an object."
            )
        questions[qid] = Question(
            id=qid,
            text=_bilingual(raw.get("text"), path, f"question '{qid}' 'text'"),
            yes_fact=raw.get("yes_fact"),
            no_fact=raw.get("no_fact"),
            laptop_only=bool(raw.get("laptop_only", False)),
        )
        if not questions[qid].yes_fact and not questions[qid].no_fact:
            raise ValueError(
                f"Questionnaire error in {path}: question '{qid}' produces no facts."
            )

    problems: List[MainProblem] = []
    for index, raw in enumerate(raw_problems):
        if not isinstance(raw, dict):
            raise ValueError(
                f"Questionnaire error in {path}: main problem #{index + 1} must be an object."
            )
        problem_id = str(raw.get("id", ""))
        if not problem_id:
            raise ValueError(
                f"Questionnaire error in {path}: main problem #{index + 1} has no 'id'."
            )
        qids = raw.get("questions", [])
        for qid in qids:
            if qid not in questions:
                raise ValueError(
                    f"Questionnaire error in {path}: problem '{problem_id}' "
                    f"references unknown question '{qid}'."
                )
        problems.append(
            MainProblem(
                id=problem_id,
                label=_bilingual(raw.get("label"), path, f"problem '{problem_id}' 'label'"),
                question_ids=list(qids),
            )
        )

    return problems, questions


def _parse_rule(raw: JsonValue, index: int, path) -> Rule:
    if not isinstance(raw, dict):
        raise ValueError(
            f"Knowledge base error in {path}: rule #{index + 1} must be an object."
        )

    rule_id = raw.get("id", "")
    if not rule_id:
        raise ValueError(f"Knowledge base error in {path}: rule #{index + 1} has no 'id'.")
    conditions = raw.get("conditions")
    conclusions = raw.get("conclusions")

    if not isinstance(conditions, list) or not conditions:
        raise ValueError(
            f"Knowledge base error in {path}: rule '{rule_id}' must have non-empty 'conditions'."
        )
    if not isinstance(conclusions, list) or not conclusions:
        raise ValueError(
            f"Knowledge base error in {path}: rule '{rule_id}' must have non-empty 'conclusions'."
        )

    explanation = _bilingual(raw.get("explanation"), path, f"rule '{rule_id}' 'explanation'")
    recommendation = raw.get("recommendation")
    if recommendation is not None:
        recommendation = _bilingual(recommendation, path, f"rule '{rule_id}' 'recommendation'")

    return Rule(
        id=rule_id,
        conditions=[str(c) for c in conditions],
        conclusions=[str(c) for c in conclusions],
        explanation=explanation,
        recommendation=recommendation,
    )


def _bilingual(value: JsonValue, path, where: str) -> Dict[str, str]:
    """Validate a bilingual text object: a dict with non-empty 'en' and 'ar'."""
    if not isinstance(value, dict):
        raise ValueError(
            f"Data file {path}: {where} must be an object with 'en' and 'ar' texts."
        )
    result: Dict[str, str] = {}
    for lang in ("en", "ar"):
        part = value.get(lang, "")
        if not isinstance(part, str) or not part.strip():
            raise ValueError(
                f"Data file {path}: {where} is missing a non-empty '{lang}' text."
            )
        result[lang] = part
    return result


def _read_json(path) -> dict:
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Data file not found: {path}")
    with path.open(encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"Data file {path} must contain a JSON object.")
    return data


def _require_list(data: dict, key: str, path) -> list:
    value = data.get(key)
    if not isinstance(value, list):
        raise ValueError(f"Data file {path} must contain a '{key}' array.")
    return value

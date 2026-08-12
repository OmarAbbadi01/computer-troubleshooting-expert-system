"""Loads and validates the JSON knowledge base and the questionnaire.

The knowledge base (rules, diagnosis names, intermediate-fact labels) is
domain knowledge and is kept completely separate from the inference
engine. Loading performs simple validation so that a malformed file
fails with a readable error instead of crashing later.
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
    return diagnoses


def load_intermediate_labels(path) -> Dict[str, str]:
    """Load human-readable labels for intermediate facts."""
    data = _read_json(path)
    labels = data.get("intermediate_facts", {})
    if not isinstance(labels, dict):
        raise ValueError(
            f"Knowledge base error in {path}: 'intermediate_facts' must be an object."
        )
    return labels


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
            text=str(raw.get("text", "")),
            yes_fact=raw.get("yes_fact"),
            no_fact=raw.get("no_fact"),
            laptop_only=bool(raw.get("laptop_only", False)),
        )
        if not questions[qid].text:
            raise ValueError(f"Questionnaire error in {path}: question '{qid}' has no text.")
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
        qids = raw.get("questions", [])
        for qid in qids:
            if qid not in questions:
                raise ValueError(
                    f"Questionnaire error in {path}: problem '{raw.get('id')}' "
                    f"references unknown question '{qid}'."
                )
        problems.append(
            MainProblem(
                id=str(raw.get("id", "")),
                label=str(raw.get("label", "")),
                question_ids=list(qids),
            )
        )

    if not all(p.id and p.label for p in problems):
        raise ValueError(f"Questionnaire error in {path}: every problem needs 'id' and 'label'.")

    return problems, questions


def _parse_rule(raw: JsonValue, index: int, path) -> Rule:
    if not isinstance(raw, dict):
        raise ValueError(
            f"Knowledge base error in {path}: rule #{index + 1} must be an object."
        )

    rule_id = raw.get("id", "")
    conditions = raw.get("conditions")
    conclusions = raw.get("conclusions")
    explanation = raw.get("explanation", "")

    if not rule_id:
        raise ValueError(f"Knowledge base error in {path}: rule #{index + 1} has no 'id'.")
    if not isinstance(conditions, list) or not conditions:
        raise ValueError(
            f"Knowledge base error in {path}: rule '{rule_id}' must have non-empty 'conditions'."
        )
    if not isinstance(conclusions, list) or not conclusions:
        raise ValueError(
            f"Knowledge base error in {path}: rule '{rule_id}' must have non-empty 'conclusions'."
        )
    if not explanation:
        raise ValueError(
            f"Knowledge base error in {path}: rule '{rule_id}' must have an 'explanation'."
        )

    priority = raw.get("priority", 0)
    if not isinstance(priority, int) or isinstance(priority, bool):
        raise ValueError(
            f"Knowledge base error in {path}: rule '{rule_id}' has an invalid 'priority'."
        )

    recommendation = raw.get("recommendation")
    if recommendation is not None and not isinstance(recommendation, str):
        raise ValueError(
            f"Knowledge base error in {path}: rule '{rule_id}' has an invalid 'recommendation'."
        )

    return Rule(
        id=rule_id,
        conditions=[str(c) for c in conditions],
        conclusions=[str(c) for c in conclusions],
        explanation=explanation,
        priority=priority,
        recommendation=recommendation,
    )


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

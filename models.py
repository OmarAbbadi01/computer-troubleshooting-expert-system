"""تعريفات البيانات المستخدمة في النظام."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Rule:
    id: str
    conditions: List[str]
    conclusions: List[str]
    explanation: str
    recommendation: Optional[str] = None


@dataclass
class Question:
    id: str
    text: str
    yes_fact: Optional[str] = None
    no_fact: Optional[str] = None
    laptop_only: bool = False


@dataclass
class MainProblem:
    id: str
    label: str
    question_ids: List[str] = field(default_factory=list)


@dataclass
class FiredRule:
    rule: Rule
    facts_added: List[str]


@dataclass
class WorkingMemory:
    facts: set = field(default_factory=set)
    fired_rules: List[FiredRule] = field(default_factory=list)

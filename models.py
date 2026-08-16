"""Simple data structures shared across the project.

Kept deliberately small: a rule, a question and the main-problem menu
entry. No domain logic lives here.

Every user-facing text is a bilingual dictionary with two keys:
"en" (English) and "ar" (Arabic).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class Rule:
    """A single IF-THEN rule from the knowledge base."""

    id: str
    conditions: List[str]
    conclusions: List[str]
    explanation: Dict[str, str]
    recommendation: Optional[Dict[str, str]] = None


@dataclass
class Question:
    """A Yes/No question that produces facts."""

    id: str
    text: Dict[str, str]
    yes_fact: Optional[str] = None
    no_fact: Optional[str] = None
    laptop_only: bool = False


@dataclass
class MainProblem:
    """One entry in the main-problem menu and the questions relevant to it."""

    id: str
    label: Dict[str, str]
    question_ids: List[str] = field(default_factory=list)


@dataclass
class FiredRule:
    """A record of one rule firing, used to explain the reasoning."""

    rule: Rule
    facts_added: List[str]


@dataclass
class WorkingMemory:
    """Facts known to the system plus a record of how they were derived."""

    facts: set = field(default_factory=set)
    fired_rules: List[FiredRule] = field(default_factory=list)

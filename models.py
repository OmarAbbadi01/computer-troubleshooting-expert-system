"""Simple data structures shared across the project.

Kept deliberately small: a rule, a question and the main-problem menu
entry. No domain logic lives here.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Rule:
    """A single IF-THEN rule from the knowledge base."""

    id: str
    conditions: List[str]
    conclusions: List[str]
    explanation: str
    priority: int = 0
    recommendation: Optional[str] = None


@dataclass
class Question:
    """A Yes/No question that produces facts."""

    id: str
    text: str
    yes_fact: Optional[str] = None
    no_fact: Optional[str] = None
    laptop_only: bool = False


@dataclass
class MainProblem:
    """One entry in the main-problem menu and the questions relevant to it."""

    id: str
    label: str
    question_ids: List[str] = field(default_factory=list)


@dataclass
class FiredRule:
    """A record of one rule firing, used for the reasoning trace."""

    step: int
    rule: Rule
    facts_added: List[str]


@dataclass
class WorkingMemory:
    """Facts known to the system plus a trace of how they were derived."""

    facts: set = field(default_factory=set)
    user_facts: set = field(default_factory=set)
    inferred_facts: set = field(default_factory=set)
    fired_rules: List[FiredRule] = field(default_factory=list)

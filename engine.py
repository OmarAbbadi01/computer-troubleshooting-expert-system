"""Generic forward-chaining inference engine.

This module knows nothing about computers, power, networks or storage.
It only understands generic concepts: facts, rule conditions, rule
conclusions and priorities. All domain knowledge lives in the JSON
knowledge base and is passed in as Rule objects.
"""

from __future__ import annotations

from typing import Iterable, List

from models import FiredRule, Rule, WorkingMemory


class InferenceEngine:
    """A small forward-chaining engine with a lightweight agenda.

    It repeatedly looks for rules whose conditions are satisfied by the
    current facts, fires them in a stable order and adds the inferred
    facts to working memory. It stops when a fixed point is reached
    (no rule can produce a new fact).
    """

    def __init__(self, rules: List[Rule]) -> None:
        self.rules = list(rules)

    def run(self, initial_facts: Iterable[str]) -> WorkingMemory:
        """Run forward chaining starting from the given facts."""
        memory = WorkingMemory()
        memory.facts = set(initial_facts)

        changed = True

        while changed:
            changed = False

            "Get initial rules from initial facts"
            applicable = self._applicable_rules(memory.facts)

            if not applicable:
                break

            # Fire rules in a deterministic order (rule id) so the
            # system behaves the same way on every run.
            applicable.sort(key=lambda r: r.id)

            for rule in applicable:
                new_facts = [c for c in rule.conclusions if c not in memory.facts]
                if not new_facts:
                    # Everything the rule concludes is already known:
                    # firing it again would be pointless.
                    continue

                memory.facts.update(new_facts)

                memory.fired_rules.append(FiredRule(rule, new_facts))
                changed = True

        return memory

    def _applicable_rules(self, facts: set) -> List[Rule]:
        return [r for r in self.rules if all(c in facts for c in r.conditions)]

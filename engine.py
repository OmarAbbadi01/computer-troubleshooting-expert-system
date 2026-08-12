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
    current facts, fires them in priority order and adds the inferred
    facts to working memory. It stops when a fixed point is reached
    (no rule can produce a new fact).
    """

    def __init__(self, rules: List[Rule]) -> None:
        self.rules = list(rules)

    def run(self, initial_facts: Iterable[str]) -> WorkingMemory:
        """Run forward chaining starting from the given facts."""
        memory = WorkingMemory()
        memory.user_facts = set(initial_facts)
        memory.facts = set(initial_facts)

        step = 0
        changed = True

        while changed:
            changed = False

            applicable = self._applicable_rules(memory.facts)

            if not applicable:
                break

            # Lightweight conflict resolution: higher priority first,
            # rule ID used as a stable tie-breaker.
            applicable.sort(key=lambda r: (-r.priority, r.id))

            for rule in applicable:
                new_facts = [c for c in rule.conclusions if c not in memory.facts]
                if not new_facts:
                    # Everything the rule concludes is already known:
                    # firing it again would be pointless.
                    continue

                memory.facts.update(new_facts)
                memory.inferred_facts.update(new_facts)

                step += 1
                memory.fired_rules.append(FiredRule(step, rule, new_facts))
                changed = True

        return memory

    def _applicable_rules(self, facts: set) -> List[Rule]:
        return [r for r in self.rules if all(c in facts for c in r.conditions)]

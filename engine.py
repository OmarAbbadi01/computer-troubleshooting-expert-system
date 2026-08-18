"""محرك الاستدلال الأمامي.

يشتغل فقط على القواعد والحقائق، لا يعرف أي معرفة عن الحاسوب.
"""

from __future__ import annotations

from typing import Iterable, List

from models import FiredRule, Rule, WorkingMemory


class InferenceEngine:
    """محرك استدلال أمامي يكرر تنفيذ القواعد حتى لا تبقى هناك قواعد جديدة."""

    def __init__(self, rules: List[Rule]) -> None:
        self.rules = list(rules)

    def run(self, initial_facts: Iterable[str]) -> WorkingMemory:
        memory = WorkingMemory()
        memory.facts = set(initial_facts)

        changed = True

        while changed:
            changed = False

            applicable = self._applicable_rules(memory.facts)

            if not applicable:
                break

            applicable.sort(key=lambda r: r.id)

            for rule in applicable:
                new_facts = [c for c in rule.conclusions if c not in memory.facts]
                if not new_facts:
                    continue

                memory.facts.update(new_facts)
                memory.fired_rules.append(FiredRule(rule, new_facts))
                changed = True

        return memory

    def _applicable_rules(self, facts: set) -> List[Rule]:
        """إيجاد القواعد التي تتطابق جميع شروطها مع الحقائق الحالية."""
        return [r for r in self.rules if all(c in facts for c in r.conditions)]

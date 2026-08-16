# AGENTS.md — Context for AI assistants working on this project

This file gives an AI agent everything it needs to resume work on this project
without re-reading every file. Read the linked files when details matter.

## Project at a glance

A **command-line expert system** in plain Python (3.9+, standard library only)
that diagnoses broad categories of computer problems. User picks one of 9 main
problems, answers relevant Yes/No questions, and a **forward-chaining
inference engine** reasons over **IF-THEN rules** stored in JSON to produce
diagnoses, explanations, and recommendations. It is an academic
demonstration of expert-system concepts — NOT a production tool.

## Repo / git state

- Local path: `/Users/omarabbadi/Desktop/AI-project/computer-troubleshooting-expert-system`
- Remote: `origin` = `https://github.com/OmarAbbadi01/computer-troubleshooting-expert-system.git`, branch `main`
- Repo-local identity: **Razan AbuBaker** / `razanabubaker@gmail.com`
- The remote push has NOT completed yet (HTTPS needs the owner's token; SSH key not authorized). The owner pushes manually. Do not attempt auth workarounds.
- Commits so far:
  - `654a960` Implement computer troubleshooting expert system (root commit, 18 files)
  - `2ec6532` Add proper Python .gitignore

## How to run

```bash
python3 main.py                          # interactive CLI
python3 -m evaluation.run_evaluation     # run the 10 (+1) test cases
python3 -m py_compile main.py engine.py questionnaire.py knowledge_base.py models.py evaluation/run_evaluation.py evaluation/cases.py   # syntax check
```

## Architecture (separation is the core requirement)

```
User -> Questionnaire -> facts -> WorkingMemory -> Forward-Chaining Engine <-> Knowledge Base (JSON)
                                                    -> diagnoses -> explanation + recommendation
```

| File | Responsibility | Domain logic? |
|------|----------------|---------------|
| `main.py` | CLI: welcome, machine type, menu, questions, result display | presentation only |
| `questionnaire.py` | Maps selected problem -> relevant questions; Yes/No answers -> facts (`Questionnaire`) | none (no diagnosis) |
| `engine.py` | Generic forward chaining (`InferenceEngine`, `WorkingMemory`) | NONE — generic only |
| `knowledge_base.py` | Loads + validates `data/*.json`; readable errors | validation only |
| `models.py` | `Rule`, `Question`, `MainProblem`, `FiredRule`, `WorkingMemory` dataclasses | — |
| `data/knowledge_base.json` | 34 IF-THEN rules + diagnoses metadata | **all domain knowledge** |
| `data/questions.json` | 9 main problems + 35 questions (yes_fact / no_fact, laptop_only) | — |
| `evaluation/cases.py` + `run_evaluation.py` | 10 (+1) scenarios; separate from the app | test-only |
| `docs/` | Academic docs + `BEGINNERS_GUIDE.md` + `DISCUSSION_FAQ.md` | — |

## Key implementation facts

- **34 rules** (P1–P5 power, D1–D4 display, B1–B4 boot, PERF1–4 performance,
  O1–O4 overheating, NET1–4 network, S1–3 storage, M1–3 memory, PE1–3
  peripheral). About half conclude **intermediate facts**
  (`power_delivery_issue`, `cooling_problem`, `os_boot_reached`,
  `local_connectivity_only`, `storage_pressure`, `memory_pressure`, etc.),
  the rest conclude `diagnosis_*` facts. Several diagnoses need 2-step
  chains; performance's startup-overload path is a 3-step chain.
- **Diagnosis facts** use the `diagnosis_` prefix (e.g. `diagnosis_network`);
  the presentation layer treats any fact with that prefix as a final diagnosis.
- **Termination**: a rule only fires if it adds at least one new fact, so no
  repeats and no infinite loops (fixed point). Facts are only added, never retracted.
- **Firing order**: rules are fired in a deterministic order (sorted by rule
  id), so the system behaves the same way on every run.
- **Facts vocabulary is shared across categories** (e.g. `computer_running`,
  `fans_running`, `post_screen_visible` are asked in multiple categories).
  Keep names consistent — avoid adding near-duplicates.
- **Rule semantics**: conditions = ALL must be present (AND). For OR logic,
  write separate rules (see P1/P2 both concluding `power_delivery_issue`).
- **Adaptive questionnaire**: laptop-only questions (e.g. `q_external_monitor`)
  are skipped for desktops via the `laptop_only` flag. The selected main
  problem determines which question ids are asked — no question logic does diagnosis.

## Rules for extending the project

- Put ALL new domain knowledge in `data/knowledge_base.json` / `data/questions.json` — **never** in the engine or CLI.
- `data/questions.json`: a question maps Yes/No to `yes_fact`/`no_fact`; every fact a rule uses must be producible by some asked question.
- Keep the knowledge base 30–35 rules and plain standard-library Python.
- `knowledge_base.py` validation runs on load — malformed JSON fails with a readable `ValueError`.
- Never hardcode the 10 evaluation cases into the application.
- If a question/fact is added, re-run `python3 -m evaluation.run_evaluation` and update `evaluation/cases.py` + `docs/testing_evaluation.md` as needed.

## Docs map

- `README.md` — title, requirements, run instructions, architecture, example session
- `docs/problem_analysis.md` — problem, target user, objectives (phase one)
- `docs/knowledge_base.md` — fact categories, intermediate facts, diagnoses, all 34 rules, sources
- `docs/inference_design.md` — why forward chaining, matching, firing order, fixed point, Mermaid diagram
- `docs/testing_evaluation.md` — the 10 (+1) cases with expected vs actual
- `docs/report_outline.md` — 15-section academic report template
- `docs/BEGINNERS_GUIDE.md` — bilingual (EN/AR) beginner walkthrough; NOT part of submission
- `docs/DISCUSSION_FAQ.md` — bilingual presentation Q&A with ready answers; NOT part of submission

## Evaluation summary (as of last run)

11/11 cases PASS: power, display, boot, network, overheating, performance,
storage, memory, peripheral, multiple-diagnoses (Performance + Storage), and
insufficient-evidence (no diagnosis when evidence is partial).

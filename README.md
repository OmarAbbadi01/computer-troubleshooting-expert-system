# Computer Troubleshooting Expert System

A command-line expert system written in plain Python that diagnoses broad
categories of computer problems. It asks the user a small set of relevant
Yes/No questions, collects the answers as facts, and uses a **forward-chaining
inference engine** over an **IF-THEN rule knowledge base** to infer possible
diagnoses with human-readable explanations.

The project is an academic demonstration of classic expert-system concepts:
knowledge base, facts / working memory, IF-THEN rules, forward chaining,
rule priorities, intermediate inferred facts, explainable reasoning, and a
clear separation between domain knowledge and inference logic.

## Requirements

- Python 3.9 or newer
- No third-party libraries (standard library only)

## How to run

```bash
python3 main.py
```

Run the independent evaluation scenarios:

```bash
python3 -m evaluation.run_evaluation
```

## Example session

```
1. Computer does not turn on
2. Computer turns on but the screen is blank
3. Computer does not boot properly
...
6. Internet/network is not working
...

--- Diagnostic questions ---
Is the computer connected to Wi-Fi? (yes/no): yes
Does the computer find any available Wi-Fi networks? (yes/no): yes
Can the computer communicate with the router (the local network)? (yes/no): yes
Can you open websites or reach the internet? (yes/no): no
...

DIAGNOSTIC RESULT
Possible diagnosis: Network problem
Reasoning:
  - The system inferred that connectivity works only inside the local
    network. Since the internet is unreachable, this is a network problem.
Recommendation:
  - Restart the router and modem. If the problem persists, contact your
    internet service provider.

Show the detailed reasoning trace? (yes/no): yes
```

## Architecture

```
User -> Questionnaire -> Input Facts -> Working Memory -> Forward-Chaining Engine
                                                          <-> Knowledge Base (JSON)
                                                          -> Inferred Facts -> Diagnoses
                                                                             -> Explanation + Recommendation
```

| Module | Responsibility |
|--------|----------------|
| `main.py` | CLI entry point: menu, questions, result and trace display |
| `questionnaire.py` | Maps the selected problem to relevant questions, turns answers into facts |
| `engine.py` | Generic forward-chaining inference engine (no domain knowledge) |
| `knowledge_base.py` | Loads and validates the JSON knowledge base and questionnaire |
| `models.py` | Small data structures (rules, questions, working memory) |
| `data/knowledge_base.json` | The domain rules, diagnoses and recommendations |
| `data/questions.json` | The questionnaire and the facts produced by each answer |
| `evaluation/` | 10 independent evaluation scenarios (not used by the app) |
| `docs/` | Academic documentation (analysis, KB, inference design, testing, outline) |

Key ideas:

- **Knowledge is data, not code.** The 34 IF-THEN rules live in
  `data/knowledge_base.json`. The engine understands only generic concepts
  (conditions, conclusions, priorities) and contains no computer-diagnostic
  logic.
- **Forward chaining.** The engine repeatedly finds satisfied rules, fires
  them in priority order, and adds the inferred facts to working memory until
  a fixed point is reached. Several diagnoses require multi-step chains such
  as `facts -> cooling_problem -> Overheating problem`.
- **Explanations.** Every rule carries a human-readable explanation and final
  diagnoses carry safe recommendations. An optional detailed reasoning trace
  shows the rules that fired and the facts each one inferred.

## Documentation

- [docs/problem_analysis.md](docs/problem_analysis.md)
- [docs/knowledge_base.md](docs/knowledge_base.md)
- [docs/inference_design.md](docs/inference_design.md)
- [docs/testing_evaluation.md](docs/testing_evaluation.md)
- [docs/report_outline.md](docs/report_outline.md)

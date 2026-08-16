# Report Outline

A template for the final university report, matching the assignment grading
rubric. Fill each section with material from the project and the docs in this
repository.

1. **Introduction**
   - Problem statement and project goal.
   - Overview of expert systems and what this project demonstrates.

2. **Problem Analysis**
   - See `docs/problem_analysis.md`.
   - Symptoms covered, target user, objectives, scope.

3. **Knowledge Acquisition**
   - Sources: PC troubleshooting guides, OS support documentation, hardware
     documentation.
   - How symptoms were translated into facts and rules.

4. **Knowledge Base**
   - The 34 IF-THEN rules, fact vocabulary, intermediate facts, final
     diagnoses. See `docs/knowledge_base.md`.

5. **Knowledge Representation**
   - Facts, IF-THEN rules with explanations, JSON storage,
     separation of knowledge from mechanism.

6. **System Architecture**
   - CLI, questionnaire, working memory, knowledge base, inference engine.
   - Diagram from `docs/inference_design.md`.

7. **Forward-Chaining Mechanism**
   - Rule matching, firing order, fixed-point termination,
     multiple diagnoses, explanation tracking. See `docs/inference_design.md`.

8. **Implementation**
   - Module-by-module description (`main.py`, `engine.py`,
     `questionnaire.py`, `knowledge_base.py`, `models.py`, data files).
   - Why plain Python and the standard library were sufficient.

9. **User Interface**
   - Menu-driven CLI, Yes/No questions, result display. Include a screenshot
     of a full session.

10. **Testing and Evaluation**
    - The 10 evaluation cases, expected vs actual results.
    - See `docs/testing_evaluation.md`.

11. **Results**
    - Summary of outcomes: all cases passed, multiple diagnoses supported,
      insufficient-evidence handling works.

12. **Strengths and Limitations**
    - Strengths: simple, explainable, generic engine, separate knowledge base.
    - Limitations: broad diagnoses only, no probabilities, no deep repair
      guidance, static rule set.

13. **Recommendations / Future Improvements**
    - More rules and finer granularity, a richer question model, dynamic
      question selection, a small GUI if desired.

14. **References**
    - Troubleshooting guides, OS support pages, expert-systems textbook
      material (see `problem_analysis.md` for source types).

15. **Screenshots**
    - Main menu, question flow, diagnosis + explanation, evaluation run.

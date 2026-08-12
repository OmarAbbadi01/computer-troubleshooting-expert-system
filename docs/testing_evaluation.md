# Testing and Evaluation

The evaluation scenarios were defined **after** the questionnaire, facts,
rules and inference behavior were frozen, so they act as genuine verification
cases rather than driving the implementation. The application contains no
test-case-specific logic and does not reference these cases.

Run the evaluation from the project root:

```bash
python3 -m evaluation.run_evaluation
```

The scenarios are defined in `evaluation/cases.py` (evaluation only) and the
runner drives the real questionnaire and the real inference engine.

## The ten (plus one) cases

Each case records the starting problem, the answers, and the expected and
actual results. All cases passed.

| # | Case | Starting problem | Expected diagnosis | Actual diagnosis | Result | Notes |
|---|------|------------------|--------------------|------------------|--------|-------|
| 1 | Power | Computer does not turn on | Power problem | Power problem | PASS | Two-step chain: facts → `internal_power_fault` → Power problem |
| 2 | Display | Computer turns on but screen is blank | Display problem | Display problem | PASS | Two-step chain: facts → `display_path_fault` → Display problem |
| 3 | Boot / OS | Computer does not boot properly | Boot / operating-system problem | Boot / operating-system problem | PASS | Two-step chain: facts → `os_boot_reached` → Boot problem |
| 4 | Network | Internet/network is not working | Network problem | Network problem | PASS | Two-step chain: facts → `local_connectivity_only` → Network problem |
| 5 | Overheating | Computer gets hot or shuts down | Overheating problem | Overheating problem | PASS | Two-step chain: facts → `cooling_problem` → Overheating problem |
| 6 | Performance | Computer is slow | Performance problem | Performance problem | PASS | Three-step chain: facts → `system_slow_indicators` → `startup_overload` → Performance problem |
| 7 | Storage | Storage-related problem | Storage problem | Storage problem | PASS | Two-step chain: facts → `storage_pressure` → Storage problem |
| 8 | Memory | Memory-related problem | Memory problem | Memory problem | PASS | Two-step chain: facts → `memory_pressure` → Memory problem |
| 9 | Peripheral | Peripheral/device is not working | Peripheral/device problem | Peripheral/device problem | PASS | Single-step rule (device itself faulty) |
| 10 | Multiple diagnoses | Computer is slow | Performance problem **and** Storage problem | Performance problem **and** Storage problem | PASS | Two independent chains fire in one session |
| 11 | Insufficient evidence | Computer gets hot or shuts down | No final diagnosis; partial "Cooling problem exists" | No final diagnosis; partial "Cooling problem exists" | PASS | `cooling_problem` inferred but no unexpected shutdown |

### Notes on coverage

- **Multiple diagnoses:** case 10 — a slow computer with a nearly-full,
  constantly active disk produces both a Performance problem and a Storage
  problem through two independent forward-chaining chains.
- **Multi-step chaining:** cases 1–8 and 10 all demonstrate at least one
  two-step chain; case 6 demonstrates a three-step chain.
- **Insufficient evidence:** case 11 — the engine infers a partial conclusion
  (cooling problem) but reports that there is not enough evidence for a final
  diagnosis.
- **Laptop adaptation:** the external-monitor question is only asked for
  laptops; desktop sessions skip it (verified separately in case 2, where the
  question is not asked).
- **No hardcoded behavior:** the scenarios are run through the normal
  questionnaire and engine; no scenario-specific branch exists in the
  application.

# Problem Analysis

## Problem Description

Computer users may observe symptoms such as failure to turn on, a blank
screen, failure to boot properly, slow performance, overheating or unexpected
shutdowns, network failure, storage-related problems, memory-related problems,
or unresponsive peripherals.

The expert system attempts to reason from observable symptoms to **broad
possible causes**. It does not try to identify an exact failed component in
every situation; instead it returns broad diagnostic categories such as
"Power problem" or "Network problem", and more than one diagnosis can be
reported when the evidence supports it.

## Target User

General computer users or students with basic computer knowledge. The
questionnaire therefore uses plain-language Yes/No questions and avoids
technical jargon such as "POST" or "DHCP lease".

## Objectives

- Collect the user's symptoms through a small set of relevant questions.
- Represent those symptoms as internal facts.
- Apply expert rules stored in a separate knowledge base.
- Infer possible problem categories with forward chaining.
- Explain the reasoning behind each conclusion in plain language.
- Offer simple, safe recommendations.

## Scope

The system covers **desktop** and **laptop** computers across these areas:
power, display, boot/operating system, performance, overheating, networking,
storage, memory, and peripherals.

## Non-Goals

- Exact component-level fault diagnosis.
- Probability or confidence scoring.
- Repairs or unsafe procedures.

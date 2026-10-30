# Agent Flow

Kernel Design Agents is a repeatable loop for agent-driven implementation work. The loop is useful when a task needs both exploration and evidence-based promotion decisions.

## Principle

Keep the reusable workflow separate from the task workspace. This repository explains the flow. The task workspace owns code, tests, datasets, benchmark scripts, private rules, and generated artifacts.

MLSys-style benchmark work is one possible application of this loop. The same flow can also be used for compiler passes, runtime kernels, infrastructure changes, or other performance-sensitive tasks.

## Minimal Loop

1. Define the task contract.
2. Let the agent inspect the local workspace.
3. Make the agent write `docs/draft.md`.
4. Convert the draft into an executable plan.
5. Implement the first candidate.
6. Validate correctness.
7. Measure the target metric when applicable.
8. Record evidence and decide whether to keep, revise, or reject the candidate.
9. Repeat until the promotion criteria are met or the remaining blockers are explicit.

## Task Contract

Each task should state:

- Objective.
- Inputs and outputs.
- Correctness requirements.
- Constraints on implementation language, dependencies, APIs, or deployment.
- Validation command.
- Evaluation command, if different from validation.
- Promotion criteria.

For a PPU task, also record:

- PPU generation and actual compiler target, SDK/runtime and backend revision.
- Logical workload, physical layouts, masks, state and quantization contracts.
- Arithmetic and rounding boundaries, independent oracle and error criteria.
- Measurement scope: kernel, all operator kernels, public API or model phase.
- Cache policy and whether execution is on a device or a performance simulator.
- Device/time allocation and the concrete build, validation and profiling commands.

Read the relevant [PPU knowledge](../skills/ppu-kernel-knowledge/SKILL.md)
before drafting. For a port, list preserved, adapted and unverified algorithm,
layout, instruction, pipeline and scheduler components. Preserve the requested
implementation structure; an incomplete port cannot establish a hardware limit.

## Evidence Records

Use simple files in the task workspace:

- `docs/draft.md` for the first plan draft.
- `docs/plan.md` for the executable plan.
- `benchmark.csv` or another tabular log for measurable results.
- `candidates.jsonl` for candidate names, parent links, and status.
- `profile/` for profiler output or report summaries.
- `runs/` or `outputs/` for generated artifacts.

The exact format is less important than consistency. A future reader should be able to reconstruct what changed, what was measured, and why a candidate was promoted.

Bind each PPU result to the source/diff, dependency, binary, input, selected
kernel and toolchain. Label host checks, native compilation, simulator
correctness/performance and physical-device results separately. Keep the
original ACU/Asys reports so analysis can be corrected without repeating capture.

Use [PPU profiling](../skills/ppu-profiling/SKILL.md): Asys for a timeline
question and ACU for a kernel-counter question.
Profiling is selected to answer the current uncertainty; it is not mandatory
after every edit. Clean evaluation and instrumented profiling are separate
measurement contexts.

## Promotion Rule

Promote a candidate only when it satisfies the task contract and has evidence that it improves or preserves the target metric. If a candidate is rejected, record the reason instead of silently discarding it.

A numeric failure invalidates that candidate's timing. Historical winners and
NVIDIA controls suggest experiments; matched PPU results decide PPU promotion.
Extend a winner only to the validated shape/type/operator scope. Missing tools
or unmeasured paths remain explicit gaps. Record the incumbent, failed ideas
and next discriminating experiment when handing off incomplete work.

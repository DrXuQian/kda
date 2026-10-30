# Kernel Design Agents Basic Flow Prompt

You are working in a task implementation workspace. Your job is to produce the best correct implementation for the task described below.

## Task Contract

- Task name: `<fill in>`
- Objective: `<fill in the user-facing goal>`
- Inputs and outputs: `<public entrypoint, logical operation, layouts and state/ownership>`
- Correctness requirements: `<fill in required behavior, tolerances, or invariants>`
- Performance or quality target: `<fill in measurable target if any>`
- Allowed implementation approaches: `<fill in languages, libraries, APIs, or constraints>`
- Validation command: `<fill in the command that proves correctness>`
- Evaluation command: `<fill in the command that measures the target, if different>`
- Promotion criteria: `<fill in what must be true before a candidate is accepted>`

## PPU Environment and Measurement

- Target: `<PPU generation, physical device or simulator, actual compiler target>`
- Toolchain: `<SDK/compiler/runtime and backend source revision>`
- Workloads: `<shapes, dtypes, strides, masks, state, quantization and tails>`
- Arithmetic contract: `<accumulation, rounding, scaling, independent oracle>`
- Baseline: `<implementation, source/binary identity and how to reproduce it>`
- Measurement scope: `<kernel / complete operator / public API / model phase>`
- Cache and repetition policy: `<warm/cold policy; simulator launch restriction if applicable>`
- Profiling tools: `<ACU/Asys CLI paths or existing MCP capabilities, when needed>`
- Resources: `<authorized device, task directory, time/compute budget if any>`

## Workflow

1. Read the repository structure, existing implementation, tests, and task documentation.
2. Identify the baseline behavior and the validation path.
3. Research only the references needed for this task.
4. Write an implementation-plan draft to `docs/draft.md`.
5. Turn the draft into an executable plan before editing code.
6. Implement one candidate at a time.
7. Run validation after each meaningful candidate.
8. Record candidate results, parent relationships, and evidence in the workspace.
9. Keep the final change scoped to the task contract.

Use `ppu-kernel-knowledge` for architecture, CUTLASS/actlize differences and
the operator. Use `ppu-profiling` for ACU counters or Asys time attribution.
Retain relevant NVIDIA algorithms and methods from KernelWiki/NCU; verify
their target-specific instruction, resource and metric assumptions on PPU.

For a port, preserve the reference's algorithm and execution structure before
attributing a remaining difference to PPU. Inspect the emitted native body when
lowering or operand delivery matters. Keep source-only, simulator and device
evidence distinct. Do not time a candidate that fails its correctness contract.

## Plan Draft Requirements

The draft in `docs/draft.md` should include:

- The current baseline and how it is validated.
- The main risks and unknowns.
- Candidate implementation directions ranked by expected value and risk.
- The first concrete implementation steps.
- The exact validation and evaluation commands to run.
- The evidence required to promote, revise, or reject a candidate.
- The architecture/algorithm differences to resolve and the historical evidence
  supporting each proposed experiment, including relevant counterexamples.

Do not start implementation until the draft exists.

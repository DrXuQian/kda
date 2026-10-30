# Prompt Templates

This directory stores generic prompts for the Kernel Design Agents workflow.

The templates are intentionally task-agnostic. Fill in the task objective, constraints, validation command, and promotion criteria before starting an agent session in a separate implementation workspace.

The basic prompt includes PPU environment and measurement fields. They apply
to linear attention, FlashAttention, SageAttention, GEMM/GEMV, MoE and other
operators without fixing a particular harness, performance target or runtime.
Select the relevant knowledge and profiler skills through
[PPU tooling](../docs/ppu-tooling.md). CLI access is sufficient; an existing
MCP is an optional way to expose the same tools.

## Available Templates

| Path | Purpose |
|---|---|
| `basic-flow.md` | Minimal prompt for research, planning, implementation, validation, and iteration. |

## How To Use

1. Create or enter the task implementation workspace.
2. Copy the relevant template content into the agent session.
3. Replace placeholders with task-specific details.
4. Ask the agent to read the workspace and write `docs/draft.md`.
5. Convert that draft into an executable plan.
6. Run the implementation loop with validation after each meaningful change.

Task-specific prompts should live with the task they describe. Do not add benchmark-specific datasets, acceptance tables, or private evaluator details to this generic repository.

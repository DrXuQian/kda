---
name: ppu-kernel-knowledge
description: Research, write, port and debug PPU kernels. Use for NVIDIA-to-PPU migration, actlize/CUTLASS differences, CuTe numerical debugging, linear attention, FlashAttention, SageAttention, quantized GEMM/GEMV and MoE.
---

# PPU Kernel Knowledge

Use this knowledge in KDA's task-contract, draft and candidate loop. Establish
the target generation and current implementation first. Read the architecture
page and the operator page relevant to the question; do not load the entire
collection for every task.

## Select a reference

| Task or symptom | Read |
|---|---|
| PPU target, MMA/copy semantics, native lowering, Hopper port | [Architecture](references/architecture.md) |
| NVIDIA CUTLASS to actlize, builder dispatch, CuTe copy/fragment contracts | [CUTLASS and actlize](references/cutlass-porting.md) |
| Gated DeltaNet, chunking, recurrent state, WY/residual | [Linear attention](references/linear-attention.md) |
| Exact attention, online softmax, masks, GQA, FA2/FA3 | [FlashAttention](references/flash-attention.md) |
| Quantized attention, QK/PV split, bridge, FP8/FP4 | [SageAttention](references/sage-attention.md) |
| K-pack, GGUF, bitplanes, cold GEMV, scale/zero | [Quantization and GEMV](references/quantization.md) |
| Dense/grouped GEMM, MoE, tile and scheduler choices | [GEMM and MoE](references/gemm-moe.md) |
| Wrong values, fragment ownership, races, sub-byte pitches | [Numerical debugging](references/numerics.md) |

For text search, run `rg -n -i 'topic' references` from this skill's directory.
[Sources](references/sources.md) identifies the reviewed revisions and local
memory notes, including corrections. Technical findings below are historical
evidence at those sources, not a new hardware-validation campaign.

## Apply a lesson

1. Match generation, SDK/backend, shape, dtype, layout and numerical schedule.
2. For a port, map the original algorithm and execution structure before
   replacing primitives. Separate a missing implementation from a hardware limit.
3. Classify the supporting evidence: host/layout, native compile, simulator,
   device correctness, or measured performance. Carry that scope into the draft.
4. Turn the lesson into a concrete hypothesis and a check that can disprove it.
5. Record the candidate and its result in the task workspace. Retain corrections
   and rejected hypotheses when updating knowledge.

Use KernelWiki for applicable algorithms, tiling, pipelining and scheduling
ideas; use NCU guidance for NVIDIA reports and shared diagnosis methods.
Check hardware-specific premises before transferring either. The
[coverage map](../../docs/ppu-adaptation.md#knowledge-coverage-and-gaps) lists
the information available for PPU and what still needs evidence.

Equal math does not guarantee equal operand delivery or rounding. Use actual
backend traits and native code, then validate on the requested PPU. For report
analysis, use [PPU profiling](../ppu-profiling/SKILL.md).

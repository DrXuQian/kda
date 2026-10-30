# Sources and evidence scope

Reviewed on 2026-10-30. These references distill kernel-design knowledge from
the sources below. They do not rerun the historical device experiments.
Source/header support, host proofs, native compilation, simulator results and
device measurements retain their original scope. Read later corrections before
applying an older memory entry.

## Source index

| ID | Source | Retained information |
|---|---|---|
| S01 | Local `marlin_ppu/memory`, selected notes below | Layout and instruction findings, operator contracts and corrected hypotheses. Memory locates evidence; it is not an independent numerical oracle. |
| S02 | Local `marlin_ppu/SKILL.md` (`ppu-ptx`) | PPU0010 MMA/copy, resource and FA lessons. Its old build-flag and AIU-only advice is superseded where noted. |
| S03 | Local `ppu17-hopper-porting` skill: `hopper-mapping.md`, `feature-delta.md`, `debug-and-simulate.md` | PPU1.7 source seams against NVIDIA CUTLASS3.6, anchored at PPU backend `023e82d03e80b4d5982f664925e15499033df314`; native 1.7 evidence remains separate. |
| S04 | [actlizeLA, 40776d7](https://github.com/DrXuQian/actlizeLA/tree/40776d7f5bc2cf51b7f7d730314f585a1a8fa322) | `docs/PPU_RETAINED_PATH.md`, `PPU_GDN_AIU_DELIVERY_AUDIT.md`, `PPU_WY_FLA_REWRITE.md`, `PPU_WY_SPLIT_ACU_20260924.md`: recurrence, native operand delivery and phase profiling. |
| S05 | [FlashAttention, 4b26264](https://github.com/DrXuQian/flash-attention-for-sail/tree/4b26264e37ab0c89c0f4f8ff7441ea923224b953) | `dev/ppu17/README.md`, `hopper/ppu17_build.py`, `hopper/backend_runtime.h`: Hopper structure, build/API seams and source/simulation limits. |
| S06 | [SageAttention, 38d2839](https://github.com/DrXuQian/SageAttention/blob/38d28393c291e376e127547cc63b3d524e4cb4b7/docs/PPU_INT8_PORT.md) | INT8-QK/FP16-PV contract, C-to-A bridge and native reference-binding defect. |
| S07 | [SageAttention low-bit, ab334f8](https://github.com/DrXuQian/SageAttention/tree/ab334f8cef77556b3ff455aee0bbd3038de67816/dev/ppu_lowbit) | `README.md`, `docs/CUTLASS4_NVFP4_AUDIT.md`: 1.5/1.7 evidence boundaries and scale ABI. |
| S08 | [Quactlize, 4fb7ce03](https://github.com/DrXuQian/quactlize/tree/4fb7ce037f36768bf900f1c33d606f7eeaf87f80) | `.codex/skills/ppu-cute-numeric-debug`, `ppu-kernel-iteration`, `ppu-cold-gemv-tuning`; `tools/asys_run.sh`, `tools/asys_kernel_time.py`: numerical diagnosis, native lowering, cache-controlled GEMV and report reading. |
| S09 | [KDA baseline](https://github.com/NVlabs/kda/tree/acdd79343c5e9d0c7cb96289f26fd3f1051ce785), [KernelWiki](https://github.com/mit-han-lab/KernelWiki/tree/76d27b56f804e7e7295d4c570e1e5d7eef4b0a75), [NCU skill](https://github.com/mit-han-lab/ncu-report-skill/tree/d1887948c7d53690cfe6605f59c1329b8a1c6bb5) | KDA flow, topic/evidence organization, hardware coverage and profiling methods. Pinned originals remain in the repo. |
| S10 | Local PPU SDK2.1.1 ACU/Asys CLI, sections and `HgRules` rules | ACU raw CSV plus metric/stall imports were exercised on an existing report. Asys subcommand help was checked; no fresh export or capture was performed. |
| S11 | [actlize, 021c693](https://github.com/DrXuQian/actlize/tree/021c69300864e03926108867d318572871a44d35) and local `ppu-cutlass-mixed-gemm` skill | Mixed-input builder/collective dispatch, PPU CuTe traits, converter/delivery constraints and resource-report counterexamples. |

S08's `ppu-kernel-iteration/references/native-lowering.md` was a modified local
working copy. Its GDN examples were checked against S04's committed reports;
the commit link does not identify those local bytes. Machine paths, SDK code,
raw conversations, reports and binaries are not distributed here.

## Local memory locators

| Topic | Notes used |
|---|---|
| Target, resources, PTX | `ppu-build-target-and-m8n16.md`, `ppu-occupancy-limits.md`, `ppu-cp-async-sm80.md`, `ppu-aiu-source-and-asm.md`, `ppu-int8-mma.md`, `ppu-marlin-cute-port.md` |
| actlize/CUTLASS | `ppu-cutlass-w4a16-actlize.md`, `quactlize-extends-actlize-additively.md`, `ppu-moe-format-collective-arch.md`, `ppu17-cutlass3-bf16-gemm.md`, `ppu17-fp8-k48-1x3-mode.md` |
| Layout and numerical failures | `ppu-swzl-cute-modelable.md`, `ppu-w2a16-aiu-cube-width-bug.md`, `ppu-subbyte-expert-pitch-bug.md`, `once-is-not-ordered.md`, `ppu-a-must-stay-in-smem.md` |
| Quantized storage/readers | `tilek-artifact-vs-tactic.md`, `format-needs-both-dequant-kernels.md`, `ppu-q65-two-plane-closed-form.md`, `ppu-marlin-warps-split-k.md`, `ppu-gemv-alu-bound-not-bandwidth.md` |
| Attention and comparisons | `ppu-linear-attn-chunked.md`, `ppu-standalone-fa-beats-fa2.md`, `ppu-fa-mask-path.md`, `align-before-attributing.md` |

Project-specific budgets, packaging procedures, collaborator policies and old
benchmark target lists are intentionally excluded. Keep new source references
beside the decision they support; update the affected claim when evidence
changes, without turning a local observation into a generation-wide rule.

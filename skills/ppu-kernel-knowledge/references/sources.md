# Sources and evidence scope

The reusable guidance is included in this repository. Read the linked local
references below on any machine; the author's memory directory, installed
skills and original worktrees are not prerequisites. External links provide
optional source inspection at fixed revisions.

Reviewed on 2026-10-30. A local reference preserves the finding, target and
limits of the original evidence; it does not reproduce a device experiment.
Unavailable original records remain historical, source-reported evidence.

## Included guidance and original sources

| ID | Read in this checkout | Origin and availability |
|---|---|---|
| S01 | [Architecture](architecture.md), [CUTLASS/actlize](cutlass-porting.md), [numerics](numerics.md), [quantization](quantization.md), [GEMM/MoE](gemm-moe.md) and the attention references | Operator-history notes. Original private memory files are not distributed; their selected findings and corrections are written into these pages. No memory-file lookup is required. |
| S02 | [PPU0010 primitives and resources](architecture.md#cudaptx-compatibility-preserve-and-check), [FlashAttention](flash-attention.md) | Historical `ppu-ptx` reference. The original local skill is not distributed. Its useful instruction/resource findings are included here; old universal build-flag and AIU-only advice is corrected in the text. |
| S03 | [PPU1.7 differences](architecture.md#ppu17-seams), [Hopper API seams](cutlass-porting.md#hopper-integration-has-api-seams-too), [simulation workflow](flash-attention.md#ppu17-hopper-path) | Historical Hopper-porting review of PPU CUTLASS `023e82d03e80b4d5982f664925e15499033df314` against NVIDIA CUTLASS3.6. The original skill and vendor backend snapshot are not bundled or publicly retrievable through this index. Included source findings are not native PPU1.7 certification. |
| S04 | [Linear attention](linear-attention.md), [profiling diagnosis](../../ppu-profiling/references/analysis.md) | Fixed actlizeLA source: [retained PPU1.0 path](https://github.com/DrXuQian/actlizeLA/blob/40776d7f5bc2cf51b7f7d730314f585a1a8fa322/docs/PPU_RETAINED_PATH.md), [operand delivery audit](https://github.com/DrXuQian/actlizeLA/blob/40776d7f5bc2cf51b7f7d730314f585a1a8fa322/docs/PPU_GDN_AIU_DELIVERY_AUDIT.md), [split-prepare evidence](https://github.com/DrXuQian/actlizeLA/blob/40776d7f5bc2cf51b7f7d730314f585a1a8fa322/docs/PPU_WY_SPLIT_ACU_20260924.md). |
| S05 | [FlashAttention](flash-attention.md), [CUTLASS/actlize](cutlass-porting.md) | Fixed [FlashAttention PPU1.7 guide](https://github.com/DrXuQian/flash-attention-for-sail/blob/4b26264e37ab0c89c0f4f8ff7441ea923224b953/dev/ppu17/README.md): Hopper structure, build/API seams and source/simulation limits. |
| S06 | [SageAttention](sage-attention.md), [numerical debugging](numerics.md) | Fixed [SageAttention INT8 port](https://github.com/DrXuQian/SageAttention/blob/38d28393c291e376e127547cc63b3d524e4cb4b7/docs/PPU_INT8_PORT.md): INT8-QK/FP16-PV, C-to-A bridge and native reference-binding defect. |
| S07 | [Low-bit attention](sage-attention.md#low-bit-experimental-targets), [PPU1.7 differences](architecture.md#ppu17-seams) | Fixed [CUTLASS4 NVFP4 audit](https://github.com/DrXuQian/SageAttention/blob/ab334f8cef77556b3ff455aee0bbd3038de67816/dev/ppu_lowbit/docs/CUTLASS4_NVFP4_AUDIT.md): target and scale ABI evidence. The vendor archive itself is not distributed here. |
| S08 | [Numerics](numerics.md), [quantization/GEMV](quantization.md), [PPU profiling](../../ppu-profiling/SKILL.md) | Fixed Quactlize sources: [CuTe numeric debugging](https://github.com/DrXuQian/QUactlize/blob/4fb7ce037f36768bf900f1c33d606f7eeaf87f80/.codex/skills/ppu-cute-numeric-debug/SKILL.md), [cold GEMV experiments](https://github.com/DrXuQian/QUactlize/blob/4fb7ce037f36768bf900f1c33d606f7eeaf87f80/.codex/skills/ppu-cold-gemv-tuning/SKILL.md), [Asys reader](https://github.com/DrXuQian/QUactlize/blob/4fb7ce037f36768bf900f1c33d606f7eeaf87f80/tools/asys_kernel_time.py). These are external provenance, not instructions to install that project's skills or adopt its policies. |
| S09 | [KDA flow](../../../docs/agent-flow.md), [PPU adaptation](../../../docs/ppu-adaptation.md) | [KDA baseline](https://github.com/NVlabs/kda/tree/acdd79343c5e9d0c7cb96289f26fd3f1051ce785), [KernelWiki](https://github.com/mit-han-lab/KernelWiki/tree/76d27b56f804e7e7295d4c570e1e5d7eef4b0a75), [NCU skill](https://github.com/mit-han-lab/ncu-report-skill/tree/d1887948c7d53690cfe6605f59c1329b8a1c6bb5). The two NVIDIA collections are optional pinned submodules; initialize them when using their additional references. |
| S10 | [ACU collection](../../ppu-profiling/references/collection.md), [metric/rule interface](../../ppu-profiling/references/metrics.md), [Asys timeline](../../ppu-profiling/references/timeline.md) | PPU SDK2.1.1 tool inspection and an existing-report import. Commands, observed metrics and version limits are included. SDK binaries and original reports are not distributed. ACU raw/metric/stall imports were exercised; Asys help was checked, without a fresh export or capture. |
| S11 | [CUTLASS/actlize](cutlass-porting.md), [physical ownership](numerics.md#trace-physical-ownership), [resources](architecture.md#resources-and-evidence) | Fixed actlize [mixed-input builder](https://github.com/DrXuQian/actlize/blob/021c69300864e03926108867d318572871a44d35/include/cutlass/gemm/collective/builders/ppu_mma_builder.inl) and [PPU0010 MMA traits](https://github.com/DrXuQian/actlize/blob/021c69300864e03926108867d318572871a44d35/include/cute/atom/mma_traits_ppu0010.hpp). Additional mixed-GEMM debugging/resource observations came from a local skill not distributed here; their scoped conclusions are included in these references. |

The linked operator documents and source files were fetched at their fixed
revisions during the portability review. S01/S02/S03 and the local part of S11
have no retrievable original through this index. Reading their included
summaries does not imply access to the original probes, logs or vendor code.
The GDN native-lowering conclusions use S04's committed audit and reports;
a modified local working copy is not presented as a retrievable source.

## Use on another machine

Clone or copy this KDA checkout with both PPU skill directories and their
references. The guidance can be read offline. Optional Claude skill symlinks
point to this new checkout, not to the author's home directory.

For execution, select the target task's actual source checkout and install its
required PPU SDK/runtime on that machine. Resolve commands through its
`PPU_SDK` or explicit tool paths. Backend-relative filenames in the guides
identify code to inspect in that selected dependency; they do not imply that
KDA bundles the backend, toolchain, kernel implementations or reports.

When an external source is unavailable, use the included explanation within
its stated evidence scope. A new target, unsupported mapping or performance
claim still needs the task's own source/native/device checks. Record missing
original evidence instead of requiring an absent private memory file.

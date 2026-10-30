# CUTLASS, actlize and PPU backend differences

Sources: [S01, S03, S05, S08, S11](sources.md). actlize retains CUTLASS/CuTe's
layered design but changes architecture atoms, builders and operand delivery.
Keep the reusable structure and inspect the actual instantiated backend.

## Choose the tree before choosing an atom

| Source family | Relevant entry points | What transfers |
|---|---|---|
| NVIDIA CUTLASS | CuTe atoms/layouts, collective builder, `GemmUniversal`, epilogue and scheduler | Layout algebra, composition and algorithm structure; architecture-specific traits need comparison. |
| Public actlize, PPU0010/0015 | `include/ppu_include.hpp`, `cute/{arch,atom}/*ppu0010*`, `cutlass/gemm/collective/builders/ppu_mma_builder.inl` | Similar APIs select PPU register MMA and AIU collectives. Start from the matching example and follow its concrete types. |
| PPU CUTLASS 3.6/4.x with 10700 support | `include/ppu/ppu_include_10700.hpp`, `ppu/cute/{arch,atom}`, SM90 builders/pipelines | BF16/FP16 retain Hopper TMA/WGMMA structure; private low-bit atoms and descriptor/runtime seams need separate checks. |

These trees are not interchangeable because their directory or version labels
look similar. Earlier PPU backend trees use `Acompute10000_*`; public actlize uses
`PPU0010_*` names. Resolve types in the selected checkout instead of installing
another tree to satisfy a guessed spelling. Record the include path, dependency
revision, real compiler target and generated specialization.

## Same schedule name can select different hardware

In actlize S11, `KernelTmaWarpSpecialized*MixedInput` and selected
`KernelAiuMultistageMixedInput*` tags enter the same PPU builder and
`ppu_mma_aiu_multistage_mixed_input.hpp` collective. A `Tma` tag does not prove
Hopper TMA execution. `examples/16_ppu_mixed_dtype_gemm` exercises this route.

Follow the chain from builder to dispatch policy, collective, tiled MMA,
copy atoms and kernel wrapper. For the reviewed mixed-input route:

- The transformed tuple chooses `SwapAB`. Putting quantized weights in B does
  not request an M/N swap. Inspect the arguments actually passed, not unused
  reversed C/D strides inherited from a copied example.
- Runtime B stride remains ordinary packed `(N,K,L)` column-major. The
  interleave contract is carried by the builder's `kContinous` and preprocessing;
  `RowsPerTile=256` must match the interleaved-256 reader.
- Scale layout is MN-major with `Stride<1,int64_t,int64_t>`. Scale application
  cadence must resolve every group touched by a copy step. A historical
  64-K copy step skipped gs=32 scaling; per-MMA-atom reload fixed that route.
- Grouped reuse must implement expert byte pitches and ragged A row offsets.
  Single-GEMM success does not validate the L dimension or a different grouped
  wrapper. Use distinct expert data and an independent dequantized reference.

These are source contracts, not a rule that every format needs that reorder
or every backend supports gs=32. Verify the selected converter and collective.

## CuTe cannot check a layout hidden by the atom

The legacy AIU `.swzl` write and matched `ld.swzl` read cancel at byte level;
the FP16 path needs no offline compensation for that pair. Sub-byte offline
reordering instead matches converter emission order to MMA fragment slots.

Some legacy `Copy_Traits` flatten that contract. They do not express each
endpoint's physical map, so a mismatched producer/read pair can still compile.
Model both endpoints when changing the pair, and model the converter separately.
Use the known FP16 identity composition as a control. Do not add a second
software unswizzle to a working matched path.

The reviewed host SWZL model was XOR-linear within a slice but needed a rotate
across slices. In the recorded PPU0010 int2 case, hardware grouped registers
0/1 in the low N half and 2/3 in the high half; the fallback's register-parity
pairing was wrong. Calibrate the actual lane/register map before composing it
with a converter. See [numerical debugging](numerics.md).

## Extend a collective without changing unrelated dispatch

Quactlize's additive extension exposed a reusable template hazard: overlapping
`CollectiveBuilder` predicates can be ambiguous, while a wrapper tag that
collapses to a vendor tag can silently select the vendor collective. Give a
new dispatch policy its own identity and make specialization predicates
disjoint. Check the selected type for both the new and existing routes.

Use the preprocessor include graph to diagnose umbrella-header cycles; copying
an umbrella does not reproduce its partial-construction state. Keep architecture
guards on shared converter primitives when moving implementations. Those guards
are portability fixes even when the converter also supports a custom format.
The original project's naming rules, CI inventory and packaging policy are not
requirements for another KDA task.

## Hopper integration has API seams too

The reviewed PPU CUTLASS3.6 integration uses `KernelHardwareInfo::sm_count`, a
two-argument accumulator store selector and a three-argument
`PipelineTmaAsync` constructor. Other PPU forks use different APIs. Preserve
the matched empty-barrier arrival count and release predicate when adapting
constructors; copying only one side can deadlock a correct algorithm.

For each changed interface, check a representative generated body and its
caller, then output ownership and numerical behavior. An nvcc template check,
PPU native compile and PPU execution answer different questions.

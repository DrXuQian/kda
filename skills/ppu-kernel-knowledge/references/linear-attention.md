# Linear attention and Gated DeltaNet

Sources: [S01, S04, S08](sources.md). Primary retained PPU1.0 source:
actlizeLA `40776d7`. The early scalar chunk prototype is historical, not the
current implementation.

## Freeze the recurrence and state contract

For the scalar-gated DeltaNet studied here, with state H indexed [key,value]:

```text
H_t = g_t (I - beta_t k_t k_t^T) H_(t-1) + beta_t k_t v_t^T
o_t = scale * q_t^T H_t
g_t = exp(graw_t)
```

The contract includes gate units, beta/QK normalization, grouped-value head
mapping, initial state, final state, tails and state precision. Validate both
output and final state against a recurrent oracle. Distinct heads and nonzero
carried state expose bugs that a zero-state single-head fixture hides.

The early chunk derivation transforms the state with the inclusive gate
cumsum; the chunk output uses the chunk-start state and the state update comes
afterwards. This is an algebraic reference, not permission to replace the
retained kernel's rounding or stable gate handling. One-token and multi-chunk
cases distinguish update order and missing gate factors.

## Compare complete numerical schedules

actlizeLA keeps original, materialized-WY and residual schedules distinct.
The retained residual path has BF16 operands/output and FP32 carried state;
its C64 full-chunk specialization and guarded tail preserve the admitted
arithmetic. An original reset approximation or a different state dtype cannot
silently become the oracle for that path.

Delivery-only changes use equality to the admitted schedule plus an independent
numerical check. Approximate recurrence changes need their own accuracy
contract and representative activations.

## Preserve the execution graph before tuning

Inspect prefix, KKT/solve, W/U preparation when present, state recurrence and
output as separate mathematical phases. Include fills and auxiliary kernels
in the declared comparison. FLA's selected generated kernel, not merely
`tl.dot`, is the structural reference for layouts, reuse and synchronization.

An early scalar chunk kernel had too few CTAs, serial chunks and no tensor
cores. That result does not reject chunking. Later native AIU/SWZL delivery
and split preparation established different implementations. The early
"in-kernel intermediates make tensor-core GDN impossible" conclusion is obsolete.
Global operands can use AIU; register-produced state/residual operands need
their own shared/fragment producer contract.

The split-prepare experiment is a useful controlled counterexample to
"fewer launches or bytes must win": it reduced W/U publication amplification
at the KVD interface, while adding intermediate traffic at L2/DRAM. Independent
phase resource budgets improved the complete profiled sum. Do not relabel
KVD savings as equal HBM savings or attribute the whole gain to one changed seam.

## Choose the next candidate

Use matched phase totals to rank remaining latency. When state and reference
have similar grid, active warps and MMA counts, inspect delivery, address
instructions, reuse and waits before changing the grid. When a publication
uses scalar stores, check transaction amplification and vector ownership.
Recheck the remaining bottleneck after each change.

Compare native GVA or clearly declared pre-expansion on equal logical inputs.
Keep all-kernel ACU sums, event/API spans and Asys timeline measurements
separate. Source/host validation, prior device receipts and a new branch merge
do not constitute a fresh speed measurement.

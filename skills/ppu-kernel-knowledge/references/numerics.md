<!-- SPDX-License-Identifier: Apache-2.0 -->

# Numerical debugging at the physical seam

Sources: [S01, S06, S08, S11](sources.md). Adapted from Quactlize's numeric-debug
guidance, with attention/ABI counterexamples. The original Quactlize material
retains Apache-2.0; see [notices](../../../THIRD_PARTY_NOTICES.md).

## Isolate the failing specialization

Bind source/diff, generated symbol, artifact/tactic, shape, seed, compiler and
binary. Save input/output/reference fingerprints, nonfinite count and first
wrong coordinate. Stop using timing from that specialization. A failed runtime
context should not contaminate subsequent independent cells.

Use inputs that distinguish the suspected axis: expert-specific data, N/K
tags, different heads, nonzero state or shifted absolute stage coordinates.
An N-only tag cannot establish K-stage freshness. Exactly representable,
order-independent subtests isolate layout from arithmetic when applicable;
the full task still needs its declared independent numerical reference.

## Trace physical ownership

Follow stored bytes through producer, descriptor, shared memory, copy view,
converter, MMA fragment, scale/zero stage and output/reduction. Use the real
CuTe types, not a second handwritten mapping with the same assumptions.
Enumerate shape, stride, size, cosize and subview base offsets.

CuTe details that have changed the diagnosis:

- `thr.partition_B(tensor)` can encode the thread's base in the iterator;
  `partition.layout()(0)` alone omits it. Include the iterator offset or derive
  a thread/value map from the actual tiled MMA and its thread-layout inverse.
- A fragment need not be compact. Index it through its layout; do not assume
  that a linear register quotient names the K atom rather than the N atom.
- `make_fragment_like` creates storage and does not preserve every broadcast
  or alias relationship. A copied scale fragment can retain stale values while
  the original view receives updates.
- Raw `int4b_t*` arithmetic advances byte-sized wrapper objects, whereas a
  sub-byte iterator counts logical codes. At a raw-byte descriptor boundary,
  an int4 expert occupies `N*K/2` bytes. Keep the unit explicit on both sides.

Equal converter cohort sizes do not imply equal physical destination strides.
Do not reuse a B retile's coordinate in an A view merely because both call a
mode K. Relate both through semantic MMA coordinates. Require full coverage
with no unwanted duplicate owner, including high-plane and tail slots.

The memory's int2 vreg-pairing correction and Sage's C-to-A bridge demonstrate
why a convenient host simulator cannot be the only logical authority. Make a
wrong-coordinate control fail, and reproduce the observed failure signature
before declaring a root cause.

## Trace time as well as addresses

List producer issue, completion, publication, consumer read and stage reuse.
An initialization performed once is not necessarily ordered before another
warp's first use. Quactlize's one-time metadata clear could overwrite a decoded
stage because its ownership map differed and the cross-warp edge was missing.
For asynchronous copies/MMA, include the corresponding completion/retirement
protocol, not only a CTA barrier.

Changing cadence, unrolling or adding waits can be a useful bisection. Passing
after such a change establishes sensitivity, not unique causality. Construct
the exact missing-owner, overlap, wrong-stride or ordering negative before
retaining a production fix.

## Close at the relevant evidence tier

Host algebra proves a modeled mapping; native compilation proves selected
lowering; device checks establish execution behavior. The Sage reference-array
bug passed layout reasoning but initialized only one accumulator register in
native code. Inspect the actual generated body when compiler binding matters.

Count NaN/Inf explicitly. A comparison such as `error > tolerance` can let NaNs
pass. Check that the target launched and wrote the expected output: two refused
launches with untouched buffers are not equality evidence. Keep the denominator
explicit so missing rows or missing owners cannot shrink a failed test into PASS.

Preserve admitted arithmetic and resource-sensitive structure for a narrow
fix. Exact equality may apply to a delivery refactor; it is not a universal
expectation for a changed BF16 reduction or quantized-attention algorithm.

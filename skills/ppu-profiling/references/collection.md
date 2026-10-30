<!-- SPDX-License-Identifier: Apache-2.0 -->

# ACU collection and import

Source anchors: [S04, S06, S08, S10](../../ppu-kernel-knowledge/references/sources.md).
Resolve paths from the task and selected SDK; no host name or GPU ordinal is
a framework default.

## Existing reports first

Preserve the `.acurep` and calculate its digest. With the SDK selected:

```bash
"$PPU_SDK/asight/bin/acu" --version
"$PPU_SDK/asight/bin/acu" --import "$REPORT" --page raw --csv > "$RAW_CSV"
"$PPU_SDK/asight/bin/acu" --import "$REPORT" --page details > "$DETAILS"
```

Set `REPORT`, `RAW_CSV` and `DETAILS` to explicit paths, with new outputs in
the task's analysis directory. Check each command's status. Use Python's CSV
parser rather than splitting on commas: kernel template names and launch
tuples contain commas. Inspect whether that version emits wide per-kernel
rows or another schema before selecting columns.

Enumerate available names and read definitions/units from the installed
sections/tool. Historical ACU reports contain PPU AIU, vector-memory, tensor,
shared, cache and DRAM metrics; not every target/report contains all of them.
Use exact recorded kernel symbols, launch geometry and IDs. A filtered or
partial capture cannot stand in for a complete operator denominator.

The inspected CLI exposes only `raw` and `details` pages. `details` may contain
no section data even when raw metrics are available; inspect the actual output.
Its import mode rejects `--set`. Re-import does not collect missing counters.
For structured metric/native-instruction analysis, use the SDK statistics rules
described in the [metric guide](metrics.md), with explicit output paths.

Report import can run without a PPU when the host tool's runtime requirements
are met. An incompatible host glibc/libstdc++ is an importer-environment issue,
not a bad kernel. An existing compatible container/private loader can read the
report without changing the system or claiming a device run.

## Capture a bounded question

Inspect `acu --help` and the task's runner before capture. The historical PPU
runner shape is:

```bash
"$PPU_SDK/asight/bin/acu" -f -o "$REPORT_BASE" --set full "$HARNESS" ...
```

Replace the arguments with the task's real workload. Use a new report base;
do not overwrite the incumbent's report. Source/line information is useful
when the selected compiler/tool supports native-source correlation.

One harness invocation can contain several kernels, and ACU may replay them
for counters. Record both application launches and profiler replay behavior.
CPU fixture generation helps control auxiliary launches; do not remove a
required reducer, quantizer or fill from a full-operation comparison.

Keep physical-device timing runs sequential and separate from profiling.
For a simulator restricted to one target invocation, use its provided
single-call application and trace protocol instead of this replay recipe.

## Import checks

Confirm report readability, matching target/symbol/shape, expected kernel
coverage, finite numeric fields and declared units. Compare reported totals
with component sums only when their definitions make them additive. Retain
absent sections as gaps. A parser fix needs a report re-import, not necessarily
a GPU rerun. A source or input change does need new relevant execution evidence.

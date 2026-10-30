# PPU tools in the KDA loop

ACU and Asys are PPU-owned profiling tools. Select the tool by the evidence
needed for the current candidate, using the installed toolchain's capabilities.

| Question | Tool or evidence |
|---|---|
| Which operator or stage consumes the call? Are launches, copies or waits dominant? | Asys device/host timeline and the selected range. |
| Why is a specific kernel slow? Which instructions, traffic or stalls changed? | ACU kernel report, matching native ISA and source. |
| Did the compiler select the intended PPU body and operand path? | PPU compiler, native disassembler and resource output. |
| Is the output correct? | Task's independent numerical oracle and failure cases. |
| Did the candidate improve the target? | Task's declared evaluation scope and matched baseline. |

## CLI access

Resolve `acu` and `asys` from the selected PPU SDK, or use explicit tool paths.
Check version/help before reusing flags from a historical run. Existing SDK
report-reading examples are:

```bash
"$PPU_SDK/asight/bin/acu" --import "$ACU_REPORT" --page raw --csv
"$PPU_SDK/asight/bin/asys" export -o "$ASYS_SQLITE" "$ASYS_REPORT"
```

Use new output paths under the task's `profile/` directory. ACU's CSV schema
and Asys's SQLite tables depend on version. Enumerate the actual columns,
metrics and units. A report parser should preserve the original report,
selected kernel/range and tool version.

The inspected SDK2.1.1 CLI supports these operations. Its ACU `HgRules`
statistics interface also exports selected metrics and analyzes native
instruction/stall data; see the [verified examples](../skills/ppu-profiling/references/metrics.md).
ACU identifies itself
as `v2.1.1_20260725-15d8b9d`, data version `15000`. Asys also exposes `profile`,
`stats`, `analyze` and `compare`; their availability is not proof that every
capture mode works on another SDK/device. Use the task's existing capture
runner where it already fixes inputs, identity and numerical admission.

A host report importer can need newer glibc/libstdc++ than the host provides.
Use an existing compatible runtime or container for that tool. A private
loader can support report-only import without replacing system libraries.
Tool startup or report import does not establish device profiling capability.

## MCP access

MCP is optional. The same skills can use a discovered ACU/Asys MCP or the
CLI/Python path. No profiler MCP is required by the upstream KDA loop or its
bundled NCU skill.

If a PPU MCP already exists, inspect its actual tool schemas. Useful
capabilities are report discovery, kernel/range enumeration, metric
enumeration with units, filtered counter queries, timeline correlation and
baseline/candidate comparison. Capture and job-status operations are useful
when the agent runs away from the PPU environment. These are capability
requirements, not claims that particular MCP method names already exist.

Returned data should identify the report digest, profiler version, target,
kernel/launch or timeline range, units, measurement scope and missing fields.
Keep report queries separate from capture, which executes or attaches to a
workload. A transport change must preserve replay/cache policy and the
distinction between instrumented and clean timing.

When shell access to the existing toolchain is available, start there. Add an
MCP adapter only if it resolves a real access, structured-query or remote-job
need. It does not supply PPU knowledge or turn a report into a correctness proof.

## Measurement boundaries

ACU forced-cold replay, rotating-weight event timing, Asys activity duration,
full API latency and performance-simulator cycles answer different questions.
Bind each table to one context. Summed durations of concurrent kernels do not
equal elapsed time. A PPU1.7 single-invocation simulation contract also excludes
profiler replay and GPU reference/initialization kernels; prepare on CPU and
check the actual trace. Do not apply that restriction to every hardware run.

Detailed workflows and source anchors are in
[PPU profiling](../skills/ppu-profiling/SKILL.md).

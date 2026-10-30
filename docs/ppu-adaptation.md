# PPU adaptation of Kernel Design Agents

KDA separates the agent workflow from the implementation workspace. Its
reusable pieces are a task contract, a planning prompt, domain knowledge and
profiling guidance. The task supplies the kernel, evaluator and promotion
criteria. The PPU fork uses that same division of responsibilities.

## Document map

The baseline is the synchronized upstream `main` at
[`acdd793`](https://github.com/NVlabs/kda/tree/acdd79343c5e9d0c7cb96289f26fd3f1051ce785)
including its optional Hugging Face exporter. PPU changes are maintained on
the rebuild branch above that baseline.

| Upstream entry | PPU treatment | Reason |
|---|---|---|
| `README.md` | Adapt introduction, skill setup and task entry; retain minimal flow and workspace layout | The workflow remains KDA; the default hardware and knowledge sources change. |
| `docs/agent-flow.md` | Preserve nine-step loop; add PPU target, arithmetic and measurement fields | These fields determine whether a candidate is valid on the requested PPU. |
| `prompts/README.md` | Preserve template usage; explain PPU skill selection | The caller still fills a task contract in a separate workspace. |
| `prompts/basic-flow.md` | Preserve contract / workflow / draft sections; add PPU fields | No fixed GEMV workload, overnight duration or benchmark is a framework default. |
| `CLAUDE.md` | Preserve repository/workspace boundary; select PPU references | Agent behavior should follow the same loop. `AGENTS.md` exposes it to other agents. |
| `skills/KernelWiki` | Keep pinned upstream submodule; add `ppu-kernel-knowledge` | Algorithms, CuTe, tiling and pipelines remain useful; compare architecture-specific premises before porting. |
| `skills/ncu-report-skill` | Keep pinned upstream submodule; add `ppu-profiling` | Keep diagnosis methods and NVIDIA report support. Use ACU definitions for PPU counters and Asys for timelines. |
| Humanize planning | Keep optional | Converting a draft into an executable plan is independent of the accelerator. |
| `docs/huggingface-export.md` | Retain upstream instructions; add separate `docs/ppu-artifacts.md` | The upstream helper accepts Python/JSON CuTe-DSL sources; PPU native libraries need their existing SDK builder and ABI contract. |
| `scripts/export_huggingface.py` and its tests | Retain unchanged from synchronized main | They continue to serve the upstream CUDA/CuTe-DSL workflow; their presence does not establish native PPU packaging support. |
| Physical ZW810 entry | Add `docs/zw810.md`, `prompts/zw810.md` and a small environment query | Run the existing KDA loop with task-owned build/oracle/benchmark commands. Query actual resources without requiring a complete hardware survey. |
| `CONTRIBUTING.md` | Add PPU evidence and request guidance; retain DCO and licensing text | Contribution mechanics remain valid; target-specific evidence must be explicit. |
| `.github/PULL_REQUEST_TEMPLATE/wishlist.md` | Adapt target/environment fields | PPU requests need generation and SDK identity, not B200/B300 checkboxes. |
| `.github/ISSUE_TEMPLATE/config.yml` | Distinguish PPU contract from upstream wishlist | Do not send PPU requests to a NVIDIA-only acceptance path. |
| `.gitignore` | Add ACU/Asys report and SQLite sidecar types | Generated evidence stays in the task workspace. |
| `.gitmodules` | Preserve both source URLs and gitlinks | PPU skills do not rewrite third-party distributions. |
| `LICENSE`, DCO text, existing `third_party_licenses/*` | Preserve verbatim | Hardware adaptation does not change third-party rights. |
| `THIRD_PARTY_NOTICES.md`, license index | Retain upstream inventory; attribute derived PPU guidance | Source references and distributed text need accurate provenance. |

## Skill correspondence

The bundled NCU reference documents were evaluated by responsibility as well:

| NCU skill document | PPU counterpart or decision |
|---|---|
| `00-directory-layout.md`, `01-workflow.md` | Keep one per-run reports/analysis and evidence-to-plan flow in `ppu-profiling`. |
| `02-harness-guide.md` | Reuse the task's real entry/inputs and native build; preserve multi-kernel scope when that is the metric. Do not force a copied standalone kernel or NVIDIA architecture flag. |
| `03-collection.md` | Use verified ACU CLI options and PPU replay/cache policy; Asys has its own capture/export commands. |
| `04-python-api.md` | Use ACU CSV, `HgRules`, or the official Asight2.2.0 `acu_report` interface when installed; no assumed `ncu_report` compatibility. |
| `05-analysis-dimensions.md` | Keep the questions about residency, work, memory and stalls; derive metrics, resources and thresholds from PPU. Asys provides call timelines, not automatically per-CU PM samples. |
| `06-diagnosis-playbook.md` | Use scoped PPU counterexamples and controlled hypotheses. Do not copy fixed B200 percentages, bank rules or automatic fixes. |
| `07-report-template.md` | Retain identity, measurements, diagnosis and ranked next experiments, with PPU evidence tiers and full-call scope. |
| `08-b200-metric-names.md` | Replace as the PPU reference with a small verified [ACU metric guide](../skills/ppu-profiling/references/metrics.md). Enumerate each actual report. |
| `09-common-issues.md` | Cover importer runtime, missing sections, native symbols, replay and Asys calibration. NVIDIA driver configuration and clock commands do not transfer. |
| `blackwell-cuda-programming.md` | Keep in the NVIDIA submodule. PPU architecture/operator pages supply the applicable primitive and layout guidance. |
| NCU helper scripts | Keep with their original dependency. Reuse PPU SDK rules and existing task parsers; no unverified API-name substitution. |

KernelWiki's source links, conditional lookup and evidence scope are retained
as a pattern. The PPU collection uses a topic router, `rg` and a source index;
it does not relabel the NVIDIA PR/archive corpus or require that
larger collection's query tooling for a small local knowledge base.

| KDA responsibility | PPU entry |
|---|---|
| Research architecture and implementation history | [PPU kernel knowledge](../skills/ppu-kernel-knowledge/SKILL.md) |
| Diagnose a kernel or locate time in a call | [PPU profiling](../skills/ppu-profiling/SKILL.md), choosing ACU or Asys by the question |
| Draft and execute the plan | [Basic flow prompt](../prompts/basic-flow.md), optionally Humanize |
| Validate and measure candidates | Existing task-owned commands, recorded in the contract |

The knowledge pages distill operator history rather than export raw memory.
Required guidance is tracked in this checkout and can be read on another
machine without the author's memory or global skills. The
[source index](../skills/ppu-kernel-knowledge/references/sources.md) maps the
included documentation and official public upstreams. Personal operator forks
are not documentation or dependency requirements. Historical extensions are
distinguished from the inspected official implementation.
Each page identifies its source and limits. In particular, corrected layout
claims, retired Sage INT8-PV experiments and old GDN delivery blockers are not
current hardware rules. PPU1.0, 1.5 and 1.7 remain distinct targets.

## Knowledge coverage and gaps

The selection starts with what an agent needs to write a kernel or port an
NVIDIA implementation. KernelWiki's primer/hardware index covers tensor
instructions, TMEM, TMA, barriers, clusters, CLC, dependent launches and low-bit
formats, alongside algorithms and optimization techniques. The NCU companion
adds a B200/H100 resource table, memory/compute peaks and diagnosis dimensions.
These define the questions to answer for PPU, not values to copy into a PPU card.

PPU1.0 is a primary target. Its native MMA, AIU/SWZL, actlize, CuTe debugging
and operator evidence are now joined by official HGGC/TIX and Asight manuals.
The [official document map](../skills/ppu-kernel-knowledge/references/official-docs.md)
records reviewed versions, public implementation starting points and specific
documentation conflicts. Keep architectural rules separate from SKU quantities
and historical measurements. The review covers PPU1.0 and 1.5; 1.7 remains a
separately scoped historical source/model path.

| Information needed | Evidence in the included material | KDA use / remaining gap |
|---|---|---|
| Device resources and performance model | Official warp/CTA limits, 810E/M890 product examples and historical ACU resource counterexamples | [Architecture](../skills/ppu-kernel-knowledge/references/architecture.md) distinguishes the 64K/128K register discrepancy, allocation questions and SKU values. Complete per-SKU performance models remain unavailable. |
| Cache topology and interface bandwidth | HGGC: per-CU L1, CE-shared L2, shared LLC; Asight: KVD/KSD roles; shared banks/groups; scoped uploaded diagram | [Memory hierarchy](../skills/ppu-kernel-knowledge/references/memory-hierarchy.md) supplies topology and scope. Diagram identity, cache capacities/aggregation, clocks and sustained rates still need target evidence. |
| Compiler target and native instruction path | Old wrapper-target failure; native 1.0/1.5 builds; 1.7 source/model work | Keep build contracts separate. The reviewed SDK cannot establish native 1.7 compilation. |
| MMA shape, dtype and fragment ownership | Official tc01/tc02 shapes and fragment diagrams, software-expanded tc01.ex forms, FP16-output native compile probe, historical maps | [TIX](../skills/ppu-kernel-knowledge/references/tix-porting.md) guides selection. Keep virtual ISA, native lowering and device correctness separate. |
| Global/shared movement and layouts | Official cache modifiers, cp.async, generation-specific AIU padding/byte offsets, historical converter/TMA seams | Preserve producer-to-consumer composition and tail writes. General 1.7 native timing/capacity data is missing. |
| Synchronization and scheduling | Documented async groups and awbar lifecycle plus historical pipeline/race lessons | Participants and completion are documented; awbar alignment has an explicit 8/64-byte discrepancy. Cluster/DSM/multicast limits need target evidence. |
| CuTe/CUTLASS interfaces | actlize builder/collective dispatch, umbrella includes, scale cadence and extension predicates | [CUTLASS/actlize](../skills/ppu-kernel-knowledge/references/cutlass-porting.md) records the changes; version labels alone are insufficient. |
| Numerical behavior and debugging | TIX scalar rounding/FTZ/FMA and reciprocal/exponential bounds; CuTe ownership, stage freshness, bridge and ABI failures | [Numerical debugging](../skills/ppu-kernel-knowledge/references/numerics.md) combines those sources. MMA internal reduction and model approximations still need task-specific evidence. |
| Operator algorithms | GDN/WY/residual, exact/quantized attention, GEMM/GEMV/MoE; official T-Head FlashAttention and PLA | Start from an appropriate official PPU implementation; retain NVIDIA algorithm/layout/oracle methods. |
| Counters and call timelines | ACU raw/rule imports, LLC metrics, public acu_report and official Asys MCP | [PPU profiling](../skills/ppu-profiling/SKILL.md) records tested versus documented interfaces and the cache-control conflict. No fresh device capture was performed here. |
| Other language/runtime backends | Official triton-for-sail for ppu001/ppu0015 and cmake-hgcc; CUDA/C++ and CuTe templates | PPU Triton is documented. Select compatible releases and validate the task natively; PPU CuTe DSL and the upstream Hugging Face builder path remain unestablished. |

For ZW810, the remaining requests are concrete: resolve register capacity and
billing, awbar alignment, ACU `none` cache behavior, per-SKU cache/performance
quantities, and MMA/model numerical details. The
[question table](../skills/ppu-kernel-knowledge/references/official-docs.md#remaining-questions-for-the-perf-model)
names the conflicting sections and required evidence. Basic topology, KVD's
role, scalar arithmetic and public Triton support no longer belong on a list
of missing materials.

A task explicitly targeting PPU1.7 still needs its native compiler/runtime and
execution evidence. UE8M0 headers do not establish a UE4M3 NVFP4 interface;
a 20000/SM100 example does not establish 10700 TMEM/tcgen05/CLC support. A CuTe
DSL or advanced-runtime task likewise needs its own supported backend and run.

These are gaps in the reviewed material, not claims that the hardware lacks
the features. Fill them only when they affect the task; do not require a full
hardware survey before a kernel whose necessary primitives are already known.

Keep a knowledge item when it changes a design choice, proves a mapping or
helps diagnose a failure. Project budget tools, product release policy and old
fixed benchmark target lists stay in their own repositories. ACU and Asys
share one workflow entry with separate tool references.

## Tool access

KDA requires usable tools and reviewable evidence, not a particular transport.
The upstream profiler skill calls CLI/Python directly. PPU ACU/Asys have
equivalent roles in the workflow through their own commands and report schemas.
An existing MCP may expose these operations; the framework does not require
building or installing a new MCP server. See [PPU tooling](ppu-tooling.md).

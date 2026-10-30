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
| `04-python-api.md` | Use ACU CSV or the SDK's `HgRules` statistics interface; no assumed `ncu_report` compatibility. |
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

PPU1.0 is a primary target of this collection. Its native MMA, AIU/SWZL,
actlize, CuTe debugging and attention/GEMM/GEMV/MoE evidence supply much of
the current knowledge. Its resource coverage is still partial: known occupancy
limits and historical card measurements do not constitute a complete hardware
profile. The gap review below includes PPU1.0 as well as PPU1.5/1.7.

| Information needed | Evidence found in memory/skills | KDA use / remaining gap |
|---|---|---|
| Device resources and performance model | PPU0010 occupancy limits, historical card values and ACU resource counterexamples | [Architecture](../skills/ppu-kernel-knowledge/references/architecture.md) records their scope. The SKU-specific profile remains partial for 1.0; complete profiles are missing for 1.5/1.7. |
| Compiler target and native instruction path | Old wrapper-target failure; native 1.0/1.5 builds; 1.7 source/model work | Keep build contracts separate. The reviewed SDK cannot establish native 1.7 compilation. |
| MMA shape, dtype and fragment ownership | FP16/INT8 n16 maps, plain/SWZL load differences, 10700 FP8/FP4 interfaces | Use target traits and device/native probes. Do not assume SM80 or SM90 register order. |
| Global/shared movement and layouts | Plain cp.async, AIU/SWZL pairing, converter reorder, TMA descriptor deltas | Preserve producer-to-consumer composition; general 1.7 native timing/capacity data is missing. |
| Synchronization and scheduling | Async lifetime, once-vs-ordered race, pipeline arrival/release pairs, grouped/ragged scheduling | Reuse reasoning and verify participants. Cluster/DSM/multicast limits need target evidence. |
| CuTe/CUTLASS interfaces | actlize builder/collective dispatch, umbrella includes, scale cadence and extension predicates | [CUTLASS/actlize](../skills/ppu-kernel-knowledge/references/cutlass-porting.md) records the changes; version labels alone are insufficient. |
| Numerical behavior and debugging | CuTe physical ownership, stage freshness, C-to-A bridge, native argument binding, state/scale contracts | [Numerical debugging](../skills/ppu-kernel-knowledge/references/numerics.md) is retained. A general per-generation floating-point behavior table is missing. |
| Operator algorithms | GDN recurrence/WY/residual, exact and quantized attention, GEMM/GEMV/MoE | Read the relevant operator reference; retain NVIDIA algorithm/layout methods where applicable. |
| Counters and call timelines | ACU raw/rule import, metric definitions, existing Asys readers | [PPU profiling](../skills/ppu-profiling/SKILL.md) replaces tool-specific interfaces. Fresh Asys capture/export was not exercised in this documentation task. |
| Other language/runtime backends | CUDA/C++ and CuTe template evidence | PPU CuTe DSL/Triton compatibility and the upstream Hugging Face builder path were not established by these sources. |

Unresolved information to obtain for a task that depends on it:

- A per-SKU/model resource sheet: CU count, registers and allocation rules,
  shared/cache capacities, clocks, sustained memory bandwidth, dtype-specific
  tensor/ALU/SFU rates and applicable launch limits for each generation.
  For PPU1.0, retain the known occupancy values and 72-CU historical case;
  resolve the exact card/clock behind peak figures, cache capacities and the
  complete allocation rules. Instruction timing and floating-point semantics
  below also remain gaps for 1.0.
- A native PPU1.7 compiler/target and execution evidence for the requested
  atoms. In particular, UE8M0 headers do not establish a UE4M3 NVFP4 interface;
  a 20000/SM100 example does not establish 10700 TMEM/tcgen05/CLC support.
- Instruction latency/throughput and floating-point semantics for the target:
  accumulation, rounding, subnormal handling and transcendental error. Existing
  operator tests cover specific schedules, not a complete ISA specification.
- For a DSL or advanced runtime task, a supported backend/version and a minimal
  native execution example. CUDA syntax compatibility alone does not supply it.

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

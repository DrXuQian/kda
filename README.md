# Kernel Design Agents for PPU

Kernel Design Agents (KDA) is an agent-centric workflow for using coding agents to research, implement, verify, and iterate on performance-sensitive CUDA kernel tasks.

This downstream fork applies the same workflow to PPU. It retains the task
contract, draft, plan, candidate and evidence loop. PPU knowledge comes from
reviewed linear-attention, FlashAttention, SageAttention, Quactlize and other
operator work. ACU and Asys are the PPU profiling tools. See the
[document adaptation map](docs/ppu-adaptation.md) for the scope of this fork.

For work directly on **ZW810 / PPU1.0**, start with
[Run KDA on ZW810](docs/zw810.md). Give the agent a kernel entry and workload;
it resolves the task's build, correctness and benchmark commands and executes
the KDA loop for optimization or NVIDIA-to-PPU migration.

This repository documents an early research prototype and remains under active development. Community feedback and contributions are welcome. If you are interested in HAN Lab Mafia's solutions ranking #1–3 on tracks at the MLSys Kernel Contest, see [mit-han-lab/mlsys2026-flashinfer-contest](https://github.com/mit-han-lab/mlsys2026-flashinfer-contest) for performance evaluation and reproduction.

## Contents

| Path | Purpose |
|---|---|
| `docs/agent-flow.md` | Minimal end-to-end KDA workflow. |
| `prompts/README.md` | How to use prompt templates. |
| `prompts/basic-flow.md` | Generic starter prompt for a new task. |
| `docs/zw810.md` | Start optimization or migration on a physical ZW810. |
| `prompts/zw810.md` | Task prompt with agent-resolved build, validation and profiling. |
| `scripts/inspect_zw810.py` | Record SDK/tool availability and runtime device properties. |
| `docs/ppu-tooling.md` | PPU toolchain, profiling access and optional MCP integration. |
| `skills/ppu-kernel-knowledge/` | PPU architecture and operator knowledge, with source references. |
| `skills/ppu-profiling/` | ACU kernel diagnosis and Asys timeline analysis, selected by the question. |
| `docs/huggingface-export.md` | Upstream export for validated CUDA CuTe-DSL candidates. |
| `docs/ppu-artifacts.md` | PPU native library packaging and artifact handoff. |
| `CLAUDE.md` | Repository-facing agent instructions. |
| `CONTRIBUTING.md` | Contribution process and DCO sign-off requirements. |
| `THIRD_PARTY_NOTICES.md` | Third-party component and license disclosures. |
| `third_party_licenses/` | Verbatim upstream license files for distributed third-party components. |

## Kernel Requests

For PPU work, use the [request template](.github/PULL_REQUEST_TEMPLATE/wishlist.md)
in this fork. Record the PPU generation, compiler/runtime, input contract,
representative workload, baseline and commands. A request does not establish
that a kernel is supported or measured on that generation.

### Upstream Community Wishlist

Have a kernel that needs optimization? [Submit a request](https://github.com/NVlabs/kda/tree/wishlist#submit) directly as a pull request to `wishlist`, with a reproducible definition, representative workloads, and your best-known baseline implementation. No issue is required. The community wishlist currently supports NVIDIA B200 and B300 GPUs only.

[Browse and upvote requests](https://github.com/NVlabs/kda/pulls?q=is%3Apr%20base%3Awishlist), [discuss an idea](https://github.com/NVlabs/kda/issues/new?title=%5Bwishlist%5D%20) if you need help preparing the files, or visit the [project website](https://nvlabs.github.io/kda/). Keep request details in `requests/<github-username>-<kernel-name>/README.md` and use the [upstream wishlist PR template](https://github.com/NVlabs/kda/blob/ef6ce61/.github/PULL_REQUEST_TEMPLATE/wishlist.md) for the short description. Merging records the request, while optimization progress and result links remain on the original pull request. Website source lives on `pages`; the PR template and issue chooser settings are maintained on `main`.

## Getting Started
Use this checkout as workflow reference and create a separate implementation
workspace. The PPU skills are ordinary Markdown; an agent with shell/file tools
can read them directly. Their selected knowledge and references are committed
here and can be read offline on another machine. The original author's memory
and global skills are not required; [sources](skills/ppu-kernel-knowledge/references/sources.md)
distinguishes included guidance from optional external evidence.
For Claude Code discovery, link them from this checkout:

```bash
mkdir -p ~/.claude/skills
ln -s "$(pwd)/skills/ppu-kernel-knowledge" ~/.claude/skills/ppu-kernel-knowledge
ln -s "$(pwd)/skills/ppu-profiling" ~/.claude/skills/ppu-profiling
```

Use the selected PPU SDK/runtime and the target repository's existing build,
correctness and evaluation commands. Fill in [the basic prompt](prompts/basic-flow.md)
and start the agent in the implementation workspace. Read only the knowledge
pages relevant to that task. MCP is optional; see [tool access](docs/ppu-tooling.md).

The original NVIDIA skills remain useful for algorithms, CuTe, tiling,
pipelines, diagnosis and NVIDIA baselines. Apply the
[PPU coverage and differences](docs/ppu-adaptation.md#knowledge-coverage-and-gaps)
before transferring hardware-specific advice. Initialize their pinned submodules
when needed. Use
KernelWiki from this repository's pinned submodule. A direct upstream
checkout may contain artifact snapshots governed by additional terms that are
omitted from this distribution.

## Submodules

The following third-party projects are included as Git submodules. The source URLs and revisions below are intentional and match the gitlinks recorded in this repository.

| Path | Source | Pinned revision | License |
|---|---|---|---|
| `skills/KernelWiki` | [mit-han-lab/KernelWiki](https://github.com/mit-han-lab/KernelWiki.git) | Based on [`76d27b56f804e7e7295d4c570e1e5d7eef4b0a75`](https://github.com/mit-han-lab/KernelWiki/commit/76d27b56f804e7e7295d4c570e1e5d7eef4b0a75), with the repository-maintained release sanitization recorded by the gitlink | MIT for original material; embedded artifacts retain their upstream terms; restricted CuTe DSL artifacts are omitted |
| `skills/ncu-report-skill` | [mit-han-lab/ncu-report-skill](https://github.com/mit-han-lab/ncu-report-skill.git) | [`d1887948c7d53690cfe6605f59c1329b8a1c6bb5`](https://github.com/mit-han-lab/ncu-report-skill/commit/d1887948c7d53690cfe6605f59c1329b8a1c6bb5) | MIT |

These submodules are not covered by this repository's first-party license. See [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) for the applicable license text and additional details.

If using Humanize for the planning step, install it through the Claude Code
plugin UI. A manually maintained executable plan also satisfies the flow:

```text
/plugin marketplace add PolyArch/humanize
/plugin install humanize@PolyArch
```

## Minimal Flow

1. Create a separate implementation workspace for the target task.
2. Define the task contract: objective, constraints, validation command, and promotion criteria.
3. Start an agent session in the implementation workspace.
4. Give the agent `prompts/basic-flow.md`, filled in with the task-specific details.
5. Ask the agent to write a short plan draft to `docs/draft.md` in the implementation workspace.
6. Convert the draft into an executable plan, either manually or with a planning tool such as Humanize.
7. Implement in small iterations, verifying after each meaningful change.
8. Record candidates, benchmark or evaluation results, profiling evidence, and final promotion decisions.

The workflow is independent of any single benchmark harness. PPU generation,
numerics, measurement scope and promotion criteria belong in the task contract.
Existing operator evaluators remain authoritative for their tasks.

Validated CuTe candidates can be [exported as Hugging Face kernels](docs/huggingface-export.md).
For native PPU libraries, use the [PPU artifact handoff](docs/ppu-artifacts.md)
and the operator repository's existing SDK builder.

## Recommended Workspace Layout

Use this repository as reference material, then do implementation work elsewhere:

```text
task-workspace/
  docs/
    draft.md
    plan.md
  runs/
  outputs/
  profile/
  benchmark.csv
  candidates.jsonl
```

The exact files can change by domain. The important rule is that the agent records enough context for another engineer to understand what was tried, what passed validation, and why the final candidate was selected.

## Contributing

This project accepts outside contributions under the Developer Certificate of Origin process. See [CONTRIBUTING.md](CONTRIBUTING.md) before opening a pull request.

## License

Except for the third-party submodules identified above, first-party documentation, prompts, skills-style content, and assets are licensed under the [Creative Commons Attribution 4.0 International License](LICENSE), and first-party source code is licensed under the [Apache License 2.0](LICENSE).

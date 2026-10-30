# PPU artifact handoff

Export follows validation and candidate selection. The task workspace owns
the implementation, supported inputs, measurements and release destination.

The upstream [Hugging Face exporter](huggingface-export.md) is retained for
Python/JSON CuTe-DSL sources with its CUDA-oriented builder/loader. It excludes
native CUDA/C++ sources. PPU native libraries use their operator repository's
SDK builder and package layout, with the delivery contract below.

## PPU delivery contract

A runnable handoff identifies:

- Source and dependency revisions, including relevant working-tree content.
- PPU generation, compiler/SDK/runtime and actual compiled entrypoints.
- Python/Torch/C++ ABI when the artifact has those dependencies.
- Public shapes, dtypes, strides, masks/state and quantization formats.
- Binary digest, exact launch/validation command and required runtime setup.
- Passed host/native/device checks and remaining unmeasured scope.

Prepare the manifest with the artifact. Verify its identity before loading;
test the installed package outside its source checkout. A source-only or
simulator-input artifact must retain that label. Changing `cuda_capabilities`
or a runtime filename cannot make a NVIDIA package a native PPU package.

Keep artifacts in the task's output location or its established artifact
store, rather than this workflow repository. Packaging does not itself
authorize upload, installation or a default-route change.

If a future PPU Hugging Face builder/loader is available, first demonstrate
target selection, ABI/import, actual execution and the task's numerical gate
through that loader. The generic validate-before-export workflow can then be
reused; product-specific packaging policy stays in the implementation repo.

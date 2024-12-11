## Setup

First clone the repository locally, including the `ProteinCartography` submodule.

```shell
git clone --recurse-submodules git@github.com:latchbio/wf-protein-cartography-single.git
```

Next, you can register the pipeline normally by running

```shell
latch register -y .
```

## Pipeline Summary

The workflow defined here calls the `ProteinCartography` snakemake workflow via `subprocess`, on a single machine configured to use 2 vCPUs and 4 GiB RAM. Environment management is done via `mamba`.

The entrypoint code is in `wf/entrypoint.py`, with parameter metadata stored in `wf/metadata.py`.

The code is run inside of a docker image which is fully specified in `Dockerfile`. The `snakemake` binary is installed inside of the `cartography_tidy` env. This env is used to call the pipeline.

Currently the pipeline recreates every environment it needs each time it runs. A potential enhancement would be to pre-build all of these environments in the host docker image and reference them by name. I did not do this here as that would require modifying the `ProteinCartography` pipeline directly.


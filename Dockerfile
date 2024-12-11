# DO NOT CHANGE
from 812206152185.dkr.ecr.us-west-2.amazonaws.com/latch-base:fe0b-main

workdir /tmp/docker-build/work/

shell [ \
    "/usr/bin/env", "bash", \
    "-o", "errexit", \
    "-o", "pipefail", \
    "-o", "nounset", \
    "-o", "verbose", \
    "-o", "errtrace", \
    "-O", "inherit_errexit", \
    "-O", "shift_verbose", \
    "-c" \
]
env TZ='Etc/UTC'
env LANG='en_US.UTF-8'

arg DEBIAN_FRONTEND=noninteractive

# Latch SDK
# DO NOT REMOVE
# Note: using stable release version of latch instead of alpha
run pip install latch==2.54.10
run mkdir /opt/latch

run apt-get update && apt-get install -y git

# install mamba
run curl -L -O \
    https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-Linux-x86_64.sh \
    && mkdir /root/.conda \
    && bash Miniforge3-Linux-x86_64.sh -b \
    && rm -f Miniforge3-Linux-x86_64.sh
env PATH /root/miniforge3/bin:$PATH

copy ProteinCartography /root/ProteinCartography
run mamba env create -f /root/ProteinCartography/envs/cartography_tidy.yml -n cartography_tidy

# Note: this makes `mamba` point to /root/miniforge3/envs/cartography_tidy/bin/mamba instead of /root/miniforge3/bin/mamba
# This is fine because we create new environments on every run
env PATH /root/miniforge3/envs/cartography_tidy/bin:$PATH

# Copy workflow data (use .dockerignore to skip files)
copy . /root/

# DO NOT CHANGE
arg tag
env FLYTE_INTERNAL_IMAGE $tag
workdir /root

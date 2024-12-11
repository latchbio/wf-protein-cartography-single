import json
import subprocess
import sys
from pathlib import Path

from latch.resources.tasks import small_task
from latch.resources.workflow import workflow
from latch.types.directory import LatchDir, LatchFile, LatchOutputDir

from .metadata import metadata


@small_task
def snakemake_runtime(
    input_dir: LatchDir,
    output_dir: LatchOutputDir,
    config_file: LatchFile,
) -> LatchDir:
    # downloads input directory
    local_input = Path(input_dir).resolve()
    local_output = Path("/root/output")

    config = {
        "input_dir": str(local_input),
        "output_dir": str(local_output),
    }

    io_config_path = Path("/root/latch_config.json")
    io_config_path.write_text(json.dumps(config, indent=2))

    try:
        subprocess.run(
            [
                "snakemake",
                "--cores",
                "2",
                "--configfile",
                str(Path(config_file)),
                str(io_config_path),
                "--conda-frontend",
                "mamba",
                "--use-conda",
            ],
            check=True,
            cwd="/root/ProteinCartography",
        )
    except subprocess.CalledProcessError:
        sys.exit(1)

    # by returning here, we upload the local output directory to latch
    return LatchDir(local_output, remote_path=output_dir.remote_path)


@workflow(metadata)
def protein_cartography_single(
    input_dir: LatchDir,
    output_dir: LatchOutputDir,
    config_file: LatchFile,
) -> LatchDir:
    return snakemake_runtime(
        input_dir=input_dir,
        output_dir=output_dir,
        config_file=config_file,
    )

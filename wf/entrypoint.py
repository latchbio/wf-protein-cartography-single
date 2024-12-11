import json
import subprocess
import sys
import typing
from enum import Enum
from pathlib import Path

from latch.resources.tasks import small_task
from latch.resources.workflow import workflow
from latch.types.directory import LatchDir, LatchOutputDir

from .metadata import PipelineMode, PlottingMode, TaxonFocus, metadata


def get_config_val(val: typing.Any):
    if isinstance(val, list):
        return [get_config_val(x) for x in val]
    if isinstance(val, dict):
        return {k: get_config_val(v) for k, v in val.items()}
    if isinstance(val, (int, float, bool, type(None))):
        return val
    if isinstance(val, Enum):
        return val.value

    return str(val)


@small_task
def snakemake_runtime(
    mode: PipelineMode,
    input_dir: LatchDir,
    output_dir: LatchOutputDir,
    analysis_name: str,
    foldseek_databases: typing.List[str],
    max_foldseek_hits: int,
    max_blast_hits: int,
    blast_word_size: int,
    blast_word_size_backoff: int,
    blast_evalue: float,
    blast_num_attempts: int,
    max_structures: int,
    min_length: int,
    max_length: int,
    plotting_modes: typing.List[PlottingMode],
    taxon_focus: TaxonFocus,
) -> LatchDir:
    # downloads input directory
    local_input = Path(input_dir).resolve()

    local_output = Path("/root/output")

    config = {
        "mode": get_config_val(mode),
        "input_dir": get_config_val(local_input),
        "output_dir": get_config_val(local_output),
        "analysis_name": get_config_val(analysis_name),
        "foldseek_databases": get_config_val(foldseek_databases),
        "max_foldseek_hits": get_config_val(max_foldseek_hits),
        "max_blast_hits": get_config_val(max_blast_hits),
        "blast_word_size": get_config_val(blast_word_size),
        "blast_word_size_backoff": get_config_val(blast_word_size_backoff),
        "blast_evalue": get_config_val(blast_evalue),
        "blast_num_attempts": get_config_val(blast_num_attempts),
        "max_structures": get_config_val(max_structures),
        "min_length": get_config_val(min_length),
        "max_length": get_config_val(max_length),
        "plotting_modes": get_config_val(plotting_modes),
        "taxon_focus": get_config_val(taxon_focus),
    }

    config_path = Path("/root/latch_config.json")
    config_path.write_text(json.dumps(config, indent=2))

    try:
        subprocess.run(
            [
                "snakemake",
                "--cores",
                "2",
                "--configfile",
                str(config_path),
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
    mode: PipelineMode = PipelineMode.search,
    input_dir: LatchDir = LatchDir("latch:///arcadia-data/input"),
    output_dir: LatchOutputDir = LatchDir("latch:///arcadia-results"),
    analysis_name: str = "example",
    foldseek_databases: typing.List[str] = [
        "afdb50",
        "afdb-swissprot",
        "afdb-proteome",
    ],
    max_foldseek_hits: int = 3000,
    max_blast_hits: int = 3000,
    blast_word_size: int = 5,
    blast_word_size_backoff: int = 6,
    blast_evalue: float = 1.0,
    blast_num_attempts: int = 3,
    max_structures: int = 5000,
    min_length: int = 0,
    max_length: int = 0,
    plotting_modes: typing.List[PlottingMode] = [
        PlottingMode.pca_tsne,
        PlottingMode.pca_umap,
    ],
    taxon_focus: TaxonFocus = TaxonFocus.euk,
) -> LatchDir:
    return snakemake_runtime(
        mode=mode,
        input_dir=input_dir,
        output_dir=output_dir,
        analysis_name=analysis_name,
        foldseek_databases=foldseek_databases,
        max_foldseek_hits=max_foldseek_hits,
        max_blast_hits=max_blast_hits,
        blast_word_size=blast_word_size,
        blast_word_size_backoff=blast_word_size_backoff,
        blast_evalue=blast_evalue,
        blast_num_attempts=blast_num_attempts,
        max_structures=max_structures,
        min_length=min_length,
        max_length=max_length,
        plotting_modes=plotting_modes,
        taxon_focus=taxon_focus,
    )

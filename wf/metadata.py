from enum import Enum

from latch.types.directory import LatchDir
from latch.types.metadata import LatchAuthor, LatchMetadata, LatchParameter


class PlottingMode(Enum):
    pca = "pca"
    tsne = "tsne"
    umap = "umap"
    pca_tsne = "pca_tsne"
    pca_umap = "pca_umap"

    def __repr__(self):
        return f"{self.__class__.__name__}.{self.value}"


class TaxonFocus(Enum):
    euk = "euk"
    bac = "bac"

    def __repr__(self):
        return f"{self.__class__.__name__}.{self.value}"


class PipelineMode(Enum):
    search = "search"
    cluster = "cluster"

    def __repr__(self):
        return f"{self.__class__.__name__}.{self.value}"


generated_parameters = {
    "mode": LatchParameter(display_name="Mode"),
    "input_dir": LatchParameter(display_name="Input Dir"),
    "output_dir": LatchParameter(display_name="Output Dir"),
    "analysis_name": LatchParameter(display_name="Analysis Name"),
    "foldseek_databases": LatchParameter(display_name="Foldseek Databases"),
    "max_foldseek_hits": LatchParameter(display_name="Max Foldseek Hits"),
    "max_blast_hits": LatchParameter(display_name="Max Blast Hits"),
    "blast_word_size": LatchParameter(display_name="Blast Word Size"),
    "blast_word_size_backoff": LatchParameter(display_name="Blast Word Size Backoff"),
    "blast_evalue": LatchParameter(display_name="Blast Evalue"),
    "blast_num_attempts": LatchParameter(display_name="Blast Num Attempts"),
    "max_structures": LatchParameter(display_name="Max Structures"),
    "min_length": LatchParameter(display_name="Min Length"),
    "max_length": LatchParameter(display_name="Max Length"),
    "plotting_modes": LatchParameter(display_name="Plotting Modes"),
    "taxon_focus": LatchParameter(display_name="Taxon Focus"),
}

metadata = LatchMetadata(
    display_name="Protein Cartography Single",
    author=LatchAuthor(name="Arcadia Biosciences"),
    parameters=generated_parameters,
)

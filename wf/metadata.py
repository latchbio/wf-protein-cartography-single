from latch.types.metadata import LatchAuthor, LatchMetadata, LatchParameter

# Using the Latch-Specific Metadata (instead of SnakemakeV2Metadata)
metadata = LatchMetadata(
    display_name="Protein Cartography Single",
    author=LatchAuthor(name="Arcadia Biosciences"),
    parameters={
        "input_dir": LatchParameter(display_name="Input Dir"),
        "output_dir": LatchParameter(display_name="Output Dir"),
        "config_file": LatchParameter(display_name="Config File"),
    },
)

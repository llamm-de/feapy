import argparse
from pathlib import Path
from .VTUFile import VTUFile
from .VTURefactorer import VTURefactorer
import json
from tqdm import tqdm
from joblib import Parallel, delayed


def _create_parser() -> argparse.ArgumentParser:
    """
    Create argument parser object
    """
    parser = argparse.ArgumentParser(
        description="Converting FEAP vtu output. Using a predefined mapping .json-file, this tool is able to convert the fields given in the vtu output generated by FEAP such that they are more human readable."
    )
    parser.add_argument(
        "-i",
        "--input_file",
        type=str,
        default="Iinput",
        help="Name of input file for FEAP computation. (Default: Iinput)",
    )
    parser.add_argument(
        "-m",
        "--mapping_file",
        type=str,
        default="mapping.json",
        help="Name of mapping file used for conversion. (Default: mapping.json)",
    )
    parser.add_argument(
        "-j",
        "--jobs",
        type=int,
        default=-1,
        help="Number of parallel jobs. (Default: Maxmimum number of cores available)",
    )
    parser.add_argument(
        "-r",
        "--remove_originals",
        action="store_true",
        help="Remove original vtu files. (Default: False)",
    )

    return parser


def _refactor_vtu_file(vtu_file_path: Path, refactoring_pattern: dict):
    """
    Routine for refactoring of single vtu file
    """
    vtu_file = VTUFile(vtu_file_path.as_posix())
    refactorer = VTURefactorer(vtu_file, refactoring_pattern)
    refactorer.refactor()
    out_file_path = Path(vtu_file_path.parent) / f"{vtu_file_path.stem}_refactored.vtu"
    vtu_file.export_file(out_file_path.as_posix())


def main() -> None:

    # Set up command line argument parsing
    parser = _create_parser()
    args = parser.parse_args()

    # Get base path
    base_path = Path.cwd()

    # Load mapping data from file
    mapping_path = base_path / args.mapping_file
    if not mapping_path.exists():
        raise FileNotFoundError(f"{mapping_path.as_posix()} does not exist.")
    else:
        print(f"Selected mapping: {mapping_path.as_posix()}")
    with mapping_path.open() as f:
        refactoring_pattern = json.load(f)

    # Get all vtu files from input file pattern
    pattern = f"P{args.input_file[1:]}[0-9][0-9][0-9][0-9][0-9].vtu"
    vtu_files = list(base_path.glob(pattern))
    if not vtu_files:
        raise FileNotFoundError("No vtu-files found in this directory.")

    # Perform refactoring using parallel computing
    Parallel(n_jobs=args.jobs)(
        delayed(_refactor_vtu_file)(vtu_file, refactoring_pattern)
        for vtu_file in tqdm(
            vtu_files,
            desc="Refactoring files",
            total=len(vtu_files),
            colour="green",
        )
    )

    # Remove old files if selected
    if args.remove_originals:
        for vtu_file in tqdm(
            vtu_files,
            desc="Removing original files",
            total=len(vtu_files),
            colour="green",
        ):
            vtu_file.unlink(missing_ok=False)


if __name__ == "__main__":
    main()

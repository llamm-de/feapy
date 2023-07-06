import argparse
from pathlib import Path
import shutil
import sys
import os


def main() -> None:
    """
    Command line script for setting up FEAP in systems path
    """
    # Set up command line argument parsing
    parser = argparse.ArgumentParser(
        description="Command line script for setting up FEAP in systems path."
    )
    parser.add_argument("path_to_feap", help="Path to running version of feap.")
    parser.add_argument(
        "--name",
        help="Name for the feap executable to be used in cmd.",
        default="feap",
    )
    parser.add_argument(
        "--dir",
        help="Name of the binary directory used for storing executables.",
        default=Path.home() / "bin",
    )
    parser.add_argument(
        "--no_link",
        help="Define that FEAP included as an executable.",
        action="store_true",
    )

    args = parser.parse_args()

    # Create path objects for later use
    bin_path = Path(args.dir)
    exe_path = Path(args.path_to_feap)
    new_path = bin_path / args.name

    # Check if path to feap exists
    if not exe_path.is_file():
        raise RuntimeError(f"Path {exe_path} is not an executable file.")

    # Check if new file path exists and should be overriden
    if new_path.exists():
        override = input(
            f"File or symlink at {new_path} already exists. Do you want to override? (yes/no) "
        )
        if override.lower() == "yes":
            print(f"Removing {new_path} !")
            new_path.unlink()
        else:
            print("Exiting")
            sys.exit()

    # Setting up bin directory in home directory
    if bin_path.is_dir():
        print(f"Using bin directory found in {Path.home()}")
    else:
        print(f"Creating bin directory in {Path.home()}")
        bin_path.mkdir(exist_ok=True)

    # Copy executable to bin directory
    if args.no_link:
        print(f"Copying executable from {exe_path} to {new_path}.")
        shutil.copy(exe_path, new_path)
    else:
        print(f"Creating symlink from {exe_path} to {new_path}.")
        new_path.symlink_to(exe_path)

    # Set Environment variable to include bin directory in path
    if bin_path.as_posix() in os.environ["PATH"]:
        print(f"{bin_path} is already set in environment path.")
    else:
        override = input(
            f"ATTENTION: This step will modify your .bashrc file! Do you want to proceed? (yes/no)"
        )
        if override.lower() == "yes":
            print(f"Setting {bin_path} as environment path in .bashrc")
            bashrc = Path().home() / ".bashrc"

            # To circumvent overriding the .bashrc, we must first load the original data
            bashrc_text = bashrc.read_text()
            bashrc_text += "export PATH=$PATH:$HOME/bin"
            bashrc.write_text(bashrc_text)
        else:
            print(
                f"{bin_path} NOT set as environment path in .bashrc. Please manually set your PATH variable to find feap."
            )


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("Something went wrong!")
        print(e)

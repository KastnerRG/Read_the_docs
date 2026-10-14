#!/usr/bin/env python3
"""Fetch and cache upstream board definitions, printing the board repository path."""

import argparse
import os
from pathlib import Path
import subprocess
import sys
import tempfile


BOARD_SOURCES = {
    "zu3": {
        "name": "aup-zu3-bsp",
        "url": "https://github.com/RealDigitalOrg/aup-zu3-bsp.git",
        "checkout": "board-files",
        "board_root": "board-files",
    },
    "pynq": {
        "name": "XilinxBoardStore",
        "url": "https://github.com/Xilinx/XilinxBoardStore.git",
        "checkout": "boards/TUL/pynq-z2",
        "board_root": "boards/TUL",
    },
}


def has_board_files(directory):
    return directory.is_dir() and any(path.is_file() for path in directory.rglob("board.xml"))


def run_git(*args):
    # Vivado prepends bundled libraries that can conflict with the host Git/SSL.
    environment = os.environ.copy()
    if "PP4FPGA_HOST_LD_LIBRARY_PATH" in environment:
        environment["LD_LIBRARY_PATH"] = environment["PP4FPGA_HOST_LD_LIBRARY_PATH"]
    environment.pop("PYTHONHOME", None)
    environment.pop("PYTHONPATH", None)
    try:
        subprocess.run(["git", *args], check=True, stdout=subprocess.PIPE,
                       stderr=subprocess.STDOUT, text=True, env=environment)
    except subprocess.CalledProcessError as error:
        raise RuntimeError(error.stdout.strip()) from error


def fetch_board_files(target, cache_dir):
    source = BOARD_SOURCES[target]
    cache_dir = Path(cache_dir).resolve()
    repository = cache_dir / source["name"]
    board_root = repository / source["board_root"]
    if repository.exists():
        if has_board_files(board_root):
            return board_root
        raise RuntimeError(
            f"Cache directory {repository} exists but contains no board definitions. "
            "Move it aside to allow a fresh download, or set BOARD_REPO."
        )

    cache_dir.mkdir(parents=True, exist_ok=True)
    # Publish only a complete checkout, so failed downloads can be retried.
    with tempfile.TemporaryDirectory(prefix=f".{source['name']}-", dir=cache_dir) as staging:
        checkout = Path(staging) / source["name"]
        run_git("clone", "--depth", "1", "--filter=blob:none", "--sparse", "--",
                source["url"], str(checkout))
        run_git("-C", str(checkout), "sparse-checkout", "set", source["checkout"])
        if not has_board_files(checkout / source["board_root"]):
            raise RuntimeError(f"No board definitions found in {source['url']}")
        try:
            checkout.rename(repository)
        except OSError:
            # Another build may have completed the same download in parallel.
            if not has_board_files(board_root):
                raise
    return board_root


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", choices=BOARD_SOURCES, required=True)
    parser.add_argument("--cache-dir", type=Path, required=True)
    args = parser.parse_args()
    try:
        print(fetch_board_files(args.target, args.cache_dir))
    except (OSError, RuntimeError) as error:
        print(f"Board-file download failed: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())

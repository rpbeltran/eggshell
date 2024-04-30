#!/usr/bin/python3

import argparse
from pathlib import Path
from typing import Text
import subprocess


def get_tidy_command(clang_tidy: Text, build_dir: Text, cpp_file: Path):
    additional_args = ['--extra-arg=-std=gnu++2b', '-header-filter=.*']
    return [clang_tidy] + additional_args + ['-p', build_dir, cpp_file]


def invoke_tidy(clang_tidy: Text, build_dir: Text, cpp_file: Path):
    command = get_tidy_command(clang_tidy, build_dir, cpp_file)
    subprocess.Popen(
        command,
        cwd=build_dir,
    ).wait()



def parse_args():
    parser = argparse.ArgumentParser("run_linters")
    parser.add_argument(
        "-b", "--build",
        dest="build_dir",
        help="path to build from last cmake run.",
        required=True,
        type=str
    )
    parser.add_argument(
        "--clang-tidy",
        help="path to clang tidy executable.",
        default="clang-tidy",
        type=str
    )
    parser.add_argument(
        "cpp_files",
        help="path to build from last cmake run.",
        nargs='+'
    )
    return parser.parse_args()


def main():
    args = parse_args()
    for cpp_file in args.cpp_files:
        cpp_file = Path(cpp_file).resolve()
        invoke_tidy(args.clang_tidy, args.build_dir, cpp_file)


if __name__ == "__main__":
    main()
import argparse
import collections
import configparser
from datetime import datetime
from fnmatch import fnmatch
import os
import zlib
import sys
from pathlib import Path


"""
Simple dummy library to understand how git actually works
"""

        
def repo_to_path(repo, *paths):
    return repo.git_path.joinpath(*paths)


class GitRepository:

    workdir: Path = None
    git_path: Path = None
    repo_name: str = ""
    config = None

    def __init__(self, path):
        self.workdir = Path(path)
        self.git_path = self.workdir / ".git"

        # read config 
        self.config = configparser.ConfigParser()
        config_path = repo_to_path(self.workdir, "config")
        if config_path.exists():
            self.config.read(config_path)
        else:
            raise FileNotFoundError(f"Could not find config in expected path: {config_path}")


def repo_init(path):

    repo = GitRepository(path)

    # Make sure that the path doesn't already exist for simplicity
    if path.exists():
        if not path.is_dir():
            raise Exception("cannot mkdir blugr - file already exists")
    else:
        path.mkdir(exist_ok=True)


def create_argparser():
    argparser = argparse.ArgumentParser(description="Simple content tracker")
    argsubparsers = argparser.add_subparsers(title="Commands", dest="command")
    argsubparsers.required = True

    argsp = argsubparsers.add_parser("init", help="Initialize tig repo")
    argsp.add_argument("path",
                       metavar="directory",
                       nargs="?",
                       default=".",
                       help="where to create repository")
        
def main(argv=sys.argv[1:]):
    argparser = create_argparser()
    args = argparser.parse_args(argv)

    breakpoint()
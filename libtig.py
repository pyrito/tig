import argparse
import collections
import configparser
import os
import sys
import zlib
from datetime import datetime
from fnmatch import fnmatch
from pathlib import Path

"""
Simple dummy library to understand how git actually works
"""


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
        config_path = repo_path(self, "config")
        if config_path.exists():
            self.config.read(config_path)


def repo_path(repo, *paths):
    return repo.git_path.joinpath(*paths)


def repo_dir(repo, *paths, mkdir=False):
    d = repo_path(repo, *paths)

    if d.exists() and d.is_dir():
        return d

    if mkdir:
        d.mkdir(parents=True)
        return d
    else:
        return None


def repo_init(path):

    repo = GitRepository(path)

    # Make sure that the path doesn't already exist for simplicity
    if repo.workdir.exists():
        if not repo.workdir.is_dir():
            raise Exception("cannot mkdir blugr - file already exists")
    else:
        repo.workdir.mkdir(parents=True)

    # We need to create a couple of directories and a couple of files
    assert repo_dir(repo, "hooks", mkdir=True)
    assert repo_dir(repo, "info", mkdir=True)
    assert repo_dir(repo, "objects", "info", mkdir=True)
    assert repo_dir(repo, "objects", "pack", mkdir=True)
    assert repo_dir(repo, "refs", mkdir=True)

    with open(repo_path(repo, "HEAD"), "w") as f:
        f.write("ref: refs/heads/main\n")

    # TODO: write the config

    with open(repo_path(repo, "description"), "w") as f:
        f.write("some description\n")


def create_argparser():
    argparser = argparse.ArgumentParser(description="Simple content tracker")
    argsubparsers = argparser.add_subparsers(title="Commands", dest="command")
    argsubparsers.required = True

    argsp = argsubparsers.add_parser("init", help="Initialize tig repo")
    argsp.add_argument(
        "path",
        metavar="directory",
        nargs="?",
        default=".",
        help="where to create repository",
    )

    return argparser


def main(argv=sys.argv[1:]):
    argparser = create_argparser()
    args = argparser.parse_args(argv)
    repo_init("test")

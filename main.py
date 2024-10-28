import argparse
from parsing import add_parse_args
from utils import (read_hparams,
                   web_search,
                   DownloadandRun,
                   )
from make_db import make_db
"""
READ ARGS OR PARAMETERS
"""
# First let's read args for our experiment
parser = argparse.ArgumentParser()
add_parse_args(parser)
args = parser.parse_args()

if args is None:
    path_to_hparams = "my_params.yaml"
    args = read_hparams(path_to_hparams)

def main():
    """
    SEARCH WEBSITE FOR DATA
    """
    web_search(args)

    """
    DOWNLOADING FILES
    """
    DownloadandRun()

    """
    CREATING SQL DATABASE
    """
    make_db(args)

if __name__ == '__main__':
    main()
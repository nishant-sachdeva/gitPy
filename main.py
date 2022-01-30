from sourceCode.constants import listOfCommands
from sourceCode.gitInit import cmd_init

import argparse
import collections
import configparser
import hashlib
import os
import re
import sys
import zlib

argparser = argparse.ArgumentParser(description='Command Tracker')
argSubParsers = argparser.add_subparsers(title='Commands', dest='command')
argSubParsers.required = True

argsp = argSubParsers.add_parser("init", help="Initialize a new empty git repository")
argsp.add_argument("path",
                    metavar="directory", 
                    nargs="?", 
                    default = ".", 
                    help= "Where to create the git repository. Current directory by default")

def main(argv=sys.argv[1:]):
    print(argv)
    args = argparser.parse_args(argv)

    if args.command in listOfCommands:
        print("Found the command", args.command)
        commandName = "cmd_" + args.command
        print("Calling", commandName)
        globals()[commandName](args)
    else:
        print("Unknown command: " + args.command)
        print("Available commands: " + ", ".join(listOfCommands))
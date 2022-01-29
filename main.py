from sourceCode.constants import listOfCommands

import argparse
import collections
import configparser
import hashlib
import os
import re
import sys
import zlib

argparser = argparse.ArgumentParser(description='Content Tracker')
argSubParsers = argparser.add_subparsers(title="Commands", dest='command')
argSubParsers.required = False

def main(argv=sys.argv[1:]):
    args = argparser.parse_args(argv)

    print("Passed this line")
    if args.command in listOfCommands:
        commandName = "cmd_" + args.command
        locals()[commandName]()
    else:
        print("Unknown command: " + args.command)
        print("Available commands: " + ", ".join(listOfCommands))
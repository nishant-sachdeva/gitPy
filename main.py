from sourceCode.randomFunction import printLog
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
argSubParsers.required = True

def main(argv=sys.argv[1:]):
    args = argparser.parse_args(argv)

    if args.command in listOfCommands:
        commandName = "cmd_" + args.command
        locals()[commandName]()
    else:
        print("Unknown command: " + args.command)
        print("Available commands: " + ", ".join(listOfCommands))
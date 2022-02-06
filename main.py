from sourceCode.constants import listOfCommands
from sourceCode.gitInit import cmd_init
from sourceCode.gitCatFile import cmd_cat_file

import argparse
import re
import sys

def configArgParser():
    argparser = argparse.ArgumentParser(description='Command Tracker')
    argSubParsers = argparser.add_subparsers(title='Commands', dest='command')
    argSubParsers.required = True

    # INIT COMMAND
    argInit = argSubParsers.add_parser("init", help="Initialize a new empty git repository")
    argInit.add_argument("path",
                        metavar="directory", 
                        nargs="?", 
                        default = ".", 
                        help= "Where to create the git repository. Current directory by default")

    # CAT FILE COMMAND
    argCatFile = argSubParsers.add_parser("cat-file", help = "Provide Content of an object")
    argCatFile.add_argument("type",
                            metavar="type",
                            choices=["blob", "commit", "tag", "tree"],
                            help="Specify the type")

    # HASH-OBJECT COMMAND
    argHashObject = argSubParsers.add_parser("hash-object", help = "Compute object ID and optionally creates a blob from a file")
    argHashObject.add_argument("-t",
                            metavar="type",
                            dest = "type",
                            choices = ["blob", "commit", "tag", "tree"],
                            default = "blob",
                            help = "Specify the type")
    
    argHashObject.add_argument("-w",
                            metavar="write",
                            dest = "write",
                            action = "store_true",
                            help = "Actually write the object into the database")
    
    argHashObject.add_argument("path", help = "Read object from <file>")

    
    # LOG COMMAND
    argLog = argSubParsers.add_parser("log", help = "Display history of a given commit")
    argLog.add_argument("commit",default="HEAD", nargs = "?", help="Commit to start from")

    # LS TREE COMMAND
    argLsTree = argSubParsers.add_parser("ls-tree", help = "List the contents of a tree object")
    argLsTree.add_argument("object", help="Tree to list")

    # CHECKOUT COMMAND
    argCheckout = argSubParsers.add_parser("checkout", help = "Checkout a commit insider of a directory")
    
    argCheckout.add_argument("commit", help="Commit to checkout")
    argCheckout.add_argument("path", help="The EMPTY Directory to checkout on")

    return argparser


def main(argparser, argv=sys.argv[1:]):
    print(argv)
    args = argparser.parse_args(argv)

    if args.command in listOfCommands:
        commandName = "cmd_" + args.command
        globals()[commandName](args)
    else:
        print("Unknown command: " + args.command)
        print("Available commands: " + ", ".join(listOfCommands))
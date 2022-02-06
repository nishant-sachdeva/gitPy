from gitObjectUtils import object_read, object_find
from gitInit import repo_find

import sys

def cat_file(repo, object, fmt=None):
    object = object_read(repo, object_find(repo, object, fmt = fmt))
    sys.stdout.buffer.write(object.serialize())

def cmd_cat_file(args):
    repo = repo_find()
    cat_file(repo, args.object, fmt = args.type.encode())
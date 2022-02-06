from gitObjectUtils import object_read, object_find
from gitInit import repo_find

import os

def tree_checkout(repo, tree, path):
    for item in tree.items:
        object = object_read(repo, item.sha)
        dest = os.path.join(path, item.path)

        if object.fmt == b'tree':
            os.mkdir(dest)
            tree_checkout(repo, object, dest)
        elif object.fmt == b'blob':
            with open(dest, 'wb') as fd:
                fd.write(object.blobdata)

def cmd_checkout(args):
    repo = repo_find()
    object = object_read(repo, object_find(repo, args.commit))

    # if the object is a commit, we grab it's tree
    if object.fmt == b'commit':
        object = object_read(repo, object.kvlm[b'tree'].decode("ascii"))

    if os.path.exists(args.path):
        if not os.path.isdir(args.path):
            raise Exception("Not a Directory {0}".format(args.path))
        if os.listdir(args.path):
            raise Exception("Not Empty {0}".format(args.path))

    else:
        os.makedirs(args.path)
    
    tree_checkout(repo, object, os.path.realpath(args.path).encode())
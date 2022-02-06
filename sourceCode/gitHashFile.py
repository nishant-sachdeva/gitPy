from gitObjectUtils import object_write
from gitObjects import gitBlob, gitCommit, gitTree, gitTag
from gitInit import gitRepository

def object_hash(fd, fmt, repo = None):
    data = fd.read()

    # choose constructor based on the object Type
    # found in the header

    if fmt == 'b'commit:
        object = gitCommit(repo,data)
    elif fmt == b'tree':
        object = gitTree(repo,data)
    elif fmt == b'tag':
        object = gitTag(repo, data)
    elif fmt == b'blob':
        object = gitBlob(repo, data)
    else:
        raise Exception("Unknown type: %s" % fmt)
    
    return object_write(object, repo)

def cmd_hash_object(args):
    if args.write:
        repo = gitRepository(".")
    else:
        repo = None
    
    with open(args.path, 'rb') as fd:
        sha = object_hash(fd, args.type.encode(), repo)
        print(sha)
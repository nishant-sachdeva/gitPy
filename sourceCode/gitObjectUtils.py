from gitInit import repo_file

import zlib
import hashlib

### Git Objects WRITE ###
def object_write(object, actually_write = True):
    # Serialize object data
    data = object.serialize()

    # Add Header
    result = object.fmt + b' ' + str(len(data)).encode() + b'\x00' + data

    # Compute Hash
    sha = hashlib.sha1(result).hexdigest()

    if actually_write:
        # Compute Path
        path = repo_file(object.repo, "objects", sha[0:2], sha[2:], mkdir=actually_write)

        with open(path, 'wb') as f:
            f.write(zlib.compress(result))    
    
    return sha


### Git Objects FIND ###
def object_find(repo, name,fmt=None, follow=True):
    return name


### Git Objects READ ###
def object_read(repo, sha):
    """ Read object object_id from Git Repository repo.
        Return a GitObject whose exact type depends on the object
    """
    path = repo_file(repo, "objects", sha[0:2], sha[2:])

    with open(path, 'rb') as f:
        raw = zlib.decompress(f.read())

        # Read object type
        x = raw.find(b' ')
        fmt = raw[0:x]

        # Read and validate object size
        y = raw.find(b'\x00', x)
        size = int(raw[x:y].decode("ascii"))

        if size != len(raw) - y - 1:
            raise Exception("Malformed object {0}: bad length".format(sha))
        
        # Pick Constructor
        if fmt == b'commit':
            constructor = gitCommit
        elif fmt == b'tree':
            constructor = gitTree
        elif fmt == b'tag':
            constructor = gitTag
        elif fmt == b'blob':
            constructor = gitBlob
        else:
            raise Exception("Unknown Type {0} for object {1}".format(fmt.decode("ascii"), sha))

        
        # call constructor and return object
        return constructor(repo, raw[y + 1:])

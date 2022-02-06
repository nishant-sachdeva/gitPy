from gitCommit import kvlm_parse, kvlm_serialize
from gitTreeUtils import tree_parse, tree_serialize

### PARENT Git Object Class
class gitObject(object):
    repo = None

    def __init__(self, repo, data=None):
        self.repo = repo

        if data is not None:
            self.deserialize(data)
    
    def serialize(self):
        """
            This function MUST be implemented by subclasses.
            It must read the object's contents from self.data, a byte string,
            and do whatever it takes to convert it into a meaningful representation.
            What exactly that means depend on each subclass.
        """
        raise Exception("Unimplemented")

    def deserialize(self, data):
        raise Exception("Unimplemented")


### Git BLOB Object
class gitBlob(gitObject):
    fmt = b'blob'

    def serialize(self):
        return self.blobData

    def deserialize(self, data):
        self.blobData = data

class gitTree(gitObject):
    fmt = b'tree'

    def deserialize(self, data):
        self.items = tree_parse(data)

    def serialize(self):
        return tree_serialize(self)

class gitCommit(gitObject):
    fmt = b'commit'

    def deserialize(self, data):
        self.kvlm = kvlm_parse(data)
    
    def serialize(self):
        return kvlm_serialize(self.kvlm)

class gitBlob(gitObject):
    pass
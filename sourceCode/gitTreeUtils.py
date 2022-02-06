class gitTreeLeaf(object):
    def __init__(self, mode, path, sha):
        self.mode = mode
        self.path = path
        self.sha = sha

def tree_parse_one(raw ,start = 0):
    # find the space terminator of the mode
    spc = raw.find(b' ', start)

    assert(spc > 0 and spc - start == 5 or spc - start == 6)

    # Read the Mode
    mode = raw[start:spc]

    # Find the Null Terminator of the path
    y = raw.find(b'\x00', spc)

    # now, read the path
    path = [spc + 1 : y]

    # Now, read the SHA and convert it to a HEX string
    sha = hex(int.from_bytes(
        raw[y + 1 : y + 21], "big"))[2:]
    
    # hex adds 0x in front. We dont need that, so the [2:]

    return y+21, gitTreeLeaf(mode, path, sha)


def tree_parse(raw):
    pos = 0
    max = len(raw)
    ret = list()

    while pos < max:
        pos, data = tree_parse_one(raw, pos)
        ret.append(data)
    
    return ret

def tree_serialize(object):
    ret = b''
    for i in obj.items:
        ret += i.mode
        ret += b' '
        ret += i.path
        ret += b'\x00'
        sha = int(i.sha, 16)
        ret += sha.to_bytes(20, byteorder="big")
    return ret
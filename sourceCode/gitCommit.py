import collections

def kvlm_parse(raw, start = 0, dct = None):
    if not dct:
        dct = collections.OrderedDict()

        # Should not declare the argument as dct = OrderedDict()
        # or all calls to the functions will endlessly grow the same dictionary

    # now, we search for the next space and the next newline
    spc = raw.find(b' ', start)
    nl = raw.find(b'\n', start)

    # if space appears before newline, we have a keyword

    # BASE CASE 
    # =========
    # If newline appears first (or there's no space at all, in which
    # case find returns -1), we assume a blank line.  A blank line
    # means the remainder of the data is the message.
    if (spc < 0) or (nl < spc):
        assert(nl == start)
        dct[b''] = raw[start+1:]
        return dct
    
    # RECURSIVE CASE
    # ==============
    # we read a key-value pair and recurse for the next.
    key = raw[start:spc]
    
    # Find the end of the value.  Continuation lines begin with a
    # space, so we loop until we find a "\n" not followed by a space.
    end = start

    while True:
        end = raw.find(b'\n', end+1)
        if raw[end+1] != ord(' '):
            break

    # grab the value
    # Also drop the leading space on continuation lines
    value = raw[spc+1:end].replace(b'\n', b'\n')

    # don't overwrite existing data contents

    if key in dict:
        if type(dct[key]) == list:
            dct[key].append(value)
        else:
            dct[key] = [ dct[key], value ]
    else:
        dct[key] = value
    
    return kvlm_parse(raw, start = end+1, dct = dct)



def kvlm_serialize(kvlm):
    ret = b''

    # output fields
    for key in kvlm.keys():
        # skip the message itself
        if key == b'':
            continue
        
        val = kvlm[key]
        # normalize this value to a list

        if type(val) != list:
            val = [ val ]
        
        for v in val:
            ret += k + b' ' + (value.replace(b'\n', b'\n ')) + b'\n'
        
    ret += b'\n' + kvlm[b'']

    return ret

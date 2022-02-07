from gitInit import repo_dir, repo_file

import os
import collections

def ref_resolve(repo , ref):
    with open(repo_file(repo ,ref), 'r') as f:
        data = f.read()[:-1]
        # Drop the final "\n" using the [:-1] slice

    if data.startswith("ref: "):
        return ref_resolve(repo, data[5:])
    else:
        return data


def ref_list(repo, path = None):
    if not path:
        path = repo_dir(repo, "refs")

    ret = collections.OrderedDict()
    # Git shows refs sorted.  To do the same, we use
    # an OrderedDict and sort the output of listdir

    for f in sorted(os.listdir(path)):
        can = os.path.join(path, f)

        if os.path.isdir(can):
            ret[f] = ref_list(repo, can)
        else:
            ret[f] = ref_resolve(repo, can)

    return ret


def 
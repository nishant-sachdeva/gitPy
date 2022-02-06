from gitCommit import log_graphviz
from gitObjectUtils import object_read, object_find
from gitInit import repo_find

def log_graphviz(repo, sha, seen):
    if sha in seen:
        return
    seen.add(sha)
    
    commit = object_read(repo, sha)
    assert (commit.fmt = b'commit')

    if not b'parent' in commit.kvlm.keys():
        "BASE CASE :: INITIAL COMMIT"
        return

    parents = commit.kvlm[b'parent']

    if type(parents) != list:
        parents = [parents]
    
    for p in parents:
        p = p.decode('ascii')
        print("c_{0} -> c_{1};".format(sha, p))
        log_graphviz(repo, p, seen)

def cmd_log(args):
    repo = repo_find()
    print("DiGraph WyagLOG {")
    log_graphviz(repo, object_find(repo, args.commit), set())
    print("}")
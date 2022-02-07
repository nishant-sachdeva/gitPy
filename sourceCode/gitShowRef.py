def cmd_show-ref(args):
    repo = repo_find()
    refs = ref_list(repo)
    show_ref(repo, refs, prefix="refs")

def show_ref(repo, refs, with_hash=True, prefix=""):
    for k, v in refs.items():
        if type(v) == str:
            print("{0}{1}{2}".format(
                v + " " if with_hash else "", 
                prefix + "/" if prefix else "",
                k
            ))
        else:
            show_ref(repo, v, with_hash=with_hash, prefix="{0}{1}{2}".format(
                prefix,
                "/" if prefix else "",
                k
            ))
    
def cmd_ls-tree(args):
    repo = repo_find()
    object = object_read(repo, object_find(repo, args.object, fmt = b'tree'))

    for item in object.items:
        print("{0} {1} {2}\t{3}".format(
            "0" * (6 - len(item.mode)) + item.mode.decode("ascii"),
            # Git's ls-tree displays the type
            # of the object pointed to.  We can do that too :)
            object_read(repo, item.sha).fmt.decode("ascii"),
            item.sha,
            item.path.decode("ascii"))
        )
        
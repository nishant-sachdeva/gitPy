def cmd_tag(args):
    repo = repo_find()

    if args.name:
        tag_create(args.name, args.object, type = "object" if args.create_object else "ref")
    else:
        refs = ref_list(repo)
        show_ref(repo, refs["tags"], with_hash = False)


class gitRepository(object):
    ''' A git repository'''

    worktree = None
    gitdir = None
    conf = None

    def __init__(self, path, force=False):
        self.worktree = path
        self.gitdir = os.path.join(path, '.git')

        if not (force or os.path.isdir(self.gitdir)):
            raise Exception('Not a Git Repository %s' % path)
        
        # Read config file in .git/config
        self.conf = configparser.ConfigParser()
        cf = repo_file(self, 'config')
        
        if cf and os.path.exists(cf):
            self.conf.read([cf])
        elif not cf:
            raise Exception('Config file not found')
        
        if not force:
            vers = int(self.conf.get("core", "repositoryformatversion"))
            if vers != 0:
                raise Exception("Unsupported repositoryformatversion %s" % vers)


def cmd_init(args):
    if args.path:
        print("Creating Git Repository at " + args.path)
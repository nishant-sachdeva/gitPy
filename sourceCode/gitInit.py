import configparser
import os
import sys

def repo_find(path = ".", required = True):
    path = os.path.realpath(path)

    if os.path.isdir(os.path.join(path, ".git")):
        return gitRepository(path)

    parent = os.path.realpath(os.path.join(path, ".."))
    if parent == path:
        if required:
            raise Exception("No git repository found")
        else:
            return None

    # Recursive case
    return repo_find(parent, required)


def repo_path(repo, *path):
    ''' compute path under repo's gitdir '''
    return os.path.join(repo.gitdir, *path)

def repo_dir(repo, *path, mkdir=False):
    '''Same as repo_path, but mkdir *path if absent if mkdir.'''
    
    path = repo_path(repo, *path)

    if os.path.exists(path):
        if(os.path.isdir(path)):
            return path
        else:
            raise Exception("Not a directory %s" % path)
    
    if mkdir:
        os.makedirs(path)
        return path
    else:
        return None

def repo_file(repo, *path, mkdir=False):
    ''' same as repo_path but creates a dirname(path) if absent.
    For example , repo_file(r,  \"refs\", \"remotes\", \"origin\", \"HEAD\") will create
    .git/refs/remotes/origin.'''

    if repo_dir(repo, *path[:-1], mkdir=mkdir):
        return repo_path(repo, *path)

def repo_default_config():
    ret = configparser.ConfigParser()

    ret.add_section("core")
    ret.set("core", "repositoryformatversion", "0")
    ret.set("core", "filemode", "false")
    ret.set("core", "bare", "false")

    return ret

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
        configFile = repo_file(self, 'config')
        
        if configFile and os.path.exists(configFile):
            self.conf.read([configFile])
        elif not force:
            raise Exception('Config file not found')
        
        if not force:
            vers = int(self.conf.get("core", "repositoryformatversion"))
            if vers != 0:
                raise Exception("Unsupported repositoryformatversion %s" % vers)


def repo_create(path):
    ''' Creating a new git repository at path '''

    repo = gitRepository(path, True)

    # First , we shall make sure that the path either doesn't exist
    # or is an empty directory.

    if os.path.exists(repo.worktree):
        if not os.path.isdir(repo.worktree):
            raise Exception("%s is not a directory" % path)
        if os.listdir(repo.worktree):
            raise Exception("%s is not empty!" % path)
    else:
        os.makedirs(repo.worktree)
    
    assert(repo_dir(repo, "branches", mkdir=True))
    assert(repo_dir(repo, "objects", mkdir=True))
    assert(repo_dir(repo, "refs", "tags", mkdir=True))
    assert(repo_dir(repo, "regs", "heads", mkdir=True))

    # .git/description
    with open(repo_file(repo, "description"), "w") as f:
        f.write("ref: refs/heads/master\n")
    
    with open(repo_file(repo, "config"), "w") as f:
        config = repo_default_config()
        config.write(f)
    
    return repo


def cmd_init(args):
    if args.path:
        print("Creating Git Repository at " + args.path)
    try:
        repo_create(args.path)
    except Exception as e:
        print(e)
        print("Failed to create repository at " + args.path)
        sys.exit(1)
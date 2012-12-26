## Dotfiles

My dotfiles for quick configuration new/clean system (it is OSX specific but I think it could work on linux).
Work in progress. I need to create logical structure for my aliases and seperate 
theme from bash-it (cause it was only thing I was using from bash-it).

Also I have plans to add ``` --move ``` for my sublime settings

## Usage of setup.py:

To install anything from ``` ./install/manifests.py ``` just use:

```
python setup.py --install all
```

To create symlinks to everything from ``` ./symlinks/ ``` to ``` ~/.$FILE ``` just use:

```
python setup.py --symlink all
```

Additionally you can add another "secret dir" with symlinks or manifests to install
(usefull for .ssh keys and "secret" aliases to servers or secret company tools to install):

**``` --directories ``` directive must be before ``` --symlink``` or ``` --install ```**

```
python setup.py --directories ~/Dropbox/system/dotfiles/ --symlink all
```

or install

```
python setup.py --directories ~/Dropbox/system/dotfiles/ --install all
```

It should work with many additional directories:

```
python setup.py --directories ~/Dropbox/system/dotfiles/ ~/very_secret_directory/ --symlink all
python setup.py --directories ~/Dropbox/system/dotfiles/ ~/very_secret_directory/ --install all
```

## Creating manifests:

### Simple:

```
manifests.append({
    'name' : 'brew',
    'install' : 'ruby -e "$(curl -fsSkL raw.github.com/mxcl/homebrew/go)"',
})
```

### Check:

By default setup is searching for brew in all paths defined in system.
But if You want to check for a file or something library specific you can add ``` check ``` parameter:

```
manifests=[]
manifests.append({
    'name' : 'configobj',
    'check' : '/Library/Python/2.7/site-packages/configobj.py',
    'install' : 'sudo pip install configobj',
})
```

``` check ``` can be path or just different name

### Force
Force parameter ignores checking if the file/command/program exist and it tries to install again.
Can be usefull with upgrades like ``` pip install configobj --upgrade ```:

```
manifests=[]
manifests.append({
    'name' : 'configobj',
    'force' : True,
    'install' : 'sudo pip install configobj --upgrade',
})
```
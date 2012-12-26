# -*- coding: utf-8 -*-
#!/usr/bin/env python

#pylint: disable=C0103, W0702
"""
Example manifest:

manifests.append({
    'name' : 'configobj',
    'check' : '/Library/Python/2.7/site-packages/configobj.py',
    'force' : True,
    'install' : 'sudo pip install configobj',
})
"""

manifests = []

manifests.append({
    'name' : 'brew',
    'install' : 'ruby -e "$(curl -fsSkL raw.github.com/mxcl/homebrew/go)"',
})

manifests.append({
    'name' : 'configobj',
    'check' : '/Library/Python/2.7/site-packages/configobj.py',
    'install' : 'sudo pip install configobj',
})

manifests.append({
    'name' : 'bash',
    'install' : 'brew install bash',
})

manifests.append({
    'name' : 'bash-completion',
    'check' : '/usr/local/etc/bash_completion',
    'install' : 'brew install bash-completion',
})

manifests.append({
    'name' : 'git',
    'install' : 'brew install git',
})

manifests.append({
    'name' : 'htop',
    'install' : 'brew install htop-osx',
})
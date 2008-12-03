#!/usr/bin/env python
"""
1. Parses repo_list.txt
2. Downloads source code to the `src` folder
3. Adds source to `ve` virtualenv PYTHONPATH

"""


import commands

f = open("repo_list.txt")
stat, cwd = commands.getstatusoutput('pwd')


for line in f.readlines():
    
    #ignore comments
    if line.startswith('#'):
        continue
        
    name, url, vcs, version = line.split()
    
    #SUBVERSION/GIT
    if vcs == 'svn' or vcs == 'git':
        #if setup.py isn't available use pipe delimiter to determine source directory and python module 
        #names for symlinking
        try:
            src_dir, py_module = name.split('|')
            ln_cmd = "cd %s/ve/lib/python2.5/site-packages; ln -s ../../../../src/%s/%s ." % (cwd, src_dir, py_module)
        except ValueError:
            src_dir = name
            ln_cmd = 'cd %s; %s/ve/bin/python setup.py install' % (src_dir, cwd)
        #TODO handle version/head logic
        if vcs == 'svn':
            co_cmd = "svn co -r %s %s %s" % (version, url, src_dir)
        else: #vcs == git
            co_cmd = "git clone %s" % url
            #TODO handle branching
        cmd = '%s; %s' % (co_cmd, ln_cmd)
        
    #SINGLE FILE DOWNLOAD
    elif vcs == 'wget':
        co_cmd = "wget %s" % url
        ln_cmd = "cd %s/ve/lib/python2.5/site-packages; ln -s ../../../../src/%s ." % (cwd, name)
        cmd = '%s; %s' % (co_cmd, ln_cmd)
    
    #CHEESESHOP
    elif vcs == 'pypi':
        cmd = "easy_install %s==%s" % (name, version)
    else:
        raise Exception, "Can't handle %s" % vcs
    print cmd
    
    #move to `src` directory and run command(s)
    stat, output = commands.getstatusoutput('(cd src; %s)' % cmd)
    if stat:
        raise Exception, '`%s` failed: %s' % (cmd, output)
    else:
        pass #print output
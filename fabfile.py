import os
import sys
        
class VersionControl(object):
    """Generates command strings for VCS tasks"""
    def __init__(self, *args, **kwargs):
        for k,v in kwargs.items():
            setattr(self, k, v)
        self.cmd = '%s ' % self.dist
        
class Subversion(VersionControl):
    def checkout(self):
        cmd = self.cmd
        if hasattr(self, 'rev'):
            cmd += '-r %s ' % self.rev
        cmd += 'co %s ./src/%s' % (self.url, self.name)
        return cmd

class Git(VersionControl):
    def clone(self):
        cmd = '%s clone %s ./src/%s' % (self.cmd, self.url, self.name)
        if hasattr(self, 'branch'):
            cmd += '\\\n&& (cd ./src/%s; git checkout --track -b %s origin/%s)' % (self.name, self.branch, self.branch) 
        return cmd
        

def install_module(src_dir, module_name='', dist_utils=False):
    """
    Installs a Python module from the ./src directory either using
    distutils or by symlinking the package to site-packages

    """

    #setup using distutils
    if dist_utils:
        cmd = '(cd src/%s;\\\n../../ve/bin/python setup.py install)' % src_dir
    #symlink to site-packages
    else:
        src_path = os.path.join(src_dir,module_name).rstrip('/')
        cmd = '(cd ve/lib/python2.5/site-packages;\\\nln -s ../../../../src/%s .)' % (src_path)
    return cmd
        

def bootstrap():
    """
    1. Creates a new virtualenv
    2. Downloads all sources from fabreqs.py, adding them 
       to the PYTHONPATH along the way
    
    """
    #put the cwd on the python path so we can use fabreqs.py
    sys.path.append('.') 
    from fabreqs import requirements
    local('virtualenv ve')
    #hack activate so it uses project directory instead of ve in prompt
    local('sed \'s/(`basename \\\\"\\$VIRTUAL_ENV\\\\\"`)/(`basename \\\\`dirname \\\\"$VIRTUAL_ENV\\\\"\\\\``)/g\' ve/bin/activate > ve/bin/activate.tmp')
    #sed 's/(`basename \\"\$VIRTUAL_ENV\\\"`)/(`basename \\`dirname \\"$VIRTUAL_ENV\\"\\``)/g'
    local('mv ve/bin/activate.tmp ve/bin/activate')
    local('mkdir src')
    for pkg in requirements:
        #easy_install package from PyPi
        if pkg['dist'] == 'pypi':
            cmd = './ve/bin/easy_install -a %s' % pkg['name']
            if pkg.has_key('rev'):
                cmd += '==%s' % pkg['rev']
            local(cmd)
            
        #download single file
        elif pkg['dist'] == 'wget':
            local('cd src && wget %s' % pkg['url'])
            local(install_module(pkg['name']))
        
        else: #it's a vcs
            if pkg['dist'] == 'svn':
                local(Subversion(**pkg).checkout())
            elif pkg['dist'] == 'git':
                local(Git(**pkg).clone())
            else:
                raise Exception, '%s is not a recognized distribution method' % pkg['dist']
            #if a package name isn't specified, assume dist_utils
            if pkg.has_key('package'):
                if isinstance(pkg['package'], list):
                    for package in pkg['package']:
                        local(install_module(pkg['name'], package))
                else:
                    local(install_module(pkg['name'], pkg['package']))
            else:
                local(install_module(pkg['name'], dist_utils=True))
                

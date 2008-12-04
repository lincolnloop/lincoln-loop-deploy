import os
import sys
        
class Subversion(object):
    """
    Generates subversion command strings

    """

    def __init__(self, *args, **kwargs):
        for k,v in kwargs.items():
            setattr(self, k, v)
    def checkout(self):
        cmd = 'svn '
        if hasattr(self,'rev'):
            cmd += '-r %s ' % self.rev
        cmd += 'co %s ./src/%s' % (self.url, self.name)
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
        src_path = os.path.join(src_dir,module_name)
        cmd = '(cd ve/lib/python2.5/site-packages;\\\nln -s ../../../../src/%s .)' % (src_path)
    return cmd
        

def bootstrap():
    """
    1. Creates a new virtualenv
    2. Downloads all sources from fabreqs.py,
       Adding them to the PYTHONPATH
    
    """
    #put the cwd on the path so we can use fabreqs.py
    sys.path.append('.') 
    from fabreqs import requirements
    local('virtualenv ve')
    #hack activate so it uses project directory instead of ve in prompt
    local('sed \'s/(`basename \\\\"\\$VIRTUAL_ENV\\\\\"`)/(`basename \\\\`dirname \\\\"$VIRTUAL_ENV\\\\"\\\\``)/g\' ve/bin/activate > ve/bin/activate.tmp')
    #sed 's/(`basename \\"\$VIRTUAL_ENV\\\"`)/(`basename \\`dirname \\"$VIRTUAL_ENV\\"\\``)/g'
    local('mv ve/bin/activate.tmp ve/bin/activate')
    local('mkdir src')
    for pkg in requirements:
        if pkg['dist'] == 'svn':
            local(Subversion(**pkg).checkout())
            #if a package name isn't specified, assume dist_utils
            if pkg.has_key('package'):
                local(install_module(pkg['name'], pkg['package']))
            else:
                local(install_module(pkg['name'], dist_utils=True))
        elif pkg['dist'] == 'pypi':
            cmd = './ve/bin/easy_install -a %s' % pkg['name']
            if pkg.has_key('rev'):
                cmd += '==%s' % pkg['rev']
            local(cmd)

                

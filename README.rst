Requirements
============

- virtualenv_
- Fabric_

::

  easy_install Fabric virtualenv
    
.. _virtualenv: http://pypi.python.org/pypi/virtualenv
.. _Fabric: http://www.nongnu.org/fab/

Quick-start
===========

Create a folder that will serve as the home for your project source code and virtual environment. Drop ``fabfile.py`` and ``fabreqs.py`` into the directory and run:

::

    fab bootstrap
    
This will create two new folders in the directory ``src``, containing all the downloaded source code, and ``ve``, which is a virtualenv that can be activated with ``source ve/bin/activate``.

Usage
=====

``fabreqs.py`` is a simple Python file that should contain all the dependencies for your project. ``requirements`` is a list of Python dictionaries defining the external dependencies. Valid keys are:

- ``name``: Used for naming the source folder (required)
- ``dist``: Distribution method for the package, valid options are  ``bzr``, ``git``, ``hg``, ``pypi``, ``svn``, ``wget`` (required)
- ``package``: The Python package assumed to be inside the source folder. If not provided, the use of distutils (``python setup.py install``) is assumed (optional)
- ``url``: URL to source (optional)
- ``rev``: Revision to download. If not defined, the most recent available version will be used. (optional)
- ``branch``: Branch to use, git and hg only. (optional)

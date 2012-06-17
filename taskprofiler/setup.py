#coding:utf-8

'''
Created on 2012/06/17

@author: Noboru
'''

import py2exe #@UnresolvedImport
from distutils.core import setup

AUTHOR = "HORITA Noboru"
INCLUDES = ["sip", "ctypes"]

PY2EXE_OPTIONS = {"includes":INCLUDES}
setup(console = ["UI.py"],
      author = AUTHOR,
      options = {"py2exe":PY2EXE_OPTIONS})
#!/usr/bin/python
# -*- coding: utf-8 -*-

#  _   _       _ _                     _
# | | | | ___ | | |__  _ __ ___   ___ | | __
# | |_| |/ _ \| | '_ \| '__/ _ \ / _ \| |/ /
# |  _  | (_) | | |_) | | | (_) | (_) |   <
# |_| |_|\___/|_|_.__/|_|  \___/ \___/|_|\_\
# wanghaikuo@gmail.com

from optparse import OptionParser

import os

def list_repositories(options, args):
    parser = OptionParser()
    repo_list= []
    list_dirs = os.walk(repo_root)
    for root, dirs, files in list_dirs:
        for d in dirs:
            print d


#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @tankywoo

"""
# Add a task
>> t task
# Edit a task
>> t -e task
# Finish a task
>> t -f task
# Remove a task
>> t -r task
# Move a task
>> t --mv taskbox1 taskbox2 TODO


-------

Task Example:
taskid  task    [priority]  [date]

# Maybe the taskid can use timestamp

"""
import sys
try:
    import argparse
except ImportError, e:
    print "argparse module missing: Please run 'sudo easy_install argparse'"
    sys.exit(1)
    # Python Version >= 2.7
    # import optparse as argparse


def get_args():
    pass

if __name__ == '__main__':
    pass

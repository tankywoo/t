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
    # TODO:import optparse as argparse


class TaskT():
    pass


def get_args():
    usage = '%(prog)s [options] [TEXT]'
    #parser = argparse.ArgumentParser(description='Command-line todo - t Help')
    parser = argparse.ArgumentParser(description='Command-line todo - t Help',
            usage = usage)

    action_group = parser.add_argument_group('Action')
    action_group.add_argument('add', default=[], nargs='*', help='Add a task')
    action_group.add_argument('-e', '--edit', dest='edit', default='', help='Edit a task')
    action_group.add_argument('-f', '--finish', dest='finish', help='Finish a task')
    action_group.add_argument('-r', '--remove', dest='remove', help='Remove a task')

    output_group = parser.add_argument_group('Output')
    output_group.add_argument('-g', '--grep', help='Grep the keyword in task box')
    output_group.add_argument('--done', help='List all the done tasks')

    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = get_args()

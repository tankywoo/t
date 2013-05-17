#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @tankywoo

# TODO:
# mv task between two task file
# support optparse

"""
# Move a task
>> t --mv taskbox1 taskbox2 TODO
-------
Task Example:
taskid  task    [priority]  [date]
"""

import os
import sys
import datetime
import hashlib
try:
    import argparse
except ImportError, e:
    print "argparse module missing: Please run 'sudo easy_install argparse'"
    sys.exit(1)
    # Python Version >= 2.7
    # import optparse as argparse
from pprint import pprint


class TaskT():

    def __init__(self, task_dir='.', task_fname='tasks'):
        self.tasks = {}
        self.done_tasks = {}
        self.task_dir = task_dir
        self.task_fname = task_fname
        filemap = (('tasks', self.task_fname), \
                ('done_tasks', '.%s.done' % self.task_fname))
        if not os.path.exists(self.task_dir):
            os.mkdir(self.task_dir)
        for kind, fname in filemap:
            path = os.path.join(os.path.expanduser(self.task_dir), fname)
            if os.path.exists(path):
                with  open(path, 'r') as fd:
                    for task in fd.readlines():
                        t_id, t_date, t_text = \
                                [t.strip() for t in task.split('|')]
                        # TODO:getattr no error?
                        #getattr(self, kind)[t_id.strip()] = \
                        #       '%s | %s' % (t_text.strip(), t_date. strip())

                        t = getattr(self, kind)[t_id] = {}
                        t['text'] = t_text
                        t['date'] = t_date

    @staticmethod
    def __hash(text):
        return str(hashlib.sha1(text).hexdigest())

    # Main Operation
    def add_task(self, task_text):
        task_id = self.__hash(task_text)
        date = str(datetime.date.today())
        task = {}
        task['text'] = task_text
        task['date'] = date
        self.tasks[task_id] = task

    def edit_task(self, task_id, task_text):
        date = str(datetime.date.today())
        if task_id not in self.tasks:
            raise Exception, 'task id is not in exist'
        task = self.tasks[task_id]
        task['date'] = date
        task['text'] = task_text
        self.tasks[task_id] = task

    def finish_task(self, task_id):
        if task_id not in self.tasks:
            raise Exception, 'task id is not in exist'
        task = self.tasks.pop(task_id)
        self.done_tasks[task_id] = task

    def remove_task(self, task_id):
        if task_id not in self.tasks:
            raise Exception, 'task id is not in exist'
        self.tasks.pop(task_id)

    def undo_task(self, task_id):
        # TODO check exist
        task = self.done_tasks.pop(task_id)
        self.tasks[task_id] = task

    def output_task(self, kind='tasks'):
        tasks = getattr(self, kind).items()
        for t_id, task in tasks:
            print '%s | %s | %s' % (t_id, task['date'], task['text'])

    def write_task(self):
        filemap = (('tasks', self.task_fname), \
                ('done_tasks', '.%s.done' % self.task_fname))
        for kind, fname in filemap:
            path = os.path.join(os.path.expanduser(self.task_dir), fname)

            with open(path, 'w') as fd:
                tasks = getattr(self, kind).items()
                for t_id, task in tasks:
                    t =  '%s | %s | %s\n' % (t_id, task['date'], task['text'])
                    fd.write(t)


def get_args():
    usage = '%(prog)s [options] [TEXT]'
    parser = argparse.ArgumentParser(description='Command-line todo - t Help',
            usage = usage)

    # ArgumentParser.add_mutually_exclusive_group()
    action_group = parser.add_argument_group('Action')
    action_group.add_argument('add', default=[], nargs='*', 
            help='Add a task')
    action_group.add_argument('-e', '--edit', dest='edit', nargs='+', 
            help='Edit a task')
    action_group.add_argument('-f', '--finish', dest='finish', 
            help='Finish a task')
    action_group.add_argument('-r', '--remove', dest='remove', 
            help='Remove a task')
    action_group.add_argument('--undo', dest='undo', help='Undo a task')
    #action_group.add_argument('--mv', dest='move', 
    #       help='Move a task to another task file')

    output_group = parser.add_argument_group('Output')
    output_group.add_argument('--done', dest='done', action='store_true', 
            help='List all the done tasks')
    #output_group.add_argument('-g', '--grep', 
    #       help='Grep the keyword in task box')

    config_group = parser.add_argument_group('Config')
    config_group.add_argument('--task-dir', dest='task_dir',
            help='Set the task directory(default is .)')
    config_group.add_argument('--list', dest='task_list',
            help='Set the task list(default is tasks)')

    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = get_args()
    tt = TaskT(task_dir=args.task_dir, task_fname=args.task_list)

    try:
        if args.finish:
            tt.finish_task(args.finish)
            tt.write_task()
        elif args.remove:
            tt.remove_task(args.remove)
            tt.write_task()
        elif args.edit:
            t_id = args.edit[0]
            t_text = ' '.join(args.edit[1:])
            tt.edit_task(t_id, t_text)
            tt.write_task()
        elif args.add:
            task = ' '.join(args.add).strip()
            tt.add_task(task)
            tt.write_task()
        else:
            kind = 'tasks' if not args.done else 'done_tasks'
            tt.output_task(kind=kind)
    except Exception ,e:
        print ">> ERROR:", str(e)
        sys.exit(1)

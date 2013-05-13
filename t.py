#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @tankywoo

# TODO:
# support optparse
# mv task between two task file

"""
# Move a task
>> t --mv taskbox1 taskbox2 TODO

-------

Task Example:
taskid  task    [priority]  [date]

# Maybe the taskid can use timestamp

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
        filemap = (('tasks', self.task_fname), ('done_tasks', '.%s.done' % self.task_fname))
        for kind, fname in filemap:
            path = os.path.join(os.path.expanduser(self.task_dir), fname)
            if os.path.exists(path):
                # TODO:with
                fd = open(path, 'r')
                for task in fd.readlines():
                    t_id, t_content, t_date = task.split('|')
                    # TODO:getattr no error?
                    getattr(self, kind)[t_id.strip()] = '%s | %s' % (t_content.strip(), t_date. strip())
                fd.close()

    def add_task(self, task):
        task_id = 'id:%s' % str(hashlib.sha1(task).hexdigest())
        date = str(datetime.date.today())
        task = "%s | %s" % (date, task)
        self.tasks[task_id] = task

    def edit_task(self, task_id, task_content):
        date = str(datetime.date.today())
        task_content = "%s | %s" % (date, task_content)
        self.tasks[task_id] = task_content

    def finish_task(self, task_id):
        # TODO: No Task
        task = self.tasks.pop(task_id)
        self.done_tasks[task_id.strip()] = task.strip()

    def remove_task(self, task_id):
        self.tasks.pop(task_id)

    def undo_task(self, task_id):
        task = self.done_tasks.pop(task_id)
        self.tasks[task_id] = task

    def output_task(self, kind='tasks'):
        tasks = getattr(self, kind).items()
        for t_id, task in tasks:
            print '%s | %s' % (t_id.strip(), task.strip())

    def write_task(self):
        filemap = (('tasks', self.task_fname), ('done_tasks', '.%s.done' % self.task_fname))
        for kind, fname in filemap:
            path = os.path.join(os.path.expanduser(self.task_dir), fname)

            # TODO:with
            fd = open(path, 'w')
            tasks = getattr(self, kind).items()
            print tasks
            for t_id, task in tasks:
                t_date, t_content = task.split('|')
                t = "%s | %s | %s\n" % (t_id.strip(), t_date.strip(), t_content.strip())
                fd.write(t)
            fd.close()


def get_args():
    usage = '%(prog)s [options] [TEXT]'
    parser = argparse.ArgumentParser(description='Command-line todo - t Help',
            usage = usage)

    action_group = parser.add_argument_group('Action')
    action_group.add_argument('add', default=[], nargs='*', help='Add a task')
    action_group.add_argument('-e', '--edit', dest='edit', nargs='+', help='Edit a task')
    action_group.add_argument('-f', '--finish', dest='finish', help='Finish a task')
    action_group.add_argument('-r', '--remove', dest='remove', help='Remove a task')
    action_group.add_argument('--undo', dest='undo', help='Undo a task')
    #action_group.add_argument('--mv', dest='move', help='Move a task to another task file')

    output_group = parser.add_argument_group('Output')
    output_group.add_argument('--done', dest='done', action='store_true', help='List all the done tasks')
    #output_group.add_argument('-g', '--grep', help='Grep the keyword in task box')

    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = get_args()
    tt = TaskT()

    try:
        if args.finish:
            tt.finish_task(args.finish)
            tt.write_task()
        elif args.remove:
            tt.remove_task(args.remove)
            tt.write_task()
        elif args.edit:
            t_id = args.edit[0]
            t_content = ' '.join(args.edit[1:])
            tt.edit_task(t_id, t_content)
            tt.write_task()
        elif args.add:
            task = ' '.join(args.add).strip()
            tt.add_task(task)
            tt.write_task()
        else:
            kind = 'tasks' if not args.done else 'done_tasks'
            tt.output_task(kind=kind)
    except:
        print '>> ERROR'

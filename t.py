#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @tankywoo

# TODO:
# mv task between two task file
# support optparse

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

def _prefixes(ids):
    """Return a mapping of ids to prefixes in O(n) time.

    Each prefix will be the shortest possible substring of the ID that
    can uniquely identify it among the given group of IDs.

    If an ID of one task is entirely a substring of another task's ID, the
    entire ID will be the prefix.
    """
    # https://github.com/sjl/t/blob/master/t.py
    ps = {}
    for id in ids:
        id_len = len(id)
        for i in range(1, id_len+1):
            # identifies an empty prefix slot, or a singular collision
            prefix = id[:i]
            if (not prefix in ps) or (ps[prefix] and prefix != ps[prefix]):
                break
        if prefix in ps:
            # if there is a collision
            other_id = ps[prefix]
            for j in range(i, id_len+1):
                if other_id[:j] == id[:j]:
                    ps[id[:j]] = ''
                else:
                    ps[other_id[:j]] = other_id
                    ps[id[:j]] = id
                    break
            else:
                ps[other_id[:id_len+1]] = other_id
                ps[id] = id
        else:
            # no collision, can safely add
            ps[prefix] = id
    ps = dict(zip(ps.values(), ps.keys()))
    if '' in ps:
        del ps['']
    return ps

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
                        t = getattr(self, kind)[t_id] = {}
                        t['text'] = t_text
                        t['date'] = t_date

    @staticmethod
    def __hash(text):
        return str(hashlib.sha1(text).hexdigest())

    @staticmethod
    def __output_cmp(x, y):
        if x[1]['date'] > y[1]['date']:     return 1
        elif x[1]['date'] < y[1]['date']:   return -1
        else:
            if x[0] > y[0]:     return -1
            elif x[0] < y[0]:   return 1
            else:               return 0

    def __get_id(self, prefix, kind='tasks'):
        """
            kind in ('tasks', 'done_tasks')
        """
        ids = getattr(self, kind).keys()
        for _id in ids:
            if _id.startswith(prefix):
                return _id
        return None

    # Main Operation
    def add_task(self, task_text):
        task_id = self.__hash(task_text)
        date = datetime.date.today().isoformat()
        task = {}
        task['text'] = task_text
        task['date'] = date
        self.tasks[task_id] = task

    def edit_task(self, task_id, task_text):
        date = datetime.date.today().isoformat()
        task_id = self.__get_id(task_id)
        if not task_id:
            raise Exception, 'task id is not in exist'
        task = self.tasks[task_id]
        task['date'] = date
        task['text'] = task_text
        self.tasks[task_id] = task

    def finish_task(self, task_id):
        task_id = self.__get_id(task_id)
        if not task_id:
            raise Exception, 'task id is not in exist'
        task = self.tasks.pop(task_id)
        self.done_tasks[task_id] = task

    def remove_task(self, task_id):
        task_id = self.__get_id(task_id)
        if not task_id:
            raise Exception, 'task id is not in exist'
        self.tasks.pop(task_id)

    def undo_task(self, task_id):
        task_id = self.__get_id(task_id, 'done_tasks')
        if not task_id:
            raise Exception, 'task id is not in done tasks'
        task = self.done_tasks.pop(task_id)
        self.tasks[task_id] = task

    def output_task(self, kind='tasks'):
        tasks = getattr(self, kind).items()
        # Sort the output by date and id
        tasks = sorted(tasks, cmp=self.__output_cmp, reverse=True)
        ids = _prefixes(getattr(self, kind).keys())
        if tasks:
            maxlen = max(map(len, ids.values()))
            for t_id, task in tasks:
                print '%s | %s | %s' % \
                        (ids[t_id].ljust(maxlen), 
                                task['date'].split('-', 1)[1], task['text'])

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
    action_group.add_argument('--undo', dest='undo', 
            help='Undo a task')

    output_group = parser.add_argument_group('Output')
    output_group.add_argument('--done', dest='done', action='store_true', 
            help='List all the done tasks')

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
        elif args.undo:
            tt.undo_task(args.undo)
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

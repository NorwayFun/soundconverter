#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# SoundConverter - GNOME application for converting between audio formats.
# Copyright 2004 Lars Wirzenius
# Copyright 2005-2017 Gautier Portet
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; version 3 of the License.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307
# USA

import time
from soundconverter.task import BackgroundTask
from soundconverter.settings import settings
from soundconverter.utils import log


class TaskQueue(BackgroundTask):
    """ A queue of tasks.

    A task queue is a queue of other tasks. If you need, for example, to
    do simple tasks A, B, and C, you can create a TaskQueue and add the
    simple tasks to it:

        q = TaskQueue()
        q.add_task(A)
        q.add_task(B)
        q.add_task(C)
        q.start()

    The task queue behaves as a single task. It will execute the
    tasks in order and start the next one when the previous finishes. """

    def __init__(self):
        BackgroundTask.__init__(self)
        self.waiting_tasks = []
        self.running_tasks = []
        self.finished_tasks = 0
        self.start_time = None
        self.count = 0
        self.paused = False
        self.jobs = settings['forced-jobs'] or settings['jobs']
        self.jobs = self.jobs or settings['cpu-count']

    def add_task(self, task):
        """ Add a task to the queue. """
        self.waiting_tasks.append(task)
        # if self.start_time and not self.running_tasks:
        if self.start_time:
            # add a task to a stalled taskqueue, shake it!
            self.start_next_task()

    def start_next_task(self):
        if len(self.waiting_tasks) == 0:
            if len(self.running_tasks) == 0:
                self.done()
            return

        to_start = self.jobs - len(self.running_tasks)
        for _ in range(to_start):
            try:
                task = self.waiting_tasks.pop(0)
            except IndexError:
                return
            self.running_tasks.append(task)
            task.add_listener('finished', self.task_finished)
            task.start()
            if self.paused:
                task.toggle_pause(True)
            self.count += 1
        total = len(self.waiting_tasks) + self.finished_tasks
        self.progress = float(self.finished_tasks) / total if total else 0

    def started(self):
        """ BackgroundTask setup callback """
        log('Queue start: %d tasks, %d thread(s).' % (
            len(self.waiting_tasks) + len(self.running_tasks), self.jobs))
        self.count = 0
        self.paused = False
        self.finished_tasks = 0
        self.start_time = time.time()
        self.start_next_task()

    def finished(self):
        """ BackgroundTask finish callback """
        log('Queue done in %.3fs (%s tasks)' % (time.time() - self.start_time, self.count))
        self.queue_ended()
        self.count = 0
        self.start_time = None
        self.running_tasks = []
        self.waiting_tasks = []
        self.running = False

    def task_finished(self, task=None):
        if not self.running_tasks:
            return
        if task in self.running_tasks:
            self.running_tasks.remove(task)
        self.finished_tasks += 1
        self.start_next_task()

    def abort(self):
        for task in self.running_tasks:
            task.abort()
        BackgroundTask.abort(self)
        self.running_tasks = []
        self.waiting_tasks = []
        self.running = False
        self.start_time = None

    def toggle_pause(self, paused):
        self.paused = paused
        for task in self.running_tasks:
            task.toggle_pause(self.paused)

    # The following is called when the Queue is finished
    def queue_ended(self):
        pass

    # The following when progress changed
    def progress_hook(self, progress):
        pass

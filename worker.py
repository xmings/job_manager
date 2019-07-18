#!/bin/python
# -*- coding: utf-8 -*-
# @File  : worker.py
# @Author: wangms
# @Date  : 2019/6/20
# @Brief: 简述报表功能
import subprocess
from multiprocessing import Process
from __init__ import SUCCESS, FAILED, logger

class Worker(object):
    def __init__(self, task):
        self.task = task

    def run(self, state_queue):
        try:
            completed = subprocess.run(self.task.script, shell=True, encoding="utf8",
                                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            logger.info("worker result: {}; {}".format(completed.stdout, completed.stderr))
            if completed.returncode != 0:
                raise Exception(completed.stderr)
            self.task.exec_result = completed.stdout
            self.task.change_status(SUCCESS)
        except Exception as e:
            self.task.exec_result = e
            self.task.change_status(FAILED)

        state_queue.put(self.task)



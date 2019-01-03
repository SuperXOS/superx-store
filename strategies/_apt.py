#!/usr/bin/python3
# example how to deal with the depcache

from itertools import zip_longest
from aptdaemon import client

class AptInterface():

    def __init__(self):
        self.aptd = client.AptClient()
        self.transactions = []
        self.transactions_list = []
        self._progress = None
        self.transactions_running = False

    def QueueTransaction(self, appSummery, action):
        transaction = None
        if action == 'install':
            transaction = self.aptd.install_packages(appSummery['pkg'])
        elif action == 'remove':
            transaction = self.aptd.remove_packages(appSummery['pkg'])
        self.transactions.append(transaction)
        self.transactions_list.append(appSummery)

    def TransProgress(self, trans, progress):
        self._progress = progress

    def TransFinished(self, exit_status):
        self.transactions_running = False

    def ProcessTransactions(self):
        for i in self.transactions:
            i.connect('progress-changed', self.TransProgress)
            i.connect('finished', lambda: self.transactions_list.pop(0))
            self.transactions_running = True
            i.run()


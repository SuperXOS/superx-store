#!/usr/bin/python3
# example how to deal with the depcache

from aptdaemon import client
from PyQt5.QtCore import QObject, pyqtSignal

class QAptInterface(QObject):

    aptProgressChanged = pyqtSignal(int)

    def __init__(self):
        super(QAptInterface, self).__init__()
        self.aptd = client.AptClient()
        self.transactions = []
        self._progress = None
        self.transactions_running = False


    def QueueTransaction(self, appSummery, action):

        if action == 'install':
            transaction = self.aptd.install_packages(appSummery['pkg'])
        elif action == 'remove':
            transaction = self.aptd.remove_packages(appSummery['pkg'])

        self.transactions.append(transaction)
        self.transactions_list.append(appSummery)

    def TransProgress(self, trans, progress):
        self.aptProgressChanged.emit(progress)

    def TransFinished(self, exit_status):
        self.transactions_running = False

    def ProcessTransactions(self):
        for i in self.transactions:
            i.connect('progress-changed', self.TransProgress)
            i.connect('finished', lambda: self.transactions_list.pop(0))
            self.transactions_running = True
            i.run()


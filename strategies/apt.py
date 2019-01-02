#!/usr/bin/python3
# example how to deal with the depcache

from aptdaemon.client import AptClient

client = AptClient()

def progress_print():
    print(trans.progress)

trans = client.install_packages(['featherpad'])
trans.connect('progress-changed', progress_print)
trans.run()





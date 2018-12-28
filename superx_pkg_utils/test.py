#!/usr/bin/python3

from appstore_backend import AppStoreBackend
a = AppStoreBackend()

print(a.getSuggested(['Network'], 'browser'))

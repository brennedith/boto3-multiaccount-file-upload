from concurrent.futures import process
import time
import os

from django.test import TestCase

from ..handleinmultipleaccounts import handleInMultipleAccounts

def formatedTimestamp(*args):
    return { 'ResponseMetadata': { 'RequestId': os.getpid() } }

class TestsHandleInMultipleAccounts(TestCase):
    def test_success_runs_function_in_different_processes(self):
        processIds = handleInMultipleAccounts(formatedTimestamp)

        print(processIds)
        self.assertTrue(all(processIds.count(id) == 1 for id in processIds))
import os

from django.test import TestCase

from ..handleinmultipleaccounts import handleInMultipleAccounts

def getProcessId(*args):
    return { 'ResponseMetadata': { 'RequestId': os.getpid() } }

class TestsHandleInMultipleAccounts(TestCase):
    def test_success_runs_function_in_different_processes(self):
        processIds = handleInMultipleAccounts(getProcessId)

        print('handleInMultipleAccounts.processIds', processIds)

        self.assertTrue(all(processIds.count(id) == 1 for id in processIds))
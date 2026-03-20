import unittest
from classes import WorkerThread, Packets

def test_func(x):
    print(x)

class TestInput(unittest.TestCase):

    def test_update_args(self):
        thread = WorkerThread(target=test_func, args=(1, ))
        thread.update_args((2, ))
        thread.start()
        

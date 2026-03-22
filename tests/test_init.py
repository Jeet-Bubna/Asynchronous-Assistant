import unittest
from classes import WorkerThread
from queue import PriorityQueue
from init import init_threads

class TestInit(unittest.TestCase):

    def test_init_threads(self):
        mocked_queue = {
            "test": PriorityQueue(),
            "test 2": PriorityQueue()
        }
        result = init_threads(mocked_queue)
        counter = 0
        for name, thread_object in result.items():
            counter += 1
            self.assertIsNotNone(thread_object)
            self.assertIsInstance(name, str)
            self.assertIsInstance(thread_object, dict[str, WorkerThread])
        self.assertEqual(counter, 4)
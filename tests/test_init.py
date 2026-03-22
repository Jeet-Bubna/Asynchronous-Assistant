import unittest
from classes import WorkerThread
from queue import PriorityQueue
from init import init_threads

class TestInit(unittest.TestCase):

    def test_init_threads(self):
        mocked_queue = {
            "main queue": PriorityQueue(),
            "listener queue": PriorityQueue(),
            "test": PriorityQueue(),
            "test 2": PriorityQueue()
        }
        result = init_threads(mocked_queue, run_test=True)
        counter = 0
        for name, thread_object in result.items():
            counter += 1
            self.assertIsInstance(name, str)
            self.assertIsNotNone(thread_object)
            self.assertIsInstance(thread_object, dict)

if __name__ == "__main__":
    unittest.main()
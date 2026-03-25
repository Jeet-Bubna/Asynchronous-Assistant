import unittest
from unittest.mock import patch, MagicMock
from classes import WorkerThread
from queue import PriorityQueue
from init import init_threads, init_embeddings

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
    
    @patch('init.encode')
    @patch('init.set_up_embeddings')
    def test_init_embeddings(self,mocked_setup, mocked_encode):
        mocked_encode.return_value = "mocked"
        mocked_setup.return_value = ("model", "tokenizer")
        result = init_embeddings(test_calling=True)

        self.assertIsInstance(result, dict)
        for cat, embed in result["embeddings"]["l1"].items():
            self.assertIsInstance(cat, str)

        for cat, obj in result["embeddings"]["l2"].items():
            self.assertIsInstance(cat, str)
            self.assertIsInstance(obj, dict)

            for command, embeds in obj.items():
                self.assertIsInstance(command, str)
                self.assertIsInstance(embeds, list)

if __name__ == "__main__":
    unittest.main()
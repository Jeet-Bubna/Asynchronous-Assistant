import unittest
from threading import Event
from unittest.mock import patch, MagicMock
from input import input_function,categoriser
from categorizer import categorise_embeddings
import numpy as np
from classes import WorkerThread, PriorityQueue, Packets

class TestInput(unittest.TestCase):

    @patch("input.categoriser")
    @patch("input.logger")
    @patch("builtins.input", return_value="jarvis end the program")
    def test_input_function_ending(self, mocked_logger, mocked_input, mocked_categoriser):
        worker_event = Event()
        mocked_input_list = {
        "workers": {"music":{"thread":WorkerThread(target=lambda x: print("test function"))}, "event":worker_event},
        "embeddings": {"embeddings": np.array([1,2,3,4,5]), "encode":""},
        "queues":{"main queue":PriorityQueue(), "music":PriorityQueue(), "listener queue":PriorityQueue()}
        }
        
        mocked_categoriser.return_value = {"category":"end", "command":"none"}
        result = input_function(mocked_input_list)
        self.assertEqual(result, "ending")  
    
    @patch("input.categoriser")
    @patch("input.logger")
    @patch("builtins.input", return_value="jarvis play some music")
    def test_input_function_normal(self, mocked_logger, mocked_input, mocked_cateoriser):
        worker_event = Event()
        mocked_input_list = {
        "workers": {"music":{"thread":WorkerThread(target=lambda x: print("test function")), "event":worker_event}},
        "embeddings": {"embeddings": np.array([1,2,3,4,5]), "encode":""},
        "queues":{"main queue":PriorityQueue(), "music":PriorityQueue(), "listener queue":PriorityQueue()}
        }

        mocked_cateoriser.return_value = {"category":"music", "command":"none"}
        input_function(mocked_input_list, run_once=True)

        priority, result = mocked_input_list["queues"]["main queue"].get(1)
        self.assertIsInstance(result, Packets)
        self.assertIsInstance(priority, int)
        self.assertEqual(result._content["raw text"], "jarvis play some music")
        self.assertIsInstance(result._queue, dict)
        
        for key, queue in result._queue.items():
            self.assertIsInstance(key, str)
            self.assertIsInstance(queue, PriorityQueue)
        
if __name__ == '__main__':
    unittest.main()
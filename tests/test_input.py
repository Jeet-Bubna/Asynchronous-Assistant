import unittest
from unittest.mock import patch
from input import input_function
from input import categoriser
from classes import WorkerThread
import numpy as np
from queue import PriorityQueue
from sentence_transformers import SentenceTransformer

class TestInput(unittest.TestCase):

    def test_input(self):
        self.works = True

    def setUp(self):
        self.input_list = {
        "workers": {"music":WorkerThread(target=self.test_input)},
        "embeddings": {"embeddings": np.array([1,2,3,4,5]), "model":SentenceTransformer},
        "queues":{"main queue":PriorityQueue(), "music":PriorityQueue()}
        }
    
    @patch('builtins.input')
    def test_main_input_thread_end(self, mocked_input):
        mocked_input.return_value = "jarvis end the program"
        result = input_function(self.input_list)
        self.assertEqual(result, 1)

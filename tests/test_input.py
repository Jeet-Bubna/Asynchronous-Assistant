import unittest
from unittest.mock import patch, MagicMock
from input import input_function, categorise_embeddings
from classes import WorkerThread
import numpy as np
from queue import PriorityQueue
from sentence_transformers import SentenceTransformer

class TestInput(unittest.TestCase):

    def input_test(self):
        self.works = True
    
    def setUp(self):
        self.input_list = {
        "workers": {"music":WorkerThread(target=self.input_test)},
        "embeddings": {"embeddings": np.array([1,2,3,4,5]), "encode":""},
        "queues":{"main queue":PriorityQueue(), "music":PriorityQueue()}
        }
    
    def test_categorise_embeddings(self):
        mock_embeddings = np.array([1.0, 0.0])
        mock_encode = lambda x: np.array([0.0, 1.0])

        result = categorise_embeddings(mock_embeddings, mock_encode, "jarvis jibberish input")
        self.assertEqual(result, "low confidence")

        result = categorise_embeddings(mock_embeddings, mock_encode, "jibberish")
        self.assertEqual(result, "lead error")
                
        

if __name__ == '__main__':
    unittest.main()
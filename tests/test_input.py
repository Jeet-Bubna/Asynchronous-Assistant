import unittest
from unittest.mock import patch, MagicMock
from input import input_function, categorise_embeddings, categoriser
import numpy as np

class TestInput(unittest.TestCase):

    @patch('input.logger')
    @patch('input.CATEGORIES', {'cat1': 0})
    def test_categorise_embeddings(self, mocked_logger):
        mock_embeddings = np.array([1.0, 0.0])
        mock_encode = lambda x: np.array([0.0, 1.0])

        result = categorise_embeddings(mock_embeddings, mock_encode, "jibberish")
        self.assertEqual(result, "low confidence")

        mock_embeddings = np.array([1.0, 0.0])
        mock_encode = lambda x: np.array([0.0])
        result = categorise_embeddings(mock_embeddings, mock_encode, "jibberish")
        self.assertEqual(result, "value error")

        mock_embeddings = np.array([[0.1, 0.1], [0.9, 0.9]])
        mock_encode = lambda x: np.array([0.9, 0.9])
        result = categorise_embeddings(mock_embeddings, mock_encode, "jibberish")        
        self.assertEqual(result, "index error")

        mocked_logger.critical.assert_called()

    @patch('input.logger')
    def test_categoriser(self, mocked_logger):
        mock_embeddings = "mock embeddings"
        mock_model = "mock model"

        mock_text = "ultron play some music by the avengers"
        result = categoriser(mock_text, mock_embeddings, mock_model)
        self.assertEqual(result, "lead error")

        mock_text = "jarvis play some music by the avengers"
        result = categoriser(mock_text, mock_embeddings, mock_model)
        self.assertEqual(result, "music")

        mock_text = "jarvis set a timer for 10 minutes"
        result = categoriser(mock_text, mock_embeddings, mock_model)
        self.assertEqual(result, "time")

        mock_text = "jarvis search the internet for avacado on toast"
        result = categoriser(mock_text, mock_embeddings, mock_model)
        self.assertEqual(result, "search")

        mocked_logger.info.assert_called() 
    
"""
    @patch("input.logger")
    @patch("builtins.input", return_value="jarvis end the program")
    @patch("input.categoriser")
    def test_input_function(self, mocked_logger, mocked_input, mocked_categoriser):
        mocked_input_list = {
        "workers": {"music":WorkerThread(target=lambda x: print("test function"))},
        "embeddings": {"embeddings": np.array([1,2,3,4,5]), "encode":""},
        "queues":{"main queue":PriorityQueue(), "music":PriorityQueue()}
        }
        
        mocked_categoriser = MagicMock()
        mocked_categoriser.return_value = "end"

        result = input_function(mocked_input_list)
        self.assertEqual(result, "ending")
        mocked_logger.info.assert_called()
"""

if __name__ == '__main__':
    unittest.main()
import unittest
from settings import ASSISTANT_NAME
import categorizer

class TestCategorizer(unittest.TestCase):

    def test_categorizer_lead_error(self):
        result = categorizer.categoriser("this should return an error", embeddings="this should not matter", model="this should not matter")
        self.assertEqual(result, "lead error")

        
        result = categorizer.categoriser(ASSISTANT_NAME+"RAND_STRING", embeddings="this should not matter", model="this should not matter")
        self.assertEqual(result, "lead error")

        result = categorizer.categoriser("RAND_STRING" + ASSISTANT_NAME, embeddings="this should not matter", model="this should not matter")
        self.assertEqual(result, "lead error")
    
    
if __name__ == '__main__':
    unittest.main()

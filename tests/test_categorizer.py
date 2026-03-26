import unittest
from settings import ASSISTANT_NAME, EMBEDDING_FILE
from init import init_embeddings
import categorizer

class TestCategorizer(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        
        obj = init_embeddings()
        cls.embeddings = obj['embeddings']
        cls.encode = obj['encode'] 

    def test_categorizer_lead_error(self):
        text = "this should return an error"
        result = categorizer.categoriser(text,  embeddings="this should not matter", model="this should not matter")['category']
        self.assertEqual(result, "lead error")

        result = categorizer.categoriser(ASSISTANT_NAME+"RAND_STRING", embeddings="this should not matter", model="this should not matter")['category']
        self.assertEqual(result, "lead error")

        result = categorizer.categoriser("RAND_STRING" + ASSISTANT_NAME, embeddings="this should not matter", model="this should not matter")['category']
        self.assertEqual(result, "lead error")
    
    def test_categorizer_categorization_music(self):
        # Map the expected command to the list of phrases
        test_data = {
            "play": [
                "play some music", "play some tunes", "put on some tunes", "let the beats flow", 
                "drop the beat", "play some jazz", "play some kanye", "play some post malone", 
                "play All of the Lights by Kanye", "play Runaway", "play Shape of you", 
                "play some ed sheeran", "play some travvis scott"
            ],
            "stop": [
                "stop the music", "stop playing music", "stop playing the tunes", 
                "stop playing", "stop"
            ],
            "resume": [
                "resume", "resume the music", "put the music back on", "restart the tunes"
            ]
        }

        for expected_command, phrases in test_data.items():
            for phrase in phrases:
                full_text = 'jarvis ' + phrase
                with self.subTest(msg=full_text):
                    result = categorizer.categorise_embeddings(self.embeddings, self.encode, full_text)
                    
                    self.assertEqual(result["category"], "music", msg=f"Failed Category: {full_text}")
                    self.assertEqual(result['command'], expected_command, msg=f"Failed Command: {full_text}")
    
    def test_categorizer_categorization_end(self):
        texts_list = ["end the program", "end", "stop running", "stop the program", "end it"]    
        for text in texts_list:
            text = 'jarvis ' + text
            
            with self.subTest(msg=f"Testing input: {text}"):
                result = categorizer.categorise_embeddings(self.embeddings,self.encode, text)
                self.assertEqual(result["category"], "end", msg=text)
                self.assertEqual(result['command'], "none", msg=text)

    
if __name__ == '__main__':
    unittest.main()

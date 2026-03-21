import unittest
from classes import Packets
from queue import PriorityQueue 
from threading import Event
from modules.music import main

class TestMusic(unittest.TestCase):

    def setUp(self):
        self.queues = {
            "queue": PriorityQueue(),
            "listening_queue":PriorityQueue()
        }

        self.event = Event()

    def test_music_end(self):
        self.queues['queue'].put((1, Packets("end", queue="test_queue_should_never_get_Called")))
        self.event.set()
        result = main(self.queues, self.event)

        self.assertEqual(result, "ending")

if __name__ == "__main__":
    unittest.main()
        
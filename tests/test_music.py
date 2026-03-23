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
        result = main(self.queues, self.event, run_once=True)

        self.assertEqual(result, "ending")
    
    def test_music_play(self):
        self.queues['queue'].put((1, Packets("jarvis play some techno" )))
        self.event.set()
        main(self.queues, self.event, run_once=True)

        priority, packet = self.queues['listening_queue'].get(timeout=2)
        self.assertTrue(packet._content['started'])

if __name__ == "__main__":
    unittest.main()
        
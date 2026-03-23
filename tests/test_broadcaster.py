import unittest
from threading import Event
from classes import Packets
from queue import PriorityQueue
from broadcaster import broadcaster

class TestBroadcaster(unittest.TestCase):

    def test_broadcaster_happy_path(self):

        mocked_listener_queue = PriorityQueue()
        mocked_queues = {"main queue": PriorityQueue(), "listener queue": mocked_listener_queue}
        mocked_event = Event()
        mocked_queue = PriorityQueue()
        mocked_queues["main queue"].put((1, Packets("jarvis play some music", {"queue": mocked_queue, "listening_queue":mocked_listener_queue}, worker=None, event=mocked_event)))
        broadcaster(mocked_queues, run_once=True)

        priority, result = mocked_queue.get_nowait()
        self.assertIsInstance(priority, int)
        self.assertIsInstance(result, Packets)
        self.assertEqual(result._content, "jarvis play some music")
    
    def test_broadcast_ending(self):

        mocked_main_queue = PriorityQueue()
        mocked_music_event = Event()
        mocked_music_queue = PriorityQueue()
        mocked_main_queue.put_nowait((
            1, Packets(
                "end",
                queue= {"queue": mocked_music_queue},
                event=mocked_music_event
            )
        ))
        mocked_listener_queue = PriorityQueue()

        mocked_queues = {
            "main queue": mocked_main_queue,
            "listener queue": mocked_listener_queue,
            "music" : mocked_music_queue
        }
        mocked_main_queue.put((1.1, Packets({"error":True}, queue=None, worker=None)))
        print("put in main queue error message")

        result = broadcaster(mocked_queues, run_once = True)
        self.assertEqual(result, "ended")
        priority, music_queue_message = mocked_music_queue.get_nowait()
        print("got from music quue")
        self.assertEqual(priority, 1)
        self.assertIsInstance(music_queue_message, Packets)
        self.assertEqual(music_queue_message._content, "end")
        self.assertIsInstance(music_queue_message._queue, PriorityQueue)
        self.assertEqual(music_queue_message._queue, mocked_main_queue)

if __name__ == "__main__":
    unittest.main()
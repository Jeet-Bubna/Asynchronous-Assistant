import unittest
from threading import Event
from classes import Packets
from queue import PriorityQueue
from broadcaster import broadcaster

class TestBroadcaster(unittest.TestCase):

    def setUp(self) -> None:
        self.main_queue = PriorityQueue()
        self.music_queue = PriorityQueue()
        self.listener_queue = PriorityQueue()

        print("IS MAIN Q EMPTY?", self.main_queue.empty())

    def test_broadcaster_happy_path(self):

        mocked_queues = {"main queue": self.main_queue, "listener queue": self.listener_queue}
        mocked_event = Event()
        mocked_queue = PriorityQueue()
        self.main_queue.put((1, Packets("jarvis play some music", {"queue": mocked_queue, "listening_queue":self.listener_queue}, worker=None, event=mocked_event)))
        broadcaster(mocked_queues, run_once=True)

        priority, result = mocked_queue.get_nowait()
        mocked_queue.task_done()

        self.assertIsInstance(priority, int)
        self.assertIsInstance(result, Packets)
        self.assertEqual(result._content, "jarvis play some music")
    
    def test_broadcast_ending(self):

        mocked_music_event = Event()
        self.main_queue.put_nowait((
            1, Packets(
                "end",
                queue= {"queue": self.music_queue},
                event=mocked_music_event
            )
        ))

        mocked_queues = {
            "main queue": self.main_queue,
            "listener queue": None,
            "music" : self.music_queue
        }

        self.main_queue.put((1.123, Packets({"error":True}, queue=None, worker=None)))
        # NOTE: 1.123 becasue we are putting two packets in the same queue, and in actual programs it will 
        # be generated sequentially. To mimic that, we increase it here as high priority has lower value

        result = broadcaster(mocked_queues, run_once = True)
        self.assertEqual(result, "ended")

        priority, music_queue_message = self.music_queue.get_nowait()
        self.music_queue.task_done()

        self.assertEqual(priority, 1)
        self.assertIsInstance(music_queue_message, Packets)
        self.assertEqual(music_queue_message._content, "end")
        self.assertEqual(music_queue_message._queue, self.main_queue)
        self.assertIsInstance(music_queue_message._queue, PriorityQueue)


if __name__ == "__main__":
    unittest.main()
from classes import Packets
from threading import Thread
import logging
from queue import ShutDown
import random
from time import sleep

logger = logging.getLogger(__name__)

def end_main(listening_queue, event, playing_thread:Thread, error = None):
    from settings import TIME_TO_JOIN_THREAD
    logger.info("Recieved END. Returning....") 
    try:
        playing_thread.join(timeout=TIME_TO_JOIN_THREAD)
        logger.info("MUSIC PLAYING THREAD has joined successfully")

    except TimeoutError:
        error = TimeoutError

    listening_queue.put(
        (1, Packets(
            content={
                "started":True,
                "function":"music",
                "end":True,
                "error":error
            }, queue=listening_queue
        ))
    )

    event.clear()
    return "ending"

def play_music(time):
    sleep(time)
    return

def main(queues, event, run_once = False):

    isRunning = True

    while isRunning:
        event.wait()
        logger.info("GOT IT! Running program...")
        main_queue = queues["main queue"]
        listening_queue = queues["listener queue"]
        listening_queue.put((random.random() + 1,Packets(content={
            "started":True,
            "function": "music",
            "end":False
        },  queue=listening_queue)))

        time = 10
        playing_thread = Thread(target=play_music, args=(time, ))
        playing_thread.start()

        try:
            priority, packet = main_queue.get()
            content = packet._content

            if content == "end":
                return end_main(listening_queue, event, playing_thread)

            else:
                logger.info("Playing music....")
        except KeyError as e:
            logger.critical(f"MUSIC: KEY ERROR: {e}", exc_info=True)
            return end_main(listening_queue, event, playing_thread, error=KeyError)
        
        except ShutDown as e:
            logger.critical(f"MUSIC: SHUTDOWN - queue was shutdown: {e}", exc_info=True)
            return end_main(listening_queue, event, playing_thread, error=ShutDown)
        
        if run_once:
            isRunning = False
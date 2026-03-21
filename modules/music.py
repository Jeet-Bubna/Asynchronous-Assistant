from classes import Packets
import logging
from queue import ShutDown
import random

logger = logging.getLogger(__name__)

def end_main(listening_queue, event):
    logger.info("Recieved END. Returning....") 
    listening_queue.put(
        (1, Packets(
            content={
                "started":True,
                "function":"music",
                "end":True
            }, queue=listening_queue
        ))
    )

    event.clear()
    isRunning = False
    return "ending"

def main(queues, event, run_once = False):

    isRunning = True

    while isRunning:
        event.wait()
        logger.info("GOT IT! Running program...")
        main_queue = queues["queue"]
        listening_queue = queues["listening_queue"]
        listening_queue.put((random.random() + 1,Packets(content={
            "started":True,
            "function": "music",
            "end":False
        },  queue=listening_queue)))
        try:
            priority, packet = main_queue.get()
            content = packet._content

            if content == "end":
                return end_main(listening_queue, event)

            else:
                logger.info("Playing music....")

        except KeyError as e:
            logger.critical(f"MUSIC: KEY ERROR: {e}", exc_info=True)
            return end_main(listening_queue, event)
        
        except ShutDown as e:
            logger.critical(f"MUSIC: SHUTDOWN - queue was shutdown: {e}", exc_info=True)
            return end_main(listening_queue, event)
        
        if run_once:
            isRunning = False
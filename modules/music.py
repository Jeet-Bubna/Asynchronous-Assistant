from queue import PriorityQueue
from classes import Packets
import logging

logger = logging.getLogger(__name__)

def main(text:str, queues):
    main_queue = queues["queue"]
    listening_queue = queues["listening_queue"]
    isRunning = True
    listening_queue.put((1,Packets(content={
        "started":True,
        "function": "music",
        "end":False
    },  queue=listening_queue)))
    while isRunning:
        try:
            priority, packet = main_queue.get()
            content = packet._content

            if content == "end":
                logger.info("Recieved END. Returning....") 
                # Do something... return 1 if succesful
                listening_queue.put(
                    (1, Packets(
                        content={
                            "started":True,
                            "function":"music",
                            "end":True
                        }, queue=listening_queue
                    ))
                )
                return 1
            
            logger.info("Playing music....")
        except Exception as e:
            logger.critical(f"MUSIC: ERROR: {e}")
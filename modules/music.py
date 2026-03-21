from classes import Packets
import logging
import random

logger = logging.getLogger(__name__)

def main(queues, event):

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
            else:
                logger.info("Playing music....")

        except Exception as e:
            logger.critical(f"MUSIC: ERROR: {e}")
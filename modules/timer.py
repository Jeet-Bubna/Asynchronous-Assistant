from queue import PriorityQueue
import logging

logger = logging.getLogger(__name__)

def main(text:str, queues):
    isRunning = True
    while isRunning:
        priority, packet = queues["commandq"].get()
        content = packet._content

        if content == "end":
            logger.info("Recieved END. Returning....") 
            # Do something... return 1 if succesful
            queues["responseq"].put((1, 1))
            return 1
        
        logger.info("Setting a timer....")
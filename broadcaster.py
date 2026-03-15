from queue import PriorityQueue
from classes import Packets, WorkerThread
import logging

logger = logging.getLogger(__name__)

def broadcaster(main_queue):
    logger.debug("Broadcaster has recieved the args")
    logger.debug(f"Type of Main_Queue is: {type(main_queue)}")
    logger.debug(f"object of Main_Queue is: {main_queue}")
    isRunning = True
    while isRunning:
        priority , packet = main_queue.get()
        logger.info(f"Recieved message: {packet._content}")
        queue:PriorityQueue = packet._queue["commandq"]
        queue.put((priority, packet))

        worker: WorkerThread = packet._worker
        logger.debug(f"THE STATUS OF THE WORKER IS: {worker.is_alive()}")
        logger.info(f"{worker} has been passed [{packet._content}], with queue [{packet._queue}] in queue [{queue}]") 

        if (packet._content == "end"):
            isRunning = False
            logger.info("Recieved END. Returning....")
            return 1

        if worker.is_alive() == False: 
            worker.update_args((packet._content, packet._queue))
            worker.start()
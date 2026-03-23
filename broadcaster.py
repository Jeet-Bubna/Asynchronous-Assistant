from queue import PriorityQueue
from classes import Packets, WorkerThread
import logging


logger = logging.getLogger(__name__)

def broadcaster(queues, event:None = None, run_once=False):
    isRunning = True
    isEnding = False
    main_queue = queues["main queue"]
    logger.debug("Broadcaster has recieved the args")
    logger.debug(f"Type of Main_Queue is: {type(main_queue)}")
    logger.debug(f"object of Main_Queue is: {main_queue}")
    while isRunning:
        if run_once:
            isRunning = False
        priority , packet = main_queue.get()
        logger.info(f"Recieved message: {packet._content}")
        queue = packet._queue["queue"]
        queue.put((priority, packet))

        if (packet._content == "end"):
            isRunning = False
            isEnding = True

            logger.debug(f"QUEUES OBJECT: {queues}")
            del queues['main queue']
            del queues['listener queue']
            for queue in queues.values():
                queue.put((1, Packets(content="end", queue=main_queue)))

            logger.info(f"ALL QUEUES HAVE BEEN SENT THE END SIGNAL")

    while isEnding:
        if run_once:
            isEnding = False
        priortiy, packet = main_queue.get()
        try:
            error = packet._content["error"]
            if error:
                logger.critical(f"BROADCASTER RECIEVED THE ERROR:{error}")
                return "ended"
        except (KeyError, TypeError):
            pass
      